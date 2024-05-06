"""
Uniformized Data objects.
Build uniformized data objects for every dataset.
"""
# standard

# third party

# local
from src.libs import constants
from src.ht_etl.domain.uniformized_data.sites import Sites
from src.ht_etl.domain.uniformized_data.peaks import Peaks
from src.ht_etl.domain.uniformized_data.tus import TUs


class UniformizedData(object):

    def __init__(self, **kwargs):
        # Params
        self.bnumbers = kwargs.get("bnumbers", None)
        self.collection_name = kwargs.get('collection_name')
        self.mg_api = kwargs.get('mg_api')
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)
        self.collection_path = kwargs.get('collection_path')
        self.genes_ranges = kwargs.get("genes_ranges", None)
        self.dataset_id = kwargs.get("dataset_id", None)
        self.serie_id = kwargs.get("serie_id", None)
        self.type = kwargs.get("type", None)
        self.old_dataset_id = kwargs.get("old_dataset_id", None)
        print(f'\t\t\tUniformized Data -- Type: {self.type}, SeireID: {self.serie_id}')

        # Local properties

        # Object properties

        # TF Binding
        self.sites = kwargs.get("sites", None)
        self.peaks = kwargs.get("peaks", None)

        # TUs
        self.tus = kwargs.get("tus", None)

        # TSS
        self.tss = kwargs.get("tss", None)
        self.pos_1 = kwargs.get("pos_1", None)
        self.promoters = kwargs.get("promoters", None)

        # TTS
        self.terminator = kwargs.get("terminator", None)

    # Local properties

    # Object properties
    @property
    def sites(self):
        return self._sites

    @sites.setter
    def sites(self, sites=None):
        self._sites = sites
        if sites is None and self.type == constants.TFBINDING:
            sites = Sites(
                dataset_id=self.dataset_id,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                genes_ranges=self.genes_ranges,
                type=self.type,
                collection_path=self.collection_path,
                serie_id=self.serie_id,
                old_dataset_id=self.old_dataset_id,
            )
        self._sites = sites

    @property
    def peaks(self):
        return self._peaks

    @peaks.setter
    def peaks(self, peaks=None):
        self._peaks = peaks
        if peaks is None and self.type == constants.TFBINDING:
            peaks = Peaks(
                sites_list=self.sites.sites_list,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                genes_ranges=self.genes_ranges,
                type=self.type,
                sub_type=constants.PEAKS,
                collection_path=self.collection_path,
                serie_id=self.serie_id,
                old_dataset_id=self.old_dataset_id,
            )
        self._peaks = peaks

    @property
    def tus(self):
        return self._tus

    @tus.setter
    def tus(self, tus=None):
        self._tus = tus
        if tus is None and self.type == constants.TUS:
            tus = TUs(
                bnumbers=self.bnumbers,
                type=self.type,
                dataset_id=self.dataset_id,
                mg_api=self.mg_api,
                sub_type=constants.PEAKS,
                collection_path=self.collection_path,
                serie_id=self.serie_id,
                old_dataset_id=self.old_dataset_id,
            )
        self._tus = tus

    # Static methods
