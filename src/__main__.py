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
from ht_etl import dataset


def set_json_object(filename, data_list, organism):
    '''
    Sets the JSON output format of the collection..

    Param
        filename, String, the the output file name.
        data_list, List, the list with the collection data.
        organism, String, the organism name.

    Returns
        json_object, Dict, the dictionary with the final JSON file format
    '''
    json_object = {
        "collectionName": filename,
        "collectionData": data_list,
        "organism": organism
    }
    return json_object


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
        datasets_list = dataset.open_excel_file(keyargs)
        collection_data = set_json_object(
            "Dataset", datasets_list, keyargs.get('organism'))
        utils.create_json(collection_data, "dataset",
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
        'dataset_type': args.dataset_type
    }
    utils.validate_directories(keyargs.get('output_path'))

    print("Initializing RegulonDB HT ETL")
    logging.info(f'Initializing RegulonDB HT ETL')

    run(keyargs)
