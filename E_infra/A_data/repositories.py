from abc import ABCMeta

from E_infra.A_data.model_context import BaseModel, SiteToSearch, make_table_name, get_table_name


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

    def add(self, **fields):
        self.__model.create(**fields)


class SiteToSearchRepository(BaseRepository):

    def get_url(self, url):
        query = f'SELECT * FROM {get_table_name(super().model)} WHERE '
        query += f' url like \'%{url}%\''
        return super().model.raw(query).get()


class PageRepository(BaseRepository):

    def get_page(self, url):
        if not isinstance(url, int):
            raise AttributeError("You must inform an Id. ")

        query = f'SELECT * FROM {get_table_name(super().model)} WHERE '
        query += f' url_id = {url}'
        print(query)
        return super().model.raw(query).get()


if __name__ == "__main__":

    r = SiteToSearchRepository(SiteToSearch())
    data = r.get_url(url='%terra.com.br%')
    print(data)