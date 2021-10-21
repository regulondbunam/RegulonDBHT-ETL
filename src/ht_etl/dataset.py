'''
Dataset record processing.
'''
# standard
import os
import logging

# third party


# local
from libs import utils
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
            keyargs.get('datasets_record_path'), keyargs.get('authors_data_path'), keyargs.get('bed_files_path'), keyargs))
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
    author_raw = filename
    excel_path = os.path.join(authors_data_path, filename)
    if os.path.isfile(excel_path) and excel_path.endswith('.xlsx'):
        raw = utils.get_data_frame(excel_path)
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
        'datasetType': dataset_type,
    }
    return sample


def excel_file_mapping(filename, authors_data_path, bed_files_path, keyargs):
    '''
    Reads one by one all the valid XLSX files and returns the corresponding data dictionaries.

    Param
        filename, String, full XLSX file path.
        authors_data_path, String, authors' XLSX file path.
        bed_files_path, String, bed files path.
        keyargs.db, String, Database to get some external data.
        keyargs.url, String, URL where database is located.
        keyargs.source_name, String, Excel record surce ("GEO or ArrayExpress").
        keyargs.dataset_type, String, Excel record type ["TF-BINDING", "GENE EXPRESION",
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
        dataset_dict.setdefault('datasetID', row['Dataset ID*'])
        dataset_dict.setdefault(
            'publication', utils.get_pubmed_data(row['PMID*'], keyargs.get('email')))
        dataset_dict.setdefault(
            'objectTested', utils.get_object_tested(row['Protein Name*'],
                                                    keyargs.get('db'),
                                                    keyargs.get('url')
                                                    )
        )
        dataset_dict.setdefault('sourceSerie', {
            'sourceId': row['ID Serie* (GEO or ArrayExpress)'],
            # TODO: pendiente si sera columna o se anota en el ID
            'sourceName': keyargs.get('source_name'),
            'title': row['Protein Name*'],
            'platformID': row['Platform ID'],
            'platformTitle': row['Platform Title'],
            # TODO: determinar si seran de una u otra coleccion
            'strategy': row['Strategy'],
            'method': row['Method Name'],
        })
        dataset_dict.setdefault('sample', set_sample(
            row['Samples Replicates Binding GEO ID Experiment  [ID, ID, ID] *'],
            row['Samples Replicates Binding GEO ID Control type1  [ID, ID, ID] Control type2 [ID, ID, ID]'],
            row['Sample GEO Title for all replicates']))
        dataset_dict.setdefault('linkedDataset', set_linked_dataset(
            row['Sample Replicates  Expression GEO ID Experimental [ID, ID, ID]'], row['Sample Replicates Expression GEO ID Control [ID, ID, ID]'], keyargs.get('dataset_type')))
        dataset_dict.setdefault('referenceGenome', row['Reference genome'])
        dataset_dict.setdefault('datasetType', keyargs.get('dataset_type'))
        dataset_dict.setdefault('temporalDatasetID', row['Dataset ID*'])
        dataset_dict.setdefault(
            'growthConditions', get_growth_conditions(row['Binding Growth Conditions Experimental*']))
        dataset_dict.setdefault('releaseDataControl', {
            'date': keyargs.get('release_process_date'),
            'version': keyargs.get('version'),
        })
        dataset_dict.setdefault('summary', {
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
        })
        peaks_dict_list.extend(peaks_datasets.bed_file_mapping(
            row['Dataset ID*'], f'{bed_files_path}/{row["Dataset ID*"]}/data/sequences/peak-motifs_test_seqcoord.bed', keyargs.get('db'), keyargs.get('url')))

        sites_dict_list.extend(sites_dataset.bed_file_mapping(
            row['Dataset ID*'], f'{bed_files_path}/{row["Dataset ID*"]}/results/sites/peak-motifs_all_motifs_seqcoord.bed', keyargs.get('db'), keyargs.get('url')))
        authors_data_list.append({
            'tfbindingAuthorsData': get_author_data(authors_data_path, row['TFBS Dataset File Name']),
            'datasetId': row['Dataset ID*'],
        })
        dataset_dict_list.append(dataset_dict)

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
