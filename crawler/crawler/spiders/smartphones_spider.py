import scrapy

# gets the data from table and puts in a json format
def get_data_from_table(response, info_path, value_path):
    infos = [x.strip() for x in response.xpath(info_path).getall()]
    values = [x.strip() for x in response.xpath(value_path).getall()]

    if(len(values) > len(infos)):
        values = values[:len(values)-1]

    return dict(zip(infos, values))

def get_title_product_price(response):
    title = response.css('title::text').get()
    if(title is None):
        title = ""
    
    product = response.css('#productTitle::text').get()
    if(product is not None):
        product = product.strip()
    else:
        product = ""

    price = response.css('#priceblock_ourprice::text').get()
    if(price is not None):
        price = price.strip()
    elif(response.css('#olp_feature_div > div.a-section.a-spacing-small.a-spacing-top-small > span.a-declarative > a > span.a-size-base.a-color-price').get() is not None):
        price = response.css('#olp_feature_div > div.a-section.a-spacing-small.a-spacing-top-small > span.a-declarative > a > span.a-size-base.a-color-price::text').get()
    else:
        price = ""
        
    return title, product, price
        
class Smartphones(scrapy.Spider):
    name = 'smartphones'
    start_urls = [
        'https://www.amazon.com.br/Celular-Xiaomi-Poco-6GB-128GB/dp/B08B9C149J',
        'https://www.amazon.com.br/Celular-Apple-iPhone-64gb-Tela/dp/B07XS47PVF',
        'https://www.amazon.com.br/Smartphone-Samsung-Octa-Core-Principal-Profundidade/dp/B08XVV828M'
    ]

    def parse(self, response):
        title, product, price = get_title_product_price(response)
        
        # Product information (RAM, Storage, Connection, Weight...)
        product_info = get_data_from_table(response, 
                                           '//*[@id="productDetails_techSpec_section_1"]/tr/th/text()',
                                           '//*[@id="productDetails_techSpec_section_1"]/tr/td/text()')
        additional_info = get_data_from_table(response, 
                                              '//*[@id="productDetails_detailBullets_sections1"]/tr/th/text()',
                                              '//*[@id="productDetails_detailBullets_sections1"]/tr/td/text()')
         
        yield {
            'title': title,
            'product': product,
            'price': price,
            'product_info': product_info,
            'additional_info': additional_info,
        }
    

        