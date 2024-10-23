"""
Collection Data object.
"""
# standard
import logging

# third party

# local


class CollectionData(object):
    def __init__(self, **kwargs):
        # Params
        self.collection_name = kwargs.get('collection_name', None)
        self.collection_source = kwargs.get('collection_source', None)

        # Local properties

        # Object properties
        self.collection_name_upper = kwargs.get('collection_name_upper', None)

    # Local properties

    # Object properties
    @property
    def collection_name_upper(self):
        return self._collection_name_upper

    @collection_name_upper.setter
    def collection_name_upper(self, collection_name_upper=None):
        """
        Parse the collection name to upper case and replace - with _.
        """
        self._collection_name_upper = collection_name_upper
        if collection_name_upper is None:
            collection_name_upper = self.collection_name.replace('-', '_').upper()
            self._collection_name_upper = collection_name_upper
