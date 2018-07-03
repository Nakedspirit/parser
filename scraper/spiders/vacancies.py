import os

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from scraper.items import VacancyItem
from scraper.pipelines import FilePipeline
from scraper.utils import SeleniumSpider


class VacanciesSpider(SeleniumSpider):
    name = 'monster-vacancies'
    start_urls = ('https://www.monster.com/jobs/',)
    allowed_domains = ('monster.com',)
    pipelines = (FilePipeline.ID,)

    def _get_location_links(self):
        location_block = self.selenium.find_element_by_xpath('//div/h3[contains(text(), "Jobs By Location")]')
        location_block = location_block.find_element_by_xpath("..")
        location_links = location_block.find_elements_by_tag_name('a')
        location_links = list(map(lambda x: x.get_attribute('href'), location_links))
        return location_links

    def _view_all_cities(self):
        view_all_btn = self.selenium.find_elements_by_xpath('//a[contains(text(), "View All")]')
        if len(view_all_btn) == 1:
            if view_all_btn[0].is_displayed():
                view_all_btn[0].click()

    def _get_city_links(self, location_link):
        """
        :param location_link: Link for one location
        :type location_link: str
        :return: cities links
        :rtype: list
        """
        self.selenium.get(location_link)
        self._view_all_cities()
        cities_block = self.selenium.find_element_by_xpath('//div/h2[contains(text(), "Popular Cities")]')
        cities_block = cities_block.find_element_by_xpath("..")
        city_links = cities_block.find_elements_by_tag_name('a')
        city_links = list(map(lambda x: x.get_attribute('href'), city_links))
        return city_links

    def _get_vacancies_by_city(self, city_link):
        """
        :param city_link: Link for one city
        :type city_link: str
        :return: vacancy description
        :rtype: str
        """
        self.selenium.get(city_link)

        next_page = True
        next_page_btn = None

        while next_page:
            if next_page_btn:
                next_page_btn.click()

            card_links = self.selenium.find_elements_by_xpath('//div[@class="jobTitle"]/h2/a')
            card_links = list(map(lambda x: x.get_attribute('href'), card_links))
            for card_link in card_links:
                self.new_tab()
                try:
                    self.selenium.get(card_link)
                    yield self.selenium.find_element_by_id('JobDescription').text
                except WebDriverException:
                    self.logger.exception(f'Failed open url {card_link}')
                finally:
                    self.close_tab()

            btns = self.selenium.find_elements_by_class_name("next")
            if len(btns) == 1:
                if btns[0].is_displayed():
                    next_page_btn = btns[0]
            else:
                next_page = False

    def get_vacancies(self):
        self.selenium.get(self.start_urls[0])
        for loc_link in self._get_location_links():
            for city_link in self._get_city_links(loc_link):
                for vacancy in self._get_vacancies_by_city(city_link):
                    yield vacancy

    def parse(self, response):
        for _description in self.get_vacancies():
            description = _description.replace(os.linesep, ' ')
            i = VacancyItem()
            i['description'] = description
            yield i
