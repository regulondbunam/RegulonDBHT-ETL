"""
Term object.
"""
# standard

# third party

# local
from src.libs import utils


class Term(object):

    def __init__(self, **kwargs):
        # Params
        self.data = kwargs.get('data', None)
        # Local properties
        self.source_data = kwargs.get('source_data', None)

        # Object properties
        self.type = kwargs.get('type', None)
        self.value = kwargs.get('value', None)
        self.associated_phrase = kwargs.get('associated_phrase', None)
        self.name_field = kwargs.get('name_field', None)
        self.score = kwargs.get('score', None)

    # Local properties
    @property
    def source_data(self):
        return self._source_data

    @source_data.setter
    def source_data(self, src_data=None):
        self._source_data = self.data.get('source_data', {})

    # Object properties
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, term_type=None):
        self._type = self.data.get('term_type', term_type)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value=None):
        self._value = self.data.get('name', value)

    @property
    def associated_phrase(self):
        return self._associated_phrase

    @associated_phrase.setter
    def associated_phrase(self, associated_phrase=None):
        self._associated_phrase = self.source_data.get('associatedPhrase', associated_phrase)

    @property
    def name_field(self):
        return self._name_field

    @name_field.setter
    def name_field(self, name_field=None):
        self._name_field = self.source_data.get('field', name_field)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score=None):
        self._score = self.source_data.get('similarity_percentage', score)
