"""
    RegulonDB HT ETL.
"""
# standard
import logging
import datetime
import shutil
import os

# third party
import multigenomic_api as mg_api

# local
from libs import arguments
from libs import utils
from libs import file_manager
from ht_etl.ht import datasets
from libs import constants


def run(**kwargs):
    """
    Run function, controls program functions and generates output files.

    Param
        kwargs.datasets_record_path, String, Datasets record path.
        kwargs.output_path, String, Output directory path.
        kwargs.organism, String, Organism name.
    """
    print(f"Reading data from {kwargs.get('datasets_record_path', None)}")
    logging.info(f"Reading data from {kwargs.get('datasets_record_path', None)}")

    bnumbers_data = file_manager.read_json_file(kwargs.get('bnumbers'))

    datasets_objs = datasets.get_dataset(
        bnumbers=bnumbers_data,
        mg_api=mg_api,
        filename=kwargs.get('datasets_record_path', None),
        rows_to_skip=kwargs.get('rows_to_skip', None),
        dataset_type=kwargs.get('dataset_type', None),
        collection_name=kwargs.get('collection_name', None),
        email=kwargs.get('email', None),
        database=kwargs.get('db', None),
        url=kwargs.get('url', None),
        version=kwargs.get('version', None),
        collection_source=kwargs.get('collection_source', None),
        collection_path=kwargs.get('collection_path', None),
        collection_status=kwargs.get('collection_status', None),
        genes_ranges=kwargs.get('genes_ranges', None)
    )

    dataset_list = []
    authors_data_list = []
    tfbinding_data_list = []
    peaks_data_list = []
    tus_data_list = []
    tss_data_list = []
    tts_data_list = []
    nlp_gc_data_list = []
    metadata_list = []

    for dataset_obj in datasets_objs:
        dataset_obj_dict = dataset_obj.dataset
        dataset_list.append(dataset_obj_dict)
        if dataset_obj.metadata and kwargs.get('dataset_type', None) != constants.RNA:
            found_metadata = utils.find_one_in_dict_list(
                dict_list=metadata_list,
                key_name='_id',
                value=dataset_obj.metadata.get('_id')
            )
            if not found_metadata:
                metadata_list.append(dataset_obj.metadata)
            else:
                new_ref = dataset_obj.metadata.get('reference', None)
                if new_ref:
                    last_ref = found_metadata.get('reference')
                    if new_ref not in last_ref:
                        last_ref.extend(new_ref)
                    last_ref = list(set(last_ref))
                    found_metadata.update({'reference': last_ref})
        if dataset_obj.authors_data:
            authors_data_list.append(dataset_obj.authors_data)
        if kwargs.get('dataset_type', None) == constants.TFBINDING:
            tfbinding_data_list.extend(dataset_obj.sites)
            peaks_data_list.extend(dataset_obj.peaks)
        if kwargs.get('dataset_type', None) == constants.TUS:
            for tu in dataset_obj.tus:
                if tu not in tus_data_list:
                    tus_data_list.append(tu)
        if kwargs.get('dataset_type', None) == constants.TSS:
            for tss in dataset_obj.tss:
                if tss not in tss_data_list:
                    tss_data_list.append(tss)
        if kwargs.get('dataset_type', None) == constants.TTS:
            for tts in dataset_obj.tts:
                if tts not in tts_data_list:
                    tts_data_list.append(tts)
        if kwargs.get('dataset_type', None) == constants.RNA:
            if not nlp_gc_data_list:
                nlp_gc_data_list.extend(dataset_obj.nlp_growth_conditions_list)
            gene_expression_data_list = dataset_obj.gene_expressions
            genex_data = file_manager.set_json_object(
                filename=f"geneExpression",
                data_list=gene_expression_data_list,
                organism=kwargs.get('organism'),
                sub_class_acronym='GED',
                child_class_acronym='GE'
            )
            file_manager.create_json(
                objects=genex_data,
                filename=f'gene_expression_data_{dataset_obj.dataset.get("_id")}_{kwargs.get("collection_source")}_'
                         f'{kwargs.get("collection_name")}',
                output=f"../VerifiedPersistentIdentifiers/gene_expression/"
            )

    collection_metadata = file_manager.set_json_object(
        filename="metadata",
        data_list=metadata_list,
        organism=kwargs.get('organism'),
        sub_class_acronym='MDD',
        child_class_acronym=None
    )
    file_manager.create_json(
        objects=collection_metadata,
        filename=f'dataset_metadata_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
        output='../VerifiedPersistentIdentifiers/'
    )

    output_path = kwargs.get('output_path')
    if kwargs.get('dataset_type', None) == constants.RNA:
        output_path = f"../VerifiedPersistentIdentifiers/"

    collection_data = file_manager.set_json_object(
        filename="dataset",
        data_list=dataset_list,
        organism=kwargs.get('organism'),
        sub_class_acronym='MDD',
        child_class_acronym=None
    )
    file_manager.create_json(
        objects=collection_data,
        filename=f'dataset_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
        output=output_path
    )

    authors_data = file_manager.set_json_object(
        filename="authorsData",
        data_list=authors_data_list,
        organism=kwargs.get('organism'),
        sub_class_acronym='BSD',
        child_class_acronym='AD'
    )
    file_manager.create_json(
        objects=authors_data,
        filename=f'authors_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
        output=output_path
    )

    if kwargs.get('dataset_type', None) == constants.TFBINDING:
        tfbinding_data = file_manager.set_json_object(
            filename="tfBinding",
            data_list=tfbinding_data_list,
            organism=kwargs.get('organism'),
            sub_class_acronym='BSD',
            child_class_acronym='BS'
        )
        file_manager.create_json(
            objects=tfbinding_data,
            filename=f'tfbinding_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
            output=kwargs.get('output_path')
        )
        peaks_data = file_manager.set_json_object(
            filename="peaks",
            data_list=peaks_data_list,
            organism=kwargs.get('organism'),
            sub_class_acronym='BSD',
            child_class_acronym='PK'
        )
        file_manager.create_json(
            objects=peaks_data,
            filename=f'peaks_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
            output=kwargs.get('output_path')
        )

    if kwargs.get('dataset_type', None) == constants.TUS:
        tus_data = file_manager.set_json_object(
            filename="transcriptionUnit",
            data_list=tus_data_list,
            organism=kwargs.get('organism'),
            sub_class_acronym='TUD',
            child_class_acronym='TU'
        )
        file_manager.create_json(
            objects=tus_data,
            filename=f'tus_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
            output=kwargs.get('output_path')
        )

    if kwargs.get('dataset_type', None) == constants.TSS:
        tss_data = file_manager.set_json_object(
            filename="transcriptionStartSite",
            data_list=tss_data_list,
            organism=kwargs.get('organism'),
            sub_class_acronym='TSD',
            child_class_acronym='TS'
        )
        file_manager.create_json(
            objects=tss_data,
            filename=f'tss_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
            output=kwargs.get('output_path')
        )

    if kwargs.get('dataset_type', None) == constants.TTS:
        tts_data = file_manager.set_json_object(
            filename="transcriptionTerminationSite",
            data_list=tts_data_list,
            organism=kwargs.get('organism'),
            sub_class_acronym='TTD',
            child_class_acronym='TT'
        )
        file_manager.create_json(
            objects=tts_data,
            filename=f'tts_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
            output=kwargs.get('output_path')
        )

    if kwargs.get('dataset_type', None) == constants.RNA:
        nlp_gc_data = file_manager.set_json_object(
            filename="nlpGrowthConditions",
            data_list=nlp_gc_data_list,
            organism=kwargs.get('organism'),
            sub_class_acronym='NLP_GC',
            child_class_acronym='GC'
        )
        file_manager.create_json(
            objects=nlp_gc_data,
            filename=f'nlp_growth_conditions_data_{kwargs.get("collection_source")}_{kwargs.get("collection_name")}',
            output=f"../VerifiedPersistentIdentifiers/"
        )


if __name__ == '__main__':
    """
    Main function RegulonDB HT ETL.
    Initializes variables for program execution.
    """

    args = arguments.load_arguments()

    mg_api.connect(args.database, args.url)

    file_manager.set_log(args.log, args.collection_name, datetime.date.today())

    file_manager.validate_directories(args.output)

    output_dirs_path = f'{args.output}{args.collection_path.replace("../InputData/", "")}'
    if os.path.isdir(output_dirs_path):
        shutil.rmtree(output_dirs_path)

    print("Initializing RegulonDB HT ETL")
    logging.info(f'Initializing RegulonDB HT ETL')

    run(
        collection_name=args.collection_type,
        collection_path=args.collection_path,
        collection_source=args.collection_source,
        release_process_date=str(datetime.datetime.now()),
        datasets_record_path=args.input,
        output_path=args.output,
        organism=args.organism,
        version=args.version,
        url=args.url,
        db=args.database,
        email=args.email,
        dataset_type=args.dataset_type,
        metadata_sheet=args.sheet,
        rows_to_skip=int(args.rows_to_skip),
        genes_ranges=utils.set_genome_intervals(),
        bnumbers=args.bnumbers,
        output_dirs_path=output_dirs_path,
        collection_status=args.collection_status
    )

    print(f'RegulonDB HT ETL process complete.')
    logging.info(f'RegulonDB HT ETL process complete')
