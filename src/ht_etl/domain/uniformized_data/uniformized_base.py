"""
Uniformized base object.
Build uniformized properties for different uniform data types.
"""
# standard
import logging
import os
import pandas

# third party

# local
from src.libs import utils
from src.libs import constants


class Base(object):

    def __init__(self, **kwargs):
        # Params
        self.collection_name = kwargs.get('collection_name')
        self.mg_api = kwargs.get('mg_api')
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)
        self.collection_path = kwargs.get('collection_path', None)
        self.genes_ranges = kwargs.get("genes_ranges", None)
        self.dataset_id = kwargs.get("dataset_id", None)
        self.serie_id = kwargs.get("serie_id", None)
        self.type = kwargs.get("type", '')
        self.sub_type = kwargs.get("sub_type", '')
        self.old_dataset_id = kwargs.get("old_dataset_id", None)

        # Local properties
        self.uniform_dataset_path = kwargs.get("uniform_dataset_path", None)
        self.uniform_dataset_dict = Base.get_uniform_datasets_dicts(
            datasets_path=self.uniform_dataset_path,
            ds_type=self.type,
            ds_sub_type=self.sub_type,
        )

        # Object properties

    # Local properties
    @property
    def uniform_dataset_path(self):
        return self._uniform_dataset_path

    @uniform_dataset_path.setter
    def uniform_dataset_path(self, uniform_dataset_path=None):
        self._uniform_dataset_path = uniform_dataset_path
        uniform_path = ''
        if uniform_dataset_path is None:
            uniform_paths = os.path.join(self.collection_path, constants.UNIFORMIZED)
            ds_id = self.old_dataset_id
            if self.type == constants.TFBINDING:
                if ds_id is None:
                    ds_id = self.dataset_id
                if ds_id and self.serie_id:
                    print(
                        str(uniform_paths),
                        self.serie_id,
                        'datasets',
                        ds_id,
                        f'{ds_id}_sites.bed'
                    )
                    uniform_path = os.path.join(
                        str(uniform_paths),
                        self.serie_id,
                        'datasets',
                        ds_id,
                        f'{ds_id}_sites.bed'
                    )
                if self.sub_type == constants.PEAKS:
                    uniform_path = os.path.join(
                        str(uniform_paths),
                        self.serie_id,
                        'datasets',
                        ds_id,
                        f'{ds_id}_peaks.bed'
                    )
            if self.type == constants.TUS:
                if ds_id is None:
                    ds_id = self.dataset_id
                uniform_path = os.path.join(
                    str(uniform_paths),
                    f'{ds_id}.tsv'
                )
            if self.type == constants.TSS:
                if ds_id is None:
                    ds_id = self.dataset_id
                uniform_path = os.path.join(
                    str(uniform_paths),
                    f'{ds_id}.tsv'
                )
            self._uniform_dataset_path = uniform_path

    # Object properties

    # Static methods
    @staticmethod
    def get_uniform_datasets_dicts(datasets_path, ds_type, ds_sub_type):
        uniform_datasets_dict = {}
        if ds_type == constants.TFBINDING:
            uniform_dataset_rows = []
            try:
                print('\t\t\t\t', f'Getting uniformized data from: {datasets_path}')
                logging.info(f'Getting uniformized data from: {datasets_path}')
                with open(datasets_path) as dataset_file:
                    for row in dataset_file:
                        if (
                            not row.startswith('track')
                            and not row.startswith('browser')
                            and not row.startswith('##')
                            and not row.startswith('#')
                        ):
                            uniform_dataset_rows.append(row.strip().split())
            except FileNotFoundError:
                logging.error(f"Dataset path {datasets_path} not found.")
            uniform_datasets_dict.setdefault('uniform_datasets', uniform_dataset_rows)
            if ds_sub_type == constants.PEAKS:
                uniform_datasets_dict.setdefault('uniform_datasets', uniform_dataset_rows)
        else:
            try:
                print('\t\t\t\t', f'Getting uniformized data from: {datasets_path}')
                logging.info(f'Getting uniformized data from: {datasets_path}')
                dataset_df = utils.get_data_frame_tsv(datasets_path)
                uniform_datasets_dict = utils.get_json_from_data_frame(dataset_df)
            except FileNotFoundError:
                logging.error(f"Dataset path {datasets_path} not found.")

        return uniform_datasets_dict
