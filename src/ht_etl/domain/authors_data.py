"""
Authors Data object.

This module provides the `AuthorsData` class, which is responsible for
loading and normalizing authors metadata files (XLSX/TSV/BED/TXT) into
a CSV-formatted string used downstream in the ETL pipeline.
"""

import logging
import os
from typing import Any, List, Optional

from libs import file_manager
from libs import constants


class AuthorsData(object):
    """
    AuthorsData represents metadata about the authors of a given dataset.

    The class encapsulates:
    - Identification fields (`id`, `dataset_ids`)
    - Configuration parameters for file discovery (`authors_data_path`,
      `dataset_id`, `file_name`)
    - The normalized authors data content (`data`) as a CSV-formatted string.

    Parameters
    ----------
    authors_data_path : str, optional
        Base path where authors files are located.
    dataset_id : str, optional
        Identifier of the dataset this authors data belongs to.
    file_name : str, optional
        File name of the authors metadata file.
    id : str, optional
        AuthorsData identifier. If not provided, it is derived as
        'AD_{dataset_id}'.
    dataset_ids : list[str], optional
        List of dataset IDs associated to this authors data. If not
        provided, defaults to `[dataset_id]`.
    data : str, optional
        Preloaded CSV-formatted string. If not provided, it is lazily loaded
        from disk when accessed via the `data` property.
    """

    def __init__(self, **kwargs: Any) -> None:
        # Params / configuration
        self.authors_data_path: Optional[str] = kwargs.get("authors_data_path")
        self.dataset_id: Optional[str] = kwargs.get("dataset_id")
        self.file_name: Optional[str] = kwargs.get("file_name")

        # Object properties (backing attributes are set via properties)
        self.id: Optional[str] = kwargs.get("id")
        self.dataset_ids: Optional[List[str]] = kwargs.get("dataset_ids")
        self.data: Optional[str] = kwargs.get("data")

    # --------------------------------------------------------------------- #
    # Object properties
    # --------------------------------------------------------------------- #

    @property
    def id(self) -> Optional[str]:
        """Return the AuthorsData identifier."""
        return self._id

    @id.setter
    def id(self, ad_id: Optional[str] = None) -> None:
        """
        Set the AuthorsData identifier.

        If `ad_id` is None, the identifier is derived from the dataset_id
        as 'AD_{dataset_id}'.
        """
        if ad_id is not None:
            self._id = ad_id
        else:
            self._id = f"AD_{self.dataset_id}" if self.dataset_id else None

    @property
    def dataset_ids(self) -> Optional[List[str]]:
        """Return the list of dataset IDs associated with this AuthorsData."""
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, dataset_ids: Optional[List[str]] = None) -> None:
        """
        Set the list of dataset IDs.

        If `dataset_ids` is None, it defaults to a single-item list
        containing `self.dataset_id`.
        """
        if dataset_ids is not None:
            self._dataset_ids = dataset_ids
        else:
            self._dataset_ids = [self.dataset_id] if self.dataset_id else None

    @property
    def data(self) -> Optional[str]:
        """
        Return the CSV-formatted authors data content.

        If the internal value is None, it is computed on-demand by loading
        the authors file from disk using `get_authors_data_content`.
        """
        return self._data

    @data.setter
    def data(self, data: Optional[str] = None) -> None:
        """
        Set the CSV-formatted authors data.

        If `data` is None, the value is lazily computed by reading the
        authors file from disk.
        """
        self._data = data
        if self._data is None and self.authors_data_path and self.file_name and self.dataset_id:
            self._data = AuthorsData.get_authors_data_content(
                authors_data_path=self.authors_data_path,
                file_name=self.file_name,
                dataset_id=self.dataset_id,
            )

    # --------------------------------------------------------------------- #
    # Static / helper methods
    # --------------------------------------------------------------------- #

    @staticmethod
    def _sanitize_dataframe(raw):
        """
        Normalize the DataFrame content by replacing commas in headers and
        values with semicolons.

        This emulates the original behavior:
        - Replace ',' in column names with ';'
        - Convert all cells to string and replace ',' with ';'
        """
        raw.columns = raw.columns.str.replace(",", ";")
        raw = raw.map(lambda x: str(x).replace(",", ";"))
        return raw

    @staticmethod
    def get_authors_data_content(
        authors_data_path: str,
        file_name: Optional[str],
        dataset_id: str,
    ) -> Optional[str]:
        """
        Load and normalize authors data from XLSX/TSV/BED/TXT into a CSV string.

        The logic is kept compatible with the original implementation:
        - For `.xlsx`:
          - Load with `file_manager.get_author_data_frame`
          - Sanitize commas
          - Export as CSV with default `index=True`
        - For `.tsv`, `.bed`, `.txt`:
          - Load with `file_manager.get_author_data_frame_tsv`
          - Drop `Unnamed` columns
          - Sanitize commas
          - Export as CSV with `index=False`
          - Replace ',,,,,#' with '#'
          - For `.bed`, additionally strip leading '#' characters.

        Parameters
        ----------
        authors_data_path : str
            Base path where authors metadata files are stored.
        file_name : str or None
            Name of the authors metadata file to load.
        dataset_id : str
            Dataset identifier, used for logging context.

        Returns
        -------
        str or None
            CSV-formatted authors data string, or None if no valid file
            could be read.
        """
        authors_dir = os.path.join(authors_data_path, constants.AUTHORS_PATHS)

        if not file_name:
            logging.error(
                f"There is not File Name for {dataset_id} can not read Author's files"
            )
            return None

        file_path = os.path.join(authors_dir, file_name)

        print(f"\t\t\tGetting authors data from: {file_path}")
        logging.info(f"Getting authors data from: {file_path}")

        if not os.path.isfile(file_path):
            logging.error(
                f"There are not valid Author's Data files for {dataset_id} can not read Author's files"
            )
            return None

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        # XLSX branch (original behavior preserved)
        if ext == ".xlsx":
            raw = file_manager.get_author_data_frame(
                filename=str(file_path),
                load_sheet=0,
                rows_to_skip=0,
            )
            raw = AuthorsData._sanitize_dataframe(raw)
            author_raw = raw.to_csv(encoding="utf-8")
            logging.info(f"Reading Author's Data files {file_path}")
            return author_raw

        # TSV / BED / TXT share most of the logic
        if ext in (".tsv", ".bed", ".txt"):
            raw = file_manager.get_author_data_frame_tsv(str(file_path))
            # Drop unnamed columns
            raw = raw.loc[:, ~raw.columns.str.contains(r"^Unnamed")]
            raw = AuthorsData._sanitize_dataframe(raw)
            author_raw = raw.to_csv(encoding="utf-8", index=False)
            author_raw = author_raw.replace(",,,,,#", "#")

            if ext == ".bed":
                # Original behavior: strip leading '#'
                author_raw = author_raw.lstrip("#")

            logging.info(f"Reading Author's Data files {file_path}")
            return author_raw

        # Unsupported format
        logging.error(
            f"There are not valid Author's Data files for {dataset_id} can not read Author's files"
        )
        return None
