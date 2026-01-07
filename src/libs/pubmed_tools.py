"""
Specialized functions for PubMed requests.
"""

# standard
import logging
import os
import ssl
from urllib.error import URLError

# third party
from Bio import Entrez, Medline


# Optional: allow disabling SSL verification via environment variable.
# If you export HT_DISABLE_PUBMED_SSL_VERIFY=1 before running the ETL,
# PubMed HTTPS requests will skip certificate verification.
# if os.getenv("HT_DISABLE_PUBMED_SSL_VERIFY") == "1":
ssl._create_default_https_context = ssl._create_unverified_context()
logging.warning(
    "HT_DISABLE_PUBMED_SSL_VERIFY=1 detected. SSL certificate verification "
    "is DISABLED for HTTPS requests (PubMed). Use with caution."
)


def format_authors(pubmed_authors):
    """
    Format PubMed authors list.

    Parameters
    ----------
    pubmed_authors : str or list
        Authors as returned by Medline record (field 'AU').

    Returns
    -------
    list
        Formatted authors list.
    """
    if isinstance(pubmed_authors, str):
        pubmed_authors = pubmed_authors.split(",")
    return pubmed_authors


def format_article_id(article_id):
    """
    Format article id (DOI) string.

    Parameters
    ----------
    article_id : list or None
        Unformatted article id list from Medline record (field 'AID').

    Returns
    -------
    str or None
        DOI string without the ' [doi]' suffix, or None if not found.
    """
    if not article_id:
        return None

    for doi in article_id:
        if " [doi]" in doi:
            return doi.replace(" [doi]", "")
    return None


def get_pubmed_data(dataset_id, pmids, email):
    """
    Connect to PubMed through the Entrez API and retrieve publication data.

    The Entrez API returns Medline data; see also:
    https://biopython.org/docs/1.75/api/Bio.Medline.html

    Parameters
    ----------
    dataset_id : str
        Dataset identifier associated with these PMIDs.
    pmids : list
        List of PubMed IDs (PMIDs) to fetch.
    email : str
        User email address for Entrez API (required by NCBI).

    Returns
    -------
    list[dict]
        List of publication dictionaries with the following possible keys:
        - authors
        - abstract
        - date
        - pmcid
        - pmid
        - title
        - doi
        Keys with None/empty values are removed from each publication.
    """
    if not pmids:
        logging.warning(f"No PMIDs provided for dataset: {dataset_id}.")
        return []

    Entrez.email = email

    publications = []

    for pmid in pmids:
        if isinstance(pmid, float):
            pmid = int(pmid)

        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=str(pmid),
                rettype="medline",
                retmode="text",
            )
            record = Medline.read(handle)
        except URLError as e:
            logging.error(
                f"Error fetching PubMed data for PMID {pmid} "
                f"(dataset {dataset_id}): {e}"
            )
            # Skip this PMID but continue with the rest
            continue
        except Exception as e:
            logging.error(
                f"Unexpected error fetching PubMed data for PMID {pmid} "
                f"(dataset {dataset_id}): {e}"
            )
            continue

        publication = {}

        pubmed_authors = format_authors(record.get("AU"))
        doi = format_article_id(record.get("AID"))

        publication.setdefault("authors", pubmed_authors)
        publication.setdefault("abstract", record.get("AB"))
        publication.setdefault("date", record.get("DP"))
        publication.setdefault("pmcid", record.get("PMC"))
        if record.get("PMID"):
            publication.setdefault("pmid", int(record.get("PMID")))
        publication.setdefault("title", record.get("TI"))
        publication.setdefault("doi", doi)

        # Remove null/empty properties
        publication = {k: v for k, v in publication.items() if v}

        publications.append(publication)

    return publications
