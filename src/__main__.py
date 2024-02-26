'''
    RegulonDB HT ETL.
'''
# standard
import logging
import datetime
import shutil
import os
import json

# third party

# local
from libs import arguments
from libs import utils
from ht_etl.ht import datasets
# from ht_etl import dataset_metadata, gene_expression_dataset_metadata


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
    datasets_objs = datasets.get_dataset(
        filename=kwargs.get('datasets_record_path', None),
        rows_to_skip=kwargs.get('rows_to_skip', None),
        dataset_type=kwargs.get('dataset_type', None),
        collection_name=kwargs.get('collection_name', None),
        email=kwargs.get('email', None),
        database=kwargs.get('db', None),
        url=kwargs.get('url', None),
        version=kwargs.get('version', None)
    )

    for dataset_obj in datasets_objs:
        dataset_obj_dict = {
            'dataset': dataset_obj.dataset.dataset_dict,
            'metadata': dataset_obj.metadata,
            'collectionName': kwargs.get('collection_name', None)
        }
        print(dataset_obj_dict)

    # exit()
    """if kwargs.get('datasets_record_path') is not None:
        print(f'Reading Datasets from {kwargs.get("datasets_record_path")}')
        logging.info(
            f'Reading Datasets from {kwargs.get("datasets_record_path")}')
        bnumbers_json = open(kwargs.get('bnumbers'))
        bnumbers_data = json.load(bnumbers_json)
        if kwargs.get('dataset_type') == 'GENE_EXPRESSION':
            gene_exp_out_path = os.path.join(kwargs.get(
                'output_path'), utils.get_collection_name(kwargs.get("datasets_record_path")))

            if os.path.isdir(gene_exp_out_path):
                shutil.rmtree(gene_exp_out_path)
            os.mkdir(gene_exp_out_path)
            datasets_list = gene_expression_dataset_metadata.open_tsv_file(
                kwargs, bnumbers_data)
        else:
            datasets_list = dataset_metadata.open_excel_file(
                file_name='',
                bnumbers_data=bnumbers_data
            )

        '''readme_file_path = f'{kwargs.get("collection_path")}README.md'
        if not os.path.isfile(readme_file_path):
            readme_file_path = f'{kwargs.get("collection_path")}README.md'
        elif os.path.isfile(readme_file_path):
            document = Document(readme_file_path)
            print(document)
            for para in document.paragraphs:
                print(para.text)'''

        collection_data = utils.set_json_object(
            "dataset", datasets_list, kwargs.get('organism'), 'MDD', None)
        utils.create_json(collection_data,
                          f'dataset_metadata_{utils.get_collection_name(kwargs.get("datasets_record_path"))}',
                          kwargs.get('output_path'))"""


if __name__ == '__main__':
    """
    Main function RegulonDB HT ETL.
    Initializes variables for program execution.
    """

    args = arguments.load_arguments()
    utils.set_log(args.log, args.collection_name, datetime.date.today())

    utils.validate_directories(args.output)

    output_dirs_path = f'{args.output}{args.collection_path.replace("../InputData/", "")}'
    if os.path.isdir(output_dirs_path):
        shutil.rmtree(output_dirs_path)

    print("Initializing RegulonDB HT ETL")
    logging.info(f'Initializing RegulonDB HT ETL')

    run(
        collection_name=args.collection_name,
        collection_path=args.collection_path,
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
        output_dirs_path=output_dirs_path
    )

    print(f'RegulonDB HT ETL process complete.')
    logging.info(f'RegulonDB HT ETL process complete')
