"""
Functions for managing files and folders.
"""
# standard
import os
import re
import json
import logging

# third party
import pandas

# local


def validate_directories(data_path):
    """
    Verify if the output path directories exists.

    Args:
        data_path: String, directories path.

    Returns:
        Rise IOError if not valid directory
    """
    if not os.path.isdir(data_path):
        raise IOError("Please, verify '{}' directory path".format(data_path))


def set_log(log_path, log_name, log_date):
    """
    Initializes the execution log to examine any problems that arise during extraction.

    Args:
        log_date: String, the execution date.
        log_name: String, the name of the log file.
        log_path: String, the execution log path.
    """
    log_file_name = f'ht_etl_{log_name}_{log_date}.log'
    log_file_name = log_file_name.replace('/', '')
    log_file_name = log_file_name.replace('-', '_')
    validate_directories(log_path)
    logging.basicConfig(filename=os.path.join(log_path, log_file_name),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def set_json_object(filename, data_list, organism, sub_class_acronym, child_class_acronym):
    """
    Sets the JSON output format of the collection.

    Args:
        filename: String, the output file name.
        sub_class_acronym: String, the subclass acronym.
        child_class_acronym: String, the class child acronym.
        data_list: List, the list with the collection data.
        organism: String, the organism name.

    Returns:
        json_object: Dict, the dictionary with the final JSON file format
    """
    json_object = {
        'collectionName': filename,
        'collectionData': data_list,
        'organism': organism,
        'subClassAcronym': sub_class_acronym,
        'classAcronym': organism,
        'childClassAcronym': child_class_acronym,
    }
    return json_object


def create_json(objects, filename, output):
    """
    Create and write the JSON file with the results.

    Args:
        objects: Object, a Python serializable object that you want to convert to JSON format.
        filename: String, JSON file name.
        output: String, output path.
    """
    filename = os.path.join(output, filename)
    logging.info(f'Writing JSON file {filename}')
    with open(f'{filename}.json', 'w') as json_file:
        json.dump(objects, json_file, indent=4, sort_keys=True)


def get_data_frame(filename: str, load_sheet: str, rows_to_skip: int) -> pandas.DataFrame:
    """
    Read and convert the Excel file to Panda DataFrame.

    Args:
        filename: String, Excel file name.
        load_sheet: String, Excel sheet name.
        rows_to_skip: Int, Number of rows to skip before table.

    Returns:
        dataset_df: pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    """
    dataset_df = pandas.read_excel(
        filename, sheet_name=load_sheet, skiprows=rows_to_skip)
    return dataset_df


def get_json_from_data_frame(data_frame: pandas.DataFrame) -> dict:
    """
    Converts DataFrame into JSON format.

    Args:
        data_frame: pandas.DataFrame, DataFrame with the Datasets Record Excel file data.

    Returns:
        json_dict: Dict, JSON string converted  to a dictionary.
    """
    string_json = data_frame.to_json(orient='records')
    string_json = re.sub(r'\([0-9]\)\s*', '', string_json)
    json_dict = json.loads(string_json)
    return json_dict


def get_excel_data(filename: str, load_sheet: str, rows_to_skip: int) -> dict:
    """
    Process the XLSX file as a DataFrame and return it as a JSON object

    Args:
        filename: String, Excel file name.
        load_sheet: String, Excel sheet name.
        rows_to_skip: Int, Number of rows to skip before table.

    Returns:
        data_frame_json: Dict, json dictionary with the Excel data.
    """
    data_frame = get_data_frame(filename, load_sheet, rows_to_skip)
    data_frame_json = get_json_from_data_frame(data_frame)
    return data_frame_json


def get_data_frame_tsv(filename: str) -> pandas.DataFrame:
    """
    Read and convert the TSV file to Panda DataFrame.

    Args:
        filename: String, full tsv file path.

    Returns:
        dataset_df: pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    """
    dataset_df = pandas.read_csv(filename, sep='\t', header=0, index_col=False)
    return dataset_df


def get_author_data_frame(filename: str, load_sheet, rows_to_skip: int) -> pandas.DataFrame:
    """
    Read and convert the Excel file to Panda DataFrame.

    Args:
        filename: String, full XLSX file path.
        load_sheet: Integer, Excel sheet number that will be loaded.
        rows_to_skip: Integer, number of rows to skip.

    Returns:
        dataset_df: pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    """
    dataset_df = pandas.read_excel(
        filename, sheet_name=load_sheet, skiprows=rows_to_skip, index_col=0)
    nan_value = float("NaN")
    dataset_df.replace("", nan_value, inplace=True)
    dataset_df.dropna(how='all', axis=1, inplace=True)
    return dataset_df


def get_author_data_frame_tsv(filename: str) -> pandas.DataFrame:
    """
    Read and convert the TSV file to Panda DataFrame.

    Args:
        filename: String, full tsv file path.

    Returns:
        dataset_df: pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    """
    dataset_df = pandas.read_csv(filename, sep='\t')
    return dataset_df
