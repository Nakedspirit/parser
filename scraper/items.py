import scrapy


class VacancyItem(scrapy.Item):
    description = scrapy.Field()
