"""
Object Tested object.
"""
# standard
import logging

# third party
import multigenomic_api as mg_api

# local
from src.ht_etl.sub_domain.genes import Genes


class ObjectTested(object):
    def __init__(self, **kwargs):
        # Params
        self.regulondb_tf_name = kwargs.get('regulondb_tf_name', None)
        self.source_tf_name = kwargs.get('source_tf_name', None)
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)
        # Local properties
        self.tf_name = kwargs.get('tf_name', None)
        self.mg_tf_object = ObjectTested.get_mg_tf_object(
            tf_name=self.tf_name,
            database=self.database,
            url=self.url
        )

        # Object properties
        self.object_tested = kwargs.get('object_tested', None)

    # Local properties
    @property
    def tf_name(self):
        return self._tf_name

    @tf_name.setter
    def tf_name(self, tf_name=None):
        """
        Sets TF Name.
        """
        self._tf_name = tf_name
        if tf_name is None:
            tf_name = self.regulondb_tf_name
            if tf_name is None:
                tf_name = self.source_tf_name
        self._tf_name = tf_name

    # Object properties
    @property
    def object_tested(self):
        return self._object_tested

    @object_tested.setter
    def object_tested(self, tf_name=None):
        """
        Sets Object Tested.
        """
        if tf_name is None:
            tf_name = self.tf_name
            genes = Genes(
                tf_name=self.tf_name,
                prod_ids=self.mg_tf_object.products_ids[0],
                database=self.database,
                url=self.url
            )
            object_tested = {
                '_id': '',
                'name': tf_name,
                'synonyms': self.mg_tf_object.synonyms,
                'genes': genes.genes,
                'note': self.mg_tf_object.note,
                'activeConformations': ObjectTested.get_tf_act_conformations(
                    self.mg_tf_object.active_conformations
                 ),
                'externalCrossReferences': ObjectTested.get_tf_ext_cross_ref(
                    self.mg_tf_object.external_cross_references
                )
            }
            self._object_tested = object_tested

    # Static methods
    @staticmethod
    def get_mg_tf_object(tf_name, database, url):
        """
        Gets TF object from Multigenomic database.
        Args:
            tf_name: String, name of TF object.
            database: String, name of database.
            url: String, URL of MongoDB database.

        Returns:
            mg_tf: multigenomic_api.transcription_factors object
        """
        mg_api.connect(database, url)
        mg_tf = mg_api.transcription_factors.find_by_abb_name(tf_name)
        mg_api.disconnect()
        return mg_tf

    @staticmethod
    def get_tf_act_conformations(act_conformations):
        """
        Gets Active conformations list from multigenomic_api constructor.
        Args:
            act_conformations: multigenomic_api.active_conformations object

        Returns:
            act_conformations_list: List, list of Active conformations ids.
        """
        act_conformations_list = []
        for act_conformation in act_conformations:
            act_conformations_list.append(act_conformation.id)
        return act_conformations_list

    @staticmethod
    def get_tf_ext_cross_ref(external_cross_refs):
        """
        Gets External Cross References list from multigenomic_api object.
        Args:
            external_cross_refs: multigenomic_api.external_cross_ref object

        Returns:
            external_cross_refs_list: Dict List, list of External Cross References dicts.
        """
        external_cross_refs_list = []
        for external_cross_ref in external_cross_refs:
            external_cross_refs_dict = {
                'externalCrossReferences_id': external_cross_ref.external_cross_references_id,
                'objectId': external_cross_ref.object_id
            }
            external_cross_refs_list.append(external_cross_refs_dict)
        return external_cross_refs_list
