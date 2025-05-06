import pandas as pd
from chainsight_backend.inventory.utils.data_processor import process_dataframe
from chainsight_backend.inventory.config.dataframe_config import DF_CONFIG

class DataLoader:
    """
    Loads data from Django ORM into pandas DataFrames,
    based entirely on configuration.
    """

    @staticmethod
    def load_dataframe(model, filters=None, transformations=None):
        queryset = model.objects.filter(**filters).values() if filters else model.objects.all().values()
        df = pd.DataFrame(list(queryset))

        if transformations:
            df = process_dataframe(df, transformations)

        return df

    @staticmethod
    def load_dataframes_from_config(config=DF_CONFIG):
        dataframes = {}
        for name, cfg in config.items():
            model = cfg.get('model')
            filters = cfg.get('filters')  # Şimdilik boş, ileride lazım olabilir
            transformations = cfg.get('transformations')

            df = DataLoader.load_dataframe(
                model=model,
                filters=filters,
                transformations=transformations
            )

            dataframes[name] = df

        return dataframes