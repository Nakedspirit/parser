# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scraper.items import VacancyItem


class FilePipeline(object):
    ID = 'FilePipeline'

    FILES_STORE = os.getenv('FILES_STORE', '/tmp/')

    def process_item(self, item, spider):
        if isinstance(item, VacancyItem):
            self.process_vacancy_item(item)

    def process_vacancy_item(self, item):
        with open(os.path.join(self.FILES_STORE, 'vacancies.txt'), 'a') as f:
            f.write(item['description'] + os.linesep)
