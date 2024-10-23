"""
Specialized functions for Pubmed requests.
"""
# standard
import logging

# third party
from Bio import Entrez, Medline
# local


def format_authors(pubmed_authors):
    """
    Format pubmed authors names list.
    Args:
        pubmed_authors: String, list of pubmed authors.

    Returns:
        pubmed_authors: List, formatted pubmed authors
    """
    if isinstance(pubmed_authors, str):
        pubmed_authors = pubmed_authors.split(',')
    return pubmed_authors


def format_article_id(article_id):
    """
    Format article id (doi) string.
    Args:
        article_id: List, un-formatted article id.

    Returns:
        doi: String, formatted article id.
    """
    for doi in article_id:
        if ' [doi]' in doi:
            return doi.replace(' [doi]', '')
    return None


def get_pubmed_data(dataset_id, pmids, email):
    """
    Connects to PUBMED database through Entrez API and gets the necessary publication data.
    The Entrez API returns a dictionary with the medline data, see also
    https://biopython.org/docs/1.75/api/Bio.Medline.html for
    more information about the keys obtained from this dictionary.

    Args:
        dataset_id: String, dataset id.
        pmids: Integer List, PUBMED publications ids.
        email: String, User email address to connect to PUBMED database.

    Returns:
        publication: Dict, dictionary with the publication data.
    """
    if not pmids:
        logging.warning(f'No PMIDs provided for dataset: {dataset_id}.')
        return []

    Entrez.email = email

    publications = []

    for pmid in pmids:
        publication = {}
        if isinstance(pmid, float):
            pmid = int(pmid)

        handle = Entrez.efetch(
            db='pubmed',
            id=pmid,
            rettype='medline',
            retmode='text'
        )
        record = Medline.read(handle)

        pubmed_authors = format_authors(record.get('AU'))
        doi = format_article_id(record.get('AID'))

        publication.setdefault('authors', pubmed_authors)
        publication.setdefault('abstract', record.get('AB'))
        publication.setdefault('date', record.get('DP'))
        publication.setdefault('pmcid', record.get('PMC'))
        publication.setdefault('pmid', int(record.get('PMID')))
        publication.setdefault('title', record.get('TI'))
        publication.setdefault('doi', doi)
        # Remove Null properties
        publication = {k: v for k, v in publication.items() if v}

        publications.append(publication)
    return publications
