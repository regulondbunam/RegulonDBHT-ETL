"""
Promoter object.
"""
# standard

# third party

# local


class Promoter(object):

    def __init__(self, **kwargs):
        # Params
        self.lend = kwargs.get('lend', None)
        self.rend = kwargs.get('rend', None)
        self.mg_api = kwargs.get('mg_api', None)

        # Local properties
        self.promoter_objects = kwargs.get('promoter_objects', None)

        # Object properties
        self.promoter_list = kwargs.get('promoter_list', None)

    # Local properties
    @property
    def promoter_objects(self):
        return self._promoter_objects

    @promoter_objects.setter
    def promoter_objects(self, promoter_objects=None):
        if promoter_objects is None:
            promoter_objects = self.mg_api.promoters.get_closer_promoters(
                (self.lend - 5),
                (self.rend + 5)
            )
        self._promoter_objects = promoter_objects

    # Object properties
    @property
    def promoter_list(self):
        return self._promoter_list

    @promoter_list.setter
    def promoter_list(self, promoter_list=None):
        promoter_list = []
        if promoter_list is []:
            for promoter_obj in self.promoter_objects:
                binds_sigma_factor = promoter_obj.binds_sigma_factor
                sigma_factor_name = None
                if binds_sigma_factor:
                    sigma_factor_id = binds_sigma_factor.sigma_factors_id
                    sigma_factor = self.mg_api.sigma_factors.find_by_id(sigma_factor_id)
                    if sigma_factor:
                        sigma_factor_name = sigma_factor.name
                promoter = {
                    '_id': promoter_obj.id,
                    'name': promoter_obj.name,
                    'strand': promoter_obj.strand,
                    'pos_1': promoter_obj.pos1,
                    'sigma': sigma_factor_name,
                    'confidenceLevel': promoter_obj.confidence_level,
                }
                promoter_list.append(promoter)
        self._promoter_list = promoter_list
