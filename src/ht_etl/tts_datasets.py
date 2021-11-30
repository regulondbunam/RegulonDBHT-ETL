'''
Functions that help to process datasets .tsv files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def file_mapping(dataset_id, filename, database, url, dataset_type, genes_ranges):
    '''
    Reads one by one all the valid TSV files and returns the corresponding data dictionaries.

    Param
        filename, String, full TSV file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    dataset_dict_list = []
    tsv_path = utils.verify_tsv_path(filename)
    if not tsv_path:
        return dataset_dict_list
    tu_data_frame = utils.get_data_frame_tsv(tsv_path)
    tu_json_list = utils.get_json_from_data_frame(tu_data_frame)

    for tu_dict in tu_json_list:
        dataset_dict = {}
        dataset_dict.setdefault('_id', tu_dict.get('id', None))
        new_dataset_id = f'{dataset_type}_{dataset_id}'
        dataset_dict.setdefault('temporalId', new_dataset_id)
        dataset_dict.setdefault('chromosome', tu_dict.get('chromosome', None))
        dataset_dict.setdefault('leftEndPosition', tu_dict.get('start', None))
        dataset_dict.setdefault('rightEndPosition', tu_dict.get('stop', None))
        dataset_dict.setdefault('strand', tu_dict.get('strand', None))
        dataset_dict.setdefault('name', tu_dict.get('id', None))
        dataset_dict.setdefault('closestGenes', utils.find_closest_gene(
            tu_dict.get('start', None), tu_dict.get('stop', None), database, url, genes_ranges))
        dataset_dict.setdefault('terminator', utils.find_terminators(
            tu_dict.get('start', None), tu_dict.get('stop', None), tu_dict.get('id', None), database, url))

        dataset_dict.setdefault('datasetIds', [dataset_id])
        dataset_dict = {k: v for k, v in dataset_dict.items() if v}
        dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
