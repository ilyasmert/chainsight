import pulp
import pandas as pd

# ──────────────────────────────────────────────────────────────
# 1) Varsayılan parametre kümesi
# ──────────────────────────────────────────────────────────────
DEFAULT_PARAMS = {
    "truck_cost":       7,
    "ship_cost":        3,
    "penalty":          100,
    "truck_per_week":   2,
    "truck_capacity":   25_000,
    "ship_capacity":    150_000,
    "truck_lead_time":  3,
    "ship_lead_time":   7,
    "projection_length":14          # hafta
}


class LPModel:
    truck_cost: int
    ship_cost: int
    penalty: int
    truck_per_week: int
    truck_capacity: int
    ship_capacity: int
    truck_lead_time: int
    ship_lead_time: int
    projection_length: int
    # ──────────────────────────────────────────────────────────
    # 2) Kurucu
    # ──────────────────────────────────────────────────────────
    def __init__(self, dataframes: dict, params: dict | None = None,
                 model_type: str = "basic"):
        self.solution = None
        self.dataframes   = dataframes
        self.params       = {**DEFAULT_PARAMS, **(params or {})}
        self.model_type   = model_type
        self.model        = None      # pulp.LpProblem
        self.weeks        = []
        # Karar değişkenleri
        self.truck_d = self.ship_d = self.stock = self.shortage = None
        self.factory_stock = None
        self.products  = []

    # ──────────────────────────────────────────────────────────
    # 3) Ortak yardımcılar
    # ──────────────────────────────────────────────────────────
    def _load_params(self):
        """Parametreleri attribute olarak kaydet: self.truck_cost …"""
        for k, v in self.params.items():
            setattr(self, k, v)

    def generate_weeks(self, start_week: int) -> list[int]:
        weeks = []
        for i in range(self.projection_length):
            w = start_week + i
            if w > 52:
                w -= 52
            weeks.append(w)
        return weeks

    def _create_decision_variables(self, products, weeks, *, advanced=False):
        truck_d = pulp.LpVariable.dicts("TruckShipment",
                                        ((p, t) for p in products for t in weeks),
                                        lowBound=0, cat="Integer")
        ship_d  = pulp.LpVariable.dicts("ShipShipment",
                                        ((p, t) for p in products for t in weeks),
                                        lowBound=0, cat="Integer")
        stock   = pulp.LpVariable.dicts("Stock",
                                        ((p, t) for p in products for t in weeks),
                                        lowBound=None, cat="Continuous")
        shortage = pulp.LpVariable.dicts("Shortage",
                                         ((p, t) for p in products for t in weeks),
                                         lowBound=0)
        factory_stock = None
        if advanced:
            factory_stock = pulp.LpVariable.dicts("FactoryStock",
                                                  ((p, t) for p in products for t in weeks),
                                                  lowBound=0, cat="Continuous")
        return truck_d, ship_d, stock, shortage, factory_stock

    def _pivot_solution(self, solution_dict, col_name, pallet_cap=None):
        rows = []
        for (p, t), val in solution_dict.items():
            qty = val * pallet_cap[p] if pallet_cap and val else (val or 0)
            rows.append({"productid": p, "week": t, col_name: qty})
        df = pd.DataFrame(rows)
        df["week"] = pd.Categorical(df["week"],
                                    categories=self.weeks, ordered=True)
        pivot = df.pivot(index="productid", columns="week", values=col_name)
        return pivot.reindex(columns=self.weeks)

    # ──────────────────────────────────────────────────────────
    # 4) Dıştan çağrılan tek method
    # ──────────────────────────────────────────────────────────
    def build_model(self):
        self._load_params()
        return (self._build_basic_model() if self.model_type == "basic"
                else self._build_advanced_model())

    # ──────────────────────────────────────────────────────────
    # 5) BASIC MODEL
    # ──────────────────────────────────────────────────────────
    def _build_basic_model(self):
        df_stock   = self.dataframes["atp_stock"]
        df_sales   = self.dataframes["sales"]
        df_intrans = self.dataframes["intransit"]
        df_pallet  = self.dataframes["pallet_info"]

        self.products = list(df_stock["productid"].unique())
        self.weeks    = self.generate_weeks(int(df_stock["weekid"].min()))

        # --- parametre sözlükleri
        init_stock = dict(df_stock[["productid", "quantity"]].values)
        demand = df_sales.groupby("productid")["quantity"].sum().to_dict()
        demand = {p: demand.get(p, 0) for p in self.products}

        intransit = {(p, t): 0 for p in self.products for t in self.weeks}
        for p, t, q in df_intrans[["productid", "eta_week", "quantity"]].values:
            if (p, t) in intransit:
                intransit[(p, t)] += q

        density = dict(df_pallet[["productid", "density"]].values)
        capacity = dict(df_pallet[["productid", "palletcapacity"]].values)

        # --- karar değişkenleri
        (self.truck_d, self.ship_d, self.stock,
         self.shortage, _) = self._create_decision_variables(self.products,
                                                             self.weeks)

        self.model = pulp.LpProblem("TransportationInventory_Basic",
                                    pulp.LpMinimize)

        # --- amaç fonksiyonu
        self.model += pulp.lpSum(
            self.truck_cost * self.truck_d[p, t] * capacity[p] +
            self.ship_cost  * self.ship_d[p, t]  * capacity[p] +
            self.penalty    * self.shortage[p, t]
            for p in self.products for t in self.weeks)

        # --- kapasite kısıtları
        for t in self.weeks:
            self.model += pulp.lpSum(self.truck_d[p, t] * capacity[p] *
                                     density[p] for p in self.products) \
                          <= self.truck_capacity * self.truck_per_week
            self.model += pulp.lpSum(self.ship_d[p, t] * capacity[p]
                                     for p in self.products) <= self.ship_capacity

        # --- envanter dinamiği
        for p in self.products:
            first = self.weeks[0]
            self.model += self.stock[p, first] == \
                          init_stock[p] + intransit[p, first] - demand[p]
            for t in self.weeks[1:]:
                prev = self.weeks[self.weeks.index(t) - 1]
                truck_week = (t - self.truck_lead_time - 1) % 52 + 1
                ship_week  = (t - self.ship_lead_time  - 1) % 52 + 1
                truck_arr = (self.truck_d[p, truck_week] * capacity[p]
                             if truck_week in self.weeks else 0)
                ship_arr  = (self.ship_d[p, ship_week]  * capacity[p]
                             if ship_week in self.weeks else 0)
                self.model += self.stock[p, t] == (
                    self.stock[p, prev] + truck_arr + ship_arr +
                    intransit[p, t] - demand[p])

        # --- shortage bağlama
        for p in self.products:
            for t in self.weeks:
                self.model += self.shortage[p, t] >= -self.stock[p, t]

    # ──────────────────────────────────────────────────────────
    # 6) ADVANCED MODEL (ready + to_be_produced)
    # ──────────────────────────────────────────────────────────
    def _build_advanced_model(self):
        df_ready   = self.dataframes["ready"]
        df_tbp     = self.dataframes["to_be_produced"]

        # önce basic modeli kur, sonra ek kısıtları ekle
        self._build_basic_model()

        # --- ilave parametre sözlükleri
        ready = dict(df_ready[["productid", "quantity"]].values)
        ready = {p: ready.get(p, 0) for p in self.products}

        tbp = {(p, t): 0 for p in self.products for t in self.weeks}
        for p, t, q in df_tbp[["productid", "etd_week", "quantity"]].values:
            if (p, t) in tbp:
                tbp[(p, t)] += q

        capacity = dict(self.dataframes["pallet_info"]
                        [["productid", "palletcapacity"]].values)

        # -- yeni karar değişkeni
        self.factory_stock = pulp.LpVariable.dicts(
            "FactoryStock", ((p, t) for p in self.products for t in self.weeks),
            lowBound=0, cat="Continuous")

        # -- fabrika stok dinamiği
        for p in self.products:
            t0 = self.weeks[0]
            self.model += self.factory_stock[p, t0] == (
                ready[p] + tbp[p, t0] -
                self.truck_d[p, t0] * capacity[p] -
                self.ship_d[p, t0]  * capacity[p])

            for t in self.weeks[1:]:
                prev = self.weeks[self.weeks.index(t) - 1]
                truck_week = (t - self.truck_lead_time - 1) % 52 + 1
                ship_week  = (t - self.ship_lead_time  - 1) % 52 + 1
                truck_arr = (self.truck_d[p, truck_week] * capacity[p]
                             if truck_week in self.weeks else 0)
                ship_arr  = (self.ship_d[p, ship_week]  * capacity[p]
                             if ship_week in self.weeks else 0)
                self.model += self.factory_stock[p, t] == (
                    self.factory_stock[p, prev] + tbp[p, t] -
                    truck_arr - ship_arr)

    # ──────────────────────────────────────────────────────────
    # 7) ÇÖZ & RAPORLA
    # ──────────────────────────────────────────────────────────
    def solve(self):
        self.model.solve(pulp.HiGHS(gapRel=0.01, timeLimit=300))
        status = pulp.LpStatus[self.model.status]

        sol = {
            "status": status,
            "total_cost": pulp.value(self.model.objective),
            "truck_shipments": {(p, t): self.truck_d[p, t].varValue
                                for p in self.products for t in self.weeks},
            "ship_shipments":  {(p, t): self.ship_d[p, t].varValue
                                for p in self.products for t in self.weeks},
            "stock":           {(p, t): self.stock[p, t].varValue
                                for p in self.products for t in self.weeks},
            "shortage":        {(p, t): self.shortage[p, t].varValue
                                for p in self.products for t in self.weeks}
        }
        if self.factory_stock:
            sol["factory_stock"] = {(p, t): self.factory_stock[p, t].varValue
                                    for p in self.products for t in self.weeks}
        self.solution = sol

    # ──────────────────────────────────────────────────────────
    # 7) ÇÖZ & RAPOR TABLOLARINI HAZIRLA
    # ──────────────────────────────────────────────────────────
    def prepare_result_tables(self) -> dict[str, pd.DataFrame]:
        """
        Çözümden altı pivot tablo oluşturup bellekte döndürür:
        truck_pallets, ship_pallets, truck_m2, ship_m2, stock, shortage
        """
        pallet_cap = dict(self.dataframes["pallet_info"]
                          [["productid", "palletcapacity"]].values)

        def _pivot(data, name, *, scale=None):
            rows = [{"productid": p,
                     "week": t,
                     name: (v * scale[p] if scale and v else v or 0)}
                    for (p, t), v in data.items()]
            df = pd.DataFrame(rows)
            df["week"] = pd.Categorical(df["week"],
                                        categories=self.weeks, ordered=True)
            return (df.pivot(index="productid", columns="week", values=name)
                     .reindex(columns=self.weeks))

        return {
            "truck_pallets": _pivot(self.solution["truck_shipments"], "truck_pallets"),
            "ship_pallets":  _pivot(self.solution["ship_shipments"],  "ship_pallets"),
            "truck_m2":      _pivot(self.solution["truck_shipments"], "truck_m2",
                                    scale=pallet_cap),
            "ship_m2":       _pivot(self.solution["ship_shipments"], "ship_m2",
                                    scale=pallet_cap),
            "stock":         _pivot(self.solution["stock"],     "stock"),
            "shortage":      _pivot(self.solution["shortage"],  "shortage"),
            "total_shipment":_pivot(self.solution["truck_shipments"], "truck_m2",
                                    scale=pallet_cap).add( _pivot(self.solution["ship_shipments"], "ship_m2",
                                    scale=pallet_cap), fill_value=0)
        }

    # (İsteğe bağlı) Excel’e yazmak hâlâ gerekirse:
    def export_tables_to_excel(self, tables: dict[str, pd.DataFrame],
                               filename: str = "plan.xlsx") -> None:
        """Hazırlanmış pivot tabloları tek dosyaya yazar."""
        with pd.ExcelWriter(filename, engine="openpyxl") as wr:
            for sheet, df in tables.items():
                df.to_excel(wr, sheet_name=sheet.capitalize())
        print(f"[LPModel] Results saved → {filename}")

    def get_week_list(self) -> list[int]:
        """
        Returns
        -------
        week_list : list[int]
        """
        return self.weeks