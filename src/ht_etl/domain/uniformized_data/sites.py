"""
TF Binding Sites object.
Build uniformized data object for every dataset.
"""
import os.path

# standard

# third party
import multigenomic_api as mg_api
# local
from src.ht_etl.domain.uniformized_data.uniformized_base import Base
from src.ht_etl.domain.uniformized_data.domain.site import Site


class Sites(Base):

    def __init__(self, **kwargs):
        super(Sites, self).__init__(**kwargs)
        # Params
        # print('\t\t\t\tTFB', self.uniform_dataset_dict)
        # Local properties
        # self.found_ris = kwargs.get("found_ris", None)
        # self.peak_id = kwargs.get("peak_id", None)
        # self.score = kwargs.get("score", None)
        # self.sequence = kwargs.get("sequence", None)
        # self.name_collection = kwargs.get("name_collection", None)

        # Object properties
        self.sites_list = kwargs.get("sites_list", None)

    # Local properties

    # Object properties
    @property
    def sites_list(self):
        return self._sites_list

    @sites_list.setter
    def sites_list(self, sites_list=None):
        sites_list = []
        for site_data in self.uniform_dataset_dict.get('uniform_datasets', []):
            site_obj = Site(
                sites_list=sites_list,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                data_row=site_data,
                database=self.database,
                url=self.url,
                genes_ranges=self.genes_ranges
            )
            site_dict = {
                'id': site_obj.id,
                'chromosome': site_obj.chromosome,
                'chrLeftPosition': site_obj.left_pos,
                'chrRightPosition': site_obj.right_pos,
                'closestGenes': site_obj.closest_genes,
                'foundRIs': site_obj.found_ris,
                'peakId': site_obj.peak_id,
                'score': site_obj.score,
                'strand': site_obj.strand,
                'sequence': site_obj.sequence,
                'datasetIds': self.tf_site_id,
                'temporalId': site_obj.temporal_id,
                'nameCollection': site_obj.collection_name
            }
            sites_list.append(site_dict)
        self._sites_list = sites_list

    # Static methods
