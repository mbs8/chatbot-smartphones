import scrapy
import re

class QaSmartphones(scrapy.Spider):
    question_limit = 50
    name = 'qa-smartphones'
    start_urls = [
        'https://www.amazon.com.br/ask/questions/asin/B08B9C149J',
        'https://www.amazon.com.br/ask/questions/asin/B07XS47PVF',
        'https://www.amazon.com.br/ask/questions/asin/B08XVV828M'
    ]
    
    # Return the selected question information in a JSON format
    def extract_question_info(self, current_question):
        # Parses question
        question = current_question.css('div.a-fixed-left-grid-col.a-col-right > a > span::text').get()
        if(question is not None):  
            question = question.strip()
            question = re.sub(r'<.[A-z]*>|\r|\n', '', question)
        else:
            question = ""
        
        # Get and format answer
        answer = current_question.css('div.a-fixed-left-grid-col.a-col-right > span > span.askLongText::text').getall()
        if(answer != []):
            answer = [ans.strip() for ans in answer]
            answer = [s for s in answer if s != '']
            answer = ' '.join([s for s in answer])
        else:
            answer = current_question.css('div.a-fixed-left-grid-col.a-col-right > span::text').get()
        
        if(answer is not None):
            answer = answer.strip()
            answer = re.sub(r'<.[A-z]*>|\r|\n', '', answer)
        else:
            answer = ""

        # Parses question id
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
    def getQA(self, response, qa_list):
        # list containing the pair of questions and answers
        selector_qa_list = response.xpath('//*[@id="a-page"]/div/div[6]/div/div/div')
        questions = 0

        for selector in selector_qa_list:
            question_info = self.extract_question_info(selector)
            qa_list.append(question_info)
            questions += 1
        
        return questions


    def get_asin_from_url(self, url):
        idx = url.find('asin')
        asin = url[5+idx:].split('/')[0]
        return asin

    # def build_index(self, asin, qa_list):
    #     qa_index = {}
    #     for qa in qa_list:
            

    def parse(self, response):
        # Number of questions saved from the product
        question_count = response.meta.get('question_count', 0)
        
        # Product identification key in Amazon
        asin = response.meta.get('asin', self.get_asin_from_url(response.url))  
        
        # Get the list os questions and answers of the current page
        qa_list = response.meta.get('qa', []) 
        
        # Get the link to the next QA page
        next_page = response.css('#askPaginationBar > ul > li.a-last > a::attr(href)').get()
        
        if(question_count < 50 and next_page is not None):                     
            question_count += self.getQA(response, qa_list)
            
            meta = {'asin': asin, 'qa': qa_list, 'question_count': question_count}
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, meta=meta)
                
        else:
            for qa in qa_list:    
                yield {
                    'asin': asin,
                    'question': qa.get('question'),
                    'answer': qa.get('answer'),
                    'q_id': qa.get('q_id')
                }
    

        