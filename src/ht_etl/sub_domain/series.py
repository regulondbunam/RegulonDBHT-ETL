"""
Dataset object Source Series metadata class.
"""
# standard


# third party

# local


class Series(object):

    def __init__(self, **kwargs):
        # Params
        self.source_id = kwargs.get('source_id', None)
        self.source_name = kwargs.get('source_name', None)

        # Local properties

        # Object properties
        self.series = kwargs.get('series', None)

    # Local properties

    # Object properties
    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, series=None):
        """
        Set the Series dict object
        """
        series_list = []
        if series is None:
            series = {
                'sourceId': self.source_id,
                'sourceName': self.source_name
            }
            series_list.append(series)
        self._series = series_list
