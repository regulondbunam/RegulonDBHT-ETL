"""
TF Binding Site object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.libs import utils
from src.libs import constants
from src.ht_etl.domain.uniformized_data.domain.base import Base
from src.ht_etl.domain.uniformized_data.domain.sub_domain.ri import RegulatoryInteraction


class Site(Base):

    def __init__(self, **kwargs):
        super(Site, self).__init__(**kwargs)
        # Params
        self.tf_sites = kwargs.get('tf_sites', [])
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
            found_ris = []
            center_pos = utils.get_center_pos(
                left_pos=self.data_row[1],
                right_pos=self.data_row[2]
            )
            for tf_site in self.tf_sites:
                tf_center = tf_site.absolute_position
                if (
                    tf_center == center_pos
                    or tf_center == (center_pos + constants.PAIR_OF_BASES)
                    or tf_center == (center_pos - constants.PAIR_OF_BASES)
                ):
                    lend = int(self.data_row[1])
                    rend = int(self.data_row[2])
                    found_ri_obj = RegulatoryInteraction(
                        lend=lend,
                        rend=rend,
                        strand=self.data_row[5],
                        tf_site=tf_site,
                        mg_api=self.mg_api,
                        origin='RegulonDB'
                    )
                    found_ri_dict = {
                        "_id": found_ri_obj.id,
                        "citations": found_ri_obj.citations,
                        "origin": found_ri_obj.origin,
                        "relativeGeneDistance": found_ri_obj.relative_gene_distance,
                        "relativeTSSDistance": found_ri_obj.relative_tss_distance,
                        "sequence": found_ri_obj.sequence,
                        "strand": found_ri_obj.strand,
                        "tfbsLeftPosition": found_ri_obj.lend,
                        "tfbsRightPosition": found_ri_obj.rend
                    }
                    found_ris.append(found_ri_dict)
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
