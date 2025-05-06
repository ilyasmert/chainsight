from inventory.models import (AtpStock, PalletInfo, Intransit, Sales, Ready, ToBeProduced)

DF_CONFIG = {
    "atp_stock": {
        "model": AtpStock,
        "transformations": []
    },
    "pallet_info": {
        "model": PalletInfo,
        "transformations": [
            {
                "type": "ratio",
                "numerator_column": "palletweight",
                "denominator_column": "palletcapacity",
                "target_column": "density"
            }
        ]
    },
    "sales": {
        "model": Sales,
        "transformations": []
    },
    "intransit": {
        "model": Intransit,
        "transformations": [
            {
                "type": "date_to_week",
                "date_column": "eta",
                "target_column": "eta_week"
            }
        ]
    },
    "ready": {
        "model": Ready,
        "transformations": []
    },
    "to_be_produced": {
        "model": ToBeProduced,
        "transformations": [
            {
                "type": "date_to_week",
                "date_column": "etd",
                "target_column": "etd_week"
            }
        ]
    },
}