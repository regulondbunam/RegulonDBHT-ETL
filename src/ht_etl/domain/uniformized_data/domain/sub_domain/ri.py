"""
Classic Regulatory Interaction object.
"""
# standard

# third party

# local
from src.libs import utils
from src.ht_etl.domain.uniformized_data.domain.sub_domain.citation import Citation


class RegulatoryInteraction(object):

    def __init__(self, **kwargs):
        # Params
        self.mg_api = kwargs.get("mg_api", None)
        self.lend = kwargs.get("lend", None)
        self.rend = kwargs.get("rend", None)
        self.strand = kwargs.get("strand", None)
        self.tf_site = kwargs.get("tf_site", None)
        self.origin = kwargs.get("origin", None)

        # Local properties
        self.mg_ri_obj = kwargs.get("mg_ri_obj", None)

        # Object properties
        self.id = kwargs.get("id", None)
        self.citations = kwargs.get("citations", None)
        self.relative_tss_distance = kwargs.get("relative_tss_distance", None)
        self.relative_gene_distance = kwargs.get("relative_gene_distance", None)
        self.sequence = kwargs.get("sequence", None)

    # Local properties
    @property
    def mg_ri_obj(self):
        return self._mg_ri_obj

    @mg_ri_obj.setter
    def mg_ri_obj(self, mg_ri_obj=None):
        if mg_ri_obj is None:
            mg_ri = self.mg_api.regulatory_interactions.find_by_reg_site(
                    self.tf_site.id
            )
            if mg_ri:
                mg_ri_obj = mg_ri[0]
        self._mg_ri_obj = mg_ri_obj

    # Object properties
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, ri_id=None):
        if ri_id is None and self.mg_ri_obj:
            ri_id = self.mg_ri_obj.id
        self._id = ri_id

    @property
    def relative_tss_distance(self):
        return self._relative_tss_distance

    @relative_tss_distance.setter
    def relative_tss_distance(self, relative_tss_distance=None):
        if relative_tss_distance is None and self.mg_ri_obj:
            relative_tss_distance = utils.get_tss_distance(
                mg_api=self.mg_api,
                regulated_entity=self.mg_ri_obj.regulated_entity,
                strand=self.strand,
                rend=self.rend,
                lend=self.lend
            )
        self._relative_tss_distance = relative_tss_distance

    @property
    def relative_gene_distance(self):
        return self._relative_gene_distance

    @relative_gene_distance.setter
    def relative_gene_distance(self, relative_gene_distance=None):
        if relative_gene_distance is None and self.mg_ri_obj:
            relative_gene_distance = utils.get_gene_distance(
                mg_api=self.mg_api,
                regulated_entity=self.mg_ri_obj.regulated_entity,
                strand=self.strand,
                rend=self.rend,
                lend=self.lend
            )
        self._relative_gene_distance = relative_gene_distance

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None):
        if sequence is None:
            sequence = self.tf_site.sequence
        self._sequence = sequence

    @property
    def citations(self):
        return self._citations

    @citations.setter
    def citations(self, citations=None):
        if citations is None:
            citations = Citation(
                mg_api=self.mg_api,
                citations_obj_list=self.tf_site.citations
            )
        self._citations = citations.citations_list
