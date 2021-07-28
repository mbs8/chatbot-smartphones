import scrapy
        
class GetUrls(scrapy.Spider):
    name = 'get-urls'
    start_urls = [
        'https://www.amazon.com.br/Celulares-e-Smartphones-Comunica%C3%A7%C3%A3o/s?rh=n%3A16243890011%2Cp_72%3A17833786011'
    ]

    # Generate the urls for products and qa
    def generate_product_url(self, product):
        asin = product.attrib['data-asin']
        url = None
        qa_url = None
        if(asin != ""):
            url = f"https://amazon.com.br/gp/product/{asin}"
            qa_url = f"https://www.amazon.com.br/ask/questions/asin/{asin}/ref=ask_ql_psf_ql_hza?isAnswered=true"
        
        return {"product": url, "qa": qa_url}

    def parse(self, response):
        grid = response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div')
        
        for product in grid:
            urls = self.generate_product_url(product)
            if(urls["product"] != None):
                yield urls 

        next_page = response.css('#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(25) > span > div > div > ul > li.a-last > a::attr(href)').get()
        if(next_page is None):
            next_page = response.css('#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(26) > span > div > div > ul > li.a-last > a::attr(href)').get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)