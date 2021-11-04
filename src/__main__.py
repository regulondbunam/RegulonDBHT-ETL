'''
    RegulonDB HT ETL.
'''
# standard
import logging
import datetime

# third party


# local
from libs import arguments
from libs import utils
from ht_etl import dataset_metadata


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
        datasets_list = dataset_metadata.open_excel_file(keyargs)
        collection_data = utils.set_json_object(
            "Dataset", datasets_list, keyargs.get('organism'))
        utils.create_json(collection_data, "dataset_metadata",
                          keyargs.get('output_path'))


if __name__ == '__main__':
    '''
    Main function RegulonDB HT ETL.
    Initializes variables for program execution.
    '''

    args = arguments.load_arguments()

    utils.set_log(args.log)

    keyargs = {
        'release_process_date': str(datetime.datetime.now()),
        'datasets_record_path': args.input,
        'authors_data_path': args.author,
        'bed_files_path': args.bed,
        'output_path': args.output,
        'organism': args.organism,
        'version': args.version,
        'url': args.url,
        'db': args.database,
        'email': args.email,
        'source_name': args.source_name,
        'dataset_type': args.dataset_type,
        'genes_ranges': utils.set_genome_intervals()
    }
    utils.validate_directories(keyargs.get('output_path'))

    print("Initializing RegulonDB HT ETL")
    logging.info(f'Initializing RegulonDB HT ETL')

    run(keyargs)

    logging.info(f'RegulonDB HT ETL process complete')
