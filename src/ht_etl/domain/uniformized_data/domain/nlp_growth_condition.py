"""
NLP Growth Condition object.
Build uniformized data object.
"""
# standard

# third party

# local
from src.ht_etl.domain.uniformized_data.domain.base import Base
from src.ht_etl.domain.uniformized_data.domain.sub_domain.term import Term
from src.libs import utils


class NLPGrowthCondition(Base):

    def __init__(self, **kwargs):
        super(NLPGrowthCondition, self).__init__(**kwargs)
        # Params

        # Local properties
        self.terms = kwargs.get("terms", None)

        # Object properties
        self.dataset_ids = kwargs.get("dataset_ids", None)
        self.temporal_id = kwargs.get("temporal_id", None)
        self.id = kwargs.get("id", None)
        self.organism = kwargs.get('organism', None)
        self.genetic_background = kwargs.get('genetic_background', None)
        self.medium = kwargs.get('medium', None)
        self.aeration = kwargs.get('aeration', None)
        self.temperature = kwargs.get('temperature', None)
        self.ph = kwargs.get('ph', None)
        self.pressure = kwargs.get('pressure', None)
        self.optical_density = kwargs.get('optical_density', None)
        self.growth_phase = kwargs.get('growth_phase', None)
        self.growth_rate = kwargs.get('growth_rate', None)
        self.vessel_type = kwargs.get('vessel_type', None)
        self.aeration_speed = kwargs.get('aeration_speed', None)
        self.medium_supplements = kwargs.get('medium_supplements', None)
        self.additional_properties = kwargs.get('additional_properties', None)

    # Local properties

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, terms=None):
        terms_dict_list = []
        if terms is None:
            terms_list = self.data_row.get('terms', None)
            for term in terms_list:
                if term.get('name') not in [
                    "Unclear",
                    "TruSeq",
                    "GEO_secondstrand",
                    "ScriptSeq",
                    "GEO_unclear"
                ]:
                    term_obj = Term(
                        data=term,
                    )
                    term_dict = {
                        'term_type': term_obj.type,
                        'value': term_obj.value,
                        'associated_phrase': term_obj.associated_phrase,
                        'name_field': term_obj.name_field,
                        'score': term_obj.score,
                    }
                    if term_dict.get('value') is not None:
                        terms_dict_list.append(term_dict)
        self._terms = terms_dict_list

    # Object properties
    @property
    def dataset_ids(self):
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, value):
        self._dataset_ids = NLPGrowthCondition.split_combined_ids(
            self.dataset_id
        )


    @property
    def temporal_id(self):
        return self._temporal_id

    @temporal_id.setter
    def temporal_id(self, temporal_id=None):
        if temporal_id is None:
            temporal_id = f'{self.type}_{self.dataset_id}'
        self._temporal_id = temporal_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, gc_id=None):
        if gc_id is None:
            gc_id = f'GC_{self.dataset_id}'
        self._id = gc_id

    @property
    def organism(self):
        return self._organism

    @organism.setter
    def organism(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='organism'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Organism'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Strain'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Substrain'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._organism = term_dict

    @property
    def genetic_background(self):
        return self._genetic_background

    @genetic_background.setter
    def genetic_background(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='genetic_background'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Genetic background'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Gtype'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._genetic_background = term_dict

    @property
    def medium(self):
        return self._medium

    @medium.setter
    def medium(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='medium'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Medium'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Med'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._medium = term_dict

    @property
    def aeration(self):
        return self._aeration

    @aeration.setter
    def aeration(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='aeration'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Aeration'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Air'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._aeration = term_dict

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='temperature'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Temperature'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Tem'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._temperature = term_dict

    @property
    def ph(self):
        return self._ph

    @ph.setter
    def ph(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='ph'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='pH'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='PH'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._ph = term_dict

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='pressure'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Pressure'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Press(NA)'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._pressure = term_dict

    @property
    def optical_density(self):
        return self._optical_density

    @optical_density.setter
    def optical_density(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='optical_density'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Optical Density (OD)'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='OD'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._optical_density = term_dict

    @property
    def growth_phase(self):
        return self._growth_phase

    @growth_phase.setter
    def growth_phase(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='growth_phase'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Growth phase'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Phase'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._growth_phase = term_dict

    @property
    def growth_rate(self):
        return self._growth_rate

    @growth_rate.setter
    def growth_rate(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='growth_rate'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Growth rate'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Grate(NA)'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._growth_rate = term_dict

    @property
    def vessel_type(self):
        return self._vessel_type

    @vessel_type.setter
    def vessel_type(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='vessel_type'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Vessel Type'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Vess'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._vessel_type = term_dict

    @property
    def aeration_speed(self):
        return self._aeration_speed

    @aeration_speed.setter
    def aeration_speed(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='aeration_speed'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Aeration speed'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Aeration Speed'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._aeration_speed = term_dict

    @property
    def medium_supplements(self):
        return self._medium_supplements

    @medium_supplements.setter
    def medium_supplements(self, term_obj=None):
        term_dict = {}
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='medium_supplements'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Medium supplement'
            )
        if term_obj is None:
            term_obj = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='Supp'
            )
        if term_obj is not None:
            term_dict = {
                'value': term_obj.get('value'),
                'associated_phrase': term_obj.get('associated_phrase'),
                'name_field': term_obj.get('name_field'),
                'score': term_obj.get('score'),
            }
        self._medium_supplements = term_dict

    @property
    def additional_properties(self):
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties=None):
        if additional_properties is None:
            additional_properties = utils.find_one_in_dict_list(
                dict_list=self.terms,
                key_name='term_type',
                value='additional_properties'
            )
            # additional_properties.pop('term_type', None)
        self._additional_properties = additional_properties

    # Static methods
    @staticmethod
    def split_combined_ids(ids_string):
        """
        Split combined ids string into list of strings.
        Args:
            ids_string:

        Returns:

        """
        dataset_ids = []
        str_id = ""
        last_char = None
        for char in ids_string:
            if str(char).isalpha() and last_char is None:
                str_id = f"{str_id}{char}"
                last_char = char
            elif str(char).isalpha() and last_char.isalpha():
                str_id = f"{str_id}{char}"
                last_char = char
            elif str(char).isalpha() and last_char.isdigit():
                dataset_ids.append(str_id)
                str_id = f"{char}"
                last_char = char
            elif str(char).isdigit() and last_char.isdigit():
                str_id = f"{str_id}{char}"
                last_char = char
            elif str(char).isdigit() and last_char.isalpha():
                str_id = f"{str_id}{char}"
                last_char = char
        dataset_ids.append(str_id)
        return dataset_ids
