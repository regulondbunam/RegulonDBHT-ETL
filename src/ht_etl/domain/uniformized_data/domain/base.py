"""
Uniformized base object.
Build uniformized properties for different uniform data types.
"""
# standard
import logging

# third party
import pymongo.errors as mongo_errors

# local
from src.libs import utils
from src.libs import constants


class Base(object):

    def __init__(self, **kwargs):
        # Params
        self.mg_api = kwargs.get('mg_api')
        self.data_row = kwargs.get('data_row', [])
        self.genes_ranges = kwargs.get('genes_ranges', [])
        self.type = kwargs.get('type', None)
        self.dataset_id = kwargs.get('dataset_id', None)

        # Local properties

        # Object properties
        self.dataset_ids = kwargs.get("dataset_ids", None)
        self.chromosome = kwargs.get("chromosome", None)
        self.left_pos = kwargs.get("left_pos", None)
        self.right_pos = kwargs.get("right_pos", None)
        self.strand = kwargs.get("strand", None)
        self.closest_genes = kwargs.get("closest_genes", None)
        self.temporal_id = kwargs.get("temporal_id", None)
        self.id = kwargs.get("id", None)

    # Local properties

    # Object Properties
    @property
    def temporal_id(self):
        return self._temporal_id

    @temporal_id.setter
    def temporal_id(self, temporal_id=None):
        if temporal_id is None:
            if isinstance(self.data_row, dict):
                temporal_id = (
                    f'[{self.type}_'
                    f'{self.dataset_id},'
                    f'{self.left_pos},'
                    f'{self.right_pos},'
                    f'{self.strand}]'
                )
            if isinstance(self.data_row, list):
                temporal_id = (
                    f'[{self.data_row[1]},'
                    f'{self.data_row[2]},'
                    f'{self.data_row[4]},'
                    f'{self.data_row[5]},'
                    f'{self.data_row[6]}]'
               )
            self._temporal_id = temporal_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, site_id=None):
        if site_id is None:
            self._id = self.temporal_id

    @property
    def chromosome(self):
        return self._chromosome

    @chromosome.setter
    def chromosome(self, chromosome=None):
        if chromosome is None:
            if isinstance(self.data_row, dict):
                chromosome = self.data_row.get("chromosome", None)
            if isinstance(self.data_row, list):
                chromosome = f'{self.data_row[0]}'
        self._chromosome = chromosome

    @property
    def left_pos(self):
        return self._left_pos

    @left_pos.setter
    def left_pos(self, left_pos=None):
        if left_pos is None:
            if isinstance(self.data_row, dict):
                left_pos = self.data_row.get("start", None)
            if isinstance(self.data_row, list):
                left_pos = f'{self.data_row[1]}'
            self._left_pos = left_pos

    @property
    def right_pos(self):
        return self._right_pos

    @right_pos.setter
    def right_pos(self, right_pos=None):
        if right_pos is None:
            if isinstance(self.data_row, dict):
                right_pos = self.data_row.get("stop", None)
            if isinstance(self.data_row, list):
                right_pos = f'{self.data_row[2]}'
            self._right_pos = right_pos

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand=None):
        if strand is None:
            if isinstance(self.data_row, dict):
                strand = self.data_row.get("strand", None)
            if isinstance(self.data_row, list):
                strand = f'{self.data_row[5]}'
            self._strand = strand

    @property
    def closest_genes(self):
        return self._closest_genes

    @closest_genes.setter
    def closest_genes(self, closest_genes=None):
        if closest_genes is None:
            if self.type == constants.TFBINDING or self.type == constants.TSS:
                try:
                    closest_genes = utils.find_closest_gene(
                        left_pos=self.left_pos,
                        right_pos=self.right_pos,
                        genes_ranges=self.genes_ranges,
                        mg_api=self.mg_api
                    )
                except mongo_errors.InvalidOperation:
                    closest_genes = None
        self._closest_genes = closest_genes
