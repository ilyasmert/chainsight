from chainsight_backend.inventory.services.data_loader import DataLoader
from chainsight_backend.inventory.services.lp_model import LPModel
from chainsight_backend.inventory.services.production_suggestion import ProductionSuggestion
from chainsight_backend.inventory.config.dataframe_config import DF_CONFIG

class OptimizationPipeline:
    """
    Main class to handle the optimization pipeline.
    It loads data, processes it, and runs the LP model.
    """

    def __init__(self,lp_params: dict):

        self.dataframes = DataLoader.load_dataframes_from_config(DF_CONFIG)
        self.lp_model_basic = LPModel(self.dataframes, lp_params, "basic")
        self.lp_model_advanced = LPModel(self.dataframes, lp_params, "advanced")

    def run(self):
        ...
        # 1) BASIC
        self.lp_model_basic.build_model()
        self.lp_model_basic.solve()
        basic_results = self.lp_model_basic.prepare_result_tables()

        # 2) ADVANCED
        self.lp_model_advanced.build_model()
        self.lp_model_advanced.solve()
        advanced_results = self.lp_model_advanced.prepare_result_tables()

        # 3) ProductionSuggestion  (sevkiyat = basic toplam)
        shipment_total_df = basic_results["total_shipment"]
        ps = ProductionSuggestion(
            self.dataframes["to_be_produced"],
            self.dataframes["ready"],
            shipment_total_df,
            self.lp_model_basic.get_week_list()
        )
        suggestion_dict = ps.summarize_suggestions()

        return {
            "truck_pallets": advanced_results["truck_pallets"],
            "ship_pallets": advanced_results["ship_pallets"],
            "truck_m2": advanced_results["truck_m2"],
            "ship_m2": advanced_results["ship_m2"],
            "stock": advanced_results["stock"],
            "shortage": advanced_results["shortage"],
            **suggestion_dict
        }




