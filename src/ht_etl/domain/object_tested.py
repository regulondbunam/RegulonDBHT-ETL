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
        self.tf_names = kwargs.get('tf_name', [])
        self.mg_tf_objects = ObjectTested.get_mg_tf_object(
            tf_names=self.tf_names,
            database=self.database,
            url=self.url
        )

        # Object properties
        self.object_tested = kwargs.get('object_tested', None)

    # Local properties
    @property
    def tf_names(self):
        return self._tf_names

    @tf_names.setter
    def tf_names(self, tf_names):
        """
        Sets TF Name.
        """
        tf_names = self.regulondb_tf_name
        if tf_names is None:
            tf_names = self.source_tf_name
        tf_names = tf_names.replace(' ', '').split(',')
        self._tf_names = tf_names

    # Object properties
    @property
    def object_tested(self):
        return self._object_tested

    @object_tested.setter
    def object_tested(self, mg_tf_objects=None):
        """
        Sets Object Tested.
        """
        objects_tested = []
        if mg_tf_objects is None:
            for mg_tf_object in self.mg_tf_objects:
                if mg_tf_object:
                    tf_id = mg_tf_object.id
                    tf_name = mg_tf_object.abbreviated_name
                    prod_id = mg_tf_object.products_ids[0]
                    synonyms = mg_tf_object.synonyms
                    note = mg_tf_object.note
                    act_conf = ObjectTested.get_tf_act_conformations(
                        mg_tf_object.active_conformations
                    )
                    external_cross_ref = ObjectTested.get_tf_ext_cross_ref(
                        mg_tf_object.external_cross_references
                    )
                    genes = Genes(
                        tf_name=tf_name,
                        prod_ids=prod_id,
                        database=self.database,
                        url=self.url
                    )
                    object_tested = {
                        '_id': tf_id,
                        'name': tf_name,
                        'synonyms': synonyms,
                        'genes': genes.genes,
                        'note': note,
                        'activeConformations': act_conf,
                        'externalCrossReferences': external_cross_ref
                    }
                    objects_tested.append(object_tested)
        self._object_tested = objects_tested

    # Static methods
    @staticmethod
    def get_mg_tf_object(tf_names, database, url):
        """
        Gets TF object from Multigenomic database.
        Args:
            tf_names: List, name of TF object.
            database: String, name of database.
            url: String, URL of MongoDB database.

        Returns:
            mg_tfs: multigenomic_api.transcription_factors object list
        """
        mg_tfs = []
        mg_api.connect(database, url)
        for tf_name in tf_names:
            mg_tf = mg_api.transcription_factors.find_by_abb_name(tf_name)
            if mg_tf:
                mg_tfs.append(mg_tf)
        mg_api.disconnect()
        return mg_tfs

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
