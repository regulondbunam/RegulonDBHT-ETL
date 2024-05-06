"""
Transcription Units object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base
from src.ht_etl.domain.uniformized_data.domain.tu import TU


class TUs(Base):

    def __init__(self, **kwargs):
        super(TUs, self).__init__(**kwargs)
        # Params
        # print(self.uniform_dataset_dict)
        self.bnumbers = kwargs.get("bnumbers", None)
        # Local properties

        # Object properties
        self.tus_list = kwargs.get("tus_list", None)

    # Local properties

    # Object properties
    @property
    def tus_list(self):
        return self._tus_list

    @tus_list.setter
    def tus_list(self, tus_list=None):
        tus_list = []
        for tu_data in self.uniform_dataset_dict:
            tu_obj = TU(
                type=self.type,
                dataset_id=self.dataset_id,
                bnumbers=self.bnumbers,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                data_row=tu_data,
                database=self.database,
                url=self.url
            )
            tu_dict = {
                '_id': tu_obj.id,
                'temporalId': tu_obj.temporal_id,
                'chromosome': tu_obj.chromosome,
                'leftPosition': tu_obj.left_pos,
                'rightPosition': tu_obj.right_pos,
                'strand': tu_obj.strand,
                'length': tu_obj.length,
                'termType': tu_obj.term_type,
                'genes': tu_obj.genes,
                'phantom': tu_obj.phantom,
                'pseudo': tu_obj.pseudo,
                'datasetIds': [tu_obj.dataset_id]
            }
            tus_list.append(tu_dict)
        self._tus_list = tus_list

    # Static methods
