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
        self.mg_prods = Genes.get_mg_prod_object(
            prod_ids=self.prod_ids,
            database=self.database,
            url=self.url
        )
        self.mg_genes = Genes.get_mg_gene_object(
            mg_prod=self.mg_prods,
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
        genes = []
        self._genes = genes
        if self.mg_genes:
            for mg_gene in self.mg_genes:
                gene = {
                    '_id': mg_gene.get('_id'),
                    'name': mg_gene.get('name')
                }
                genes.append(gene)
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
        mg_prods = []
        for prod_id in prod_ids:
            mg_prod = collection.find_one({'_id': prod_id})
            mg_prods.append(mg_prod)
        return mg_prods

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
        mg_genes = []
        for prod_id in mg_prod:
            mg_gene = collection.find_one({'_id': prod_id.get('genes_id')})
            mg_genes.append(mg_gene)
        return mg_genes
