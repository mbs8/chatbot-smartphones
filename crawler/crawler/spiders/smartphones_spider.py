import scrapy

def get_data_from_table(response, info_path, value_path):
    infos = [x.strip() for x in response.xpath(info_path).getall()]
    values = [x.strip() for x in response.xpath(value_path).getall()]

    if(len(values) > len(infos)):
        values = values[:len(values)-1]

    return dict(zip(infos, values))

class Smartphones(scrapy.Spider):
    name = 'smartphones'
    start_urls = [
        'https://www.amazon.com.br/Celular-Xiaomi-Poco-6GB-128GB/dp/B08B9C149J?ref_=Oct_s9_apbd_otopr_hd_bw_bHjJLCl&pf_rd_r=KM37FK0NZ6YVJ8KT06XS&pf_rd_p=1da659a0-948a-52ba-a216-243433981446&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=16243803011'
    ]

    def parse(self, response):
        title = response.css('title::text').get()
        product = response.css('#productTitle::text').get().strip()
        price = response.css('#priceblock_ourprice::text').get().strip()
        
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
    

        