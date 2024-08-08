"""
Gene Expression object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.domain.base import Base


class GeneExpression(Base):

    def __init__(self, **kwargs):
        super(GeneExpression, self).__init__(**kwargs)
        # Params
        self.bnumbers = kwargs.get("bnumbers", None)

        # Local properties

        # Object properties
        self.id = kwargs.get("id", None)
        self.count = kwargs.get("count", None)
        self.fpkm = kwargs.get("fpkm", None)
        self.tpm = kwargs.get("tpm", None)
        self.gene = kwargs.get("gene", None)

    # Local properties

    # Object properties
    @property
    def dataset_ids(self):
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, dataset_ids=None):
        self._dataset_ids = dataset_ids
        if dataset_ids is None:
            dataset_ids = [f'{self.type}_{self.data_row[1]}']
            self._dataset_ids = dataset_ids

    @property
    def temporal_id(self):
        return self._temporal_id

    @temporal_id.setter
    def temporal_id(self, temporal_id=None):
        if temporal_id is None:
            temporal_id = f'{self.type}_{self.data_row[1]}_{self.data_row[2]}'
        self._temporal_id = temporal_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, genex_id=None):
        if genex_id is None:
            genex_id = self.temporal_id
        self._id = genex_id

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count=None):
        if count is None:
            count = float(self.data_row[3])
        self._count = count

    @property
    def fpkm(self):
        return self._fpkm

    @fpkm.setter
    def fpkm(self, fpkm=None):
        if fpkm is None:
            fpkm = float(self.data_row[4])
        self._fpkm = fpkm

    @property
    def tpm(self):
        return self._tpm

    @tpm.setter
    def tpm(self, tpm=None):
        if tpm is None:
            tpm = float(self.data_row[5])
        self._tpm = tpm

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene=None):
        if gene is None:
            gene = self.bnumbers.get(self.data_row[2])
        self._gene = gene
