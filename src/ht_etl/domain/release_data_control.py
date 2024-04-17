"""
Sample object.
"""
# standard
import logging
import datetime

# third party

# local


class ReleaseControl(object):
    def __init__(self, **kwargs):
        # Params
        self.version = kwargs.get('version', None)
        # Local properties

        # Object properties
        self.release_date = kwargs.get('release_date', None)

    # Local properties

    # Object properties
    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, release_date=None):
        self._release_date = release_date
        if self._release_date is None:
            release_date = datetime.datetime.today().strftime("%d/%m/%Y")
            self._release_date = release_date
