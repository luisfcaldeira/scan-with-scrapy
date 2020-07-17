from abc import ABCMeta, abstractmethod
from datetime import datetime

import scrapy

from D_domain.entities.entities import UrlFoundEntityDomain, SiteToSearchEntityDomain
from E_infra.A_data.model_context import SiteToSearch, UrlFound
from E_infra.A_data.repositories import BaseRepository, SiteToSearchRepository
from E_infra.B_cross_cutting.System.errors import RepeatedUrl, NoFollowUrl, SiteNotInSearchList
from E_infra.B_cross_cutting.mappers import MapperSpiderLinkToObject, MapperModelListToObjectList
from E_infra.B_cross_cutting.regex_funs import split_url


class DomainServiceBase(metaclass=ABCMeta):

    def __init__(self, repository: BaseRepository):
        self.__repository = repository

    @property
    def repository(self):
        return self.__repository

    def get(self, **args):
        return self.__repository.get(**args)

    def get_all(self):
        return self.__repository.get_all()

    def get_by_id(self, entity_id):
        return self.__repository.get_by_id(entity_id)

    def get_or_create(self, **args):
        return self.__repository.get_or_create(**args)

    def update(self, entity):
        self.__repository.update(entity)

    def remove(self, entity):
        self.__repository.remove(entity)

    def add(self, **fields):
        self.__repository.add(**fields)


class SiteToSearchDomainService(DomainServiceBase):

    def is_url_in_search_list(self, url: str):

        if not isinstance(url, str):
            # print(type(url))
            raise AttributeError("You must pass a string")

        search_url = self.__extract_main_url(url) + '/'
        try:
            return super().repository.get_url(url=search_url)
        except:
            return False

    def __extract_main_url(self, url: str):
        group = split_url(url)
        return self.__form_main_url(group)

    def __form_main_url(self, group: tuple):
        search_url = ''
        dot = ''

        for item in group:
            if item is None:
                return search_url
            if item != 'www':
                search_url += f'{dot}{item}'
                if dot == '':
                    dot = '.'

        return search_url


class UrlFoundDomainService(DomainServiceBase):

    def parse(self, link: UrlFoundEntityDomain, searched_links: list, last_url):

        if link.url in searched_links:
            raise RepeatedUrl(f"Ignoring repeated url ({link.url}).")

        if link.nofollow:
            raise NoFollowUrl(f"Ignoring \'nofollow\' url ({link.url}).")

        if not isinstance(link, UrlFoundEntityDomain):
            raise AttributeError("link must be a UrlFoundEntityDomain instance. ")

        url_to_search, created = super().repository.get_or_create(url=link.url)
        url_to_search.last_updated = datetime.now()
        url_to_search.referral_url = last_url
        super().repository.update(url_to_search)
        return url_to_search


class PageDomainService(DomainServiceBase):

    def get_page(self, url):

        return super().repository.get_page(url)


if __name__ == '__main__':
    def __convert_url_found(link):
        mapper = MapperSpiderLinkToObject()
        mapper.convert(link, UrlFoundEntityDomain)
        return mapper.get_result()

    def __get_sites_to_search_in_entity_domain():
        site_to_search_service_base = SiteToSearchDomainService(SiteToSearchRepository(SiteToSearch()))
        sites_to_search = site_to_search_service_base.get_all()
        mapper = MapperModelListToObjectList()
        mapper.convert(sites_to_search, SiteToSearchEntityDomain)
        return mapper.get_result()

    link = scrapy.link.Link(url='https://www.terra.com.br' )
    url_found = __convert_url_found(link)
    service_base = UrlFoundDomainService(BaseRepository(UrlFound()))
    searched_links = []
    sites_to_search = __get_sites_to_search_in_entity_domain()
    last_url = 'http://www.meucu.com.br'

    result = service_base.parse(url_found, searched_links, sites_to_search, last_url)
    print(result)
