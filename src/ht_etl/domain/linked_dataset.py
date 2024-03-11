"""
Sample object.
"""
# standard
import logging

# third party

# local


class LinkedDataset(object):
    def __init__(self, **kwargs):
        # Params
        self.sample_replicate_exp = kwargs.get('sample_exp_replicate_exp', None)
        self.sample_replicate_ctrl = kwargs.get('sample_exp_replicate_ctrl', None)
        self.dataset_type = kwargs.get('dataset_type', None)
        # Local properties

        # Object properties
        self.linked_dataset = kwargs.get('linked_dataset', None)

    # Local properties

    # Object properties
    @property
    def linked_dataset(self):
        return self._linked_dataset

    @linked_dataset.setter
    def linked_dataset(self, linked_dataset=None):
        if linked_dataset is None:
            control_id = LinkedDataset.sample_replicate_ids(self.sample_replicate_ctrl)
            experiment_id = LinkedDataset.sample_replicate_ids(self.sample_replicate_exp)
            linked_dataset = {
                'controlId': control_id,
                'experimentId': experiment_id,
                'datasetType': self.dataset_type,
            }
        self._linked_dataset = linked_dataset

    # Static methods
    @staticmethod
    def sample_replicate_ids(sample_replicate_ids):
        """
        Separates replicates ids in the string.

        Args:
            sample_replicate_ids: String, list of replicate ids in string.

        Returns:
            sample_replicates: List, list of replicate ids.
        """
        sample_replicates = []
        if not sample_replicate_ids:
            logging.warning('No sample_experimental_replicate_ids provided')
            return sample_replicates
        sample_replicate_ids = sample_replicate_ids.replace('\t', '')
        sample_replicate_ids = sample_replicate_ids.split('] [')
        for sample_replicate_id in sample_replicate_ids:
            sample_replicate_id = sample_replicate_id.replace('[', '').replace(']', '')
            sample_replicate_id = sample_replicate_id.replace(', ', ',').replace('  ', ',').replace(' ', ',').split(',')
            sample_replicates.append(sample_replicate_id)
        return sample_replicates
