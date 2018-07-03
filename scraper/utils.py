# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from scraper import settings


class SeleniumSpider(scrapy.Spider):

    def parse(self, response):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger.info('Start Chrome session.')
        self.selenium = webdriver.Remote(
            command_executor=f'http://{settings.SELENIUM_HUB}/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.logger.info('Chrome session created.')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SeleniumSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    @classmethod
    def make_browser(cls):
        browser = webdriver.Remote(
            command_executor=f'http://{settings.SELENIUM_HUB}/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )
        return browser

    def spider_closed(self, spider):
        spider.logger.info('Close Chrome session.')
        spider.selenium.quit()

    def new_tab(self):
        self.selenium.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    def close_tab(self):
        self.selenium.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
