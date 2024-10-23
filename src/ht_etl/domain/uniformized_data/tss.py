"""
Transcription Start Site object.
Build uniformized data object for every dataset.
"""
# standard
import logging

# third party

# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base
from src.ht_etl.domain.uniformized_data.domain.tss import TSS


class TSSs(Base):

    def __init__(self, **kwargs):
        super(TSSs, self).__init__(**kwargs)
        # Params

        # Local properties

        # Object properties
        self.tss_list = kwargs.get('tss_list', None)

    # Local properties

    # Object properties
    @property
    def tss_list(self):
        return self._tss_list

    @tss_list.setter
    def tss_list(self, tss_list=None):
        tss_list = []
        for tss_data in self.uniform_dataset_dict:
            tss_obj = TSS(
                genes_ranges=self.genes_ranges,
                type=self.type,
                dataset_id=self.dataset_id,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                data_row=tss_data,
                database=self.database,
                url=self.url
            )
            tss_dict = {
                '_id': tss_obj.id,
                'temporalId': tss_obj.temporal_id,
                'chromosome': tss_obj.chromosome,
                'leftEndPosition': tss_obj.left_pos,
                'rightEndPosition': tss_obj.right_pos,
                'strand': tss_obj.strand,
                'pos_1': tss_obj.pos_1,
                'closestGenes': tss_obj.closest_genes,
                'promoter': tss_obj.promoters,
                'datasetIds': [tss_obj.dataset_id]
            }
            tss_list.append(tss_dict)
        self._tss_list = tss_list

    # Static methods
