"""
Citation object.
"""
# standard
import logging

# third party

# local


class Citation(object):

    def __init__(self, **kwargs):
        # Params
        self.mg_api = kwargs.get('mg_api', None)
        self.citations_obj_list = kwargs.get('citations_obj_list', None)

        # Local properties

        # Object properties
        self.citations_list = kwargs.get("citations_list", None)

    # Local properties

    # Objects properties
    @property
    def citations_list(self):
        return self._citations_list

    @citations_list.setter
    def citations_list(self, citations_list=None):
        citations_list = []
        for citation_obj in self.citations_obj_list:
            evidence_id = citation_obj.evidences_id
            publication_id = citation_obj.publications_id
            citation = {
                'evidence': Citation.set_evidence(
                    mg_api=self.mg_api,
                    evidence_id=evidence_id,
                ),
                'publication': Citation.set_publication(
                    mg_api=self.mg_api,
                    publication_id=publication_id,
                )
            }
            citation = {k: v for k, v in citation.items() if v}
            citations_list.append(citation)
        self._citations_list = citations_list

    # Static method
    @staticmethod
    def set_evidence(mg_api, evidence_id):
        evidence = None
        try:
            mg_evidence = mg_api.evidences.find_by_id(evidence_id)
            evidence = {
                'id': mg_evidence.id,
                'name': mg_evidence.name,
                'code': mg_evidence.code,
                'type': mg_evidence.type
            }
            evidence = {k: v for k, v in evidence.items() if v}
        except Exception:
            logging.error(f'Can not find Evidence {evidence_id}')
        return evidence

    @staticmethod
    def set_publication(mg_api, publication_id):
        publication = None
        try:
            mg_publication = mg_api.publications.find_by_id(publication_id)
            publication = {
                'id': mg_publication.id,
                'authors': mg_publication.authors,
                'pmid': mg_publication.pmid,
                'title': mg_publication.title,
                'url': mg_publication.url,
                'year': mg_publication.year,
                # TODO: 'citation': mg_publication.citation what is this?
            }
            publication = {k: v for k, v in publication.items() if v}
        except Exception:
            logging.error(f'Can not find Publication {publication_id}')
        return publication
