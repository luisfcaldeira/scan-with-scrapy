import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from A_apresentacao.view_models import SiteToSearchViewModel
from E_infra.A_data.model_context import PageElement
from E_infra.B_cross_cutting.System.errors import RepeatedUrl, NoFollowUrl, SiteNotInSearchList
from E_infra.B_cross_cutting.System.log_file import log_file
from E_infra.B_cross_cutting.mappers import MapperModelListToObjectList
from datetime import datetime

from B_aplicacao.app_service import SiteToSearchAppService, UrlFoundAppService, PageAppService, PageElementsAppService


class NewsSpider(scrapy.Spider):
    name = "news"
    urls = []
    last_url = None

    def __init__(self):
        self.__site_to_search_app_service = SiteToSearchAppService()
        self.__url_found_app_service = UrlFoundAppService()
        self.__page_app_service = PageAppService()
        self.__page_element_app_service = PageElementsAppService()
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
            raise AttributeError(r"The attribute 'link' must be a 'str' type.")

        link = SiteToSearchViewModel()
        link.url = link

        NewsSpider.urls.append(link)

    def __parse_page(self, response):

        url_found = self.__url_found_app_service.parse(response.url, NewsSpider.urls, NewsSpider.last_url)
        page, created = self.__page_app_service.get_or_create(url=url_found.id)

        self.__log(url_found.url)
        self.__log(response.xpath('//title/text()').get())
        page.title = response.xpath('//title/text()').get()

        selector = Selector(text=response.xpath('/html//body[1]').get())

        elements = []
        elements += self.__get_elements(selector=selector, css_selector='h1', url=url_found.id)
        elements += self.__get_elements(selector=selector, css_selector='h2', url=url_found.id)
        elements += self.__get_elements(selector=selector, css_selector='h3', url=url_found.id)
        elements += self.__get_elements(selector=selector, css_selector='h4', url=url_found.id)
        elements += self.__get_elements(selector=selector, css_selector='h5', url=url_found.id)
        elements += self.__get_elements(selector=selector, css_selector='p', url=url_found.id)

        self.__page_element_app_service.save_elements_for(url_found.id, elements)

        self.__log('===================================================================================')

        self.__page_app_service.update(page)

        NewsSpider.last_url = response.url

    def __get_elements(self, selector: Selector, css_selector, url=None):
        if not isinstance(selector, Selector):
            raise AttributeError(r"The attribute 'selector' must be a 'scrapy.Selector' type.")

        result = []
        elements = selector.css(css_selector)

        for element in elements:

            page_element = PageElement()
            page_element.classes = ''
            page_element.id_attr = ''

            text = element.css('::text').get()
            classes = element.css('::attr(class)').getall()
            ids = element.css('::attr(id)').getall()

            if text is not None and text != '':
                page_element.tag = css_selector
                page_element.value = text
                if url is not None:
                    page_element.url = url

                for clss in classes:
                    page_element.classes += clss

                for id in ids:
                    page_element.id_attr += id

                result.append(page_element)

        return result

    def __log(self, *texts):
        dt_time = self.__dt_time.replace(" ", "_")
        dt_time = dt_time.replace(":", ".")
        log = ''
        for text in texts:
            log += text

        log_file(f"found_url_{dt_time}.txt", f"{log} - {datetime.now()}")



