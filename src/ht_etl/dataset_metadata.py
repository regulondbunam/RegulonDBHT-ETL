'''
Dataset record processing.
'''
# standard
import os
import logging
import shutil
import re

# third party


# local
from src.libs import utils
from src.libs import constants
from src.ht_etl import peaks_datasets, sites_dataset, tu_datasets, tss_datasets, tts_datasets


def open_excel_file(keyargs, bnumbers_data):
    """
    This function lists and filters all XLSX files in the directory path.

    Param
        excel_path, String, Excel file path.

    Returns
        collection_data, List, list of datasets dictionaries.
    """

    collection_data = []

    if os.path.isfile(keyargs.get('datasets_record_path')) and keyargs.get('datasets_record_path').endswith('.xlsx'):
        collection_data.extend(excel_file_mapping(
            keyargs.get('datasets_record_path'), keyargs, bnumbers_data))
    else:
        logging.warning(
            f'{keyargs.get("datasets_record_path")} is not a valid XLSX file will be ignored')

    return collection_data


def get_author_data(authors_data_path, filename, dataset_id):
    """
    Gets and converts the author's Excel data to a CSV formatted String.

    Param
        filename, String, authors' XLSX file name, path.
        authors_data_path, String, authors' XLSX files path.

    Returns
        authors_raw, String, CSV formatted String.
    """
    # print('Getting authors data')
    if not filename:
        logging.error(
            f'There is not File Name for {dataset_id} can not read Author\'s files')
        return None
    author_raw = filename
    excel_path = os.path.join(authors_data_path, filename)
    # print(author_raw, excel_path)
    # print(os.path.isfile(excel_path))
    if os.path.isfile(excel_path) and excel_path.endswith('.xlsx'):
        # print('IS A XLSX')
        raw = utils.get_author_data_frame(str(excel_path), 0, 0)
        author_raw = raw.to_csv(encoding='utf-8')
        logging.info(
            f'Reading Author\'s Data files {excel_path}')
        return author_raw
    elif os.path.isfile(excel_path) and excel_path.endswith('.tsv'):
        # print('IS A TSV')
        raw = utils.get_author_data_frame_tsv(str(excel_path))
        raw = raw.loc[:, ~raw.columns.str.contains('^Unnamed')]
        author_raw = raw.to_csv(encoding='utf-8', index=True)
        author_raw = author_raw.replace(',,,,,#', '#')
        logging.info(
            f'Reading Author\'s Data files {excel_path}')
        return author_raw
    elif os.path.isfile(excel_path) and excel_path.endswith('.txt'):
        # print('IS A TSV')
        raw = utils.get_author_data_frame_tsv(str(excel_path))
        raw = raw.loc[:, ~raw.columns.str.contains('^Unnamed')]
        author_raw = raw.to_csv(encoding='utf-8', index=True)
        author_raw = author_raw.replace(',,,,,#', '#')
        logging.info(
            f'Reading Author\'s Data files {excel_path}')
        return author_raw
    else:
        '''print(
            f'There are not valid Author\'s Data files for {dataset_id} can not read Author\'s files'
        )'''
        logging.error(
            f'There are not valid Author\'s Data files for {dataset_id} can not read Author\'s files')
        return None


def get_growth_conditions(gc_raw, dataset_id):
    """
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

    """
    gc_dict = {}
    if not gc_raw:
        return None
    if ' |' not in gc_raw:
        gc_dict = {
            'otherTerms': gc_raw
        }
        return gc_dict
    gc_list = gc_raw.split(' |')
    for condition in gc_list:
        if ':' in condition:
            condition = condition.split(':')
            gc_dict.setdefault(utils.to_camel_case(
                condition[0].lower()), condition[1])
        else:
            logging.error(
                f'There are not valid Growth Conditions for {dataset_id} can not read property')
    if gc_dict:
        gc_dict = {k: v for k, v in gc_dict.items() if v}
    return gc_dict


def set_sample(experiment_id, control_id, title):
    """
    Formats sample object and converts IDs Strings into Strings arrays.

    Param
        experiment_id, String, Sample experiment ID un-formatted.
        control_id, String, Sample control ID unformatted.
        title, String, Sample title.

    Returns
        sample, Dict, dictionary with the formatted Sample data.
    """
    if not experiment_id:
        experiment_id = None
    else:
        experiment_id = experiment_id.rstrip()
        experiment_id = experiment_id.replace('] [', ', ').replace(
            '[', '').replace(']', '').split(', ')
    if not control_id:
        control_id = None
    else:
        control_id = control_id.rstrip()
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
    if title:
        title = title.rstrip()
    sample = {
        'experimentId': experiment_ids,
        'controlId': control_ids,
        'title': title,
    }
    if sample:
        sample = {k: v for k, v in sample.items() if v}
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
        experiment_id = experiment_id.rstrip()
        experiment_id = experiment_id.replace('] [', ', ').replace(
            '[', '').replace(']', '').split(', ')
    if not control_id:
        control_id = None
    else:
        control_id = control_id.rstrip()
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

    linked_dataset = {
        'experimentId': experiment_ids,
        'controlId': control_ids,
        'datasetType': dataset_type,
    }
    if linked_dataset:
        linked_dataset = {k: v for k, v in linked_dataset.items() if v}
    return linked_dataset


def excel_file_mapping(filename, keyargs, bnumbers_data):
    '''
    Reads one by one all the valid XLSX files and returns the corresponding data dictionaries.

    Param
        filename, String, full XLSX file path.
        keyargs.collection_path, String, Path to read de origin files data.
        keyargs.db, String, Database to get some external data.
        keyargs.url, String, URL where database is located.
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
    tus_dict_list = []
    tss_dict_list = []
    tts_dict_list = []

    dataframe_dict = utils.get_excel_data(filename, keyargs.get(
        'metadata_sheet'), keyargs.get('rows_to_skip'))
    for row in dataframe_dict:
        dataset_dict = {}
        dataset_id = row.get(constants.DATASET_ID, None)
        if dataset_id is None:
            logging.error(
                f'Not Dataset ID')
            continue
        dataset_id = str(dataset_id).rstrip()
        # Publications
        pmid = row.get(constants.PMID, None)
        if pmid:
            dataset_dict.setdefault(
                'publications', utils.get_pubmed_data(pmid, keyargs.get('email')))

        # ObjectsTested
        tf_name = row.get(constants.TF_NAME, None)
        if not tf_name:
            tf_name = row.get(constants.TF_NAME_CHIP, None)
        if not tf_name:
            tf_name = row.get(constants.PROTEIN_NAME, None)
        if not tf_name:
            tf_name = row.get(constants.TF_NAME_TEC, None)
        if not tf_name:
            tf_name = row.get(constants.TF_NAME_RDB, None)
        if not tf_name:
            tf_name = row.get(constants.TF_COMMON_NAME, None)
        if not tf_name:
            tf_name = row.get(constants.TF_NAME_SOURCE, None)
        if tf_name:
            tf_name = tf_name.rstrip()
            if re.findall('([α-ωΑ-Ω])', tf_name):
                tf_name = row.get(constants.TF_NAME_SOURCE, None)
            tf_name = tf_name.replace(' ', '')
            tf_name = tf_name.split(',')
            if isinstance(tf_name, str):
                tf_name = [tf_name]
        dataset_dict.setdefault(
            'objectsTested', utils.get_object_tested(tf_name,
                                                     keyargs.get('db'),
                                                     keyargs.get('url')
                                                     )
        )
        # SourceSerie
        series_list = []
        serie_id = row.get(constants.SERIE_ID, None)
        serie_db = row.get(constants.SOURCE_DATABASE, None)
        serie_obj = {
            'sourceId': serie_id,
            'sourceName': serie_db,
        }
        if serie_obj:
            serie_obj = {k: v for k, v in serie_obj.items() if v}
        if serie_obj != {}:
            series_list.append(serie_obj)

        platform_id = row.get(constants.PLATFORM_ID, None)
        platform_title = row.get(constants.PLATFORM_TITLE, None)
        platform_obj = {
            '_id': platform_id,
            'title': platform_title,
        }
        platform_obj = {k: v for k, v in platform_obj.items() if v}

        source_db = row.get(constants.SOURCE_DATABASE, None)
        strategy = row.get(constants.STRATEGY, None)
        if strategy:
            strategy = strategy.rstrip()
        method_name = row.get(constants.METHOD_NAME, None)
        if method_name:
            method_name = method_name.rstrip()
        experiment_title = row.get(constants.EXPERIMENT_TITLE, None)
        if experiment_title:
            experiment_title = experiment_title.rstrip()

        source_serie_obj = {
            'series': series_list,
            'platform': platform_obj,
            'sourceDB': source_db,
            'title': experiment_title,
            'strategy': strategy,
            'method': method_name,
        }
        if source_serie_obj:
            source_serie_obj = {k: v for k, v in source_serie_obj.items() if v}
        dataset_dict.setdefault('sourceSerie', source_serie_obj)
        # Sample
        dataset_dict.setdefault('sample',
                                set_sample(
                                    row.get(
                                        constants.SAMPLES_REPLICATES_EXPERIMET_ID, None),
                                    row.get(
                                        constants.SAMPLES_REPLICATES_CONTROL_ID, None),
                                    row.get(constants.TITLE_FOR_ALL_REPLICATES, None))
                                )
        linked_dataset_type = None
        if keyargs.get('dataset_type') == 'TFBINDING':
            linked_dataset_type = 'GeneExpression'
        dataset_dict.setdefault('linkedDataset',
                                set_linked_dataset(
                                    row.get(
                                        constants.SAMPLES_EXPERIMET_REPLICATES_EXPRESSION_ID, None),
                                    row.get(
                                        constants.SAMPLES_CONTROL_REPLICATES_EXPRESSION_ID, None),
                                    linked_dataset_type)
                                )
        # LinkedDataset
        ref_genome = row.get(constants.REFERENCE_GENOME, None)
        if ref_genome:
            ref_genome = ref_genome.rstrip()
        dataset_dict.setdefault('referenceGenome', ref_genome)
        gc_metadata = row.get(constants.GC_EXPERIMENTAL, None)
        if gc_metadata:
            gc_metadata = gc_metadata.rstrip()
        gc_dict = get_growth_conditions(gc_metadata, dataset_id)
        if gc_dict:
            dataset_dict.setdefault('growthConditions', gc_dict)
        dataset_dict.setdefault('releaseDataControl', {
            'date': keyargs.get('release_process_date'),
            'version': keyargs.get('version'),
        })
        assembly_genome_id = row.get(constants.ASSEMBLY_GENOME_ID, None)
        if assembly_genome_id:
            assembly_genome_id = assembly_genome_id.rstrip()
        dataset_dict.setdefault('assemblyGenomeId', assembly_genome_id)
        five_enrichment = row.get(constants.FIVE_ENRICHMENT, None)
        if five_enrichment:
            five_enrichment = five_enrichment.rstrip()
        dataset_dict.setdefault('fivePrimeEnrichment', five_enrichment)
        experiment_condition = row.get(constants.EXPERIMENT_CONDITION, None)
        if experiment_condition:
            experiment_condition = experiment_condition.rstrip()
        dataset_dict.setdefault('experimentCondition', experiment_condition)
        dataset_dict.setdefault('datasetType', keyargs.get('dataset_type'))
        dataset_dict.setdefault('cutOff', row.get(constants.CUT_OFF, None))
        dataset_dict.setdefault('notes', row.get(constants.PUBLIC_NOTES, None))

        source_reference_genome = row.get(constants.SOURCE_REFERENCE_GENOME, None)
        if source_reference_genome:
            source_reference_genome = source_reference_genome.strip()
        dataset_dict.setdefault(
            'sourceReferenceGenome',
            source_reference_genome
        )

        external_references = row.get(constants.EXTERNAL_DB_LINK, None)
        if external_references:
            dataset_dict.setdefault('externalReferences', utils.get_external_reference(
                external_references))

        datasets_source_path = f'{keyargs.get("collection_path")}{constants.BED_PATHS}/{serie_id}/datasets/{dataset_id}'
        old_dataset_id = row.get(constants.OLD_DATASET_ID, None)
        if old_dataset_id:
            datasets_source_path = f'{keyargs.get("collection_path")}{constants.BED_PATHS}/{serie_id}/datasets/{old_dataset_id}'
        print(datasets_source_path)
        new_dataset_id = f'{keyargs.get("dataset_type")}_{dataset_id}'
        new_datasets_path = f'{keyargs.get("output_dirs_path")}{new_dataset_id}'

        # Uniformized TFBINDING
        if keyargs.get('dataset_type') == 'TFBINDING':
            if serie_id:
                if utils.validate_directory(datasets_source_path):
                    logging.info(
                        f'Coping datasets from {datasets_source_path} \n\t to {new_datasets_path}')
                    shutil.copytree(datasets_source_path, new_datasets_path)
                    bed_path = f'{datasets_source_path}/{dataset_id}'
                    if old_dataset_id:
                        bed_path = f'{datasets_source_path}/{old_dataset_id}'
                    tf_sites_ids = utils.get_sites_ids_by_tf(
                        tf_name,
                        keyargs.get('db'),
                        keyargs.get('url'),)
                    tf_sites = []
                    for tf_site_id in tf_sites_ids:
                        tf_site = utils.get_tf_sites_abs_pos(
                            tf_site_id, keyargs.get('db'), keyargs.get('url'))
                        if tf_site:
                            tf_sites.append(tf_site)
                    sites_dict_list.extend(
                        sites_dataset.bed_file_mapping(
                            new_dataset_id,
                            f'{bed_path}_sites.bed',
                            keyargs.get('db'),
                            keyargs.get('url'),
                            keyargs.get('genes_ranges'),
                            sites_dict_list,
                            keyargs.get('collection_path'),
                            tf_sites
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

        # Uniformized TUS
        if keyargs.get('dataset_type') == 'TUS':
            datasets_source_path = f'{keyargs.get("collection_path")}{constants.TSV_PATHS}'
            if utils.validate_directory(datasets_source_path):
                logging.info(
                    f'Coping datasets from {datasets_source_path} \n\t to {new_datasets_path}')
                shutil.copytree(datasets_source_path, new_datasets_path)
                bed_path = f'{datasets_source_path}/{dataset_id}'
                tus_dict_list.extend(
                    tu_datasets.file_mapping(
                        new_dataset_id,
                        f'{bed_path}.tsv',
                        keyargs.get('db'),
                        keyargs.get('url'),
                        keyargs.get("dataset_type"),
                        bnumbers_data
                    )
                )

        # Uniformized TSS
        if keyargs.get('dataset_type') == 'TSS':
            datasets_source_path = f'{keyargs.get("collection_path")}{constants.TSV_PATHS}'
            if utils.validate_directory(datasets_source_path):
                logging.info(
                    f'Coping datasets from {datasets_source_path} \n\t to {new_datasets_path}')
                shutil.copytree(datasets_source_path, new_datasets_path)
                bed_path = f'{datasets_source_path}/{dataset_id}'
                tss_dict_list.extend(
                    tss_datasets.file_mapping(
                        new_dataset_id,
                        f'{bed_path}.tsv',
                        keyargs.get('db'),
                        keyargs.get('url'),
                        keyargs.get("dataset_type"),
                        keyargs.get('genes_ranges'),
                        bnumbers_data
                    )
                )

        # Uniformized TTS
        if keyargs.get('dataset_type') == 'TTS':
            datasets_source_path = f'{keyargs.get("collection_path")}{constants.TSV_PATHS}'
            if utils.validate_directory(datasets_source_path):
                logging.info(
                    f'Coping datasets from {datasets_source_path} \n\t to {new_datasets_path}')
                shutil.copytree(datasets_source_path, new_datasets_path)
                bed_path = f'{datasets_source_path}/{dataset_id}'
                tts_dict_list.extend(
                    tts_datasets.file_mapping(
                        new_dataset_id,
                        f'{bed_path}.tsv',
                        keyargs.get('db'),
                        keyargs.get('url'),
                        keyargs.get("dataset_type"),
                        keyargs.get('genes_ranges'),
                        bnumbers_data
                    )
                )

        if keyargs.get('dataset_type') == 'TFBINDING':
            collection_type = utils.get_collection_type(
                keyargs.get("collection_path"))
            new_dataset_id = f'{keyargs.get("dataset_type")}_{collection_type}{dataset_id}'
        print(new_dataset_id)
        dataset_dict.setdefault('temporalId', new_dataset_id)
        dataset_dict.setdefault('_id', new_dataset_id)

        # Author's Files
        authors_file = row.get(constants.DATASET_FILE_NAME, None)
        if authors_file:
            authors_file = authors_file.rstrip()
        authors_data_string = get_author_data(
            f'{keyargs.get("collection_path")}{constants.AUTHORS_PATHS}/', authors_file, dataset_id)
        '''print(f'{keyargs.get("collection_path")}{EC.AUTHORS_PATHS}/',
              f'"{authors_file}"', dataset_id)'''
        if authors_data_string:
            authors_data_string = re.sub(
                "Unnamed\:\s\d*\,{0,1}", "", authors_data_string)
            authors_data = {
                'authorsData': authors_data_string,
                '_id': f'AD_{new_dataset_id}',
                'datasetIds': [new_dataset_id]
            }
            if authors_data.get('authorsData'):
                authors_data_list.append(authors_data)
        elif not authors_data_string:
            print(
                f'No authors data for dataset:{dataset_id}, author file required: {authors_file}')
        summary_obj = {
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
        if summary_obj:
            summary_obj = {k: v for k, v in summary_obj.items() if v}
        dataset_dict.setdefault(
            'summary', summary_obj
        )
        dataset_dict = {k: v for k, v in dataset_dict.items() if v}
        dataset_dict_list.append(dataset_dict)

    if keyargs.get('dataset_type') == 'TTS':
        collection_data = utils.set_json_object(
            "transcriptionTerminationSite", tts_dict_list, keyargs.get('organism'), 'TTD', 'TT')
        utils.create_json(
            collection_data, f'tts_{utils.get_collection_name(keyargs.get("datasets_record_path"))}', keyargs.get('output_path'))
        collection_data = utils.set_json_object(
            "authorsData", authors_data_list, keyargs.get('organism'), 'TTD', 'AD')
        utils.create_json(collection_data, f'authors_data_{utils.get_collection_name(keyargs.get("datasets_record_path"))}',
                          keyargs.get('output_path'))

    if keyargs.get('dataset_type') == 'TSS':
        collection_data = utils.set_json_object(
            "transcriptionStartSite", tss_dict_list, keyargs.get('organism'), 'TSD', 'TS')
        utils.create_json(
            collection_data, f'tss_{utils.get_collection_name(keyargs.get("datasets_record_path"))}', keyargs.get('output_path'))
        collection_data = utils.set_json_object(
            "authorsData", authors_data_list, keyargs.get('organism'), 'TSD', 'AD')
        utils.create_json(collection_data, f'authors_data_{utils.get_collection_name(keyargs.get("datasets_record_path"))}',
                          keyargs.get('output_path'))

    if keyargs.get('dataset_type') == 'TUS':
        collection_data = utils.set_json_object(
            "transcriptionUnit", tus_dict_list, keyargs.get('organism'), 'TUD', 'TU')
        utils.create_json(
            collection_data, f'tus_{utils.get_collection_name(keyargs.get("datasets_record_path"))}', keyargs.get('output_path'))
        collection_data = utils.set_json_object(
            "authorsData", authors_data_list, keyargs.get('organism'), 'TUD', 'AD')
        utils.create_json(collection_data, f'authors_data_{utils.get_collection_name(keyargs.get("datasets_record_path"))}',
                          keyargs.get('output_path'))

    if keyargs.get('dataset_type') == 'TFBINDING' or keyargs.get('dataset_type') == 'RNAP_BINDING_SITES':
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

    if peaks_dict_list is [] and authors_data_list is []:
        logging.error(
            f'There are not peaks and authors data in {dataset_id}')

    return dataset_dict_list
