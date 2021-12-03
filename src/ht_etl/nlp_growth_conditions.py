'''
Functions that help to process datasets .tsv files.
'''
# standard
import os
import logging
from re import T, template

# third party


# local
from libs import utils


def file_mapping(keyargs):
    '''
    Reads one by one all the valid TSV files and returns the corresponding data dictionaries.

    Param
        filename, String, full TSV file path.

    Returns
        dataset_dict, Dict, a dictionary with the necessary dataset data.
    '''
    nlp_gc_dict_list = []
    geo_nlp_gc_json_path = utils.verify_json_path(os.path.join(keyargs.get("collection_path"), "metadata/srr_htregulondb_full.json"))
    if not geo_nlp_gc_json_path:
        return nlp_gc_dict_list
    geo_gc_json = utils.read_json_from_path(geo_nlp_gc_json_path)
    nlp_gc_dict_list = gc_term_mapper(geo_gc_json, nlp_gc_dict_list)

    no_geo_nlp_gc_json_path = utils.verify_json_path(os.path.join(keyargs.get("collection_path"), "metadata/no_geo_gc.json"))
    if not no_geo_nlp_gc_json_path:
        return nlp_gc_dict_list
    no_geo_gc_json = utils.read_json_from_path(no_geo_nlp_gc_json_path)
    nlp_gc_dict_list = gc_term_mapper(no_geo_gc_json, nlp_gc_dict_list)
 
    return nlp_gc_dict_list


def gc_term_mapper(gc_json, nlp_gc_dict_list):
    for key, dict in gc_json.items():
        gc_term_dict = {}
        gc_term_dict.setdefault('_id', f'GC_{key}')
        gc_term_dict.setdefault('datasetIds', key)
        gc_term_dict.setdefault('additionalProperties', [])
        for term in dict['terms']:
            if term['name'] != "Unclear" and term['name'] != "TruSeq" and term['name'] != "GEO_secondstrand" and term['name'] != "ScriptSeq" and term['name'] != "GEO_unclear":
                term_dict = {
                        "value": term["name"],
                        "associatedPhrase": term["source_data"]["associatedPhrase"],
                        "score": term["source_data"]["similarity_percentage"] 
                }
                if term['term_type'] == "Organism" or term['term_type'] == "Strain" or term['term_type'] == "Substrain":
                    gc_term_dict.setdefault("organism", []).append(term_dict)
                elif term['term_type'] == "Genetic background" or term['term_type'] == "Gtype":
                    gc_term_dict.setdefault("geneticBackground", []).append(term_dict)
                elif term['term_type'] == "Medium" or term['term_type'] == "Med":
                    gc_term_dict.setdefault("medium", []).append(term_dict)
                elif term['term_type'] == "Aeration" or term['term_type'] == "Air":
                    gc_term_dict.setdefault("aeration", []).append(term_dict)
                elif term['term_type'] == "Temperature" or term['term_type'] == "Tem":
                    gc_term_dict.setdefault("temperature", []).append(term_dict)
                elif term['term_type'] == "pH" or term['term_type'] == "pH":
                    gc_term_dict.setdefault("ph", []).append(term_dict)
                elif term['term_type'] == "Pressure" or term['term_type'] == "Press(NA)":
                    gc_term_dict.setdefault("pressure", []).append(term_dict)
                elif term['term_type'] == "Optical Density (OD)" or term['term_type'] == "OD":
                    gc_term_dict.setdefault("opticalDensity", []).append(term_dict)
                elif term['term_type'] == "Growth phase" or term['term_type'] == "Phase":
                    gc_term_dict.setdefault("growthPhase", []).append(term_dict)
                elif term['term_type'] == "Growth rate" or term['term_type'] == "Grate(NA)":
                    gc_term_dict.setdefault("growthRate", []).append(term_dict)
                elif term['term_type'] == "Vessel Type" or term['term_type'] == "Vess":
                    gc_term_dict.setdefault("vesselType", []).append(term_dict)
                elif term['term_type'] == "Medium supplement" or term['term_type'] == "Supp":
                    gc_term_dict.setdefault("mediumSupplements", []).append(term_dict)
                else:
                    gc_term_dict["additionalProperties"].append({
                        "name": term['term_type'], 
                        "value": term_dict
                    })
            nlp_gc_dict_list.append(gc_term_dict)
    return nlp_gc_dict_list
