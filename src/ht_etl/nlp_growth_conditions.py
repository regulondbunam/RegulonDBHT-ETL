'''
Functions that help to process datasets .tsv files.
'''
# standard
import os
import logging
from posixpath import join
from re import S, T, template

# third party


# local
from libs import utils
from libs import constants as EC


def file_mapping(keyargs):
    '''
    Reads one by one all the valid TSV files and returns the corresponding data dictionaries.

    Param
        filename, String, full TSV file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    nlp_gc_dict_list = []
    dataset_type = keyargs.get('dataset_type', None)
    geo_nlp_gc_json_path = utils.verify_json_path(os.path.join(
        keyargs.get("collection_path"), "metadata/srr_htregulondb_correct_full.json"))
    if not geo_nlp_gc_json_path:
        return nlp_gc_dict_list
    geo_gc_json = utils.read_json_from_path(geo_nlp_gc_json_path)
    nlp_gc_dict_list = gc_term_mapper(
        geo_gc_json, nlp_gc_dict_list, dataset_type)

    no_geo_nlp_gc_json_path = utils.verify_json_path(os.path.join(
        keyargs.get("collection_path"), "metadata/no_geo_gc.json"))
    if not no_geo_nlp_gc_json_path:
        return nlp_gc_dict_list
    no_geo_gc_json = utils.read_json_from_path(no_geo_nlp_gc_json_path)
    nlp_gc_dict_list = gc_term_mapper(
        no_geo_gc_json, nlp_gc_dict_list, dataset_type)

    return nlp_gc_dict_list


def split_combinated_ids(ids_string):
    datasetIds = []
    str_id = ""
    last_char = None
    for char in ids_string:
        if str(char).isalpha() and last_char == None:
            str_id = f"{str_id}{char}"
            last_char = char
        elif str(char).isalpha() and last_char.isalpha():
            str_id = f"{str_id}{char}"
            last_char = char
        elif str(char).isalpha() and last_char.isdigit():
            datasetIds.append(str_id)
            str_id = f"{char}"
            last_char = char
        elif str(char).isdigit() and last_char.isdigit():
            str_id = f"{str_id}{char}"
            last_char = char
        elif str(char).isdigit() and last_char.isalpha():
            str_id = f"{str_id}{char}"
            last_char = char
    datasetIds.append(str_id)
    return datasetIds


def gc_term_mapper(gc_json, nlp_gc_dict_list, dataset_type):
    for key, dict in gc_json.items():
        gc_term_dict = {}
        if len(key) > 11:
            gc_term_dict.setdefault('datasetIds', split_combinated_ids(key))
        else:
            gc_term_dict.setdefault(
                'datasetIds', [f'{dataset_type}_{key}'])  # {dataset_type}_
        gc_term_dict.setdefault('_id', f'GC_{key}')
        gc_term_dict.setdefault('additionalProperties', [])
        for term in dict['terms']:
            if term['name'] != "Unclear" and term['name'] != "TruSeq" and term['name'] != "GEO_secondstrand" and term['name'] != "ScriptSeq" and term['name'] != "GEO_unclear":
                score = term["source_data"]["similarity_percentage"]
                if score == '':
                    score = None
                term_dict = {
                    "value": term["name"],
                    "associatedPhrase": term["source_data"]["associatedPhrase"],
                    "score": score,
                    "nameField": term["source_data"]["field"]
                }
                if term['term_type'] == "Organism" or term['term_type'] == "Strain" or term['term_type'] == "Substrain":
                    gc_term_dict.setdefault("organism", []).append(term_dict)
                elif term['term_type'] == "Genetic background" or term['term_type'] == "Gtype":
                    gc_term_dict.setdefault(
                        "geneticBackground", []).append(term_dict)
                elif term['term_type'] == "Medium" or term['term_type'] == "Med":
                    gc_term_dict.setdefault("medium", []).append(term_dict)
                elif term['term_type'] == "Aeration" or term['term_type'] == "Air":
                    gc_term_dict.setdefault("aeration", []).append(term_dict)
                elif term['term_type'] == "Temperature" or term['term_type'] == "Tem":
                    gc_term_dict.setdefault(
                        "temperature", []).append(term_dict)
                elif term['term_type'] == "pH" or term['term_type'] == "pH":
                    gc_term_dict.setdefault("ph", []).append(term_dict)
                elif term['term_type'] == "Pressure" or term['term_type'] == "Press(NA)":
                    gc_term_dict.setdefault("pressure", []).append(term_dict)
                elif term['term_type'] == "Optical Density (OD)" or term['term_type'] == "OD":
                    gc_term_dict.setdefault(
                        "opticalDensity", []).append(term_dict)
                elif term['term_type'] == "Growth phase" or term['term_type'] == "Phase":
                    gc_term_dict.setdefault(
                        "growthPhase", []).append(term_dict)
                elif term['term_type'] == "Growth rate" or term['term_type'] == "Grate(NA)":
                    gc_term_dict.setdefault("growthRate", []).append(term_dict)
                elif term['term_type'] == "Vessel Type" or term['term_type'] == "Vess":
                    gc_term_dict.setdefault("vesselType", []).append(term_dict)
                elif term['term_type'] == "Medium supplement" or term['term_type'] == "Supp":
                    gc_term_dict.setdefault(
                        "mediumSupplements", []).append(term_dict)
                else:
                    if len(gc_term_dict['additionalProperties']) > 0:
                        for add_prop in gc_term_dict["additionalProperties"]:
                            if add_prop['name'] == term['term_type']:
                                value_list = add_prop['value']
                                value_list.append(term_dict)
                                add_prop['value'] = value_list
                    else:
                        add_prop_dict = {
                            "name": term['term_type'],
                        }
                        add_prop_dict.setdefault("value", []).append(term_dict)
                        gc_term_dict["additionalProperties"].append(
                            add_prop_dict)
        nlp_gc_dict_list.append(gc_term_dict)
    return nlp_gc_dict_list
