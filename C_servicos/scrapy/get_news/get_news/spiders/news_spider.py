import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from A_apresentacao.view_models import SiteToSearchViewModel
from E_infra.B_cross_cutting.System.errors import RepeatedUrl, NoFollowUrl, SiteNotInSearchList
from E_infra.B_cross_cutting.System.log_file import log_file
from E_infra.B_cross_cutting.mappers import MapperModelListToObjectList
from datetime import datetime

from B_aplicacao.app_service import SiteToSearchAppService, UrlFoundAppService, PageAppService


class NewsSpider(scrapy.Spider):
    name = "varredura"
    urls = []
    last_url = None

    def __init__(self):
        self.__site_to_search_app_service = SiteToSearchAppService()
        self.__url_found_app_service = UrlFoundAppService()
        self.__page_app_service = PageAppService()
        mapper = MapperModelListToObjectList()

        urls = self.__site_to_search_app_service.get_all()
        mapper.convert(urls, SiteToSearchViewModel)

        urls = mapper.get_result()
        NewsSpider.urls = urls

        self.__dt_time = datetime.now().__str__()

    def start_requests(self):

        for url in NewsSpider.urls:
            yield scrapy.Request(url=url.url, callback=self.parse)

    def parse(self, response):

        try:

            self.__log(response.url)
            self.__add_scrapy_link(response.url)
            self.__parse_page(response)

            extractors = LinkExtractor()
            links = extractors.extract_links(response)
            for link in links:
                yield scrapy.Request(link.url, callback=self.parse)

        except SiteNotInSearchList as e:
            self.__log(e)
            print(e)

        except RepeatedUrl as e:
            self.__log(e)
            print(e)

        except NoFollowUrl as e:
            self.__log(e)
            print(e)

        except Exception as e:
            msg = '=============================== UNKNOWN ERROR ============================='
            self.__log(msg)
            self.__log(e)
            print(msg)
            print(e)




    def __add_scrapy_link(self, link: str):
        if not isinstance(link, str):
            raise AttributeError("The attribute 'link' must be a \'str\' type.")

        link = SiteToSearchViewModel()
        link.url = link

        NewsSpider.urls.append(link)

    def __parse_page(self, response):

        url_found = self.__url_found_app_service.parse(response.url, NewsSpider.urls, NewsSpider.last_url)
        page, created = self.__page_app_service.get_or_create(url=url_found.id)

        self.__log('===================================================================================')
        self.__log(url_found.url)
        self.__log(response.xpath('//title/text()').get())

        page.title = response.xpath('//title/text()').get()
        page.content = response.text

        self.__log(page.title)
        self.__log('===================================================================================')

        self.__page_app_service.update(page)

        NewsSpider.last_url = response.url

    def __log(self, link):
        dt_time = self.__dt_time.replace(" ", "_")
        dt_time = dt_time.replace(":", ".")
        log_file(f"found_url_{dt_time}.txt", f"{link} - {datetime.now()}")





