'''
Functions that help to process datasets .bed files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def get_sites_ids(sites, peak_id):
    sites_ids = []
    for site in sites:
        if site.get('peakId') == peak_id:
            sites_ids.append(site.get('_id'))
    return sites_ids


def bed_file_mapping(dataset_id, filename, database, url, genes_ranges, sites_dict_list):
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
                dataset_dict.setdefault('_id', row[3])
                dataset_dict.setdefault('temporalId', row[3])
                dataset_dict.setdefault('closestGenes', utils.find_closest_gene(
                    row[1], row[2], database, url, genes_ranges))
                dataset_dict.setdefault('chromosome', row[0])
                dataset_dict.setdefault('peakLeftPosition', int(row[1]))
                dataset_dict.setdefault('peakRightPosition', int(row[2]))
                dataset_dict.setdefault('score', float(row[4]))
                dataset_dict.setdefault('name', row[3])
                dataset_dict.setdefault(
                    'siteIds', get_sites_ids(sites_dict_list, row[3]))
                dataset_dict.setdefault('datasetIds', [dataset_id])
                dataset_dict = {k: v for k, v in dataset_dict.items() if v}
                dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
