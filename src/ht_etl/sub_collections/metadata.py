"""
Dataset MetaData object.
"""
# standard
import logging
import datetime

# third party

# local
from src.libs.readme_data import ReadmeData


class Metadata(object):
    def __init__(self, **kwargs):
        # Params
        self.dataset_type = kwargs.get('dataset_type', None)
        self.collection_name = kwargs.get('collection_name', None)
        self.readme_path = kwargs.get('readme_path', None)
        self.source = kwargs.get('collection_source', None)
        self.status = kwargs.get('collection_status', None)
        self.reference = kwargs.get('pmid', None)

        # Local properties
        self.metadata_content = kwargs.get('metadata_content', None)
        self.pmids = kwargs.get('pmids', None)

        # Object properties
        self.metadata = kwargs.get('metadata', None)

    # Local properties
    @property
    def pmids(self):
        return self._pmids

    @pmids.setter
    def pmids(self, pmids=None):
        """
        Parses PMIDs to List type.
        """
        self._pmids = pmids
        if pmids is None:
            pmids = []
            pmid = self.reference
            if isinstance(pmid, int) or isinstance(pmid, float):
                pmids = [pmid]
            elif isinstance(pmid, str):
                pmids = pmid.replace(' ', '')
                pmids = pmids.split(',')
            pmids = [int(pmid) for pmid in pmids]
            self._pmids = pmids

    @property
    def metadata_content(self):
        return self._metadata_content

    @metadata_content.setter
    def metadata_content(self, metadata_content=None):
        if not metadata_content:
            metadata_content = ReadmeData(
                path=self.readme_path,
                dataset_name=self.dataset_type
            )
        self._metadata_content = metadata_content.readme_txt

    # Object properties
    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata_dict=None):
        if metadata_dict is None:
            metadata_dict = {
                'dataset_type': self.dataset_type,
                'source': self.source,
                'metadata_content': self.metadata_content,
                'status': self.status,
                'release_date': datetime.datetime.today().strftime("%d/%m/%Y"),
                'reference': self.pmids
            }
        self._metadata = metadata_dict
