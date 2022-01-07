'''
Dataset record processing.
'''
# standard
import os
import logging
from posixpath import join
import shutil
import re
from numpy import number, string_

# third party
import pandas

# local
from libs import utils
from libs import constants as EC
from ht_etl import nlp_growth_conditions, gene_exp_datasets


def open_tsv_file(keyargs):
    '''
    This function lists and filters all tsv files in the directory path.

    Param
        tsv_path, String, tsv file path.

    Returns
        collection_data, List, list of datasets dictionaries.
    '''

    collection_data = []

    if os.path.isfile(keyargs.get('datasets_record_path')) and keyargs.get('datasets_record_path').endswith('.tsv'):
        collection_data.extend(tsv_file_mapping(
            keyargs.get('datasets_record_path'), keyargs))
    else:
        logging.warning(
            f'{keyargs.get("datasets_record_path")} is not a valid txt file will be ignored')

    return collection_data


def get_author_data(authors_data_path, filename, dataset_id):
    '''
    Gets and converts the author's Excel data to a CSV formatted String.

    Param
        filename, String, authors' XLSX file name, path.
        authors_data_path, String, authors' XLSX files path.

    Returns
        authors_raw, String, CSV formated String.
    '''
    if not filename:
        logging.error(
            f'There is not File Name for {dataset_id} can not read Author\'s files')
        return None
    author_raw = filename
    excel_path = os.path.join(authors_data_path, filename)
    if os.path.isfile(excel_path) and excel_path.endswith('.xlsx'):
        raw = utils.get_data_frame(excel_path, 0, 0)
        author_raw = raw.to_csv(encoding='utf-8')
        logging.info(
            f'Reading Author\'s Data files {excel_path}')
        return author_raw
    elif os.path.isfile(excel_path) and excel_path.endswith('.tsv'):
        raw = utils.get_data_frame_tsv(excel_path)
        author_raw = raw.to_csv(encoding='utf-8')
        logging.info(
            f'Reading Author\'s Data files {excel_path}')
        return author_raw
    else:
        logging.error(
            f'There are not valid Author\'s Data files for {dataset_id} can not read Author\'s files')
        return None


def set_sample(experiment_id, control_id, title):
    '''
    Formats sample object and converts IDs Strings into Strings arrays.

    Param
        experiment_id, String, Sample experiment ID unformatted.
        control_id, String, Sample control ID unformatted.
        title, String, Sample title.

    Returns
        sample, Dict, dictionary with the formatted Sample data.
    '''
    if not experiment_id:
        experiment_id = None
    else:
        experiment_id = experiment_id.replace('] [', ', ').replace(
            '[', '').replace(']', '').split(', ')
    if not control_id:
        control_id = None
    else:
        control_id = control_id.replace('] [', ', ').replace(
            '[', '').replace(']', '').split(', ')
    experiment_ids = []
    control_ids = []
    if experiment_id:
        for exp_id in experiment_id:
            experiment_ids.append(exp_id.replace('\t', ''))
    if control_id:
        for ctrl_id in control_id:
            control_ids.append(ctrl_id.replace('\t', ''))
    sample = {
        'experimentId': experiment_ids,
        'controlId': control_ids,
        'title': title,
    }
    return sample


def set_linked_dataset(experiment_id, control_id, dataset_type):
    '''
    Formats sample object and converts IDs Strings into Strings arrays.

    Param
        experiment_id, String, Sample experiment ID unformatted.
        control_id, String, Sample control ID unformatted.
        dataset_type, String, Dataset type.

    Returns
        sample, Dict, dictionary with the formatted Sample data.
    '''
    if not experiment_id:
        experiment_id = None
    else:
        experiment_id = experiment_id.replace('] [', ', ').replace(
            '[', '').replace(']', '').split(', ')
    if not control_id:
        control_id = None
    else:
        control_id = control_id.replace('] [', ', ').replace(
            '[', '').replace(']', '').split(', ')
    experiment_ids = []
    control_ids = []
    if experiment_id:
        for exp_id in experiment_id:
            experiment_ids.append(exp_id.replace('\t', ''))
    if control_id:
        for ctrl_id in control_id:
            control_ids.append(ctrl_id.replace('\t', ''))

    sample = {
        'experimentId': experiment_ids,
        'controlId': control_ids,
        'datasetType': dataset_type,
    }
    return sample


def tsv_file_mapping(filename, keyargs):
    '''
    Reads one by one all the valid XLSX files and returns the corresponding data dictionaries.

    Param
        filename, String, full XLSX file path.
        keyargs.collection_path, String, Path to read de origin files data.
        keyargs.db, String, Database to get some external data.
        keyargs.url, String, URL where database is located.
        keyargs.source_name, String, Excel record surce ("GEO or ArrayExpress").
        keyargs.dataset_type, String, Excel record type ["GENE EXPRESSION"].
        keyargs.release_process_date, String, Date record of program execution.
        keyargs.version, String, Input data version.
        keyargs.email, String, User email address to connect to PUBMED database.


    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    dataset_dict_list = []

    nlp_gc_collection_data = nlp_growth_conditions.file_mapping(keyargs)
    collection_data = utils.set_json_object(
        "nlpGrowthConditions", nlp_gc_collection_data, keyargs.get('organism'), 'NLP_GC', 'GC')
    utils.create_json(
        collection_data, f'nlp_growth_conditions{utils.get_collection_name(keyargs.get("datasets_record_path"))}', keyargs.get('output_path'))
    tsv_path = utils.verify_tsv_path(filename)
    if not tsv_path:
        return dataset_dict_list
    gene_expression_js = utils.get_tsv_data(filename)

    filtered_gene_expression_path = utils.verify_txt_path(os.path.join(
        keyargs.get("collection_path"), "metadata/GeneExpList-SRR-GSE-GSM-Filter.txt"))
    if filtered_gene_expression_path:
        filtered_gene_expression_datasets = pandas.read_csv(
            filtered_gene_expression_path, delimiter="\t")
        filtered_gene_expression = utils.get_json_from_data_frame(
            filtered_gene_expression_datasets)
    for row in gene_expression_js:
        dataset_dict = {}
        dataset_id = row.get(EC.GE_DATASET_ID, None)
        if dataset_id is None:
            continue

        # geneExpressionFiltered
        dataset_dict.setdefault("geneExpressionFiltered", False)
        if utils.find_one_in_dict_list(filtered_gene_expression, "PASS-FILTER", dataset_id) != None:
            dataset_dict.setdefault("geneExpressionFiltered", True)

        #  Serie
        serie_id = row.get(EC.SERIE_ID, None)
        if serie_id:
            serie_id = (((row.get(EC.SERIE_ID, None)).split(' '))
                        [0]).replace(';', '')

        # PMID
        pmid = row.get(EC.PMID, None)
        if pmid:
            try:
                pmid = int(pmid)
                dataset_dict.setdefault(
                    'publications', []).append(utils.get_pubmed_data(pmid, keyargs.get('email')))
            except:
                pmids = pmid.split(",")
                for pmid in pmids:
                    pmid = int(pmid)
                    dataset_dict.setdefault(
                        'publications', []).append(utils.get_pubmed_data(pmid, keyargs.get('email')))
        else:
            pubmed_authors = row.get(EC.AUTHORS, None)
            if isinstance(pubmed_authors, str):
                pubmed_authors = pubmed_authors.split(',')
            dataset_dict.setdefault('publications', []).append(
                                    {
                                        'authors': pubmed_authors,
                                        'abstract': None,
                                        'date': row.get(EC.RELEASE_DATE, None),
                                        'pmcid': None,
                                        'pmid': None,
                                        'title': row.get(EC.EXPERIMENT_TITLE, None)
                                    })

        # objectTested
        dataset_dict.setdefault('objectsTested', [])
        objectsTested = utils.get_object_tested(row.get(EC.PROTEIN_NAME, None),
                                                    keyargs.get('db'),
                                                    keyargs.get('url')
                                                    )
        if objectsTested["name"] != None:
            dataset_dict.setdefault('objectsTested', []).append(objectsTested)

        # SourceSerie
        platform_id = row.get(EC.PLATFORM_ID, None)
        if platform_id:
            platform_id = platform_id.replace('\t', '')
        platform_title = row.get(EC.PLATFORM_TITLE, None)
        if platform_title:
            platform_title = platform_title.replace('\t', '')

        dataset_dict.setdefault('sourceSerie', {
            'sourceId': serie_id,
            'sourceName': keyargs.get('source_name'),
            'titles': row.get(EC.PROTEIN_NAME, None),
            'platformId': platform_id,
            'platformTitle': platform_title,
            'strategy': row.get(EC.STRATEGY),
            'method': row.get(EC.METHOD_NAME, None),
        })
        # Sample
        dataset_dict.setdefault('sample',
                                set_sample(
                                    row.get(
                                        EC.GE_SAMPLES_REPLICATES_EXPERIMENT_ID, None),
                                    None,
                                    row.get(EC.TITLE_FOR_ALL_REPLICATES, None))
                                )
        # linked dataset?
        dataset_dict.setdefault('linkedDataset',
                                set_linked_dataset(
                                    row.get(
                                        EC.SAMPLES_EXPERIMET_REPLICATES_EXPRESSION_ID, None),
                                    row.get(
                                        EC.SAMPLES_CONTROL_REPLICATES_EXPRESSION_ID, None),
                                    'GeneExpression')
                                )
        dataset_dict.setdefault(
            'referenceGenome', None)
        dataset_dict.setdefault('releaseDataControl', {
            'date': keyargs.get('release_process_date'),
            'version': keyargs.get('version'),
        })
        dataset_dict.setdefault(
            'assemblyGenomeId', None)

        dataset_dict.setdefault('datasetType', keyargs.get('dataset_type'))

        new_dataset_id = f'{dataset_id}'  # {keyargs.get("dataset_type")}_

        dataset_dict.setdefault('temporalId', new_dataset_id)
        dataset_dict.setdefault('_id', new_dataset_id)

        # uniformized #TODO: HAPPY 2022!
        '''ge_dict_list = []
        datasets_source_path = f'{keyargs.get("collection_path")}{EC.BED_PATHS}/v1.0/{dataset_id}.txt'
        ge_dict_list = gene_exp_datasets.file_mapping(
            datasets_source_path,
            keyargs
        )
        collection_data = utils.set_json_object(
            "geneExpression", ge_dict_list, keyargs.get('organism'), 'GED', 'GE')
        utils.create_json(
            collection_data, f'ge_{dataset_id}', os.path.join(keyargs.get('output_path'), utils.get_collection_name(keyargs.get("datasets_record_path"))))'''

        dataset_dict = {k: v for k, v in dataset_dict.items() if v}
        dataset_dict_list.append(dataset_dict)

    return dataset_dict_list
