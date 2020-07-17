from abc import abstractmethod, ABCMeta

import scrapy

from D_domain.entities.entities import UrlFoundEntityDomain, SiteToSearchEntityDomain
from D_domain.services.domain_services import UrlFoundDomainService, SiteToSearchDomainService, PageDomainService
from E_infra.A_data.model_context import SiteToSearch, UrlFound, Page
from E_infra.A_data.repositories import BaseRepository, SiteToSearchRepository, PageRepository
from E_infra.B_cross_cutting.System.errors import SiteNotInSearchList
from E_infra.B_cross_cutting.mappers import MapperSpiderLinkToObject, MapperModelListToObjectList


class AppServiceBase(metaclass=ABCMeta):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def remove(self, entity):
        pass

    @abstractmethod
    def add(self, entity):
        pass


class SiteToSearchAppService(AppServiceBase):

    def __init__(self):
        self.__service_base = SiteToSearchDomainService(SiteToSearchRepository(SiteToSearch()))

    def get_all(self):
        return self.__service_base.get_all()

    def get_by_id(self, entity_id):
        return self.__service_base.get_by_id(entity_id)

    def get_or_create(self, **args):
        return self.__service_base.get_or_create(**args)

    def update(self, entity):
        self.__service_base.update(entity)

    def remove(self, entity):
        self.__service_base.remove(entity)

    def add(self, **fields):
        self.__service_base.add(**fields)

    def is_url_in_search_list(self, url):
        return self.__service_base.is_url_in_search_list(url)


class UrlFoundAppService(AppServiceBase):

    def __init__(self):
        self.__service_base = UrlFoundDomainService(BaseRepository(UrlFound()))
        self.__site_to_search_service_base = SiteToSearchDomainService(SiteToSearchRepository(SiteToSearch()))

    def get_all(self):
        return self.__service_base.get_all()

    def get_by_id(self, entity_id):
        return self.__service_base.get_by_id(entity_id)

    def get_or_create(self, **args):
        return self.__service_base.get_or_create(**args)

    def update(self, entity):
        self.__service_base.update(entity)

    def remove(self, entity):
        self.__service_base.remove(entity)

    def add(self, **fields):
        self.__service_base.add(**fields)

    def parse(self, link: scrapy.link.Link, searched_links: list, last_url):
        """ I`ll return an UrlFound model from DB """

        if not isinstance(link, scrapy.link.Link):
            raise AttributeError("You sould pass a \'scrapy.link.Link\' type in link attribute")

        if not self.__site_to_search_service_base.is_url_in_search_list(link.url):
            raise SiteNotInSearchList(f"This site ({link.url}) is not the list of sites to read. Ignoring...")

        url_found = self.__convert_url_found(link)
        return self.__service_base.parse(url_found, searched_links, last_url)

    def __convert_url_found(self, link):
        mapper = MapperSpiderLinkToObject()
        mapper.convert(link, UrlFoundEntityDomain)
        return mapper.get_result()


class PageAppService(AppServiceBase):

    def __init__(self):
        self.__page_service_base = PageDomainService(PageRepository(Page()))

    def get_all(self):
        return self.__page_service_base.get_all()

    def get_by_id(self, entity_id):
        return self.__page_service_base.get_by_id(entity_id)

    def get_or_create(self, **args):
        return self.__page_service_base.get_or_create(**args)

    def update(self, entity):
        self.__page_service_base.update(entity)

    def remove(self, entity):
        self.__page_service_base.remove(entity)

    def add(self, **fields):
        self.__page_service_base.add(**fields)

    def get_page(self, url):
        return self.__page_service_base.get_page(url)

if __name__ == '__main__':
    url_found_app_service = UrlFoundAppService()
    site_to_search_app_service = SiteToSearchAppService()
    page_app_service = PageAppService()

    link = scrapy.link.Link(url='https://www.boasaude.com.br/dicionario-medico/Todos')
    link.nofollow = False
    url_found_model, created = url_found_app_service.get_or_create(url=link.url)
    print(type(url_found_model))

    page = page_app_service.get_or_create(url=url_found_model.id)

    searched_links = []

    last_url = ''

    # url_found_app_service.parse(link, searched_links=searched_links, last_url=last_url)
    is_in_list = site_to_search_app_service.is_url_in_search_list(link.url)

    if is_in_list:
        print("existe")
    print(is_in_list)
