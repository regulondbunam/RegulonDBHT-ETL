'''
    RegulonDB HT ETL.
'''
# standard
import logging
import datetime
import shutil
import os

# third party


# local
from libs import arguments
from libs import utils
from ht_etl import dataset_metadata, gene_expression_dataset_metadata, gene_exp_datasets


def run(keyargs):
    '''
    Run function, controls program functions and generates output files.

    Param
        keyargs.datasets_record_path, String, Datasets record path.
        keyargs.output_path, String, Output directory path.
        keyargs.organism, String, Organism name.
    '''

    if keyargs.get('datasets_record_path') is not None:
        print(f'Reading Datasets from {keyargs.get("datasets_record_path")}')
        logging.info(
            f'Reading Datasets from {keyargs.get("datasets_record_path")}')
        datasets_list = []
        if keyargs.get('dataset_type') == 'GENE_EXPRESSION':
            gene_exp_out_path = os.path.join(keyargs.get(
                'output_path'), utils.get_collection_name(keyargs.get("datasets_record_path")))

            if os.path.isdir(gene_exp_out_path):
                shutil.rmtree(gene_exp_out_path)
            os.mkdir(gene_exp_out_path)
            datasets_list = gene_expression_dataset_metadata.open_tsv_file(
                keyargs)
        else:
            datasets_list = dataset_metadata.open_excel_file(keyargs)
        collection_data = utils.set_json_object(
            "dataset", datasets_list, keyargs.get('organism'), 'MDD', None)
        utils.create_json(collection_data, f'dataset_metadata_{utils.get_collection_name(keyargs.get("datasets_record_path"))}',
                          keyargs.get('output_path'))


if __name__ == '__main__':
    '''
    Main function RegulonDB HT ETL.
    Initializes variables for program execution.
    '''

    args = arguments.load_arguments()

    utils.set_log(args.log)

    keyargs = {
        'collection_path': args.collection_path,
        'release_process_date': str(datetime.datetime.now()),
        'datasets_record_path': args.input,
        'output_path': args.output,
        'organism': args.organism,
        'version': args.version,
        'url': args.url,
        'db': args.database,
        'email': args.email,
        'dataset_type': args.dataset_type,
        'metadata_sheet': args.sheet,
        'rows_to_skip': int(args.rows_to_skip),
        'genes_ranges': utils.set_genome_intervals()
    }
    utils.validate_directories(keyargs.get('output_path'))

    keyargs.setdefault('output_dirs_path',
                       f'{keyargs.get("output_path")}{(keyargs.get("collection_path")).replace("../InputData/", "")}')
    if os.path.isdir(keyargs.get("output_dirs_path")):
        shutil.rmtree(keyargs.get('output_dirs_path'))

    print("Initializing RegulonDB HT ETL")
    logging.info(f'Initializing RegulonDB HT ETL')

    run(keyargs)

    logging.info(f'RegulonDB HT ETL process complete')
