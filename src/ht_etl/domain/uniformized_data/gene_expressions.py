"""
Gene Expression object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base
from src.ht_etl.domain.uniformized_data.domain.gene_expression import GeneExpression


class GeneExpressions(Base):

    def __init__(self, **kwargs):
        super(GeneExpressions, self).__init__(**kwargs)
        # Params
        self.bnumbers = kwargs.get("bnumbers", None)

        # Local properties

        # Object properties
        self.genex_list = kwargs.get('genex_list', None)

    # Local properties

    # Object properties
    @property
    def genex_list(self):
        return self._genex_list

    @genex_list.setter
    def genex_list(self, genex_list=None):
        genex_list = []
        for genex_data in self.uniform_dataset_dict.get('uniform_datasets', []):
            genex_obj = GeneExpression(
                type=self.type,
                dataset_id=self.dataset_id,
                bnumbers=self.bnumbers,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                data_row=genex_data,
                database=self.database,
                url=self.url
            )
            genex_dict = {
                '_id': genex_obj.id,
                'count': genex_obj.count,
                'dataset_id': [genex_obj.dataset_id],
                'fpkm': genex_obj.fpkm,
                'gene': genex_obj.gene,
                'temporalId': genex_obj.temporal_id,
                'tpm': genex_obj.tpm
            }
            genex_list.append(genex_dict)
        self._genex_list = genex_list

    # Static methods
