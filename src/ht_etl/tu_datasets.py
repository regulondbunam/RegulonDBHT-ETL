'''
Functions that help to process datasets .bed files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def bed_file_mapping(dataset_id, filename, database, url, genes_ranges):
    '''
    Reads one by one all the valid BED files and returns the corresponding data dictionaries.

    Param
        filename, String, full BED file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    dataset_dict_list = []
    bed_path = utils.verify_bed_path(filename)
    if not bed_path:
        return dataset_dict_list
    with open(bed_path)as bed_file:
        for line in bed_file:
            if not line.startswith('track') and not line.startswith('browser') and not line.startswith('##') and not line.startswith('#'):
                dataset_dict = {}
                row = line.strip().split()
                dataset_dict.setdefault('_id', '')
                dataset_dict.setdefault('chromosome', row[0])
                dataset_dict.setdefault('leftEndPosition', row[1])
                dataset_dict.setdefault('lightEndPosition', row[2])
                dataset_dict.setdefault(
                    'name', 'concatenación de nombres de genes de acuerdo a su strand')
                dataset_dict.setdefault('strand', '')
                dataset_dict.setdefault('length', '')
                dataset_dict.setdefault('termType', '')
                dataset_dict.setdefault('genes', utils.find_closest_gene(
                    row[1], row[2], database, url, genes_ranges))  # TODO: Is the same?
                dataset_dict.setdefault('phantom', '')
                dataset_dict.setdefault('pseudo', '')
                dataset_dict.setdefault('datasetIds', [dataset_id])
                dataset_dict = {k: v for k, v in dataset_dict.items() if v}
                dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
