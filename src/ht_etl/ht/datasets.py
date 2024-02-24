"""
Dataset getter.
Calls for Datasets class and returns a constructor with all datasets objects.
"""
# standard

# third party


# local
def get_dataset(**kwargs):
    """
    Returns a constructor with all datasets.
    Args:
        **kwargs:

    Returns:
        dataset: Datasets object
    """
    from src.ht_etl.collections.datasets_metadata import DatasetsMetadata

    filename = kwargs.get('filename', None)
    rows_to_skip = kwargs.get('rows_to_skip', None)

    dataset_rows = dataset_dict(filename, rows_to_skip)

    for row in dataset_rows:
        dataset = DatasetsMetadata(
            dataset_dict=row,
            dataset_type=kwargs.get('dataset_type', None),
            email=kwargs.get('email', None),
            database=kwargs.get('database', None),
            url=kwargs.get('url', None)
        )
        yield dataset


def dataset_dict(filename, rows_to_skip):
    """
    Load dataset file and return dataset in dictionary format.

    Args:
        filename: String
        rows_to_skip: Integer

    Returns:
        data_dict: Dictionary
    """
    from src.libs.constants import METADATA_SHEET
    from src.libs import file_manager
    data_dict = file_manager.get_excel_data(
        filename,
        METADATA_SHEET,
        rows_to_skip
    )
    return data_dict
