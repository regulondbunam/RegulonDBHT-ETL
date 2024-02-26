"""
Source Serie object.
"""
# standard
import logging

# third party

# local
from src.ht_etl.sub_domain.platform import Platform
from src.ht_etl.sub_domain.series import Series


class SourceSerie(object):
    def __init__(self, **kwargs):
        # Params
        self.serie_id = kwargs.get('serie_id', None)
        self.source_name = kwargs.get('source_name', None)
        self.platform_id = kwargs.get('platform_id', None)
        self.platform_title = kwargs.get('platform_title', None)
        self.title = kwargs.get('title', None)
        self.strategy = kwargs.get('strategy', None)
        self.method = kwargs.get('method', None)
        self.read_type = kwargs.get('read_type', None)
        self.source_db = kwargs.get('source_db', None)

        # Local properties

        # Object properties
        self.source_serie = kwargs.get('publications_list', None)

    # Local properties

    # Object properties
    @property
    def source_serie(self):
        return self._source_serie

    @source_serie.setter
    def source_serie(self, source_serie):
        """
        Sets Source Serie dict object.
        """
        self._source_serie = source_serie
        if source_serie is None:
            source_serie = Series(
                source_id=self.serie_id,
                source_name=self.source_name
            )
            platform = Platform(
                platform_id=self.platform_id,
                platform_title=self.platform_title
            )
            source_serie = {
                'series': [source_serie.series],
                'platform': platform.platform,
                'title': self.title,
                'strategy': self.strategy,
                'method': self.method,
                'readType': self.read_type,
                'sourceDB': self.source_db
            }

            source_serie = {k: v for k, v in source_serie.items() if v}
            self._source_serie = source_serie
