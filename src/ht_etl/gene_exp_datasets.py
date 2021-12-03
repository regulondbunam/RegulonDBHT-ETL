'''
Functions that help to process datasets .tsv files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def file_mapping(keyargs):
    '''
    Reads one by one all the valid TSV files and returns the corresponding data dictionaries.

    Param
        filename, String, full TSV file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    filepath = 'uniformized/all_normalized_GEO_data_112921.csv'
    filename = os.path.join(keyargs.get('collection_path', None), filepath)
    database = keyargs.get('db', None)
    url = keyargs.get('url', None)
    dataset_type = keyargs.get('dataset_type', None)

    dataset_dict_list = []
    tsv_path = utils.verify_csv_path(filename)
    if not tsv_path:
        return dataset_dict_list
    ge_data_frame = utils.get_data_frame_tsv_coma(tsv_path)
    ge_json_list = utils.get_json_from_data_frame(ge_data_frame)

    for ge_dict in ge_json_list:
        dataset_dict = {}
        gene_exp_id = f'{ge_dict.get("sample_id", None)},{ge_dict.get("feature_id", None)}'
        print(gene_exp_id)
        dataset_dict.setdefault('_id', gene_exp_id)
        new_dataset_id = f'{dataset_type}_{ge_dict.get("sample_id", None)}'
        dataset_dict.setdefault('temporalId', new_dataset_id)
        dataset_dict.setdefault('count', ge_dict.get('count', None))
        dataset_dict.setdefault('tpm', ge_dict.get('tpm', None))
        dataset_dict.setdefault('fpkm', ge_dict.get('fpkm', None))

        dataset_dict.setdefault('gene', utils.get_gene_by_bnumber(
            ge_dict.get('feature_id', None), database, url))

        dataset_dict.setdefault('datasetIds', [ge_dict.get('sample_id', None)])
        dataset_dict = {k: v for k, v in dataset_dict.items() if v}
        dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
