"""
Transcription Start Site object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base


class TSS(Base):

    def __init__(self, **kwargs):
        super(TSS, self).__init__(**kwargs)
        # Params
        self.tss = kwargs.get('tss')

        # Local properties

        # Object properties

    # Local properties

    # Object properties

    # Static methods
