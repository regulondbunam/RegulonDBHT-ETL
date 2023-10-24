'''
Functions that help to process datasets .tsv files.
'''
# standard
import os
import logging

# third party


# local
from libs import utils


def file_mapping(dataset_id, filename, database, url, dataset_type, bnumbers):
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
        dataset_dict.setdefault('length', tu_dict.get('length', None))
        dataset_dict.setdefault('termType', tu_dict.get('term_type', None))

        genes_list = []
        genes = tu_dict.get('genes', None)
        if genes:
            genes = genes.split(',')
            for gene in genes:
                if bnumbers.get(gene):
                    tu_gene = {
                        "_id": bnumbers.get(gene).get('_id'),
                        "name": bnumbers.get(gene).get('name'),
                        "bnumber": bnumbers.get(gene).get('bnumber'),
                    }
                    genes_list.append(tu_gene)
        print(genes_list)
        dataset_dict.setdefault('genes', genes_list)
        name = ''
        if genes_list is not None:
            names = []
            for gene in genes_list:
                names.append(gene.get('name', None))
            if tu_dict.get('strand', None) == '-':
                names.reverse()
            name = '-'.join(names)
        dataset_dict.setdefault('name', name),
        if not genes_list:
            logging.error(
                f'There are not genes in {tu_dict.get("id", None)} can not process genes and name')
        dataset_dict.setdefault('phantom', tu_dict.get('phantom', None))
        dataset_dict.setdefault('pseudo', tu_dict.get('pseudo', None))
        dataset_dict.setdefault('datasetIds', [dataset_id])
        dataset_dict = {k: v for k, v in dataset_dict.items() if v}
        dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
