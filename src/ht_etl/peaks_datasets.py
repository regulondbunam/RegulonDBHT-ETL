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
    ds_count = 0
    with open(bed_path)as bed_file:
        for line in bed_file:
            if not line.startswith('track') and not line.startswith('browser') and not line.startswith('##'):
                '''ds_count += 1
                dataset_dict_list.append(f'{dataset_id}:peak:{ds_count}')'''
                dataset_dict = {}
                dataset_dict.setdefault('datasetId', [dataset_id])
                row = line.strip().split()
                dataset_dict.setdefault(
                    '_id', None)
                dataset_dict.setdefault('chromosome', row[0])
                dataset_dict.setdefault('closestGenes', utils.find_closest_gene(
                    row[1], row[2], database, url, genes_ranges))
                dataset_dict.setdefault('peakLeftPosition', row[1])
                dataset_dict.setdefault('peakRightPosition', row[2])
                dataset_dict.setdefault('score', row[4])
                dataset_dict.setdefault('name', row[3])
                dataset_dict.setdefault('siteIds', [])
                dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
