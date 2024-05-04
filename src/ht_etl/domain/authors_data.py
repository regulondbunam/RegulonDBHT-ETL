"""
Authors Data object.
"""
# standard
import logging
import os
# third party

# local
from src.libs import utils
from src.libs import constants


class AuthorsData(object):

    def __init__(self, **kwargs):
        # Params
        self.authors_data_path = kwargs.get('authors_data_path')
        self.dataset_id = kwargs.get('dataset_id')
        self.file_name = kwargs.get('file_name')

        # Local properties

        # Object properties
        self.id = kwargs.get('id', None)
        self.dataset_ids = kwargs.get('dataset_ids', None)
        self.data = kwargs.get('data', None)

    # Local properties

    # Object properties
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, ad_id=None):
        self._id = ad_id
        if ad_id is None:
            self._id = f'AD_{self.dataset_id}'

    @property
    def dataset_ids(self):
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, dataset_ids=None):
        self._dataset_ids = dataset_ids
        if dataset_ids is None:
            dataset_ids = [self.dataset_id]
            self._dataset_ids = dataset_ids

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data=None):
        self._data = data
        if self._data is None:
            data = AuthorsData.get_authors_data_content(
                authors_data_path=self.authors_data_path,
                file_name=self.file_name,
                dataset_id=self.dataset_id
            )
            self._data = data

    # Static methods
    @staticmethod
    def get_authors_data_content(authors_data_path: str, file_name, dataset_id):
        """
        Gets and converts the author's Excel data to a CSV formatted String.

        Param
            file_name, String, authors' XLSX file name, path.
            authors_data_path, String, authors' XLSX files path.

        Returns
            authors_raw, String, CSV formatted String.
        """
        authors_data_path = os.path.join(authors_data_path, constants.AUTHORS_PATHS)
        if not file_name:
            logging.error(f'There is not File Name for {dataset_id} can not read Author\'s files')
            return None
        excel_path = os.path.join(authors_data_path, file_name)
        print(f'\t\tGetting authors data form: {excel_path}')
        logging.info(f'Getting authors data form: {excel_path}')
        if os.path.isfile(excel_path) and excel_path.endswith('.xlsx'):
            raw = utils.get_author_data_frame(
                filename=str(excel_path),
                load_sheet=0,
                rows_to_skip=0
            )
            author_raw = raw.to_csv(encoding='utf-8')
            logging.info(
                f'Reading Author\'s Data files {excel_path}')
            return author_raw
        elif os.path.isfile(excel_path) and excel_path.endswith('.tsv'):
            raw = utils.get_author_data_frame_tsv(str(excel_path))
            raw = raw.loc[:, ~raw.columns.str.contains('^Unnamed')]
            author_raw = raw.to_csv(encoding='utf-8', index=True)
            author_raw = author_raw.replace(',,,,,#', '#')
            logging.info(
                f'Reading Author\'s Data files {excel_path}')
            return author_raw
        elif os.path.isfile(excel_path) and excel_path.endswith('.txt'):
            raw = utils.get_author_data_frame_tsv(str(excel_path))
            raw = raw.loc[:, ~raw.columns.str.contains('^Unnamed')]
            author_raw = raw.to_csv(encoding='utf-8', index=True)
            author_raw = author_raw.replace(',,,,,#', '#')
            logging.info(
                f'Reading Author\'s Data files {excel_path}')
            return author_raw
        else:
            logging.error(
                f'There are not valid Author\'s Data files for {dataset_id} can not read Author\'s files')
            return None
