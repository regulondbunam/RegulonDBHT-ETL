"""
TTS object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.libs import utils
from src.ht_etl.domain.uniformized_data.domain.base import Base


class TTS(Base):

    def __init__(self, **kwargs):
        super(TTS, self).__init__(**kwargs)
        # Params

        # Local properties

        # Object properties
        self.terminator = kwargs.get("terminator", None)

    # Local properties

    # Object properties
    @property
    def terminator(self):
        return self._terminator

    @terminator.setter
    def terminator(self, terminator=None):
        if terminator is None:
            terminator = utils.find_terminators(
                left_pos=self.left_pos,
                right_pos=self.right_pos,
                tts_id=self.id,
                mg_api=self.mg_api
            )
        self._terminator = terminator

