from elasticsearch import Elasticsearch

class EsHandle:
    def __init__(self):
        self._products_index = 'products'
        self._qa_index = 'qa'
        self._es = Elasticsearch()
    
    # Query all the indices that aren't system indices in the elasticsearch
    def get_useful_indices(self):
        filtered_idx = filter(lambda x : '.' not in x, [f['index'] for f in self._es.cat.indices(format='json')])
        indices_names = [idx for idx in filtered_idx]
        return indices_names

    # Get the product in the 'products' index by name
    def get_product_by_name(self, name):
        query_body = {
            "query": {
                "match": {
                    "product": name
                }
            }
        }
        possible_products = []
        query = self._es.search(index=self._products_index, body=query_body)['hits']['hits']
        
        for p in query:
            possible_products.append(p['_source'])
        
        return possible_products

    # Get the products names and id's from the 'products' index
    def get_products(self):
        result = []
        query = self._es.search(index=self._products_index)['hits']['hits']
        
        for p in query:
            p_id = p['_id']
            p_name = p['_source']['product']
            result.append((p_name, p_id))
        return result

if __name__ == "__main__":
    print("Starting test...")
    handle = EsHandle()
    handle.get_useful_indices()