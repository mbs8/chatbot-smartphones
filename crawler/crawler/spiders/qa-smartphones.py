import scrapy
import re

# Return the selected question information in a JSON format
def extract_question_info(current_question):
    question = current_question.css('div.a-fixed-left-grid-col.a-col-right > a > span::text').get()
    if(question is not None):  
        question = question.strip()
        question = re.sub(r'<.[A-z]*>|\r|\n', '', question)
    else:
        question = ""
        
    answer = current_question.css('div.a-fixed-left-grid-col.a-col-right > span').get()
    if(answer is not None):
        answer = answer.strip()
        answer = re.sub(r'<.[A-z]*>|\r|\n', '', answer)
    else:
        answer = ""

    q_id = current_question.css('div.a-fixed-left-grid-col.a-col-right > div').attrib['id']
    if(q_id is not None):
        q_id = q_id.split('-')[1]
    else:
        q_id = ""
    
    return {"question" : question, "answer": answer, "q_id": q_id}

# return a list of json in the format:
# qa: [
# 		(q1, a1, id1),
# 		(q2, a2, id2),
# 		...
# 		(qN, aN, idN)
# 	]
def getQA(response):
    # list containing the pair of questions and answers
    selector_qa_list = response.xpath('//*[@id="a-page"]/div/div[6]/div/div/div')
    qa_list = []

    for selector in selector_qa_list:
        question_info = extract_question_info(selector)
        qa_list.append(question_info)

    return qa_list

def get_asin_from_url(url):
    idx = url.find('asin')
    asin = url[5+idx:].split('/')[0]
    return asin

class QaSmartphones(scrapy.Spider):
    name = 'qa-smartphones'
    start_urls = [
        'https://www.amazon.com.br/ask/questions/asin/B08B9C149J',
        'https://www.amazon.com.br/ask/questions/asin/B07XS47PVF',
        'https://www.amazon.com.br/ask/questions/asin/B08XVV828M'
    ]

    def parse(self, response):
        asin = get_asin_from_url(response.url)         # Product identification key in Amazon
        qa_list = getQA(response)                      # Get the list os questions and answers of the current page
         
        yield {
            'asin': asin,
            'qa': qa_list
        }
        
        next_page = response.css('#askPaginationBar > ul > li.a-last > a::attr(href)').get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    

        