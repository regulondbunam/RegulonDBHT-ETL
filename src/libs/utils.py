'''
Some functions that help to HT process.
'''
# standard
import os
import logging
import json
import pandas
import json
import re

# third party
from Bio import Entrez, Medline
import multigenomic_api as mg_api

# local
from libs import constants as EC


def get_collection_name(collection_path):
    '''
    Checks collection path to determine the collection name.
    Param
        collection_path, String, Raw collection path.
    Returns
        collection_name, String, Final collection name.
    '''
    collection_name = collection_path
    if 'CHIP-exo' in collection_name or 'ChIP-exo' in collection_name:
        collection_name = EC.CHIP_EXO
    if 'CHIP-Seq' in collection_name or 'ChIP-Seq' in collection_name:
        collection_name = EC.CHIP_SEQ
    if 'TUs' in collection_name:
        collection_name = EC.TUS
    if 'TSS' in collection_name:
        collection_name = EC.TSS
    if 'TTS' in collection_name:
        collection_name = EC.TTS
    if 'RNA' in collection_name:
        collection_name = EC.RNA
    if 'gSELEX' in collection_name:
        collection_name = EC.GSELEX
    if 'DAP' in collection_name:
        collection_name = EC.DAPS
    return collection_name


def get_collection_type(collection_path):
    '''
    Determines the Strategy which was used to process the collection.
    Param
        collection_path, String, Raw collection path.
    Returns
        collection_type, String, Final collection type.
    '''
    collection_type = collection_path
    if 'CHIP-exo' in collection_type or 'ChIP-exo' in collection_type:
        collection_type = 'CHIP_EXO_'
    if 'CHIP-Seq' in collection_type or 'ChIP-Seq' in collection_type:
        collection_type = ''
    if 'gSELEX' in collection_type:
        collection_type = 'GSELEX_'
    if 'DAP' in collection_type:
        collection_type = 'DAPS_'
    return collection_type


def set_json_object(filename, data_list, organism, sub_class_acronym, child_class_acronym):
    '''
    Sets the JSON output format of the collection..

    Param
        filename, String, the the output file name.
        data_list, List, the list with the collection data.
        organism, String, the organism name.

    Returns
        json_object, Dict, the dictionary with the final JSON file format
    '''
    json_object = {
        'collectionName': filename,
        'collectionData': data_list,
        'organism': organism,
        'subClassAcronym': sub_class_acronym,
        'classAcronym': organism,
        'childClassAcronym': child_class_acronym,
    }
    return json_object


def verify_bed_path(bed_path):
    '''
    This function filters BED files in the path and returns only correctly formatted path.

    Param
        bed_path, String, raw directory path.

    Returns
        bed_path, String, verified directory path.
    '''

    if os.path.isfile(bed_path) and bed_path.endswith('.bed'):
        logging.info(
            f'Reading dataset {bed_path}')
        return bed_path
    else:
        logging.warning(
            f'{bed_path} is not a valid BED file will be ignored')
        return None


def verify_txt_path(txt_path):
    '''
    This function filters TXT files in the path and returns only correctly formatted path.

    Param
        txt_path, String, raw directory path.

    Returns
        txt_path, String, verified directory path.
    '''

    if os.path.isfile(txt_path) and txt_path.endswith('.txt'):
        logging.info(
            f'Reading dataset {txt_path}')
        return txt_path
    else:
        logging.warning(
            f'{txt_path} is not a valid TXT file will be ignored')
        return None


def verify_tsv_path(tsv_path):
    '''
    This function filters TSV files in the path and returns only correctly formatted path.

    Param
        tsv_path, String, raw directory path.

    Returns
        tsv_path, String, verified directory path.
    '''

    if os.path.isfile(tsv_path) and tsv_path.endswith('.tsv'):
        logging.info(
            f'Reading dataset {tsv_path}')
        return tsv_path
    else:
        logging.warning(
            f'{tsv_path} is not a valid TSV file will be ignored')
        return None


def verify_csv_path(csv_path):
    '''
    This function filters CSV files in the path and returns only correctly formatted path.

    Param
        csv_path, String, raw directory path.

    Returns
        csv_path, String, verified directory path.
    '''

    if os.path.isfile(csv_path) and csv_path.endswith('.csv'):
        logging.info(
            f'Reading dataset {csv_path}')
        return csv_path
    else:
        logging.warning(
            f'{csv_path} is not a valid TSV file will be ignored')
        return None


def validate_directory(data_path):
    '''
    Verify if the output path directory exists.

    Param
        data_path, String, directory path.

    Return
        Boolean, boolean.
    '''
    if not os.path.isdir(data_path):
        logging.error(
            f'There is not {data_path} directory')
        return False
    else:
        return True


def validate_directories(data_path):
    '''
    Verify if the output path directories exists.

    Param
        data_path, String, directories path.

    Return
        Rise IOError if not valid directory
    '''
    if not os.path.isdir(data_path):
        raise IOError("Please, verify '{}' directory path".format(data_path))


def set_log(log_path):
    '''
    Initializes the execution log to examine any problems that arise during extraction.

    Param
        log_path, String, the execution log path.
    '''
    validate_directories(log_path)
    logging.basicConfig(filename=os.path.join(log_path, 'ht_etl.log'),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def create_json(objects, filename, output):
    '''
    Create and write the JSON file with the results.

    Param
        objects, Object, a Python serializable object that you want to convert to JSON format.
        filename, String, JSON file name.
        output, String, output path.
    '''
    filename = os.path.join(output, filename)
    with open(f'{filename}.json', 'w') as json_file:
        json.dump(objects, json_file, indent=4, sort_keys=True)

# TODO: Not used, must be deleted?


def list_to_dict(data):
    '''
    Turns a data List into a directory object.

    Param
        data, List, data list.

    Returns
        data_dict, Dict, data list converted to dictionary.
    '''
    data_dict = {}
    for object_dict in data:
        data_dict.update(object_dict)
    return data_dict


def get_data_frame(filename: str, load_sheet, rows_to_skip: int) -> pandas.DataFrame:
    '''
    Read and convert the Excel file to Panda DataFrame.

    Param
        filename, String, full XLSX file path.
        load_sheet, Integer, Excel sheet number that will be loaded.
        rows_to_skip, Integer, number of rows to skip.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    '''
    dataset_df = pandas.read_excel(
        filename, sheet_name=load_sheet, skiprows=rows_to_skip)
    return dataset_df


def get_author_data_frame(filename: str, load_sheet, rows_to_skip: int) -> pandas.DataFrame:
    '''
    Read and convert the Excel file to Panda DataFrame.

    Param
        filename, String, full XLSX file path.
        load_sheet, Integer, Excel sheet number that will be loaded.
        rows_to_skip, Integer, number of rows to skip.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    '''
    dataset_df = pandas.read_excel(
        filename, sheet_name=load_sheet, skiprows=rows_to_skip, index_col=0)
    nan_value = float("NaN")
    dataset_df.replace("", nan_value, inplace=True)
    dataset_df.dropna(how='all', axis=1, inplace=True)
    return dataset_df


def get_data_frame_tsv(filename: str) -> pandas.DataFrame:
    '''
    Read and convert the TSV file to Panda DataFrame.

    Param
        filename, String, full tsv file path.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    '''
    dataset_df = pandas.read_csv(filename, sep='\t', header=0, index_col=False)
    return dataset_df


def get_author_data_frame_tsv(filename: str) -> pandas.DataFrame:
    '''
    Read and convert the TSV file to Panda DataFrame.

    Param
        filename, String, full tsv file path.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    '''
    dataset_df = pandas.read_csv(filename, sep='\t',)
    return dataset_df


# TODO: Not used, must be deleted?
def get_data_frame_tsv_coma(filename: str) -> pandas.DataFrame:
    '''
    Read and convert the TSV file to Panda DataFrame.

    Param
        filename, String, full tsv file path.

    Returns
        dataset_df, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.
    '''
    dataset_df = pandas.read_csv(filename, sep=',', header=0)
    return dataset_df


def get_json_from_data_frame(data_frame: pandas.DataFrame) -> dict:
    '''
    Converts DataFrame into JSON format.

    Param
        data_frame, pandas.DataFrame, DataFrame with the Datasets Record Excel file data.

    Returns
        json_dict, Dict, JSON string converted  to a dictionary.
    '''
    string_json = data_frame.to_json(orient='records')
    string_json = re.sub(r'\([0-9]\)\s*', '', string_json)
    json_dict = json.loads(string_json)
    return json_dict


def get_excel_data(filename: str, load_sheet, rows_to_skip: int) -> dict:
    '''
    Process the XLSX file as a DataFrame and return it as a JSON object

    Param
        filename, String, Excel file name.

    Returns
        data_frame_json, Dict, json dictionary with the Excel data.
    '''
    data_frame = get_data_frame(filename, load_sheet, rows_to_skip)
    data_frame_json = get_json_from_data_frame(data_frame)
    return data_frame_json


def get_tsv_data(filename: str) -> dict:
    '''
    Process the tsv file as a DataFrame and return it as a JSON object

    Param
        filename, String, tsv file name.

    Returns
        data_frame_json, Dict, json dictionary with the tsv data.
    '''
    data_frame = get_data_frame_tsv(filename)
    data_frame_json = get_json_from_data_frame(data_frame)
    return data_frame_json


def to_camel_case(snake_str):
    '''
    Converts snake_case String into camelCase.
    Capitalize the first letter of each component except the first one with the 'title' method and join them together.

    Param
        snake_str, String, snake_case string.

    Returns
        camelStr, String, camelCase string.
    '''
    components = snake_str.split('_')
    camelStr = components[0] + ''.join(x.title() for x in components[1:])
    return camelStr


def get_pubmed_data(pmids, email):
    '''
    Connects to PUBMED database through Entrez API and gets the necessary publication data.
    The Entrez API returns a dictionary with the medline data, see also https://biopython.org/docs/1.75/api/Bio.Medline.html for more information about the keys obtained from this dictionary.

    Param
        pmid, Integer, PUBMED publication id.
        email, String, User email address to connect to PUBMED database.

    Returns
        publication, Dict, dictionary with the publication data.
    '''
    if not pmids:
        return None
    Entrez.email = email
    publications = []
    if isinstance(pmids, int) or isinstance(pmids, float):
        pmids = [pmids]
    elif isinstance(pmids, str):
        pmids = pmids.replace(' ', '')
        pmids = pmids.split(',')
    for pmid in pmids:
        handle = Entrez.efetch(db='pubmed', id=pmid,
                               rettype='medline', retmode='text')
        publication = {}
        record = Medline.read(handle)
        pubmed_authors = record.get('AU')
        if isinstance(pubmed_authors, str):
            pubmed_authors = pubmed_authors.split(',')
        publication.setdefault('authors', pubmed_authors)
        publication.setdefault('abstract', record.get('AB'))
        publication.setdefault('date', record.get('DP'))
        publication.setdefault('pmcid', record.get('PMC'))
        publication.setdefault('pmid', int(record.get('PMID')))
        publication.setdefault('title', record.get('TI'))
        article_identifier = record.get('AID')
        for identifier in article_identifier:
            if ' [doi]' in identifier:
                publication.setdefault('doi', identifier.replace(' [doi]', ''))
        publication = {k: v for k, v in publication.items() if v}
        publications.append(publication)
    return publications


def format_cross_reference_url(url, object_id):
    '''
    Corrects the External Cross References URL removing '~A' characters and adding object_id at the end.

    Param
        url, String, External Cross References raw URL.
        object_id, String, External Cross References Object ID.

    Returns
        formated_url, String, External Cross References final URL.
    '''
    formated_url = f'{url.replace("~A", "")}{object_id}'
    return formated_url


def get_object_tested(protein_names, database, url):
    '''
    Gets TF data from the RegulonDBMultigenomic database and returns the object tested dictionary.

    Param
        protein_name, String, TF protein name.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.

    Returns
        object_tested, Dict, dictionary with the object tested data.
    '''
    # TODO: check unique objects
    mg_api.connect(database, url)
    objects_tested = []
    if protein_names:
        for protein_name in protein_names:
            object_tested = {}
            mg_tf = mg_api.transcription_factors.find_by_name(protein_name)
            if mg_tf:
                active_conformations = []
                external_cross_references = []
                for active_conf in mg_tf[0].active_conformations:
                    active_conformations.append(active_conf.id)
                for cross_ref in mg_tf[0].external_cross_references:
                    mg_cross_ref = mg_api.external_cross_references.find_by_id(
                        cross_ref.external_cross_references_id)
                    external_cross_references.append(
                        {
                            'externalCrossReferenceId': cross_ref.external_cross_references_id,
                            'objectId': cross_ref.object_id,
                            'externalCrossReferenceName': mg_cross_ref.name,
                            'url': format_cross_reference_url(mg_cross_ref.url, cross_ref.object_id)
                        }
                    )
                genes = []
                for product_id in mg_tf[0].products_ids:
                    mg_product = mg_api.products.find_by_id(product_id)
                    mg_gene = mg_api.genes.find_by_id(mg_product.genes_id)
                    gene = {
                        '_id': mg_gene.id,
                        'name': mg_gene.name
                    }
                    genes.append(gene)

                object_tested = {
                    '_id': mg_tf[0].id,
                    'name': mg_tf[0].name,
                    'synonyms': mg_tf[0].synonyms,
                    'genes': genes,
                    'note': mg_tf[0].note,
                    'activeConformations': active_conformations,
                    'externalCrossReferences': external_cross_references
                }
                object_tested = {k: v for k, v in object_tested.items() if v}
                objects_tested.append(object_tested)
            else:
                object_tested = {
                    '_id': None,
                    'name': protein_name,
                    'synonyms': [],
                    'genes': [],
                    'note': None,
                    'activeConformations': [],
                    'externalCrossReferences': [],
                }
                object_tested = {k: v for k, v in object_tested.items() if v}
                objects_tested.append(object_tested)
    mg_api.disconnect()
    return objects_tested


def get_center_pos(left_pos, right_pos):
    '''
    Calculates the center center position of the chromosome.

    Param
        left_pos, String, Start position in the sequence (it's converted to Integer).
        right_pos, String, End position in the sequence (it's converted to Integer).

    Returns
        center_pos, Float, Center position in the sequence.
    '''
    center_pos = int(right_pos) - int(left_pos)
    center_pos = (center_pos / 2) + int(left_pos)
    return center_pos


def set_genome_intervals():
    '''
    Set the genes ranges to calculate the closest_genes.

    Param

    Returns
        genes_ranges, List, Array of coordinate pairs of the calculated ranges.
    '''
    genome_length = EC.GENOME_LENGTH
    intervals = EC.INTERVALS
    intervals_length = int(genome_length / intervals)
    genes_ranges = []
    for interval in range(intervals):
        genes_ranges.append(
            [intervals_length + ((interval - 1) * intervals_length), intervals_length + (interval * intervals_length)])
    return genes_ranges


def find_closest_gene(left_pos, right_pos, database, url, genes_ranges):
    '''
    Calculates the center center position of the chromosome.

    Param
        left_pos, String, Start position in the sequence (it's converted to Integer).
        right_pos, String, End position in the sequence (it's converted to Integer).
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
        genes_ranges, List, Array of coordinate pairs of the calculated ranges.

    Returns
        closest_genes, List, Dict List with the verified closest genes.
    '''
    minimum_distance = EC.MINIMUM_DISTANCE
    genome_length = EC.GENOME_LENGTH
    intervals = EC.INTERVALS

    chromosome_center_pos = get_center_pos(int(left_pos), int(right_pos))

    found_genes_interval = genes_ranges[int(
        (chromosome_center_pos * intervals) / genome_length)]

    mg_api.connect(database, url)

    mg_genes = mg_api.genes.get_closest_genes_to_central_position(
        (found_genes_interval[0] - minimum_distance), (found_genes_interval[1] + minimum_distance), chromosome_center_pos, minimum_distance)
    closest_genes = []
    for gene in mg_genes:
        gene_strand = gene.strand
        gene_left_pos = gene.left_end_position
        gene_right_pos = gene.right_end_position
        gene_product_name = []
        tus_dict_list = []
        try:
            mg_tus = mg_api.transcription_units.find_by_gene_id(gene.id)
            for mg_tu in mg_tus:
                tu_dict = {}
                tu_dict.setdefault('_id', mg_tu. id)
                tu_dict.setdefault('name', mg_tu.name)
                tus_dict_list.append(tu_dict)
        except Exception:
            logging.error(f'Can not find TU in Gene {gene.id}')
        try:
            mg_products = mg_api.products.find_by_gene_id(gene.id)
            for product in mg_products:
                gene_product_name.append(product.name)
        except Exception:
            logging.error(f'Can not find Product Name in Gene {gene.id}')
        if gene_strand == 'forward':
            distance = float(gene_left_pos) - chromosome_center_pos
            closest_genes.append(
                {'_id': gene.id, 'name': gene.name, 'distanceTo': abs(distance), 'productName': gene_product_name, 'transcriptionUnits': tus_dict_list})
        elif gene_strand == 'reverse':
            distance = chromosome_center_pos - float(gene_right_pos)
            closest_genes.append(
                {'_id': gene.id, 'name': gene.name, 'distanceTo': abs(distance), 'productName': gene_product_name, 'transcriptionUnits': tus_dict_list})
    mg_api.disconnect()
    return closest_genes


def find_terminators(left_pos, right_pos, tts_id, database, url):
    '''
    Calculates the center center position of the chromosome.

    Param
        left_pos, String, Start position in the sequence (it's converted to Integer).
        right_pos, String, End position in the sequence (it's converted to Integer).
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
        genes_ranges, List, Array of coordinate pairs of the calculated ranges.

    Returns
        closest_genes, List, Dict List with the verified closest genes.
    '''
    mg_api.connect(database, url)

    terminators = []
    try:
        mg_terminators = mg_api.terminators.get_closer_terminators(
            (left_pos - 30), (right_pos + 30))
        for terminator in mg_terminators:
            terminator_dict = {}
            terminator_dict.setdefault('_id', terminator.id)
            terminator_dict.setdefault('name', terminator.name)
            mg_tus = mg_api.transcription_units.find_by_terminator_id(
                terminator.id)
            tus_dict_list = []
            if mg_tus:
                for tu in mg_tus:
                    tu_dict = {}
                    tu_dict.setdefault('_id', tu.id)
                    tu_dict.setdefault('name', tu.name)
                    mg_promoter = mg_api.promoters.find_by_id(tu.promoters_id)
                    promoter = {}
                    promoter.setdefault('_id', mg_promoter.id)
                    promoter.setdefault('name', mg_promoter.name)
                    promoter.setdefault('sequence', mg_promoter.sequence)
                    promoter.setdefault('leftEndPosition',
                                        mg_promoter.left_end_position)
                    promoter.setdefault('rightEndPosition',
                                        mg_promoter.right_end_position)
                    promoter.setdefault('strand', mg_promoter.strand)

                    tu_dict.setdefault('promoter', promoter)
                    tus_dict_list.append(tu_dict)

            terminator_dict.setdefault('transcriptionUnits', tus_dict_list)

            terminators.append(terminator_dict)
    except Exception:
        logging.error(f'Can not find Terminator Name in Gene {tts_id}')
    mg_api.disconnect()
    return terminators


def get_sites_ids_by_tf(tf_names, database, url):
    '''
    Uses MG API to get the sites IDs by TF name.

    Param
        tf_names, List, TF names list.
        database, String, RegulonDB Multigenomic database name
        url, String, URL to RegulonDB Multigenomic database.

    Returns
        sites_ids, List, List of sites IDs.
    '''
    sites_ids = []
    mg_api.connect(database, url)
    for tf_name in tf_names:
        try:
            mg_tf = mg_api.transcription_factors.find_by_name(tf_name)
            tf_id = mg_tf[0].id
            try:
                mg_sites = mg_api.regulatory_sites.get_tf_binding_sites(tf_id)
                for site in mg_sites:
                    sites_ids.append(site.id)
            except Exception:
                logging.error(f'Can not find Sites in TF {tf_id}')
        except IndexError:
            logging.error(f'Can not find Trasncription Factor {tf_name}')
    mg_api.disconnect()
    return sites_ids


def get_tf_sites_abs_pos(tf_id, database, url):
    '''
    Gets Regualtory Sites objects with absolutePosition.

    Param
        tf_id, String, TF ID.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.

    Returns
        site, Object, Site object with absolutePosition property.
    '''
    site = None
    mg_api.connect(database, url)
    try:
        mg_site = mg_api.regulatory_sites.find_by_id(tf_id)
        site = {
            '_id': tf_id,
            'absolutePosition': mg_site.absolute_position,
            'siteObject': mg_site
        }
    except Exception:
        logging.error(f'Can not find Sites in TF {tf_id}')
    mg_api.disconnect()
    return site


def get_citations(database, url, citations_obj_list):
    '''
    Uses Multigenomic API to get the formatted Citations list.

    Param
        citations_obj_list, List, Citations Object List.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.

    Returns
        citations, List, formatted Citations list.
    '''
    citations = []
    citation = {}
    mg_api.connect(database, url)
    for citation_obj in citations_obj_list:
        evidence_id = citation_obj.evidences_id
        publication_id = citation_obj.publications_id
        evidence = {}
        publication = {}
        try:
            mg_evidence = mg_api.evidences.find_by_id(evidence_id)
            evidence.setdefault('id', mg_evidence.id)
            evidence.setdefault('name', mg_evidence.name)
            evidence.setdefault('code', mg_evidence.code)
            evidence.setdefault('type', mg_evidence.type)
        except Exception:
            logging.error(f'Can not find Evidence {evidence_id}')
        try:
            mg_publication = mg_api.publications.find_by_id(publication_id)
            publication.setdefault('id', mg_publication.id)
            publication.setdefault('authors', mg_publication.authors)
            publication.setdefault('citation', mg_publication.citation)
            publication.setdefault('pmid', mg_publication.pmid)
            publication.setdefault('title', mg_publication.title)
            publication.setdefault('url', mg_publication.url)
            publication.setdefault('year', mg_publication.year)
        except Exception:
            logging.error(f'Can not find Publication {publication_id}')
        citation = {
            'evidence': evidence,
            'publication': publication
        }
        citations.append(citation)
    mg_api.disconnect()
    return citations


def get_tss_distance(database, url, regulated_entity, strand, rend, lend):
    '''
    Calculates the distance between the given Regualtory Interaction and the closest Trasncription Start Site.

    Param
        regulated_entity, Object, Regualtory Interaction regulated entity object.
        strand, String, Regualtory Site strand forward or reverse ('-', '+').
        lend, String, Start position in the sequence.
        rend, String, End position in the sequence.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.

    Returns
        distance, Integer, Distance between the given Regualtory Interaction and the closest Trasncription Start Site.
    '''
    mg_api.connect(database, url)
    distance = None
    reg_entity_type = regulated_entity.type
    reg_entity_id = regulated_entity.id
    if reg_entity_type == 'gene':
        try:
            mg_tu = mg_api.transcription_units.find_by_gene_id(reg_entity_id)
            promoter_id = mg_tu[0].promoters_id
            mg_promoter = mg_api.promoters.find_by_id(promoter_id)
            tss = mg_promoter.transcription_start_site
            tss_rend = tss.right_end_position
            tss_lend = tss.left_end_position
            if strand == '-':
                distance = lend - tss_rend
            if strand == '+':
                distance = rend - tss_lend
        except Exception:
            logging.error(
                f'Can not find TU from {reg_entity_id}')
    if reg_entity_type == 'transcriptionUnit':
        try:
            mg_tu = mg_api.transcription_units.find_by_id(reg_entity_id)
            promoter_id = mg_tu.promoters_id
            mg_promoter = mg_api.promoters.find_by_id(promoter_id)
            tss = mg_promoter.transcription_start_site
            tss_rend = tss.right_end_position
            tss_lend = tss.left_end_position
            if strand == '-':
                distance = lend - tss_rend
            if strand == '+':
                distance = rend - tss_lend
        except Exception:
            logging.error(
                f'Can not find TU from {reg_entity_id}')
    if reg_entity_type == 'promoter':
        try:
            mg_promoter = mg_api.promoters.find_by_id(reg_entity_id)
            tss = mg_promoter.transcription_start_site
            tss_rend = tss.right_end_position
            tss_lend = tss.left_end_position
            if strand == '-':
                distance = lend - tss_rend
            if strand == '+':
                distance = rend - tss_lend
        except Exception:
            logging.error(
                f'Can not find Promoter from {reg_entity_id}')
    if distance:
        distance = abs(distance)
    return distance


def get_gene_distance(database, url, regulated_entity, strand, rend, lend):
    '''
    Calculates the distance between the given Regualtory Interaction and the closest Gene.

    Param
        regulated_entity, Object, Regualtory Interaction regulated entity object.
        strand, String, Regualtory Site strand forward or reverse ('-', '+').
        lend, String, Start position in the sequence.
        rend, String, End position in the sequence.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.

    Returns
        distance, Integer, Distance between the given Regualtory Interaction and the closest Gene.
    '''
    mg_api.connect(database, url)
    distance = None
    reg_entity_type = regulated_entity.type
    reg_entity_id = regulated_entity.id
    if reg_entity_type == 'gene':
        try:
            mg_gene = mg_api.genes.find_by_id(reg_entity_id)
            gene_rend = mg_gene.right_end_position
            gene_lend = mg_gene.left_end_position
            if strand == '-':
                distance = lend - gene_rend
            if strand == '+':
                distance = rend - gene_lend
        except Exception:
            logging.error(
                f'Can not find TU from {reg_entity_id}')
    if reg_entity_type == 'transcriptionUnit':
        try:
            mg_tu = mg_api.transcription_units.find_by_id(reg_entity_id)
            genes_ids = mg_tu.genes_ids
            temp_gene_distances = []
            for gene_id in genes_ids:
                mg_gene = mg_api.genes.find_by_id(gene_id)
                gene_rend = mg_gene.right_end_position
                gene_lend = mg_gene.left_end_position
                if strand == '-':
                    temp_gene_distances.append(abs(lend - gene_rend))
                if strand == '+':
                    temp_gene_distances.append(abs(rend - gene_lend))
            temp_gene_distances.sort()
            distance = temp_gene_distances[0]
        except Exception:
            logging.error(
                f'Can not find TU from {reg_entity_id}')
    if reg_entity_type == 'promoter':
        try:
            mg_tu = mg_api.transcription_units.find_by_promoter_id(
                reg_entity_id)
            genes_ids = mg_tu[0].genes_ids
            temp_gene_distances = []
            for gene_id in genes_ids:
                mg_gene = mg_api.genes.find_by_id(gene_id)
                gene_rend = mg_gene.right_end_position
                gene_lend = mg_gene.left_end_position
                if strand == '-':
                    temp_gene_distances.append(abs(lend - gene_rend))
                if strand == '+':
                    temp_gene_distances.append(abs(rend - gene_lend))
            temp_gene_distances.sort()
            distance = temp_gene_distances[0]
        except Exception:
            logging.error(
                f'Can not find TU from {reg_entity_id}')
    if distance:
        distance = abs(distance)
    return distance


def get_classic_ris(lend, rend, strand, tf_sites, database, url, origin):
    '''
    Gets Regualtory Interactions on RegulonDB Multigenomic database.

    Param
        lend, Float, RI's leftEndPosition.
        rend, Float, RI's rigthEndPosition.
        strand, Float, RI's strand.
        tf_sites, List, Sites in the dataset.

    Returns
        classic_ris, List, RIs found on RegulonDB List.
    '''
    center_pos = get_center_pos(lend, rend)
    classic_ris = []
    for site in tf_sites:
        tf_center = site.get('absolutePosition', None)
        site_object = site.get('siteObject', None)
        if tf_center and site_object:
            if tf_center == center_pos or tf_center == (center_pos + EC.PAIR_OF_BASES) or tf_center == (center_pos - EC.PAIR_OF_BASES):
                classic_ri = {}
                ri_regulated_entity = {}
                mg_api.connect(database, url)
                try:
                    mg_ri = mg_api.regulatory_interactions.find_by_reg_site(
                        site_object.id)
                    classic_ri.setdefault('_id', mg_ri[0].id)
                    ri_regulated_entity = mg_ri[0].regulated_entity
                except Exception:
                    logging.error(
                        f'Can not find RI from Site {site_object.id}')
                relative_tss_distance = get_tss_distance(
                    database, url, ri_regulated_entity, strand, site_object.right_end_position, site_object.left_end_position)
                classic_ri.setdefault(
                    'relativeTSSDistance', relative_tss_distance)
                relative_gene_distance = get_gene_distance(
                    database, url, ri_regulated_entity, strand, site_object.right_end_position, site_object.left_end_position)
                classic_ri.setdefault(
                    'relativeGeneDistance', relative_gene_distance)
                classic_ri.setdefault('tfbsLeftPosition',
                                      site_object.left_end_position)
                classic_ri.setdefault('tfbsRightPosition',
                                      site_object.right_end_position)
                classic_ri.setdefault('strand', strand)
                classic_ri.setdefault('sequence',
                                      site_object.sequence)
                citations = get_citations(database, url, site_object.citations)
                classic_ri.setdefault('citations', citations)
                classic_ri.setdefault('origin', origin)
                classic_ris.append(classic_ri)
    return classic_ris


def get_tu_by_gene_id(gene_id, database, url):
    '''
    Gets TU in the RegulonDB Multigenomic database by Gene ID.

    Param
        gene_id, String, Gene ID.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
    Returns
        tu, Object, Trasncription Unit object from RegulonDB Multigenomic database.
    '''
    tu = None
    mg_api.connect(database, url)
    try:
        tu = mg_api.transcription_units.find_by_gene_id(
            gene_id)
    except IndexError:
        # logging.error(f'Can not find TU from: {gene_id}')
        pass
    mg_api.disconnect()
    return tu


def get_promoter(lend, rend, database, url):
    '''
    Gets Closer Promoter in the RegulonDB Multigenomic database by left_end_position and right_end_position.

    Param
        lend, Float, dataset leftEndPosition.
        rend, Float, dataset rigthEndPosition.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
    Returns
        promoters, List, Closer Promoters to dataset in RegulonDB Multigenomic database.
    '''
    promoters = []
    mg_api.connect(database, url)
    try:
        promoters_objects = mg_api.promoters.get_closer_promoters(
            (lend - 5), (rend + 5))
        for promoter_obj in promoters_objects:
            binds_sigma_factor = promoter_obj.binds_sigma_factor
            sigma_factor_name = None
            if binds_sigma_factor:
                sigma_factor_id = binds_sigma_factor.sigma_factors_id
                sigma_factor = mg_api.sigma_factors.find_by_id(sigma_factor_id)
                if sigma_factor:
                    sigma_factor_name = sigma_factor.name
            promoter = {
                '_id': promoter_obj.id,
                'name': promoter_obj.name,
                'strand': promoter_obj.strand,
                'pos+1': promoter_obj.pos1,
                'sigma': sigma_factor_name,
                'confidenceLevel': promoter_obj.confidence_level,
            }
            promoters.append(promoter)
    except IndexError:
        logging.error(f'Can not find Promoter from: {lend}, {rend}')
    mg_api.disconnect()
    return promoters


def get_genes_by_bnumber(bnumbers, database, url):
    '''
    Gets Genes in the RegulonDB Multigenomic database by Gene BNumber.

    Param
        bnumbers, List, Bnumbers String Array.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
    Returns
        genes, List, Genes List from RegulonDB Multigenomic database.
    '''
    genes = []
    mg_genes = []
    mg_api.connect(database, url)
    try:
        for bnumber in bnumbers:
            mg_genes.append(mg_api.genes.find_by_bnumber(bnumber)[0])
        for gene in mg_genes:
            gene_dict = {}
            gene_dict.setdefault('_id', gene.id)
            gene_dict.setdefault('name', gene.name)
            gene_dict.setdefault('bnumber', gene.bnumber)
            genes.append(gene_dict)

    except IndexError:
        logging.error(f'Can not find Gene bnumbers: {bnumbers}')
    mg_api.disconnect()
    return genes


def get_gene_by_bnumber(bnumber, database, url):
    '''
    Gets Gene in the RegulonDB Multigenomic database associated to a Gene BNumber.

    Param
        bnumber, List, Bnumbers String Array.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
    Returns
        gene, Dict, Gene object from RegulonDB Multigenomic database.
    '''
    gene_dict = {}
    mg_api.connect(database, url)
    try:
        gene = mg_api.genes.find_by_bnumber(bnumber)[0]
        gene_dict.setdefault('_id', gene.id)
        gene_dict.setdefault('name', gene.name)
        gene_dict.setdefault('bnumber', gene.bnumber)
        gene_dict.setdefault('synonyms', gene.synonyms)
        gene_dict.setdefault('leftEndPosition', gene.left_end_position)
        gene_dict.setdefault("rightEndPosition", gene.right_end_position)

    except IndexError:
        logging.error(f'Can not find Gene bnumbers: {bnumber}')
    mg_api.disconnect()
    return gene_dict


def find_one_in_dict_list(dict_list, key_name, value):
    '''
    Finds dictionary in a dictionary List by certain key.

    Param
        dict_list, List, Dictionaries List.
        key_name, String, Key Name to search.
        value, String, Value to find the dictionary by key name.
    Returns
        found_dict, Dict, Dictionary that matches the search.
    '''
    found_dict = next(
        (item for item in dict_list if item[key_name] == value),
        None
    )
    return found_dict


def verify_json_path(json_path):
    '''
    This function reads JSON file in the path and returns an valid dir for use

    Param
        json_path, String, raw directory path.

    Returns
        txt_path, String, verified directory path.
    '''

    if os.path.isfile(json_path) and json_path.endswith('.json'):
        logging.info(
            f'Reading JSON file {json_path}')
        return json_path
    else:
        logging.warning(
            f'{json_path} is not a valid JSON file will be ignored')
        return None


def read_json_from_path(json_path):
    '''
    Opens a JSON file and returns JSON object.

    Param
        json_path, String, path to JSON.
    Returns
        Loaded JSON Object.
    '''
    json_file = open(json_path)
    return json.load(json_file)


def get_external_reference(external_ref):
    '''
    [Description]

    Param
        [Description]

    Returns
        [Description]
    '''
    external_references_list = []
    external_references = [external_ref]
    for external_reference in external_references:
        reference_name = external_reference.split(':')[0]
        reference_url = re.search(
            "(?P<url>https?://[^\s]+)", external_reference).group("url")
        external_reference_dict = {
            'name': reference_name,
            'url': reference_url,
            'description': '',
            'internalComment': '',
            'note': '',
        }
        external_references_list.append(external_reference_dict)

    return external_references_list
