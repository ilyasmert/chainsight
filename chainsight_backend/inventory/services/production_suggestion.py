import pandas as pd

class ProductionSuggestion:
    """
    Class to handle production suggestion logic.
    """


    def __init__(self,to_be_produced_df: pd.DataFrame, ready_df: pd.DataFrame,
                 shipment_plan_total_df:pd.DataFrame, week_list: list[int]):
        """
        Initialize the ProductionSuggestion class.
        :param to_be_produced_df:
        :param ready_df:
        :param shipment_plan_total_df:
        :param week_list: Already ordered weeks. Could be 51, 52, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        """
        self.to_be_produced_df = to_be_produced_df
        self.ready_df = ready_df
        self.shipment_plan_total_df = shipment_plan_total_df
        self.week_list = week_list
        self.to_be_produced_pivoted_df = None
        self.projected_factory_stock_df = None
        self.__process_dataframes()

    def __process_dataframes(self) -> None:
        """
        1) to_be_produced     → pivot   (adet / hafta)
        2) ready              → ilk hafta stoğa ekle
        3) projection         → kümüle stok
        4) shipment_plan      → aynı ızgaraya hizala
        5) projection -= shipment  →   gerçek stok simülasyonu
        """
        # ────────────────────────────────────────────────
        # 0) Hazırlık: ortak grid
        prods = pd.unique(
            pd.concat([self.to_be_produced_df["productid"],
                       self.ready_df["productid"],
                       self.shipment_plan_total_df.index])
        )
        # İstediğimiz sütun sırası zaten week_list
        grid_index = pd.Index(prods, name="productid")
        grid_columns = self.week_list  # [51, 52, 1, 2, …]

        # ────────────────────────────────────────────────
        # 1) Üretimdeki partiler (bitme haftasına göre)
        tbp = (self.to_be_produced_df
               .groupby(["productid", "etd_week"])["quantity"]
               .sum().unstack(fill_value=0)
               .reindex(index=grid_index, columns=grid_columns,
                        fill_value=0))

        # ────────────────────────────────────────────────
        # 2) Ready → ilk haftaya ekle
        first_w = grid_columns[0]
        ready = self.ready_df.groupby("productid")["quantity"].sum()
        tbp.loc[ready.index, first_w] += ready

        # ────────────────────────────────────────────────
        # 3) Kümülatif stok (projeksiyon)
        proj = tbp.cumsum(axis=1)

        # ────────────────────────────────────────────────
        # 4) Nakliye planını aynı ızgaraya oturt
        ship = (self.shipment_plan_total_df
                .reindex(index=grid_index, columns=grid_columns,
                         fill_value=0)
                .cumsum(axis=1))  # hafta-içi birikimli çıkaracağız

        # ────────────────────────────────────────────────
        # 5) Gerçek stok = projeksiyon − sevkiyat
        self.projected_factory_stock_df = proj.subtract(ship, fill_value=0)

        # Sonuç veri setlerini sakla (ileride lazım olabilir)
        self.to_be_produced_pivoted_df = tbp
        self.shipment_plan_aligned_df = ship

    def __split_by_stock_status(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns
        -------
        neg_last_df : pd.DataFrame
            En az bir haftası negatif OLAN ve *son haftası da negatif* ürünler
        pos_last_df : pd.DataFrame
            En az bir haftası negatif OLAN fakat *son haftası pozitif / sıfır* ürünler
        """
        proj = self.projected_factory_stock_df.copy()

        # 1) Her haftası ≥ 0 olanları çıkar
        mask_all_pos = (proj >= 0).all(axis=1)
        proj = proj[~mask_all_pos]

        # 2) Son haftaya göre ayır
        last_week = self.week_list[-1]
        neg_last_df = proj[proj[last_week] < 0]
        pos_last_df = proj[proj[last_week] > 0]

        return neg_last_df, pos_last_df

    def summarize_suggestions(self) -> dict[str, pd.DataFrame]:
        """
        Returns
        -------
        critical_products       : ürün | has_current_prod | suggested_finish_week | shortage
        suggested_rearrangements: ürün | actual_finish_week | suggested_finish_week | difference
        """
        neg_last, pos_last = self.__split_by_stock_status()  # önceden yazdığımız ayırma
        first_neg_week = (self.projected_factory_stock_df < 0) \
            .apply(lambda r: r.idxmax() if (r < 0).any() else None, axis=1)

        # ────────────────────────────────────────────────
        # 1) critical_products  (neg_last tabloları baz alınır)
        # mevcut üretim var mı?
        has_prod = self.to_be_produced_pivoted_df.sum(axis=1) > 0
        critical_products = (pd.DataFrame({
            "productid": neg_last.index,
            "has_current_production": has_prod.loc[neg_last.index].map({True: "Yes", False: "No"}),
            "suggested_finish_week": first_neg_week.loc[neg_last.index],
            "shortage": neg_last.lookup(neg_last.index,
                                        first_neg_week.loc[neg_last.index])
                .abs()
        }).set_index("productid"))

        # ────────────────────────────────────────────────
        # 2) suggested_rearrangements  (pos_last tabloları baz alınır)
        # actual_finish = to_be_produced_df’deki en küçük etd_week (> first_week)
        actual_finish = (self.to_be_produced_df
                         .groupby("productid")["etd_week"].min())
        suggested_finish = first_neg_week.loc[pos_last.index]

        suggested_rearrangements = (pd.DataFrame({
            "productid": pos_last.index,
            "actual_finish_week": actual_finish.reindex(pos_last.index),
            "suggested_finish_week": suggested_finish,
        })
                                    .assign(difference=lambda df:
        df["actual_finish_week"] - df["suggested_finish_week"])
                                    .set_index("productid"))

        return {
            "critical_products": critical_products,
            "suggested_rearrangements": suggested_rearrangements
        }



