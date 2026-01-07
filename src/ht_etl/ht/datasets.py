"""
Dataset getter.
Calls for Datasets class and returns a constructor with all datasets objects.
"""
# standard

# third party

# local
from libs import constants
from libs import file_manager
from libs import nlp_growth_conditions_utils


def get_dataset(**kwargs):
    """
    Returns a constructor with all datasets.
    Args:
        **kwargs:

    Returns:
        dataset: Datasets object
    """
    from ht_etl.collections.datasets_metadata import DatasetsMetadata

    filename = kwargs.get('filename', '')
    rows_to_skip = kwargs.get('rows_to_skip', None)

    dataset_rows = dataset_dict(filename, rows_to_skip)

    nlp_growth_conditions_list = []
    if kwargs.get('dataset_type', None) == constants.RNA:
        nlp_growth_conditions_list = nlp_growth_conditions(
            mg_api=kwargs.get('mg_api', None),
            collection_name=kwargs.get('collection_name', None),
            collection_path=kwargs.get('collection_path', None)
        )

    for row in dataset_rows:
        dataset = DatasetsMetadata(
            nlp_growth_conditions_list=nlp_growth_conditions_list,
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
    from libs.constants import METADATA_SHEET
    from libs import file_manager
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


def nlp_growth_conditions(mg_api, collection_path, collection_name):
    """
    Returns a constructor with all NLPGrowthConditions objects.
    Args:
        collection_name:
        collection_path:
        mg_api:

    Returns:

    """
    geo_nlp_gc_json_path = nlp_growth_conditions_utils.geo_nlp_gc_json_path(collection_path)
    no_geo_nlp_gc_json_path = nlp_growth_conditions_utils.no_geo_nlp_gc_json_path(collection_path)

    nlp_gcs_list = []
    nlp_gc_dict_list = file_manager.read_json_file(geo_nlp_gc_json_path)
    for nlp_gc_data in nlp_gc_dict_list.items():
        nlp_gc_dict = nlp_growth_conditions_utils.get_nlp_gc(
            nlp_gc_data,
            collection_name,
            mg_api
        )
        nlp_gcs_list.append(nlp_gc_dict)
    nlp_gc_dict_list = file_manager.read_json_file(no_geo_nlp_gc_json_path)
    for nlp_gc_data in nlp_gc_dict_list.items():
        nlp_gc_dict = nlp_growth_conditions_utils.get_nlp_gc(
            nlp_gc_data,
            collection_name,
            mg_api
        )
        nlp_gcs_list.append(nlp_gc_dict)
    return nlp_gcs_list
