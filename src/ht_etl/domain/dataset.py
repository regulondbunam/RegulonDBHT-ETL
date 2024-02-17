import os


class Dataset(object):
    def __init__(self, **kwargs):
        # Params
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

        self.id = kwargs.get('id', None)
        self.publications = kwargs.get('publications', None)
        self.object_tested = kwargs.get('object_tested', None)
        self.source_serie = kwargs.get('source_serie', None)
        self.sample = kwargs.get('sample', None)
        self.linked_dataset = kwargs.get('linked_dataset', None)
        self.grow_conditions = kwargs.get('grow_conditions', None)
        self.summary = kwargs.get('summary', None)
        self.release_data_control = kwargs.get('release_data_control', None)
        self.external_cross_references = kwargs.get('external_cross_references', None)
        self.collection_data = kwargs.get('collection_data', None)
        self.reference_genome = kwargs.get('reference_genome', None)
        self.temporal_id = kwargs.get('temporal_id', None)
        self.assembly_genome_id = kwargs.get('assembly_genome_id', None)
        self.five_prime_enrichment = kwargs.get('five_prime_enrichment', None)
        self.gene_expression_filtered = kwargs.get('gene_expression_filtered', None)
        self.experiment_condition = kwargs.get('experiment_condition', None)
        self.cut_off = kwargs.get('cut_off', None)
        self.notes = kwargs.get('notes', None)
        self.source_reference_genome = kwargs.get('source_reference_genome', None)

    # Local properties

    # Object properties
    @property
    def dataset_dict(self):
        return self._dataset_dict

    @dataset_dict.setter
    def dataset_dict(self, dataset_dict=None):
        self._dataset_dict = dataset_dict
        if dataset_dict is None:
            dataset_dict = {
                '_id': self.dataset_id,
                'pmid': self.pmid,
                'authors': self.authors
            }
            self._dataset_dict = dataset_dict
