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
        self.control_id = kwargs.get('control_id', None)
        self.experiment_id = kwargs.get('experiment_id', None)

    # Local properties

    # Object properties
    @property
    def control_id(self):
        return self._control_id

    @control_id.setter
    def control_id(self, control_id=None):
        """
        Sets the control id.
        """
        self._control_id = control_id
        if control_id is None:
            control_id = LinkedDataset.sample_replicate_ids(self.sample_replicate_ctrl)
            self._control_id = control_id

    @property
    def experiment_id(self):
        return self._experiment_id

    @experiment_id.setter
    def experiment_id(self, experiment_id=None):
        """
        Sets the experiment id.
        """
        self._experiment_id = experiment_id
        if experiment_id is None:
            experiment_id = LinkedDataset.sample_replicate_ids(self.sample_replicate_exp)
            self._experiment_id = experiment_id

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

        sample_replicate_ids = (sample_replicate_ids.replace(' ', '').replace('][', ',')
                                .replace('[', '').replace(']', '').replace(';', ','))
        sample_replicates.extend(sample_replicate_ids.split(','))
        return sample_replicates
