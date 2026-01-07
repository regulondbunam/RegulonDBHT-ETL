"""
Source Serie object.
"""
# standard
import logging

# third party

# local
from ht_etl.sub_domain.platform import Platform
from ht_etl.sub_domain.series import Series


class SourceSerie(object):
    strategies = {
        "chip-seq": "ChIP-seq",
        "dapseq": "DAP",
        "gselex-chip": "gSELEX-chip",
        "chip-exo": "ChIP-exo",
        "gselex": "gSELEX",
        "rna-seq": "RNA-seq",
        "5'race": "5' RACE",
    }
    def __init__(self, **kwargs):
        # Params
        self.serie_id = kwargs.get('serie_id', None)
        self.source_name = kwargs.get('source_name', None)
        self.platform_id = kwargs.get('platform_id', None)
        self.platform_title = kwargs.get('platform_title', None)
        self.title = kwargs.get('title', None)
        self.strategy_text = kwargs.get('strategy', None)
        self.method = kwargs.get('method', None)
        self.read_type = kwargs.get('read_type', None)
        self.source_db = kwargs.get('source_db', None)

        # Local properties

        # Object properties
        self.strategy = kwargs.get('strategy', None)
        self.source_series = kwargs.get('source_series', None)
        self.platform = kwargs.get('platform', None)

    # Local properties
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy_value=None):
        if self.strategy_text:
            strategy_value = self.strategy_text.replace(' ', '')
            strategy_value = strategy_value.lower()
            if strategy_value in self.strategies:
                self._strategy = self.strategies[strategy_value]
            else:
                self._strategy = self.strategy_text
        else:
            self._strategy = self.strategy_text

    # Object properties
    @property
    def source_series(self):
        return self._source_series

    @source_series.setter
    def source_series(self, source_series=None):
        """
        Sets the source series.
        """
        self._source_series = source_series
        if source_series is None:
            source_series = Series(
                source_id=self.serie_id,
                source_name=self.source_name
            )
            self.source_series = source_series.series

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, platform=None):
        """
        Sets the platform.
        """
        self._platform = platform
        if platform is None:
            platform = Platform(
                platform_id=self.platform_id,
                platform_title=self.platform_title
            )
            platform_dict = {
                '_id': platform.id,
                'title': platform.title
            }
            platform_dict = {k: v for k, v in platform_dict.items() if v}
            self._platform = platform_dict
