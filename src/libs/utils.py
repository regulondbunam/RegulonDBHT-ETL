'''
Some functions that help to HT process.
'''
# standard
import os
import logging
import json
import pandas
import json
import re

# third party
from Bio import Entrez, Medline
import multigenomic_api as mg_api

# local


def validate_directories(data_path):
    '''
    Verify that the output path directory exists.

    Param
        data_path, String, directory path.

    Return
        Rise IOError if not valid directory
    '''
    if not os.path.isdir(data_path):
        raise IOError("Please, verify '{}' directory path".format(data_path))


def set_log(log_path):
    '''
    Initializes the execution log to examine any problems that arise during extraction.

    Param
        log_path, String, the execution log path.
    '''
    validate_directories(log_path)
    logging.basicConfig(filename=os.path.join(log_path, 'ht_etl.log'),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def create_json(objects, filename, output):
    '''
    Create and write the JSON file with the results.

    Param
        objects, Object, a Python serializable object that you want to convert to JSON format.
        filename, String, JSON file name.
        output, String, output path.
    '''
    filename = os.path.join(output, filename)
    with open("{}.json".format(filename), 'w') as json_file:
        json.dump(objects, json_file, indent=4, sort_keys=True)


def list_to_dict(data):  # TODO: Not used, must be deleted?
    '''
    Turns a data List into a directory object.

    Param
        data, List, data list.

    Returns
        data_dict, Dict, data list converted to dictionary.
    '''
    data_dict = {}
    for object_dict in data:
        data_dict.update(object_dict)
    return data_dict


def get_data_frame(filename: str, load_sheet: int = 0, rows_to_skip: int = 0) -> pandas.DataFrame:
    '''
    Read and convert the Excel file to Panda DataFrame.

    Param
        filename, String, full XLSX file path.
        load_sheet, Integer, Excel sheet number that will be loaded.
        rows_to_skip, Integer, number of rows to skip.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    '''
    dataset_df = pandas.read_excel(
        filename, sheet_name=load_sheet, skiprows=rows_to_skip)
    return dataset_df


def get_json_from_data_frame(data_frame: pandas.DataFrame) -> dict:
    '''
    Converts DataFrame into JSON format.

    Param
        data_frame, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.

    Returns
        json_dict, Dict, JSON string converted  to a dictionary.
    '''
    string_json = data_frame.to_json(orient='records')
    string_json = re.sub(r'\([0-9]\)\s*', '', string_json)
    json_dict = json.loads(string_json)
    return json_dict


def get_excel_data(filename: str) -> dict:
    '''
    Process the XLSX file as a DataFrame and return it as a JSON object

    Param
        filename, String, Excel file name.

    Returns
        data_frame_json, Dict, json dictionary with the Excel data.
    '''
    data_frame = get_data_frame(filename)
    data_frame_json = get_json_from_data_frame(data_frame)
    return data_frame_json


def to_camel_case(snake_str):
    '''
    Converts snake_case String into camelCase.
    Capitalize the first letter of each component except the first one with the 'title' method and join them together.

    Param
        snake_str, String, snake_case string.

    Returns
        camelStr, String, camelCase string.
    '''
    components = snake_str.split('_')
    camelStr = components[0] + ''.join(x.title() for x in components[1:])
    return camelStr


def get_pubmed_data(pmid, email):
    '''
    Connects to PUBMED database through Entrez API and gets the necessary publication data.
    The Entrez API returns a dictionary with the medline data, see also https://biopython.org/docs/1.75/api/Bio.Medline.html for more information about the keys obtained from this dictionary.

    Param
        pmid, Integer, PUBMED publication id.
        email, String, User email address to connect to PUBMED database.

    Returns
        publication, Dict, dictionary with the publication data.
    '''
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed', id=pmid,
                           rettype='medline', retmode='text')

    publication = {}
    record = Medline.read(handle)
    publication.setdefault('authors', record.get('AU'))
    publication.setdefault('abstract', record.get('AB'))
    publication.setdefault('date', record.get('DP'))
    publication.setdefault('pmcid', record.get('PMC'))
    publication.setdefault('pmid', int(record.get('PMID')))
    publication.setdefault('title', record.get('TI'))
    article_identifier = record.get('AID')
    for identifier in article_identifier:
        if ' [doi]' in identifier:
            publication.setdefault('doi', identifier.replace(' [doi]', ''))

    return publication


def get_object_tested(protein_name, database, url):
    '''
    Gets TF data from the RegulonDBMultigenomic database and returns the object tested dictionary.

    Param
        protein_name, String, TF protein name.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.

    Returns
        object_tested, Dict, dictionary with the object tested data.
    '''
    mg_api.connect(database, url)
    mg_tf = mg_api.transcription_factors.find_by_name(protein_name)
    active_conformations = []
    external_cross_references = []
    for active_conf in mg_tf[0].active_conformations:
        active_conformations.append(active_conf.id)
    for cross_ref in mg_tf[0].external_cross_references:
        mg_cross_ref = mg_api.external_cross_references.find_by_id(
            cross_ref.external_cross_references_id)
        external_cross_references.append(
            {
                'externalCrossReferenceId': cross_ref.external_cross_references_id,
                'objectId': cross_ref.object_id,
                'externalCrossReferenceName': mg_cross_ref.name,
                'url': mg_cross_ref.url
            }
        )
    genes = []
    for product_id in mg_tf[0].products_ids:
        mg_product = mg_api.products.find_by_id(product_id)
        mg_gene = mg_api.genes.find_by_id(mg_product.genes_id)
        gene = {
            '_id': mg_gene.id,
            'name': mg_gene.name
        }
        genes.append(gene)

    object_tested = {
        '_id': mg_tf[0].id,
        'name': mg_tf[0].name,
        'synonyms': mg_tf[0].synonyms,
        'genes': genes,  # TODO: now is an string array
        'summary': mg_tf[0].note,
        'activeConformations': active_conformations,
        'externalCrossReferences': external_cross_references
    }
    mg_api.disconnect()
    return object_tested


def find_site(abs_pos):
    pass
