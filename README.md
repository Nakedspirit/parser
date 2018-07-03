Парсер описаний вакансий с сайта monster.com
### Requirements

    https://docs.scrapy.org/en/latest/intro/install.html
    In case of any trouble related to these dependencies, please refer to their respective installation instructions:
 
 * Python 3.6+
 * Selenium (https://hub.docker.com/r/selenium/standalone-chrome/)   
 * [lxml installation](http://lxml.de/installation.html)
 * [cryptography installation](https://cryptography.io/en/latest/installation/)
 
 
 ### Запуск:

 > $ docker-compose up -d
 > $ pip install -r requirements.txt
 > $ scrapy crawl monster-vacancies
 
 ### Settings
 Адрес selenium hub или selenium node
 > export SELENIUM=localhost:4444
 
 Путь сохранения файла с вакансиями
 > export FILES_STORE=/tmp/

