import scrapy
import re

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
        question = selector.css('div.a-fixed-left-grid-col.a-col-right > a > span::text').get().strip()
        question = re.sub(r'<.[A-z]*>|\r|\n', '', question)

        answer = selector.css('div.a-fixed-left-grid-col.a-col-right > span').get()
        if(answer != None):
            answer = answer.strip()
            answer = re.sub(r'<.[A-z]*>|\r|\n', '', answer)
        else:
            answer = ""

        q_id = selector.css('div.a-fixed-left-grid-col.a-col-right > div').attrib['id'].split('-')[1]

        qa_list.append({"question": question, "answer": answer, "q_id": q_id})

    return qa_list

class QaSmartphones(scrapy.Spider):
    name = 'qa-smartphones'
    start_urls = [
        'https://www.amazon.com.br/ask/questions/asin/B08B9C149J',
        'https://www.amazon.com.br/ask/questions/asin/B07XS47PVF',
        'https://www.amazon.com.br/ask/questions/asin//B08XVV828M'
    ]

    def parse(self, response):
        asin = response.url.split('/')[-1]             # Product identification key in Amazon
        qa_list = getQA(response)                      # Get the list os questions and answers of the current page
         
        yield {
            'asin': asin,
            'qa': qa_list
        }
    

        