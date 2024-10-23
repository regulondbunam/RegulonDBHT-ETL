"""
Total Of object.
"""
# standard

# third party

# local


class TotalOf(object):
    def __init__(self, **kwargs):
        # Params
        self.peaks = kwargs.get('peaks', None)
        self.sites = kwargs.get('sites', None)
        self.genes = kwargs.get('genes', None)

        # Local properties

        # Object properties
        self.in_dataset = kwargs.get('in_dataset', None)
        self.in_rdb_classic = kwargs.get('in_rdb_classic', None)
        self.shared_items = kwargs.get('shared_items', None)
        self.not_in_rdb = kwargs.get('not_in_rdb', None)
        self.not_in_dataset = kwargs.get('not_in_dataset', None)

    # Local properties

    # Object properties
    @property
    def in_dataset(self):
        return self._in_dataset

    @in_dataset.setter
    def in_dataset(self, in_dataset):
        if self.peaks:
            in_dataset = len(self.peaks)
        if self.sites:
            in_dataset = len(self.sites)
        if self.genes:
            in_dataset = len(self.genes)
        self._in_dataset = in_dataset

