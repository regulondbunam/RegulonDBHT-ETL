'''
Functions that help to process datasets .bed files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils
from libs import constants as EC


def bed_file_mapping(dataset_id, filename, database, url, genes_ranges, sites_dict_list, collection_path, tf_sites):
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
                site_id = f'[{row[1]},{row[2]},{row[4]},{row[5]},{row[6]}]'
                found_site = utils.find_one_in_dict_list(
                    sites_dict_list, '_id', site_id)
                if found_site is None:
                    dataset_dict.setdefault(
                        '_id', site_id)
                    dataset_dict.setdefault('chromosome', row[0])
                    dataset_dict.setdefault('chrLeftPosition', int(row[1]))
                    dataset_dict.setdefault('chrRightPosition', int(row[2]))
                    dataset_dict.setdefault('closestGenes', utils.find_closest_gene(
                        row[1], row[2], database, url, genes_ranges))
                    classic_ris = utils.get_classic_ris(
                        row[1], row[2], row[5], tf_sites)
                    dataset_dict.setdefault('foundRIs', classic_ris)
                    dataset_dict.setdefault('peakId', row[3])
                    dataset_dict.setdefault('score', float(row[4]))
                    dataset_dict.setdefault('strand', row[5])
                    dataset_dict.setdefault('datasetIds', [dataset_id])
                    dataset_dict.setdefault('sequence', row[6])
                    dataset_dict.setdefault('temporalId', site_id)
                    dataset_dict.setdefault(
                        'nameCollection', utils.get_collection_name(collection_path))
                    dataset_dict = {k: v for k, v in dataset_dict.items() if v}
                    dataset_dict_list.append(dataset_dict)
                else:
                    found_site.setdefault('datasetIds', (found_site.get(
                        'datasetIds').append(dataset_id)))
    return dataset_dict_list
