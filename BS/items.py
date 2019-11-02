import scrapy


class QuestionItem(scrapy.Item):
    ques = scrapy.Field()
    quesImage = scrapy.Field()
    answer_url = scrapy.Field()
    answer = scrapy.Field()
    analyze = scrapy.Field()
    awImage = scrapy.Field()



