import re
import json

import pandas


def get_data_frame(filename: str, load_sheet: str, rows_to_skip: int) -> pandas.DataFrame:
    """
    Read and convert the Excel file to Panda DataFrame.

    Param
        filename, String, Excel file name.
        load_sheet, String, Excel sheet name.
        rows_to_skip, Int, Number of rows to skip before table.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    """
    dataset_df = pandas.read_excel(
        filename, sheet_name=load_sheet, skiprows=rows_to_skip)
    return dataset_df


def get_json_from_data_frame(data_frame: pandas.DataFrame) -> dict:
    """
    Converts DataFrame into JSON format.

    Param
        data_frame, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.

    Returns
        json_dict, Dict, JSON string converted  to a dictionary.
    """
    string_json = data_frame.to_json(orient='records')
    string_json = re.sub(r'\([0-9]\)\s*', '', string_json)
    json_dict = json.loads(string_json)
    return json_dict


def get_excel_data(filename: str, load_sheet: str, rows_to_skip: int) -> dict:
    """
    Process the XLSX file as a DataFrame and return it as a JSON object

    Param
        filename, String, Excel file name.
        load_sheet, String, Excel sheet name.
        rows_to_skip, Int, Number of rows to skip before table.
    Returns
        data_frame_json, Dict, json dictionary with the Excel data.
    """
    data_frame = get_data_frame(filename, load_sheet, rows_to_skip)
    data_frame_json = get_json_from_data_frame(data_frame)
    return data_frame_json
