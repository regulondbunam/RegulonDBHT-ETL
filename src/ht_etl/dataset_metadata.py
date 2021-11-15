'''
Dataset record processing.
'''
# standard
import os
import logging
import shutil

# third party


# local
from libs import utils
from libs import constants as EC
from ht_etl import peaks_datasets, sites_dataset


def open_excel_file(keyargs):
    '''
    This function lists and filters all XLSX files in the directory path.

    Param
        excel_path, String, excel file path.

    Returns
        collection_data, List, list of datasets dictionaries.
    '''

    collection_data = []

    if os.path.isfile(keyargs.get('datasets_record_path')) and keyargs.get('datasets_record_path').endswith('.xlsx'):
        collection_data.extend(excel_file_mapping(
            keyargs.get('datasets_record_path'), keyargs))
    else:
        logging.warning(
            f'{keyargs.get("datasets_record_path")} is not a valid XLSX file will be ignored')

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


def get_growth_conditions(gc_raw, dataset_id):
    '''
    Converts the growth conditions sentences in a dictionary.
    Splits the phrase by | and separates the terms names from snake_case to camelCase in a dictionary format.

    ORGANISM -> organism
    GENETIC_BACKGROUND -> geneticBackground
    MEDIUM -> medium
    MEDIUM_SUPPLEMENTS -> mediumSupplements
    AERATION -> aeration
    TEMPERATURE -> temperature
    pH -> ph
    PRESSURE -> pressure
    OPTICAL_DENSITY -> opticalDensity
    GROWTH_PHASE -> growthPhase
    GROWTH_RATE -> growthRate
    VESSEL_TYPE -> vesselType
    AGITATION_SPEED -> aerationSpeed

    Param
        gc_raw, String, growth conditions phrase.

    Returns
        gc_dict, Dict, dictionary with the growth conditions terms.

    '''
    gc_dict = {}
    if not gc_raw:
        return None
    gc_list = gc_raw.split(' |')
    if not ' |' in gc_list:
        logging.error(
            f'There are not valid Growth Conditions for {dataset_id} can not read property')
        return None
    for condition in gc_list:
        condition = condition.split(':')
        gc_dict.setdefault(utils.to_camel_case(
            condition[0].lower()), condition[1])
    return gc_dict


def set_sample(experimentId, controlId, title):
    '''
    Formats sample object and converts IDs Strings into Strings arrays.

    Param
        experimentId, String, Sample experiment ID unformatted.
        controlId, String, Sample control ID unformatted.
        title, String, Sample title.

    Returns
        sample, Dict, dictionary with the formatted Sample data.
    '''
    if not experimentId:
        experimentId = None
    else:
        experimentId = experimentId.replace(
            '[', '').replace(']', '').split(', ')
    if not controlId:
        controlId = None
    else:
        controlId = controlId.replace('[', '').replace(']', '').split(', ')

    sample = {
        'experimentId': experimentId,
        'controlId': controlId,
        'title': title,
    }
    return sample


def set_linked_dataset(experimentId, controlId, dataset_type):
    '''
    Formats sample object and converts IDs Strings into Strings arrays.

    Param
        experimentId, String, Sample experiment ID unformatted.
        controlId, String, Sample control ID unformatted.
        dataset_type, String, Dataset type.

    Returns
        sample, Dict, dictionary with the formatted Sample data.
    '''
    if not experimentId:
        experimentId = None
    else:
        experimentId = experimentId.replace(
            '[', '').replace(']', '').replace('\t', '').split(', ')
    if not controlId:
        controlId = None
    else:
        controlId = controlId.replace('[', '').replace(
            ']', '').replace('\t', '').split(', ')

    sample = {
        'experimentId': experimentId,
        'controlId': controlId,
        'datasetType': dataset_type,
    }
    return sample


def excel_file_mapping(filename, keyargs):
    '''
    Reads one by one all the valid XLSX files and returns the corresponding data dictionaries.

    Param
        filename, String, full XLSX file path.
        keyargs.collection_path, String, Path to read de origin files data.
        keyargs.db, String, Database to get some external data.
        keyargs.url, String, URL where database is located.
        keyargs.source_name, String, Excel record surce ("GEO or ArrayExpress").
        keyargs.dataset_type, String, Excel record type ["TFBINDING", "GENE EXPRESION",
                 "TSS", "TUS", "TTS", "REGULONS"].
        keyargs.release_process_date, String, Date record of program execution.
        keyargs.version, String, Input data version.
        keyargs.email, String, User email address to connect to PUBMED database.


    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    dataset_dict_list = []
    peaks_dict_list = []
    sites_dict_list = []
    authors_data_list = []
    dataframe_dict = utils.get_excel_data(filename, keyargs.get(
        'metadata_sheet'), keyargs.get('rows_to_skip'))
    for row in dataframe_dict:
        dataset_dict = {}
        dataset_id = row[EC.DATASET_ID]
        serie_id = None
        if row[EC.SERIE_ID]:
            serie_id = (((row[EC.SERIE_ID]).split(' '))[0]).replace(';', '')
        if row[EC.PMID]:
            dataset_dict.setdefault(
                'publication', utils.get_pubmed_data(row[EC.PMID], keyargs.get('email')))
        else:
            pubmed_authors = row[EC.AUTHORS]
            if isinstance(pubmed_authors, str):
                pubmed_authors = pubmed_authors.split(',')
            dataset_dict.setdefault('publication',
                                    {
                                        'authors': pubmed_authors,
                                        'abstract': None,
                                        'date': row[EC.RELEASE_DATE],
                                        'pmcid': None,
                                        'pmid': None,
                                        'title': row[EC.EXPERIMENT_TITLE]
                                    }
                                    )
        dataset_dict.setdefault(
            'objectTested', utils.get_object_tested(row[EC.PROTEIN_NAME],
                                                    keyargs.get('db'),
                                                    keyargs.get('url')
                                                    )
        )
        dataset_dict.setdefault('sourceSerie', {
            'sourceId': serie_id,
            'sourceName': keyargs.get('source_name'),
            'title': row[EC.PROTEIN_NAME],
            'platformID': row[EC.PLATFORM_ID],
            'platformTitle': row[EC.PLATFORM_TITLE],
            'strategy': row[EC.STRATEGY],
            'method': row[EC.METHOD_NAME],
        })
        dataset_dict.setdefault('sample',
                                set_sample(
                                    row[EC.SAMPLES_REPLICATES_EXPERIMET_ID],
                                    row[EC.SAMPLES_REPLICATES_CONTROL_ID],
                                    row[EC.TITLE_FOR_ALL_REPLICATES])
                                )
        dataset_dict.setdefault('linkedDataset',
                                set_linked_dataset(
                                    row[EC.SAMPLES_EXPERIMET_REPLICATES_EXPRESSION_ID],
                                    row[EC.SAMPLES_CONTROL_REPLICATES_EXPRESSION_ID],
                                    'GeneExpression')
                                )
        dataset_dict.setdefault('referenceGenome', row[EC.REFERENCE_GENOME])
        gc_dict = get_growth_conditions(row[EC.GC_EXPERIMENTAL], dataset_id)
        if gc_dict:
            dataset_dict.setdefault('growthConditions', gc_dict)
        dataset_dict.setdefault('releaseDataControl', {
            'date': keyargs.get('release_process_date'),
            'version': keyargs.get('version'),
        })

        dataset_dict.setdefault('datasetType', keyargs.get('dataset_type'))

        beds_source_path = f'{keyargs.get("collection_path")}{EC.BED_PATHS}/{serie_id}/datasets/{dataset_id}'
        new_dataset_id = f'{keyargs.get("dataset_type")}_{dataset_id}'
        new_beds_path = f'{keyargs.get("output_dirs_path")}{new_dataset_id}'
        if keyargs.get('dataset_type') == 'TFBINDING':
            if serie_id:
                if utils.validate_directory(beds_source_path):
                    logging.info(
                        f'Coping datasets from {beds_source_path} \n\t to {new_beds_path}')
                    shutil.copytree(beds_source_path, new_beds_path)
                    bed_path = f'{beds_source_path}/{dataset_id}'
                    sites_dict_list.extend(
                        sites_dataset.bed_file_mapping(
                            new_dataset_id,
                            f'{bed_path}_sites.bed',
                            keyargs.get('db'),
                            keyargs.get('url'),
                            keyargs.get('genes_ranges'),
                            sites_dict_list,
                            keyargs.get('collection_path')
                        )
                    )
                    peaks_dict_list.extend(
                        peaks_datasets.bed_file_mapping(
                            new_dataset_id,
                            f'{bed_path}_peaks.bed',
                            keyargs.get('db'),
                            keyargs.get('url'),
                            keyargs.get('genes_ranges'),
                            sites_dict_list
                        )
                    )
            else:
                logging.error(
                    f'There is not Serie ID for {dataset_id} can not read .bed files')

        if keyargs.get('dataset_type') == 'TUS':
            dataset_dict.setdefault(
                'assemblyGenomeId', row['Assembly Genome ID'])
            dataset_dict.setdefault('fiveRichment', row['5\'Richment'])

        dataset_dict.setdefault('temporalID', new_dataset_id)
        dataset_dict.setdefault('_id', new_dataset_id)

        authors_data = {
            'tfBindingAuthorsData': get_author_data(f'{keyargs.get("collection_path")}{EC.AUTHORS_PATHS}/', row[EC.DATASET_FILE_NAME], dataset_id),
            '_id': f'AD_{new_dataset_id}',
            'datasetIds': [new_dataset_id]
        }
        if authors_data.get('tfBindingAuthorsData'):
            authors_data_list.append(authors_data)

        dataset_dict.setdefault(
            'summary', {
                'totalOfPeaks': {
                    'inDataset': 0,
                    'inRDBClassic': 0,
                    'sharedItems': 0,
                    'notInRDB': 0,
                    'notInDataset': 0,
                },
                'totalOfTFBS': {
                    'inDataset': 0,
                    'inRDBClassic': 0,
                    'sharedItems': 0,
                    'notInRDB': 0,
                    'notInDataset': 0,
                },
                'totalOfGenes': {
                    'inDataset': 0,
                    'inRDBClassic': 0,
                    'sharedItems': 0,
                    'notInRDB': 0,
                    'notInDataset': 0,
                },
            }
        )
        dataset_dict_list.append(dataset_dict)

    if keyargs.get('dataset_type') == 'TFBINDING':
        collection_data = utils.set_json_object(
            "peaks", peaks_dict_list, keyargs.get('organism'), 'BSD', 'PK')
        utils.create_json(
            collection_data, f'peaks_{utils.get_collection_name(keyargs.get("datasets_record_path"))}', keyargs.get('output_path'))

        collection_data = utils.set_json_object(
            "tfBinding", sites_dict_list, keyargs.get('organism'), 'BSD', 'BS')
        utils.create_json(
            collection_data, f'tf_binding_{utils.get_collection_name(keyargs.get("datasets_record_path"))}', keyargs.get('output_path'))

    collection_data = utils.set_json_object(
        "authorsData", authors_data_list, keyargs.get('organism'), 'BSD', 'AD')
    utils.create_json(collection_data, f'authors_data_{utils.get_collection_name(keyargs.get("datasets_record_path"))}',
                      keyargs.get('output_path'))

    return dataset_dict_list
