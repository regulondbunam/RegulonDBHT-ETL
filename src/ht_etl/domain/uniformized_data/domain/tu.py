"""
TU object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.domain.base import Base


class TU(Base):

    def __init__(self, **kwargs):
        super(TU, self).__init__(**kwargs)
        # Params
        self.bnumbers = kwargs.get("bnumbers", None)
        # Local properties

        # Object properties
        self.length = kwargs.get("length", None)
        self.term_type = kwargs.get("term_type", None)
        self.genes = kwargs.get("genes", None)
        self.phantom = kwargs.get("phantom", None)
        self.pseudo = kwargs.get("pseudo", None)

    # Local properties

    # Object properties
    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length=None):
        if length is None:
            if isinstance(self.data_row, dict):
                length = self.data_row.get("length", None)
            self._length = length

    @property
    def term_type(self):
        return self._term_type

    @term_type.setter
    def term_type(self, term_type=None):
        if term_type is None:
            if isinstance(self.data_row, dict):
                term_type = self.data_row.get("term_type", None)
            self._term_type = term_type

    @property
    def phantom(self):
        return self._phantom

    @phantom.setter
    def phantom(self, phantom=None):
        if phantom is None:
            if isinstance(self.data_row, dict):
                phantom = self.data_row.get("phantom", None)
            self._phantom = phantom

    @property
    def pseudo(self):
        return self._pseudo

    @pseudo.setter
    def pseudo(self, pseudo=None):
        if pseudo is None:
            if isinstance(self.data_row, dict):
                pseudo = self.data_row.get("pseudo", None)
            self._pseudo = pseudo

    @property
    def genes(self):
        return self._genes

    @genes.setter
    def genes(self, genes=None):
        genes_list = []
        if genes is None:
            if isinstance(self.data_row, dict):
                genes_bnums = self.data_row.get("genes", '')
                if genes_bnums and genes_bnums != '':
                    bnums_list = genes_bnums.split(',')
                    for bnumber in bnums_list:
                        tu_gene = TU.get_gene_object(
                            bnumber=bnumber,
                            bnumber_data=self.bnumbers
                        )
                        if tu_gene:
                            genes_list.append(tu_gene)
        self._genes = genes_list

    # Static methods
    @staticmethod
    def get_gene_object(bnumber, bnumber_data):
        tu_gene = None
        if bnumber_data.get(bnumber):
            tu_gene = {
                "_id": bnumber_data.get(bnumber).get('_id'),
                "name": bnumber_data.get(bnumber).get('name'),
                "bnumber": bnumber_data.get(bnumber).get('bnumber'),
            }
        return tu_gene
