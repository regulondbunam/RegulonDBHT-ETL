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
        self.collection_data = kwargs.get('collection_data', None)

    # Local properties

    # Object properties
    @property
    def collection_data(self):
        return self._collection_data

    @collection_data.setter
    def collection_data(self, collection_data):
        """
        Sets Collection Data dict object.
        """
        self._collection_data = collection_data
        if collection_data is None:
            collection_name = self.collection_name.replace('-', '_').upper()
            collection_data = {
                'type': collection_name,
                'source': self.collection_source
            }
            collection_data = {k: v for k, v in collection_data.items() if v}
        self._collection_data = collection_data
