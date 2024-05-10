"""
Some functions that help to HT process.
"""
# standard
import logging

# third party

# local
from src.libs import constants


def format_cross_reference_url(url, object_id):
    """
    Corrects the External Cross References URL removing '~A' characters and adding object_id at the end.

    Args:
        url: String, External Cross References raw URL.
        object_id: String, External Cross References Object ID.

    Returns:
        formated_url: String, External Cross References final URL.
    """
    formated_url = f'{url.replace("~A", "")}{object_id}'
    return formated_url


def get_center_pos(left_pos, right_pos):
    """
    Calculates the center position of the chromosome.

    Args:
        left_pos: Integer, Start position in the sequence (it's converted to Integer).
        right_pos: Integer, End position in the sequence (it's converted to Integer).

    Returns:
        center_pos: Float, Center position in the sequence.
    """
    center_pos = int(right_pos) - int(left_pos)
    center_pos = (center_pos / 2) + int(left_pos)
    return center_pos


def set_genome_intervals():
    """
    Set the genes ranges to calculate the closest_genes.

    Returns:
        genes_ranges - List, Array of coordinate pairs of the calculated ranges.
    """
    genome_length = constants.GENOME_LENGTH
    intervals = constants.INTERVALS
    intervals_length = int(genome_length / intervals)
    genes_ranges = []
    for interval in range(intervals):
        genes_ranges.append(
            [intervals_length + ((interval - 1) * intervals_length), intervals_length + (interval * intervals_length)])
    return genes_ranges


def find_closest_gene(left_pos, right_pos, genes_ranges, mg_api):
    """
    Calculates the center position of the chromosome.

    Args:
        left_pos: String, Start position in the sequence (it's converted to Integer).
        right_pos: String, End position in the sequence (it's converted to Integer).
        genes_ranges: List, Array of coordinate pairs of the calculated ranges.
        mg_api: API, Multigenomic database connection.

    Returns:
        closest_genes: List, Dict List with the verified closest genes.
    """
    minimum_distance = constants.MINIMUM_DISTANCE
    genome_length = constants.GENOME_LENGTH
    intervals = constants.INTERVALS

    chromosome_center_pos = get_center_pos(int(left_pos), int(right_pos))

    found_genes_interval = genes_ranges[int(
        (chromosome_center_pos * intervals) / genome_length)]

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
                {
                    '_id': gene.id,
                    'name': gene.name,
                    'distanceTo': abs(distance),
                    'productName': gene_product_name,
                    'transcriptionUnits': tus_dict_list
                }
            )
        elif gene_strand == 'reverse':
            distance = chromosome_center_pos - float(gene_right_pos)
            closest_genes.append(
                {
                    '_id': gene.id,
                    'name': gene.name,
                    'distanceTo': abs(distance),
                    'productName': gene_product_name,
                    'transcriptionUnits': tus_dict_list
                }
            )

    return closest_genes


def find_terminators(left_pos, right_pos, tts_id, mg_api):
    """
    Calculates the center position of the chromosome.

    Args:
        left_pos: String, Start position in the sequence (it's converted to Integer).
        right_pos: String, End position in the sequence (it's converted to Integer).
        mg_api: API, Multigenomic database connection.
        tts_id: String, TTS-ID.

    Returns:
        closest_genes: List, Dict List with the verified closest genes.
    """
    terminators = []
    try:
        mg_terminators = mg_api.terminators.get_closer_terminators(
            (left_pos - 30), (right_pos + 30))
        for terminator in mg_terminators:
            terminator_dict = {}
            terminator_dict.setdefault('_id', terminator.id)
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
                                        mg_promoter.transcription_start_site.left_end_position)
                    promoter.setdefault('rightEndPosition',
                                        mg_promoter.transcription_start_site.right_end_position)
                    promoter.setdefault('strand', mg_promoter.strand)

                    tu_dict.setdefault('promoter', promoter)
                    tus_dict_list.append(tu_dict)

            terminator_dict.setdefault('transcriptionUnits', tus_dict_list)

            terminators.append(terminator_dict)
    except Exception:
        logging.error(f'Can not find Terminator Name in Gene {tts_id}')
    return terminators


def get_tf_sites(tf_name, mg_api):
    """
    Uses MG API to get the sites IDs by TF name.

    Args:
        tf_name: String, TF name.
        mg_api: API, Multigenomic database connection.

    Returns:
        tf_id: String, TF IDs.
    """
    mg_sites = []
    try:
        mg_tf = mg_api.transcription_factors.find_by_abb_name(tf_name)
        if mg_tf is None:
            return mg_sites
        tf_id = mg_tf.id
        try:
            mg_sites = mg_api.regulatory_sites.get_tf_binding_sites(tf_id)
        except Exception:
            logging.error(f'Can not find Sites from  TF {tf_id}')
    except IndexError:
        logging.error(f'Can not find Transcription Factor {tf_name}')
    return mg_sites


def get_tf_sites_abs_pos(tf_id, mg_api):
    """
    Gets Regulatory Sites objects with absolutePosition.

    Args:
        tf_id: String, TF ID.
        mg_api: API, Multigenomic database connection.

    Returns
        site: Object, Site object with absolutePosition property.
    """
    site = None
    try:
        mg_site = mg_api.regulatory_sites.find_by_id(tf_id)
        site = {
            '_id': tf_id,
            'absolutePosition': mg_site.absolute_position,
            'siteObject': mg_site
        }
    except Exception:
        logging.error(f'Can not find Sites in TF {tf_id}')
    return site


def get_tss_distance(mg_api, regulated_entity, strand, rend, lend):
    """
    Calculates the distance between the given Regulatory Interaction and the closest Transcription Start Site.

    Args:
        regulated_entity: Object, Regulatory Interaction regulated entity object.
        strand: String, Regulatory Site strand forward or reverse ('-', '+').
        lend: String, Start position in the sequence.
        rend: String, End position in the sequence.
        mg_api: API, Multigenomic database connection.

    Returns
        distance, Integer, Distance between the given Regulatory Interaction and the closest Transcription Start Site.
    """
    if regulated_entity is None:
        return None
    if isinstance(lend, str):
        lend = int(lend)
    if isinstance(rend, str):
        rend = int(lend)

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


def get_gene_distance(mg_api, regulated_entity, strand, rend, lend):
    """
    Calculates the distance between the given Regulatory Interaction and the closest Gene.

    Args:
        regulated_entity: Object, Regulatory Interaction regulated entity object.
        strand: String, Regulatory Site strand forward or reverse ('-', '+').
        lend: String, Start position in the sequence.
        rend: String, End position in the sequence.
        mg_api: API, Multigenomic database connection.

    Returns:
        distance: Integer, Distance between the given Regulatory Interaction and the closest Gene.
    """
    if regulated_entity is None:
        return None
    if isinstance(lend, str):
        lend = int(lend)
    if isinstance(rend, str):
        rend = int(lend)
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


"""def find_one_in_dict_list(dict_list, key_name, value):
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
    return found_dict"""
