'''
Functions that help to process datasets .bed files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def open_bed_file(bed_path):
    '''
    This function lists and filters all BED files in the directory path.

    Param
        bed_path, String, directory path.

    Returns
        datasets_data, List, list of datasets dictionaries.
    '''

    datasets_data = []

    if os.path.isfile(bed_path) and bed_path.endswith('.bed'):
        logging.info(
            f'Reading dataset {bed_path}')
        datasets_data.extend(bed_file_reader(bed_path))
    else:
        logging.warning(
            f'{bed_path} is not a valid BED file will be ignored')
    return datasets_data


def get_site_abosolute_pos(left_pos, right_pos):  # TODO: PENDIENTE
    '''
    Calculates the absolute center position of the chromosome.

    Param
        left_pos, String, Start position in the sequence (it's converted to Integer).
        right_pos, String, End position in the sequence (it's converted to Integer).

    Returns
        abs_pos, Float, Absolute center position in the sequence.
    '''
    abs_pos = int(left_pos) + int(right_pos)
    abs_pos = (abs_pos / 2)
    return abs_pos


def bed_file_reader(filename):
    '''
    Reads one by one all the valid BED files and returns the corresponding data dictionaries.

    Param
        filename, String, full BED file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    dataset_dict_list = []
    with open(filename)as bed_file:
        for line in bed_file:
            if not line.startswith('track') and not line.startswith('browser') and not line.startswith('##'):
                dataset_dict = {}
                row = line.strip().split()
                # TODO: siteID -> array
                dataset_dict.setdefault(
                    'siteId', get_site_abosolute_pos(row[1], row[2]))
                # TODO: De donde se toma el Site?
                dataset_dict.setdefault('chromosome', row[0])
                dataset_dict.setdefault('chrLeftPosition', row[1])
                dataset_dict.setdefault('chrRightPosition', row[2])
                dataset_dict.setdefault('name', row[3])
                dataset_dict.setdefault('score', row[4])
                dataset_dict.setdefault('strand', row[5])
                dataset_dict.setdefault('closerGene', {
                    '_id': None,
                    'name': None,
                })
                dataset_dict.setdefault('transcriptionUnit', {
                    # TODO: find site in RI -> get reg_entity -> check if TU Promoter or Gene
                    '_id': None,
                    'name': None,
                })
                dataset_dict.setdefault('foundClassicRIs', {
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
                })
                dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
