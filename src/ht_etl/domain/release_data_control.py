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
        self.release_data_control = kwargs.get('release_data_control', None)

    # Local properties

    # Object properties
    @property
    def release_data_control(self):
        return self._release_data_control

    @release_data_control.setter
    def release_data_control(self, release_data_control=None):
        if release_data_control is None:
            release_data_control = {
                'date': datetime.datetime.today().strftime("%d/%m/%Y"),
                'version': self.version
            }
        self._release_data_control = release_data_control
