"""
TF Binding Site object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.libs import utils
from src.ht_etl.domain.uniformized_data.domain.base import Base


class Site(Base):

    def __init__(self, **kwargs):
        super(Site, self).__init__(**kwargs)
        # Params
        self.sites_list = kwargs.get('sites_list', [])
        # Local properties

        # Object properties
        self.found_ris = kwargs.get('found_ris', None)
        self.peak_id = kwargs.get('peak_id', None)
        self.score = kwargs.get('score', None)
        self.sequence = kwargs.get('sequence', None)
        self.collection_name = kwargs.get('collection_name', None)

    # Local properties

    # Object properties
    @property
    def found_ris(self):
        return self._found_ris

    @found_ris.setter
    def found_ris(self, found_ris=None):
        if found_ris is None:
            found_ris = utils.get_classic_ris(
                lend=self.data_row[1],
                rend=self.data_row[2],
                strand=self.data_row[5],
                tf_sites=self.sites_list,
                mg_api=self.mg_api,
                origin='RegulonDB'
            )
        self._found_ris = found_ris

    @property
    def peak_id(self):
        return self._peak_id

    @peak_id.setter
    def peak_id(self, peak_id=None):
        if peak_id is None:
            peak_id = self.data_row[3]
        self._peak_id = peak_id

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score=None):
        if score is None:
            score = float(self.data_row[4])
        self._score = score

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None):
        if sequence is None:
            sequence = self.data_row[6]
        self._sequence = sequence

    # Static methods
