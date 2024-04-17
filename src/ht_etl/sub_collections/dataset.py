"""
Dataset object.
Build dataset object and special objects for every dataset.
"""
# standard
import logging

# third party

# local
from src.ht_etl.domain.publications import Publications
from src.ht_etl.domain.object_tested import ObjectTested
from src.ht_etl.domain.source_serie import SourceSerie
from src.ht_etl.domain.sample import Sample
from src.ht_etl.domain.linked_dataset import LinkedDataset
from src.ht_etl.domain.release_data_control import ReleaseControl
from src.ht_etl.domain.collection_data import CollectionData
from src.ht_etl.domain.external_references import ExternalReference


class Dataset(object):
    def __init__(self, **kwargs):
        # Params
        self.collection_source = kwargs.get('collection_source', None)
        self.collection_name = kwargs.get('collection_name', None)
        self.version = kwargs.get('version', None)
        self.dataset_type = kwargs.get('dataset_type', None)
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)
        self.email = kwargs.get("email", None)
        self.dataset_id = kwargs.get('dataset_id', None)
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
        self.grow_conditions_experimental = kwargs.get('grow_conditions_experimental', None)
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
        self.grow_conditions_contrast = kwargs.get('grow_conditions_contrast', None)
        self.gene_expression_filtered = kwargs.get('gene_expression_filtered', None)
        self.summary = kwargs.get('summary', None)

    # Local properties

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
                collection_name=self.collection_name
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
    def grow_conditions_contrast(self):
        return self._grow_conditions_contrast

    @grow_conditions_contrast.setter
    def grow_conditions_contrast(self, grow_conditions_contrast=None):
        """
        Sets grow conditions contrast.
        """
        if grow_conditions_contrast is None:
            self._grow_conditions_contrast = grow_conditions_contrast

    @property
    def gene_expression_filtered(self):
        return self._gene_expression_filtered

    @gene_expression_filtered.setter
    def gene_expression_filtered(self, gene_expression_filtered=None):
        """
        Sets gene expression filtered.
        """
        if gene_expression_filtered is None:
            self._gene_expression_filtered = gene_expression_filtered

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary=None):
        """
        Sets summary and starts uniformized data processing.
        """
        if summary is None:
            self._summary = summary
            # TODO: Could i start uniformized extractions?

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
