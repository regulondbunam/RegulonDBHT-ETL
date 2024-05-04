"""
Transcription Termination Site object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base


class TTS(Base):

    def __init__(self, **kwargs):
        super(TTS, self).__init__(**kwargs)
        # Params
        self.tts = kwargs.get('tts')

        # Local properties

        # Object properties

    # Local properties

    # Object properties

    # Static methods
