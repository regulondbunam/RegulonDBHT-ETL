"""
NLP Growth Conditions utils.
Build uniformized data object for every dataset.
"""
# standard
import os

# third party

# local
from src.ht_etl.domain.uniformized_data.domain.nlp_growth_condition import NLPGrowthCondition
from src.libs import constants


def geo_nlp_gc_json_path(collection_path):
    """
    Set path to geo-NLP Growth Conditions JSON.
    Args:
        collection_path:

    Returns:

    """
    json_path = os.path.join(
        collection_path,
        "metadata/srr_htregulondb_correct_full.json"
    )
    return json_path


def no_geo_nlp_gc_json_path(collection_path):
    """
    Set path to NO-geo-NLP Growth Conditions JSON.
    Args:
        collection_path:

    Returns:

    """
    json_path = os.path.join(
        collection_path,
        "metadata/no_geo_gc.json"
    )
    return json_path


def get_nlp_gc(nlp_gc_data, collection_name, mg_api):
    """
    Get geo-NLP Growth Conditions Dict.
    Args:
        mg_api:
        collection_name:
        nlp_gc_data:

    Returns:

    """
    nlp_gc_obj = NLPGrowthCondition(
        type=constants.RNA,
        dataset_id=nlp_gc_data[0],
        data_row=nlp_gc_data[1],
        collection_name=collection_name,
        mg_api=mg_api
    )
    nlp_gc_dict = {
        '_id': nlp_gc_obj.id,
        'temporalId': nlp_gc_obj.temporal_id,
        'organism': nlp_gc_obj.organism,
        'geneticBackground': nlp_gc_obj.genetic_background,
        'medium': nlp_gc_obj.medium,
        'aeration': nlp_gc_obj.aeration,
        'temperature': nlp_gc_obj.temperature,
        'ph': nlp_gc_obj.ph,
        'pressure': nlp_gc_obj.pressure,
        'opticalDensity': nlp_gc_obj.optical_density,
        'growthPhase': nlp_gc_obj.growth_phase,
        'growthRate': nlp_gc_obj.growth_rate,
        'vesselType': nlp_gc_obj.vessel_type,
        'aerationSpeed': nlp_gc_obj.aeration_speed,
        'mediumSupplements': nlp_gc_obj.medium_supplements,
        'additionalProperties': nlp_gc_obj.additional_properties,
        'datasetIds': nlp_gc_obj.dataset_ids,
    }
    nlp_gc_dict = {k: v for k, v in nlp_gc_dict.items() if v}
    return nlp_gc_dict
