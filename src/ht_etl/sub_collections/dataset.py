"""
Dataset object.
Build dataset object and special objects for every dataset.
"""
# standard
import logging

# third party

# local
from src.ht_etl.domain.publications import Publications
from src.ht_etl.domain.source_serie import SourceSerie


class Dataset(object):
    def __init__(self, **kwargs):
        # Params
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

        # Local properties

        # Object properties
        self.dataset_dict = kwargs.get('dataset_dict', None)

    # Local properties

    # Object properties
    @property
    def dataset_dict(self):
        return self._dataset_dict

    @dataset_dict.setter
    def dataset_dict(self, dataset_dict=None):
        """
        Set dataset dictionary to build the final result.
        Gets data from the object and buidl sub collection objects.
        """
        self._dataset_dict = dataset_dict
        if dataset_dict is None:
            dataset_publications = Publications(
                dataset_id=self.dataset_id,
                pmid=self.pmid,
                email=self.email
            )

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
            logging.info(source_serie.source_serie)
            dataset_dict = {
                '_id': self.dataset_id,
                'publications': dataset_publications.publications_list,
                'objectTested': self.regulondb_tf_name,
                'sourceSerie': source_serie.source_serie,
                'sample': '',
                'linkedDataset': '',
                'growConditionsContrast': '',
                'summary': '',
                'releaseDataControl': '',
                'externalCrossReferences': '',
                'collectionData': '',
                'referenceGenome': '',
                'temporalId': '',
                'assemblyGenomeId': '',
                'fivePrimeEnrichment': '',
                'geneExpressionFiltered': '',
                'experimentCondition': '',
                'cutOff': '',
                'notes': '',
                'sourceReferenceGenome': '',
            }
            self._dataset_dict = dataset_dict
