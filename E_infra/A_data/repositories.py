from abc import ABCMeta

from peewee import DoesNotExist

from E_infra.A_data.model_context import BaseModel, SiteToSearch, get_table_name


class BaseRepository(metaclass=ABCMeta):

    def __init__(self, model: BaseModel):
        self.__model = model

    @property
    def model(self):
        return self.__model

    def get_all(self):
        ''' Returns an iterable object '''
        return self.__model.select()

    def get_by_id(self, entity_id):
        return self.__model.get(id=entity_id)

    def get_or_create(self, **args):
        return self.__model.get_or_create(**args)

    def update(self, entity):
        entity.save()

    def remove(self, entity):
        entity.delete_instance()
        entity.execute()

    def remove_id(self, id):
        q = self.__model.__class__.delete().where(self.__model.__class__.id == id)
        q.execute()

    def add(self, **fields):
        self.__model.create(**fields)

    def save_list(self, element_list: list):

        for element in element_list:
            if not isinstance(element, self.__model.__class__):
                raise AttributeError(f'The item type ({element.__class__.__name__}) is not a {self.__model.__class__.__name__} instance')

            element.save()

class SiteToSearchRepository(BaseRepository):

    def get_url(self, url):
        try:
            return super().model.select().where(SiteToSearch.url % f'%{url}%').get()
        except DoesNotExist as e:
            print("SiteToSearchRepository: Data not found \n", e)
            return False
        except Exception as e:
            print("Repositories: Exception \n", e)


class PageRepository(BaseRepository):

    def get_page(self, url):
        if not isinstance(url, int):
            raise AttributeError("You must inform an Id. ")

        query = f'SELECT * FROM public.{get_table_name(super().model)} WHERE '
        query += f' url_id = {url}'

        print(query)
        return super().model.raw(query).get()


class PageElementsRepository(BaseRepository):

    def remove_url_id(self, id):
        q = super().model.__class__.delete().where(super().model.__class__.url_id == id)
        q.execute()


if __name__ == "__main__":

    r = SiteToSearchRepository(SiteToSearch())
    data = r.get_url(url='%terra.com.br%')
    print(data)