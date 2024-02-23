"""
Dataset object Source Series Platform class.
"""
# standard

# third party

# local


class Platform(object):

    def __init__(self, **kwargs):
        # Params
        self.id = kwargs.get('platform_id', None)
        self.title = kwargs.get('platform_title', None)

        # Local properties

        # Object properties
        self.platform = kwargs.get('platform', None)

    # Local properties

    # Object properties
    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, platform=None):
        """
        Set the Platform dict object
        """
        self._platform = platform
        if self._platform is None:
            platform = {
                '_id': self.id,
                'title': self.title
            }
            self._platform = platform
