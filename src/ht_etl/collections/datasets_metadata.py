"""
Datasets metadata collection.
Build first level from HT Dataset Model.
"""
# standard
import logging

# third party

# local
from src.libs import constants
from src.ht_etl.sub_collections.dataset import Dataset
from src.ht_etl.sub_collections.metadata import Metadata


class DatasetsMetadata(object):
    def __init__(self, **kwargs):
        # Params
        self.mg_api = kwargs.get('mg_api')
        self.genes_ranges = kwargs.get("genes_ranges", None)
        self.dataset_type = kwargs.get('dataset_type', None)
        self.email = kwargs.get('email', None)
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)
        self.version = kwargs.get('version', None)
        self.src_collection_name = kwargs.get('src_collection_name', None)
        self.collection_source = kwargs.get('collection_source', None)
        self.collection_path = kwargs.get('collection_path', None)
        self.collection_status = kwargs.get('collection_status', None)
        self.dataset_source_dict = kwargs.get('dataset_source_dict', None)

        # Local properties
        self.authors_data = kwargs.get('authors_data', None)
        self.sites = kwargs.get('sites', None)
        self.peaks = kwargs.get('peaks', None)
        self.tus = kwargs.get('tu', None)
        self.tss = kwargs.get('tss', None)
        self.tts = kwargs.get('tts', None)

        # Object properties
        self.dataset = kwargs.get('dataset', None)
        self.collection_name = kwargs.get('collection_name', None)
        self.metadata = kwargs.get('metadata', None)

    # Local properties

    # Object properties
    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset=None):
        """
        Gets all values from dataset catalog dict and build a Dataset object.
        """
        if dataset is None:
            if self.dataset_source_dict.get(constants.DATASET_ID, None) is not None:
                print(f"\tProcessing Dataset ID: {self.dataset_source_dict.get(constants.DATASET_ID, None)}")
                logging.info(f"Processing Dataset ID: {self.dataset_source_dict.get(constants.DATASET_ID, None)}")
                dataset = Dataset(
                    mg_api=self.mg_api,
                    genes_ranges=self.genes_ranges,
                    collection_path=self.collection_path,
                    collection_source=self.collection_source,
                    collection_name=self.src_collection_name,
                    version=self.version,
                    dataset_type=self.dataset_type,
                    database=self.database,
                    url=self.url,
                    email=self.email,
                    dataset_id=self.dataset_source_dict.get(constants.DATASET_ID, None),
                    old_dataset_id=self.dataset_source_dict.get(constants.OLD_DATASET_ID, None),
                    pmid=self.dataset_source_dict.get(constants.PMID, None),
                    authors=self.dataset_source_dict.get(constants.AUTHORS, None),
                    regulondb_tf_name=self.dataset_source_dict.get(constants.REGULONDB_TF_NAME, None),
                    source_tf_name=self.dataset_source_dict.get(constants.SOURCE_TF_NAME, None),
                    source_database=self.dataset_source_dict.get(constants.SOURCE_DATABASE, None),
                    serie_id=self.dataset_source_dict.get(constants.SERIE_ID, None),
                    experiment_title=self.dataset_source_dict.get(constants.EXPERIMENT_TITLE, None),
                    platform_id=self.dataset_source_dict.get(constants.PLATFORM_ID, None),
                    platform_title=self.dataset_source_dict.get(constants.PLATFORM_TITLE, None),
                    strategy=self.dataset_source_dict.get(constants.STRATEGY, None),
                    library_layout=self.dataset_source_dict.get(constants.LIBRARY_LAYOUT, None),
                    method_name=self.dataset_source_dict.get(constants.METHOD_NAME, None),
                    samples_replicates_exp_ids=self.dataset_source_dict.get(constants.SAMPLES_REPLICATES_EXPERIMET_ID, None),
                    samples_replicates_control_ids=self.dataset_source_dict.get(constants.SAMPLES_REPLICATES_CONTROL_ID, None),
                    title_for_all_replicates=self.dataset_source_dict.get(constants.TITLE_FOR_ALL_REPLICATES, None),
                    experiment_condition=self.dataset_source_dict.get(constants.EXPERIMENT_CONDITION, None),
                    grow_conditions_exp_ids=self.dataset_source_dict.get(constants.GC_EXPERIMENTAL, None),
                    organism=self.dataset_source_dict.get(constants.ORGANISM, None),
                    src_reference_genome=self.dataset_source_dict.get(constants.SOURCE_REFERENCE_GENOME, None),
                    ref_genome=self.dataset_source_dict.get(constants.REFERENCE_GENOME, None),
                    assembly_genome_id=self.dataset_source_dict.get(constants.ASSEMBLY_GENOME_ID, None),
                    five_prime_enrichment=self.dataset_source_dict.get(constants.FIVE_ENRICHMENT, None),
                    dataset_file_name=self.dataset_source_dict.get(constants.DATASET_FILE_NAME, None),
                    internal_curation_notes=self.dataset_source_dict.get(constants.INTERNAL_CURATION_NOTES, None),
                    curation_notes=self.dataset_source_dict.get(constants.CURATOR, None),
                    samples_exp_replicates_expression_ids=self.dataset_source_dict.get(
                        constants.SAMPLES_EXPERIMET_REPLICATES_EXPRESSION_ID, None
                    ),
                    samples_control_replicates_expression_ids=self.dataset_source_dict.get(
                        constants.SAMPLES_CONTROL_REPLICATES_EXPRESSION_ID, None
                    ),
                    expression_growcon_ctrl=self.dataset_source_dict.get(constants.EXPRESSION_GC_CONTROL, None),
                    expression_growcon_control_ids=self.dataset_source_dict.get(constants.EXPRESSION_GC_EXPERIMENTAL, None),
                    source_cut_off=self.dataset_source_dict.get(constants.CUT_OFF, None),
                    public_notes=self.dataset_source_dict.get(constants.PUBLIC_NOTES, None),
                    exp_condition_notes=self.dataset_source_dict.get(constants.EXPERIMENT_CONDITION, None),
                    external_db_links=self.dataset_source_dict.get(constants.EXTERNAL_DB_LINK, None)
                )
                dataset_dict = {
                    '_id': dataset.dataset_id,
                    'publications': dataset.dataset_publications,
                    'objectsTested': dataset.objects_tested,
                    'sourceSerie': dataset.source_serie,
                    'sample': dataset.sample,
                    'linkedDataset': dataset.linked_dataset,
                    'releaseDataControl': dataset.release_data_control,
                    'collectionData': dataset.collection_data,
                    'temporalId': dataset.temporal_id,
                    'referenceGenome': dataset.ref_genome,
                    'assemblyGenomeId': dataset.assembly_genome_id,
                    'fivePrimeEnrichment': dataset.five_prime_enrichment,
                    'experimentCondition': dataset.exp_condition,
                    'cutOff': dataset.source_cut_off,
                    'notes': dataset.public_notes,
                    'sourceReferenceGenome': dataset.src_reference_genome,
                    'externalReferences': dataset.external_references,
                    'growConditionsContrast': dataset.grow_conditions_contrast,
                    'geneExpressionFiltered': dataset.gene_expression_filtered,
                    'summary': dataset.summary,
                }
                self._dataset = dataset_dict
                self.authors_data = {
                    'id': dataset.authors_data.id,
                    'datasetIds': dataset.authors_data.dataset_ids,
                    'authorsData': dataset.authors_data.data,
                }
                if self.dataset_type == constants.TFBINDING:
                    self.sites = dataset.uniformized_data.sites.sites_list
            else:
                logging.warning(f"No Dataset ID provided for {self.dataset_source_dict.get(constants.PMID, None)}")

    @property
    def collection_name(self):
        return self._collection_name

    @collection_name.setter
    def collection_name(self, new_collection_name=None):
        self._collection_name = new_collection_name
        if new_collection_name is None:
            collection_name = self.src_collection_name
            collection_name = collection_name.replace('-', '_').upper()
            self._collection_name = collection_name

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata=None):
        if metadata is None:
            metadata = Metadata(
                dataset_type=self.dataset_type,
                readme_path=self.collection_path,
                collection_name=self.collection_name,
                collection_source=self.collection_source,
                collection_status=self.collection_status,
                pmid=self.dataset_source_dict.get(constants.PMID, None)
            )
            metadata_dict = {
                'dataset_type': metadata.dataset_type,
                'source': metadata.source,
                'metadata_content': metadata.metadata_content,
                'status': metadata.status,
                'release_date': metadata.release_date,
                'reference': metadata.pmids
            }
            self._metadata = metadata_dict
