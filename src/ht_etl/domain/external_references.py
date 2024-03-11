"""
Sample object.
"""
# standard
import logging

# third party

# local


class ExternalReference(object):
    def __init__(self, **kwargs):
        # Params
        self.urls = kwargs.get('urls', None)

        # Local properties
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.note = kwargs.get('note', None)

        # Object properties
        self.external_references = kwargs.get('external_references', None)

    # Local properties

    # Object properties
    @property
    def external_references(self):
        return self._external_references

    @external_references.setter
    def external_references(self, external_references):
        external_references = []
        if self.urls:
            urls = self.urls.replace(' ', '')
            for url in urls.split(','):
                url_data = url.split('|')
                try:
                    name = url_data[0]
                except IndexError:
                    name = ''
                try:
                    link = url_data[2]
                except IndexError:
                    link = ''
                external_reference = {
                    'name': name,
                    'url': link,
                    'description': self.description,
                    'note': self.note
                }
                external_references.append(external_reference)
        self._external_references = external_references

    # Static methods

