"""
Summary object.
"""
# standard

# third party

# local
from src.ht_etl.sub_domain.total_of import TotalOf


class Summary(object):
    def __init__(self, **kwargs):
        # Params
        self.peaks = kwargs.get('peaks', None)
        self.sites = kwargs.get('sites', None)
        self.genes = kwargs.get('genes', None)

        # Local properties

        # Object properties
        self.total_of_peaks = kwargs.get('total_of_peaks', None)
        self.total_of_tfbs = kwargs.get('total_of_tfbs', None)
        self.total_of_genes = kwargs.get('total_of_genes', None)

    # Local properties

    # Object properties
    @property
    def total_of_peaks(self):
        return self._total_of_peaks

    @total_of_peaks.setter
    def total_of_peaks(self, total_of):
        total_of = TotalOf(
            peaks=self.peaks,
        )
        total_of_peaks = {
            'inDataset': total_of.in_dataset,
            'inRDBClassic': total_of.in_rdb_classic,
            'sharedItems': total_of.shared_items,
            'notInRDB': total_of.not_in_rdb,
            'notInDataset': total_of.not_in_dataset
        }
        total_of_peaks = {k: v for k, v in total_of_peaks.items() if v}
        self._total_of_peaks = total_of_peaks

    @property
    def total_of_tfbs(self):
        return self._total_of_tfbs

    @total_of_tfbs.setter
    def total_of_tfbs(self, total_of):
        total_of = TotalOf(
            sites=self.sites,
        )
        total_of_tfbs = {
            'inDataset': total_of.in_dataset,
            'inRDBClassic': total_of.in_rdb_classic,
            'sharedItems': total_of.shared_items,
            'notInRDB': total_of.not_in_rdb,
            'notInDataset': total_of.not_in_dataset
        }
        total_of_tfbs = {k: v for k, v in total_of_tfbs.items() if v}
        self._total_of_tfbs = total_of_tfbs

    @property
    def total_of_genes(self):
        return self._total_of_genes

    @total_of_genes.setter
    def total_of_genes(self, total_of):
        total_of = TotalOf(
            genes=self.genes,
        )
        total_of_genes = {
            'inDataset': total_of.in_dataset,
            'inRDBClassic': total_of.in_rdb_classic,
            'sharedItems': total_of.shared_items,
            'notInRDB': total_of.not_in_rdb,
            'notInDataset': total_of.not_in_dataset
        }
        total_of_genes = {k: v for k, v in total_of_genes.items() if v}
        self._total_of_genes = total_of_genes


