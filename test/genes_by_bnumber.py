# standard
import os
import json

# third party
import multigenomic_api as mg_api
import pymongo

# local


def get_gene_by_bnumber(bnumber, database, url):
    '''
    Gets Gene in the RegulonDB Multigenomic database associated to a Gene BNumber.

    Param
        bnumber, List, Bnumbers String Array.
        database, String, Multigenomic database to get external data.
        url, String, URL where database is located.
    Returns
        gene, Dict, Gene object from RegulonDB Multigenomic database.
    '''
    gene_dict = {}
    mg_api.connect(database, url)
    try:
        gene = mg_api.genes.find_by_bnumber(bnumber)
        gene_dict.setdefault('_id', gene.id)
        gene_dict.setdefault('name', gene.name)
        gene_dict.setdefault('bnumber', gene.bnumber)
        gene_dict.setdefault('synonyms', gene.synonyms)
        gene_dict.setdefault('leftEndPosition', gene.left_end_position)
        gene_dict.setdefault("rightEndPosition", gene.right_end_position)

    except IndexError:
        print(f'Can not find Gene bnumbers: {bnumber}')
    mg_api.disconnect()
    return gene_dict


def create_json(objects, filename, output):
    '''
    Create and write the JSON file with the results.

    Param
        objects, Object, a Python serializable object that you want to convert to JSON format.
        filename, String, JSON file name.
        output, String, output path.
    '''
    filename = os.path.join(output, filename)
    with open(f'{filename}.json', 'w') as json_file:
        json.dump(objects, json_file, indent=4, sort_keys=True)


url = "mongodb://localhost:27017/"
database = "regulondbmultigenomic"
collection_name = "genes"
mongo_client = pymongo.MongoClient(url)
mg_db = mongo_client[database]
collection = mg_db[collection_name]
mg_bnumbers = collection.find({}, {"bnumber": 1, "_id": 0})

gene_objects = {}
for bnumber in mg_bnumbers:
    print(bnumber)
    if bnumber:
        gene_obj = genes = get_gene_by_bnumber(
            bnumber.get("bnumber"), database, url)
        print(gene_obj)
        gene_objects.update({bnumber.get("bnumber"): gene_obj})

create_json(gene_objects, 'bnumbers', 'config')
