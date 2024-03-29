'''
Functions that help to process datasets .txt files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def file_mapping(filename, keyargs, bnumbers):
    '''
    Reads one by one all the valid TXT files and returns the corresponding data dictionaries.

    Param
        filename, String, full TXT file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    database = keyargs.get('db', None)
    url = keyargs.get('url', None)
    dataset_type = keyargs.get('dataset_type', None)

    dataset_dict_list = []
    txt_path = utils.verify_txt_path(filename)
    if not txt_path:
        return dataset_dict_list

    with open(txt_path)as txt_file:
        for line in txt_file:
            dataset_dict = {}
            # run_id 0 ,sample_id 1, feature_id 2, count 3, fpkm 4, tpm 5
            row = line.strip().split(',')
            gene_exp_id = f'{row[1]},{row[2]}'
            dataset_dict.setdefault('_id', gene_exp_id)
            new_dataset_id = f'{dataset_type}_{row[1]}'
            dataset_dict.setdefault('temporalId', new_dataset_id)
            dataset_dict.setdefault('count', float(row[3]))
            dataset_dict.setdefault('tpm', float(row[5]))
            dataset_dict.setdefault('fpkm', float(row[4]))

            dataset_dict.setdefault('gene', bnumbers.get(row[2]))
            # utils.get_gene_by_bnumber(row[2], database, url))

            dataset_dict.setdefault(
                'datasetIds', [f'{keyargs.get("dataset_type")}_{row[1]}'])
            dataset_dict = {k: v for k, v in dataset_dict.items() if v}
            dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
