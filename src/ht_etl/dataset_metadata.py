'''
Dataset record processing.
'''
# standard
import os
import logging

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


def get_author_data(authors_data_path, filename):
    '''
    Gets and converts the author's Excel data to a CSV formatted String.

    Param
        filename, String, authors' XLSX file name, path.
        authors_data_path, String, authors' XLSX files path.

    Returns
        authors_raw, String, CSV formated String.
    '''
    if not filename:
        return None
    author_raw = filename
    excel_path = os.path.join(authors_data_path, filename)
    if os.path.isfile(excel_path) and excel_path.endswith('.xlsx'):
        raw = utils.get_data_frame(excel_path, 0, EC.ROWS_TO_SKIP)
        author_raw = raw.to_csv(encoding='utf-8')
    else:
        return None
    return author_raw


def get_growth_conditions(gc_raw):
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
    for condition in gc_raw.split('|'):
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
    dataframe_dict = utils.get_excel_data(filename)
    for row in dataframe_dict:
        dataset_dict = {}
        dataset_id = row[EC.DATASET_ID]
        serie_id = None
        if row[EC.SERIE_ID]:
            serie_id = (((row[EC.SERIE_ID]).split(' '))[0]).replace(';', '')
        print(dataset_id, serie_id)
        dataset_dict.setdefault('datasetID', dataset_id)
        if row[EC.PMID]:
            dataset_dict.setdefault(
                'publication', utils.get_pubmed_data(row[EC.PMID], keyargs.get('email')))
        else:
            dataset_dict.setdefault('publication',
                                    {
                                        'authors': row[EC.AUTHORS],
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
        dataset_dict.setdefault('temporalDatasetID', dataset_id)
        dataset_dict.setdefault(
            'growthConditions', get_growth_conditions(row[EC.GC_EXPERIMENTAL]))
        dataset_dict.setdefault('releaseDataControl', {
            'date': keyargs.get('release_process_date'),
            'version': keyargs.get('version'),
        })
        print(
            f'{keyargs.get("collection_path")}{EC.AUTHORS_PATHS}/{row[EC.DATASET_FILE_NAME]}')
        authors_data_list.append({
            'tfbindingAuthorsData': get_author_data(f'{keyargs.get("collection_path")}{EC.AUTHORS_PATHS}/', row[EC.DATASET_FILE_NAME]),
            'datasetId': dataset_id,
        })

        dataset_dict.setdefault('datasetType', keyargs.get('dataset_type'))

        if keyargs.get('dataset_type') == 'TFBINDING':
            if serie_id:
                bed_paths = f'{keyargs.get("collection_path")}{EC.BED_PATHS}/{serie_id}/datasets/{dataset_id}'
                if utils.validate_directory(bed_paths):
                    bed_paths = f'{bed_paths}/{dataset_id}'
                    sites_dict_list.extend(
                        sites_dataset.bed_file_mapping(
                            dataset_id,
                            f'{bed_paths}_sites.bed',
                            keyargs.get('db'),
                            keyargs.get('url'),
                            keyargs.get('genes_ranges'),
                            sites_dict_list
                        )
                    )
                    peaks_dict_list.extend(
                        peaks_datasets.bed_file_mapping(
                            dataset_id,
                            f'{bed_paths}_peaks.bed',
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
            "Peaks", peaks_dict_list, keyargs.get('organism'))
        utils.create_json(collection_data, "peaks", keyargs.get('output_path'))

        collection_data = utils.set_json_object(
            "Sites", sites_dict_list, keyargs.get('organism'))
        utils.create_json(collection_data, "sites", keyargs.get('output_path'))

    collection_data = utils.set_json_object(
        "AuthorsData", authors_data_list, keyargs.get('organism'))
    utils.create_json(collection_data, "authorsData",
                      keyargs.get('output_path'))

    return dataset_dict_list
