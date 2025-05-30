import pandas as pd


def convert_date_to_week(df, date_column, target_column):
    """
    Convert a date column to week number and store in a new column

    Args:
        df (pd.DataFrame): Dataframe to process
        date_column (str): Name of the date column to convert
        target_column (str): Name of the new column to create

    Returns:
        pd.DataFrame: Processed dataframe
    """
    # Convert to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])

    # Extract week number
    df[target_column] = df[date_column].dt.isocalendar().week

    return df


def calculate_ratio(df, numerator_column, denominator_column, target_column):
    """
    Calculate ratio between two columns and store in a new column

    Args:
        df (pd.DataFrame): Dataframe to process
        numerator_column (str): Name of the column to use as numerator
        denominator_column (str): Name of the column to use as denominator
        target_column (str): Name of the new column to create

    Returns:
        pd.DataFrame: Processed dataframe
    """
    df[target_column] = df[numerator_column] / df[denominator_column]

    return df


def process_dataframe(df, transformations):
    """
    Apply a list of transformations to a dataframe

    Args:
        df (pd.DataFrame): Dataframe to process
        transformations (list): List of transformation configurations

    Returns:
        pd.DataFrame: Processed dataframe
    """
    for transform in transformations:
        transform_type = transform.get('type')

        if transform_type == 'date_to_week':
            df = convert_date_to_week(
                df,
                transform.get('date_column'),
                transform.get('target_column')
            )

        elif transform_type == 'ratio':
            df = calculate_ratio(
                df,
                transform.get('numerator_column'),
                transform.get('denominator_column'),
                transform.get('target_column')
            )

    return df
