def get_dataset(**kwargs):
    from src.ht_etl.collections.datasets_metadata import DatasetsMetadata

    filename = kwargs.get('filename', None)
    rows_to_skip = kwargs.get('rows_to_skip', None)

    dataset_rows = dataset_dict(filename, rows_to_skip)

    for row in dataset_rows:
        dataset = DatasetsMetadata(
            dataset_dict=row,
            dataset_type=kwargs.get('dataset_type', None)
        )
        yield dataset


def dataset_dict(filename, rows_to_skip):
    from src.libs.constants import METADATA_SHEET
    from src.libs import file_manager
    data_dict = file_manager.get_excel_data(
        filename,
        METADATA_SHEET,
        rows_to_skip
    )
    return data_dict
