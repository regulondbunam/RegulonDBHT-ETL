"""
Transcription Termination Site object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from ht_etl.domain.uniformized_data.uniformized_base import Base
from ht_etl.domain.uniformized_data.domain.tts import TTS


class TTSs(Base):

    def __init__(self, **kwargs):
        super(TTSs, self).__init__(**kwargs)
        # Params

        # Local properties

        # Object properties
        self.tts_list = kwargs.get('tts_list', None)

    # Local properties

    # Object properties
    @property
    def tts_list(self):
        return self._tts_list

    @tts_list.setter
    def tts_list(self, tts_list=None):
        tts_list = []
        for tts_data in self.uniform_dataset_dict:
            tts_obj = TTS(
                genes_ranges=self.genes_ranges,
                type=self.type,
                dataset_id=self.dataset_id,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                data_row=tts_data,
                database=self.database,
                url=self.url
            )
            tts_dict = {
                '_id': tts_obj.id,
                'temporalId': tts_obj.temporal_id,
                'chromosome': tts_obj.chromosome,
                'leftEndPosition': tts_obj.left_pos,
                'rightEndPosition': tts_obj.right_pos,
                'strand': tts_obj.strand,
                'closestGenes': tts_obj.closest_genes,
                'terminator': tts_obj.terminator,
                'datasetIds': [tts_obj.dataset_id]
            }
            tts_list.append(tts_dict)
        self._tts_list = tts_list

    # Static methods
