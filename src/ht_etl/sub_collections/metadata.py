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

        # Object properties
        self.metadata_id = kwargs.get("metadata_id", None)
        self.metadata_content = kwargs.get('metadata_content', None)
        self.pmids = kwargs.get('pmids', None)
        self.release_date = kwargs.get('release_date', None)

    # Local properties

    # Object properties
    @property
    def metadata_id(self):
        return self._metadata_id

    @metadata_id.setter
    def metadata_id(self, metadata_id):
        metadata_id = f'METADATA_{self.collection_name}_{self.dataset_type}_{self.source}'
        self._metadata_id = metadata_id

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
                pmids = pmids.replace(';', ',')
                pmids = pmids.split(',')
            pmids = [int(pmid) for pmid in pmids]
            self._pmids = pmids

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, release_date):
        """
        Sets release date.
        """
        self._release_date = release_date
        if self._release_date is None:
            release_date = datetime.datetime.today().strftime("%d/%m/%Y")
            self._release_date = release_date

    @property
    def metadata_content(self):
        return self._metadata_content

    @metadata_content.setter
    def metadata_content(self, metadata_content=None):
        """
        Sets metadata content.
        """
        if not metadata_content:
            metadata_content = ReadmeData(
                path=self.readme_path,
                dataset_name=self.dataset_type
            )
        self._metadata_content = metadata_content.readme_txt
