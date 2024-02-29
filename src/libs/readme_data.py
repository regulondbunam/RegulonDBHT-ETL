"""
Reads README.md file in Datasets collections
"""
# standard
import os
import logging

# third party

# local


class ReadmeData(object):
    def __init__(self, **kwargs):
        # Params
        self.path = kwargs.get('path', None)

        # Local properties

        # Object properties
        self.readme_txt = kwargs.get('readme_txt', None)

    # Local properties

    # Object properties
    @property
    def readme_txt(self):
        return self._readme_txt

    @readme_txt.setter
    def readme_txt(self, txt=None):
        if txt is None:
            path = os.path.join(self.path, 'README.md')
            if not os.path.isfile(path):
                logging.info(f"Metadata file {path} not found. Please check if README.md file exists.")
            elif os.path.isfile(path):
                file = open(path, "r")
                txt = file.read()
                file.close()
                # logging.info(txt) # For Debugging
        self._readme_txt = txt
