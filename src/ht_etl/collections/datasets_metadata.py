"""
Datasets metadata collection.
Build first level from HT Dataset Model.
"""
# standard
import logging

# third party

# local
from src.libs import constants
from src.ht_etl.sub_collections.dataset import Dataset


class DatasetsMetadata(object):
    def __init__(self, **kwargs):
        # Params
        self.dataset_type = kwargs.get('dataset_type', None)
        self.email = kwargs.get('email', None)

        # Local properties
        self.dataset_dict = kwargs.get('dataset_dict', None)

        # Object properties
        self.dataset = kwargs.get('dataset', None)
        self.metadata = kwargs.get('metadata', None)
        self.collection_name = kwargs.get('collection_name', None)

    # Local properties

    # Object properties
    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset=None):
        """
        Gets all values from dataset catalog dict and build a Dataset object.
        """
        if dataset is None:
            if self.dataset_dict.get(constants.DATASET_ID, None) is not None:
                logging.info(f"Processing Dataset ID: {self.dataset_dict.get(constants.DATASET_ID, None)}")
                dataset = Dataset(
                    email=self.email,
                    dataset_id=self.dataset_dict.get(constants.DATASET_ID, None),
                    pmid=self.dataset_dict.get(constants.PMID, None),
                    authors=self.dataset_dict.get(constants.AUTHORS, None),
                    regulondb_tf_name=self.dataset_dict.get(constants.REGULONDB_TF_NAME, None),
                    source_tf_name=self.dataset_dict.get(constants.SOURCE_TF_NAME, None),
                    source_database=self.dataset_dict.get(constants.SOURCE_DATABASE, None),
                    serie_id=self.dataset_dict.get(constants.SERIE_ID, None),
                    experiment_title=self.dataset_dict.get(constants.EXPERIMENT_TITLE, None),
                    platform_id=self.dataset_dict.get(constants.PLATFORM_ID, None),
                    platform_title=self.dataset_dict.get(constants.PLATFORM_TITLE, None),
                    strategy=self.dataset_dict.get(constants.STRATEGY, None),
                    library_layout=self.dataset_dict.get(constants.LIBRARY_LAYOUT, None),
                    method_name=self.dataset_dict.get(constants.METHOD_NAME, None),
                    samples_replicates_exp_ids=self.dataset_dict.get(constants.SAMPLES_REPLICATES_EXPERIMET_ID, None),
                    samples_replicates_control_ids=self.dataset_dict.get(constants.SAMPLES_REPLICATES_CONTROL_ID, None),
                    title_for_all_replicates=self.dataset_dict.get(constants.TITLE_FOR_ALL_REPLICATES, None),
                    experiment_condition=self.dataset_dict.get(constants.EXPERIMENT_CONDITION, None),
                    grow_conditions_exp_ids=self.dataset_dict.get(constants.GC_EXPERIMENTAL, None),
                    organism=self.dataset_dict.get(constants.ORGANISM , None),
                    src_reference_genome=self.dataset_dict.get(constants.SOURCE_REFERENCE_GENOME, None),
                    ref_genome=self.dataset_dict.get(constants.REFERENCE_GENOME, None),
                    dataset_file_name=self.dataset_dict.get(constants.DATASET_FILE_NAME, None),
                    internal_curation_notes=self.dataset_dict.get(constants.INTERNAL_CURATION_NOTES, None),
                    curation_notes=self.dataset_dict.get(constants.CURATOR, None),
                    samples_exp_replicates_expression_ids=self.dataset_dict.get(
                        constants.SAMPLES_EXPERIMET_REPLICATES_EXPRESSION_ID, None
                    ),
                    samples_control_replicates_expression_ids=self.dataset_dict.get(
                        constants.SAMPLES_CONTROL_REPLICATES_EXPRESSION_ID, None
                    ),
                    expression_growcon_ctrl=self.dataset_dict.get(constants.EXPRESSION_GC_CONTROL, None),
                    expression_growcon_control_ids=self.dataset_dict.get(constants.EXPRESSION_GC_EXPERIMENTAL, None),
                    source_cut_off=self.dataset_dict.get(constants.CUT_OFF, None)
                )
            else:
                logging.warning(f"No Dataset ID provided for {self.dataset_dict.get(constants.PMID, None)}")

        self._dataset = dataset

