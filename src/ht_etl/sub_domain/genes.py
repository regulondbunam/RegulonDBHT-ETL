"""
Dataset object ObjectTested Genes class.
"""
# standard

# third party
from pymongo import MongoClient

# local


class Genes(object):

    def __init__(self, **kwargs):
        # Params
        self.tf_id = kwargs.get('tf_id', None)
        self.prod_ids = kwargs.get('prod_ids', None)
        self.database = kwargs.get('database', None)
        self.url = kwargs.get('url', None)

        # Local properties
        self.mg_prod = Genes.get_mg_prod_object(
            prod_ids=self.prod_ids,
            database=self.database,
            url=self.url
        )
        self.mg_genes = Genes.get_mg_gene_object(
            mg_prod=self.mg_prod,
            database=self.database,
            url=self.url
        )

        # Object properties
        self.genes = kwargs.get('genes', None)

    # Local properties

    # Object properties
    @property
    def genes(self):
        return self._genes

    @genes.setter
    def genes(self, genes=None):
        """
        Set the Platform dict object
        """
        self._genes = genes
        if self._genes is None and self.mg_genes:
            genes = {
                '_id': self.mg_genes.get('id'),
                'name': self.mg_genes.get('name')
            }
        self._genes = genes

    # Static methods
    @staticmethod
    def get_mg_prod_object(prod_ids, database, url):
        """
        Gets Product object from Multigenomic database.
        Args:
            prod_ids: String, name of TF product.
            database: String, name of database.
            url: String, URL of MongoDB database.

        Returns:
            mg_prod: Dict, product object.
        """
        if not prod_ids:
            return None
        client = MongoClient(url)
        db = client[database]
        collection = db['products']
        mg_prod = collection.find_one({'_id': prod_ids})
        return mg_prod

    @staticmethod
    def get_mg_gene_object(mg_prod, database, url):

        """
        Gets Gene object from Multigenomic database.
        Args:
            mg_prod: Object, multigenomic TF product.
            database: String, name of database.
            url: String, URL of MongoDB database.

        Returns:
            mg_prod: Dict, gene object.
        """
        if not mg_prod:
            return None
        client = MongoClient(url)
        db = client[database]
        collection = db['genes']
        mg_genes = collection.find_one({'_id': mg_prod.get('genes_id')})
        return mg_genes
