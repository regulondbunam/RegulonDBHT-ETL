"""
Peaks object.
Build uniformized data object for every dataset.
"""
# standard

# third party

# local
from ht_etl.domain.uniformized_data.uniformized_base import Base
from ht_etl.domain.uniformized_data.domain.peak import Peak
from libs import utils


class Peaks(Base):

    def __init__(self, **kwargs):
        super(Peaks, self).__init__(**kwargs)
        # Params

        # Local properties

        # Object properties
        self.sites_list = kwargs.get("sites_list", None)
        self.peaks_list = kwargs.get("peaks_list", None)

    # Local properties

    # Object properties
    @property
    def peaks_list(self):
        return self._peaks_list

    @peaks_list.setter
    def peaks_list(self, peaks_list=None):
        peaks_list = []
        for peak_data in self.uniform_dataset_dict.get('uniform_datasets', []):
            peak_obj = Peak(
                sites_list=self.sites_list,
                collection_name=self.collection_name,
                mg_api=self.mg_api,
                data_row=peak_data,
                database=self.database,
                url=self.url,
                genes_ranges=self.genes_ranges,
                dataset_id=self.dataset_id,
                type=self.type
            )
            peak_dict = {
                '_id': peak_obj.id,
                'temporalId': peak_obj.temporal_id,
                'closestGenes': peak_obj.closest_genes,
                'chromosome': peak_obj.chromosome,
                'peakLeftPosition': peak_obj.left_pos,
                'peakRightPosition': peak_obj.right_pos,
                'score': peak_obj.score,
                'name': peak_obj.name,
                'siteIds': peak_obj.site_ids,
                'datasetIds': peak_obj.dataset_ids
            }
            peaks_list.append(peak_dict)
        self._peaks_list = peaks_list

    # Static methods
