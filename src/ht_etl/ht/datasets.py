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

    filename = kwargs.get('filename', '')
    rows_to_skip = kwargs.get('rows_to_skip', None)

    dataset_rows = dataset_dict(filename, rows_to_skip)

    for row in dataset_rows:
        dataset = DatasetsMetadata(
            bnumbers=kwargs.get('bnumbers', None),
            mg_api=kwargs.get('mg_api', None),
            dataset_source_dict=row,
            dataset_type=kwargs.get('dataset_type', None),
            email=kwargs.get('email', None),
            database=kwargs.get('database', None),
            url=kwargs.get('url', None),
            version=kwargs.get('version', None),
            src_collection_name=kwargs.get('collection_name', None),
            collection_source=kwargs.get('collection_source', None),
            collection_path=kwargs.get('collection_path', None),
            collection_status=kwargs.get('collection_status', None),
            genes_ranges=kwargs.get('genes_ranges', None)
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
    data_dict = {}
    if filename.endswith('.xlsx'):
        data_dict = file_manager.get_excel_data(
            filename,
            METADATA_SHEET,
            rows_to_skip
        )
    if filename.endswith('.csv'):
        pass
    if filename.endswith('.tsv'):
        file_data_frame = file_manager.get_data_frame_tsv(
            filename=filename
        )
        data_dict = file_manager.get_json_from_data_frame(file_data_frame)
    return data_dict
