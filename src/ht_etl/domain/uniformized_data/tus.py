"""
Transcription Units object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base


class TUs(Base):

    def __init__(self, **kwargs):
        super(TUs, self).__init__(**kwargs)
        # Params
        self.tus = kwargs.get('tus')

        # Local properties

        # Object properties

    # Local properties

    # Object properties

    # Static methods
