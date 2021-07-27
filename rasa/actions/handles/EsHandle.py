from elasticsearch import Elasticsearch

# Singleton class, use variable es_handle
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

        # insert URL into Dict
        for prod in possible_products:
            prod.update({"URL": f"www.amazon.com.br/gp/product/{prod['additional_info']['ASIN']}"})

        return possible_products

    def get_qa_by_asin(self, asin, question):
        query_body = {
            "query": {
                "bool": {
                "must": [
                    {
                    "match": {
                        "asin": asin
                    }
                    },
                    {
                    "match": {
                        "question": question
                    }
                    }
                ]
                }
            }
            }

        possible_answers = []
        query = self._es.search(index=self._qa_index, body=query_body)['hits']['hits']
        
        for p in query:
            possible_answers.append(p['_source'])
        
        return possible_answers


    # Get the products names and id's from the 'products' index
    def get_products(self):
        result = []
        query = self._es.search(index=self._products_index)['hits']['hits']
        
        for p in query:
            p_id = p['_id']
            p_name = p['_source']['product']
            result.append((p_name, p_id))
        return result
    
    # Get specific product fact
    def get_product_fact(self, product_name, product_fact):
        products_jsons = self.get_product_by_name(product_name)
        possible_products = []

        for product in products_jsons:
            title = product.get("product", "TITLE")
            url = product.get("URL", "no page")
            fact_json = product["product_info"]
            value = fact_json.get(product_fact, "FACT")
            possible_products.append({"Produto": title, product_fact: value, "URL": url})
        
        return possible_products

    def get_product_qa(self, product_name, question):
        products_jsons = self.get_product_by_name(product_name)
        if(len(products_jsons) < 1):
            return []

        product = products_jsons[0]
        title = product["product"]
        add_info_json = product["additional_info"]
        asin = add_info_json["ASIN"]
        
        qa_list = self.get_qa_by_asin(asin, question)
        return {"Produto": title, "qa": qa_list, "URL": product["URL"]}

    def get_product_price(self, product_name):
        products_jsons = self.get_product_by_name(product_name)
        possible_products = []

        for product in products_jsons:
            title = product.get("product", "TITLE")
            price = product.get("price", "PRICE")
            url = product.get("URL", "no page")
            possible_products.append({"Produto": title, "price": price, "URL": url})
        
        return possible_products

    # def get_product_url(self, product_name):
    #     products_json = self.get_product_by_name(product_name)
    #     possible_products = [{"Produto": prod.get("product", "TITLE"), "URL": f"www.amazon.com.br/gp/product/{prod['additional_info']['ASIN']}"} for prod in products_json]
    #     return possible_products 



# Singleton implementation
es_handle = EsHandle()

if __name__ == "__main__":
    print("Starting test...")
    handle = EsHandle()
    print(handle.get_product_qa("celular", "vem com nota fiscal?"))