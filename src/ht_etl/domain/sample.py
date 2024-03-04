"""
Sample object.
"""
# standard
import logging

# third party

# local


class Sample(object):
    def __init__(self, **kwargs):
        # Params
        self.sample_replicate_exp = kwargs.get('sample_replicate_exp', None)
        self.sample_replicate_ctrl = kwargs.get('sample_replicate_ctrl', None)
        self.title_for_replicates = kwargs.get('title_for_replicates', None)
        # Local properties

        # Object properties
        self.sample = kwargs.get('sample', None)

    # Local properties

    # Object properties
    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, sample=None):
        if sample is None:
            control_id = Sample.sample_replicate_ids(self.sample_replicate_ctrl)
            experiment_id = Sample.sample_replicate_ids(self.sample_replicate_exp)
            sample = {
                'controlId': control_id,
                'experimentId': experiment_id,
                'title': self.title_for_replicates,
                'ssrId': ''  # TODO: ask for this property
            }
        self._sample = sample

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
            # logging.warning('No sample_replicate_ids provided')
            return sample_replicates
        sample_replicate_ids = sample_replicate_ids.replace('\t', '')
        sample_replicate_ids = sample_replicate_ids.split('] [')
        for sample_replicate_id in sample_replicate_ids:
            sample_replicate_id = sample_replicate_id.replace('[', '').replace(']', '')
            # sample_replicate_id = sample_replicate_id.split(',')
            sample_replicates.append(sample_replicate_id)
        return sample_replicates
