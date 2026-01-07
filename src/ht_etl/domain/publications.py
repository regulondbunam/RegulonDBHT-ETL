"""
Publications object.
"""
# standard

# third party

# local
import libs.pubmed_tools as pubmed_tools


class Publications(object):
    def __init__(self, **kwargs):
        # Params
        self.dataset_id = kwargs.get('dataset_id', None)
        self.pmid = kwargs.get('pmid', None)
        self.email = kwargs.get('email', None)

        # Local properties
        self.pmids = kwargs.get('pmids', None)

        # Object properties
        self.publications_list = kwargs.get('publications_list', None)

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
            pmid = self.pmid
            if isinstance(pmid, int) or isinstance(pmid, float):
                pmids = [pmid]
            elif isinstance(pmid, str):
                pmids = pmid.replace(' ', '')
                pmids = pmids.split(',')
            self._pmids = pmids

    # Object properties
    @property
    def publications_list(self):
        return self._publications_list

    @publications_list.setter
    def publications_list(self, publications_list=None):
        """
        Gets publications list from pmids.
        """
        self._publications_list = publications_list
        if self.publications_list is None:
            publications_list = pubmed_tools.get_pubmed_data(
                dataset_id=self.dataset_id,
                pmids=self.pmids,
                email=self.email
            )
            self._publications_list = publications_list
