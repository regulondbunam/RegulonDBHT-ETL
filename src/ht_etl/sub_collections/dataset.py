"""
Dataset object.
Build dataset object and special objects for every dataset.
"""
# standard
import logging

# third party

# local
from src.libs import utils
from src.ht_etl.domain.publications import Publications
from src.ht_etl.domain.object_tested import ObjectTested
from src.ht_etl.domain.source_serie import SourceSerie
from src.ht_etl.domain.sample import Sample
from src.ht_etl.domain.linked_dataset import LinkedDataset
from src.ht_etl.domain.release_data_control import ReleaseControl
from src.ht_etl.domain.collection_data import CollectionData
from src.ht_etl.domain.external_references import ExternalReference
from src.ht_etl.domain.authors_data import AuthorsData
from src.ht_etl.domain.uniform_data import UniformizedData


class Dataset(object):
    def __init__(self, **kwargs):
        # Params
        self.bnumbers = kwargs.get("bnumbers", None)
        self.mg_api = kwargs.get('mg_api')
        self.genes_ranges = kwargs.get("genes_ranges", None)
        self.collection_path = kwargs.get('collection_path', None)
        self.collection_source = kwargs.get('collection_source', None)
        self.collection_name = kwargs.get('collection_name', None)
        self.version = kwargs.get('version', None)
        self.dataset_type = kwargs.get('dataset_type', None)
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)
        self.email = kwargs.get("email", None)
        self.dataset_id = kwargs.get('dataset_id', None)
        self.old_dataset_id = kwargs.get('old_dataset_id', None)
        self.pmid = kwargs.get('pmid', None)
        self.authors = kwargs.get('authors', None)
        self.regulondb_tf_name = kwargs.get('regulondb_tf_name', None)
        self.source_tf_name = kwargs.get('source_tf_name', None)
        self.source_database = kwargs.get('source_database', None)
        self.serie_id = kwargs.get('serie_id', None)
        self.experiment_title = kwargs.get('experiment_title', None)
        self.platform_id = kwargs.get('platform_id', None)
        self.platform_title = kwargs.get('platform_title', None)
        self.strategy = kwargs.get('strategy', None)
        self.library_layout = kwargs.get('library_layout', None)
        self.method_name = kwargs.get('method_name', None)
        self.samples_replicates_exp_ids = kwargs.get('samples_replicates_exp_ids', None)
        self.samples_replicates_control_ids = kwargs.get('samples_replicates_control_ids', None)
        self.title_for_all_replicates = kwargs.get('title_for_all_replicates', None)
        self.exp_condition = kwargs.get('exp_condition', None)
        self.growth_conditions_experimental = kwargs.get('growth_conditions_experimental', None)
        self.organism = kwargs.get('organism', None)
        self.src_reference_genome = kwargs.get('src_reference_genome', None)
        self.ref_genome = kwargs.get('ref_genome', None)
        self.assembly_genome_id = kwargs.get('assembly_genome_id', None)
        self.five_prime_enrichment=kwargs.get('five_prime_enrichment', None)
        self.reference_name = kwargs.get('reference_name', None)
        self.dataset_file_name = kwargs.get('dataset_file_name', None)
        self.internal_curation_notes = kwargs.get('internal_curation_notes', None)
        self.curator = kwargs.get('curator', None)
        self.samples_exp_replicates_expression_ids = kwargs.get('samples_exp_replicates_expression_ids', None)
        self.samples_ctrl_replicates_expression_ids = kwargs.get('samples_ctrl_replicates_expression_ids', None)
        self.expression_growcon_ctrl = kwargs.get('expression_growcon_ctrl', None)
        self.expression_growcon_experimental = kwargs.get('expression_growcon_experimental', None)
        self.source_cut_off = kwargs.get('source_cut_off', None)
        self.public_notes = kwargs.get('public_notes', None)
        self.external_db_links = kwargs.get('external_db_links', None)

        # Local properties

        # Object properties
        self.dataset_publications = kwargs.get('dataset_publications', None)
        self.objects_tested = kwargs.get('objects_tested', None)
        self.source_serie = kwargs.get('source_serie', None)
        self.sample = kwargs.get('sample', None)
        self.linked_dataset = kwargs.get('linked_dataset', None)
        self.release_data_control = kwargs.get('release_data_control', None)
        self.collection_data = kwargs.get('collection_data', None)
        self.temporal_id = Dataset.set_temp_id(
            self.dataset_type,
            self.collection_name,
            self.dataset_id
        )
        self.external_references = kwargs.get('external_references', None)
        self.growth_conditions = kwargs.get('growth_conditions', None)
        self.summary = kwargs.get('summary', None)

        # Uniformized data
        self.authors_data = kwargs.get('authors_data', None)
        self.uniformized_data = kwargs.get('uniformized_data', None)

    # Local properties
    @property
    def authors_data(self):
        return self._authors_data

    @authors_data.setter
    def authors_data(self, authors_data=None):
        self._authors_data = authors_data
        if self._authors_data is None:
            authors_data = AuthorsData(
                authors_data_path=self.collection_path,
                file_name=self.dataset_file_name,
                dataset_id=self.dataset_id
            )
            self._authors_data = authors_data

    @property
    def uniformized_data(self):
        return self._uniformized_data

    @uniformized_data.setter
    def uniformized_data(self, uniformized_data=None):
        self._uniformized_data = uniformized_data
        if self._uniformized_data is None:
            uniformized_data = UniformizedData(
                tf_name=self.regulondb_tf_name,
                bnumbers=self.bnumbers,
                dataset_id=self.dataset_id,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                collection_path=self.collection_path,
                serie_id=self.serie_id,
                type=self.dataset_type,
                genes_ranges=self.genes_ranges,
                old_dataset_id=self.old_dataset_id,
                database=self.database,
                url=self.url
            )
            self._uniformized_data = uniformized_data

    # Object properties

    @property
    def dataset_publications(self):
        return self._dataset_publications

    @dataset_publications.setter
    def dataset_publications(self, dataset_publications=None):
        """
        Sets dataset publications
        """
        self._dataset_publications = dataset_publications
        if dataset_publications is None:
            dataset_publications = Publications(
                dataset_id=self.dataset_id,
                pmid=self.pmid,
                email=self.email
            )
            self._dataset_publications = dataset_publications.publications_list

    @property
    def objects_tested(self):
        return self._objects_tested

    @objects_tested.setter
    def objects_tested(self, objects_tested=None):
        """
        Sets objects tested
        """
        self._objects_tested = objects_tested
        if objects_tested is None:
            objects_tested = ObjectTested(
                mg_api=self.mg_api,
                regulondb_tf_name=self.regulondb_tf_name,
                source_tf_name=self.source_tf_name,
                database=self.database,
                url=self.url
            )
            self._objects_tested = objects_tested.objects_tested

    @property
    def source_serie(self):
        return self._source_serie

    @source_serie.setter
    def source_serie(self, source_serie=None):
        """
        Sets source serie
        """
        self._source_serie = source_serie
        if source_serie is None:
            source_serie = SourceSerie(
                serie_id=self.serie_id,
                source_name=self.source_database,
                platform_id=self.platform_id,
                platform_title=self.platform_title,
                title=self.experiment_title,
                strategy=self.strategy,
                method=self.method_name,
                read_type=None,  # TODO: Ask for this property
                source_db=self.source_database
            )
            source_serie_dict = {
                'series': source_serie.source_series,
                'platform': source_serie.platform,
                'title': source_serie.title,
                'strategy': source_serie.strategy,
                'method': source_serie.method,
                'readType': source_serie.read_type,
                'sourceDB': source_serie.source_db
            }
            source_serie_dict = {k: v for k, v in source_serie_dict.items() if v}
            self._source_serie = source_serie_dict

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, sample=None):
        """
        Sets sample.
        """
        self._sample = sample
        if sample is None:
            sample = Sample(
                sample_replicate_exp=self.samples_replicates_exp_ids,
                sample_replicate_ctrl=self.samples_replicates_control_ids,
                title_for_replicates=self.title_for_all_replicates
            )
            sample_dict = {
                'controlId': sample.control_id,
                'experimentId': sample.experiment_id,
                'title': sample.title_for_replicates,
                'ssrId': ''  # TODO: ask for this property
            }
            sample_dict = {k: v for k, v in sample_dict.items() if v}
            self._sample = sample_dict

    @property
    def linked_dataset(self):
        return self._linked_dataset

    @linked_dataset.setter
    def linked_dataset(self, linked_dataset=None):
        """
        Sets linked dataset.
        """
        self._linked_dataset = linked_dataset
        if linked_dataset is None:
            linked_dataset = LinkedDataset(
                sample_exp_replicate_exp=self.samples_replicates_exp_ids,
                sample_exp_replicate_ctrl=self.samples_replicates_control_ids,
                dataset_type=self.dataset_type
            )
            linked_dataset_dict = {
                'controlId': linked_dataset.control_id,
                'experimentId': linked_dataset.experiment_id,
                'datasetType': linked_dataset.dataset_type,
            }
            linked_dataset_dict = {k: v for k, v in linked_dataset_dict.items() if v}
            self._linked_dataset = linked_dataset_dict

    @property
    def release_data_control(self):
        return self._release_data_control

    @release_data_control.setter
    def release_data_control(self, release_data_control=None):
        """
        Sets release data control.
        """
        self._release_data_control = release_data_control
        if release_data_control is None:
            release_data_control = ReleaseControl(
                version=self.version
            )
            release_data_control_dict = {
                'date': release_data_control.release_date,
                'version': release_data_control.version
            }
            self._release_data_control = release_data_control_dict

    @property
    def collection_data(self):
        return self._collection_data

    @collection_data.setter
    def collection_data(self, collection_data=None):
        """
        Sets collection data.
        """
        self._collection_data = collection_data
        if collection_data is None:
            collection_data = CollectionData(
                collection_source=self.collection_source,
                collection_name=self.dataset_type
            )
            collection_data_dict = {
                'type': collection_data.collection_name_upper,
                'source': collection_data.collection_source
            }
            collection_data_dict = {k: v for k, v in collection_data_dict.items() if v}
            self._collection_data = collection_data_dict

    @property
    def external_references(self):
        return self._external_references

    @external_references.setter
    def external_references(self, external_references=None):
        """
        Sets external references.
        """
        self._external_references = external_references
        if external_references is None:
            external_references = ExternalReference(
                urls=self.external_db_links,
            )
            self._external_references = external_references.external_references

    @property
    def growth_conditions(self):
        return self._growth_conditions

    @growth_conditions.setter
    def growth_conditions(self, growth_conditions=None):
        """
        Sets grow conditions contrast.
        """
        if growth_conditions is None:
            growth_conditions = Dataset.get_growth_conditions(self.growth_conditions_experimental)
            if type(growth_conditions) is not list:
                growth_conditions = [growth_conditions]
            if growth_conditions == [None]:
                growth_conditions = None
            self._growth_conditions = growth_conditions

    # Static methods
    @staticmethod
    def set_temp_id(dataset_type, collection_name, dataset_id):
        """
        Generates temporary dataset id.

        Args:
            dataset_type: String, dataset type.
            collection_name: String, collection name.
            dataset_id: String, source dataset id.

        Returns:
            temp_id: String, Temp dataset id.
        """
        temp_id = ''
        if collection_name is not None:
            collection_type = collection_name.replace('-', '_').upper()
            temp_id = f"{dataset_type}_{collection_type}_{dataset_id}"
        return temp_id

    @staticmethod
    def get_growth_conditions(gc_raw):
        """
        Converts the growth conditions sentences in a dictionary.
        Splits the phrase by | and separates the terms names from snake_case to camelCase in a dictionary format.

        ORGANISM -> organism
        GENETIC_BACKGROUND -> geneticBackground
        MEDIUM -> medium
        MEDIUM_SUPPLEMENTS -> mediumSupplements
        AERATION -> aeration
        TEMPERATURE -> temperature
        pH -> ph
        PRESSURE -> pressure
        OPTICAL_DENSITY -> opticalDensity
        GROWTH_PHASE -> growthPhase
        GROWTH_RATE -> growthRate
        VESSEL_TYPE -> vesselType
        AGITATION_SPEED -> aerationSpeed

        Args:
            gc_raw: String, growth conditions phrase.

        Returns:
            gc_dict: Dict, dictionary with the growth conditions terms.

        """
        gc_list = []
        if not gc_raw:
            return None
        gc_raw = gc_raw.replace(' |', '|')
        if '|' not in gc_raw:
            gc_list = [
                {
                    'otherTerms': gc_raw
                }
            ]
            return gc_list
        gc_raw_list = gc_raw.split('|;|')
        for gc_phrase in gc_raw_list:
            gc_terms = gc_phrase.split('|')
            gc_dict = {}
            for condition in gc_terms:
                if ':' in condition:
                    condition = condition.split(':')
                    gc_dict.setdefault(utils.to_camel_case(
                        condition[0].lower()), condition[1])
            if gc_dict:
                gc_dict = {k: v for k, v in gc_dict.items() if v}
            gc_list.append(gc_dict)
        return gc_list
