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
                dataset_dict.setdefault(
                    'tempId', f'{dataset_id}:site:{ds_count}')'''
                # dataset_dict_list.append(f'{dataset_id}:site:{ds_count}')
                dataset_dict = {}
                row = line.strip().split()
                # TODO: siteID -> array
                # TODO: De donde se toma el Site?
                dataset_dict.setdefault('datasetId', [dataset_id])
                dataset_dict.setdefault('siteIds', [])
                dataset_dict.setdefault('chromosome', row[0])
                dataset_dict.setdefault('chrLeftPosition', row[1])
                dataset_dict.setdefault('chrRightPosition', row[2])
                dataset_dict.setdefault('name', row[3])
                dataset_dict.setdefault('score', row[4])
                dataset_dict.setdefault('strand', row[5])
                dataset_dict.setdefault('closestGenes', '''utils.find_closest_gene(
                    row[1], row[2], database, url, genes_ranges)''')
                dataset_dict.setdefault('transcriptionUnit', {
                    # TODO: find site in RI -> get reg_entity -> check if TU Promoter or Gene
                    '_id': None,
                    'name': None,
                })
                '''dataset_dict.setdefault('foundClassicRIs', {
                    'tfbsLeftPosition': None,
                    'tfbsRightPosition': None,
                    'transcriptionFactorID': None,
                    'transcriptionFactorName': None,
                    'relativeGeneDistance': None,
                    'relativeTSSDistance': None,
                    'strand': None,
                    'sequence': None,
                })
                dataset_dict.setdefault('foundDatasetRIs', {
                    # TODO: PENDIENTE
                    'tfbsLeftPosition': None,
                    'tfbsRightPosition': None,
                    'transcriptionFactorID': None,
                    'transcriptionFactorName': None,
                    'relativeGeneDistance': None,
                    'relativeTSSDistance': None,
                    'strand': None,
                    'sequence': None,
                })'''
                dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
