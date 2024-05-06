"""
TSS object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.libs import utils
from src.ht_etl.domain.uniformized_data.domain.base import Base


class TSS(Base):

    def __init__(self, **kwargs):
        super(TSS, self).__init__(**kwargs)
        # Params

        # Local properties

        # Object properties
        self.pos_1 = kwargs.get('pos_1', None)
        self.promoters = kwargs.get('promoters', None)

    # Local properties

    # Object properties
    @property
    def pos_1(self):
        return self._pos_1

    @pos_1.setter
    def pos_1(self, pos_1=None):
        if pos_1 is None:
            if isinstance(self.data_row, dict):
                pos_1 = self.data_row.get("pos_1", None)
        self._pos_1 = pos_1

    @property
    def promoters(self):
        return self._promoters

    @promoters.setter
    def promoters(self, promoters=None):
        if promoters is None:
            promoters = utils.get_promoter(
                lend=self.left_pos,
                rend=self.right_pos,
                mg_api=self.mg_api
            )
        self._promoters = promoters
