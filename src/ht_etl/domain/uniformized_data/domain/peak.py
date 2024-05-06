"""
TF Binding Peak object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.domain.base import Base


class Peak(Base):

    def __init__(self, **kwargs):
        super(Peak, self).__init__(**kwargs)
        # Params
        self.sites_list = kwargs.get("sites_list", [])

        # Local properties

        # Object properties
        self.score = kwargs.get("score", None)
        self.name = kwargs.get("name", None)
        self.site_ids = Peak.get_sites_ids(self.sites_list, self.id)

    # Local properties

    # Object properties
    @property
    def temporal_id(self):
        return self._temporal_id

    @temporal_id.setter
    def temporal_id(self, temporal_id=None):
        if temporal_id is None:
            temporal_id = self.data_row[3]
        self._temporal_id = temporal_id

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score=None):
        if score is None:
            score = float(self.data_row[4])
        self._score = score

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if name is None:
            name = self.data_row[3]
        self._name = name

    @staticmethod
    def get_sites_ids(sites, peak_id):
        """
        Finds the Peaks in the Sites list previously processed.

        Args:
            sites: List, Sites objects list.
            peak_id: String, Current Peak ID.

        Returns:
            sites_ids: List, Sites ID list
        """
        sites_ids = []
        for site in sites:
            if site.get('peakId') == peak_id:
                sites_ids.append(site.get('_id'))
        return sites_ids
