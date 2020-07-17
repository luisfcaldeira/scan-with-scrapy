from abc import ABCMeta, abstractmethod

import peewee
import scrapy
from scrapy.link import Link

from A_apresentacao.view_models import ViewModel
from E_infra.A_data.model_context import SiteToSearch


class MapperBase(metaclass=ABCMeta):

    def do_object(self, view_object, fields):
        view = view_object()

        for attr in fields:
            value = fields[attr]

            # if not hasattr(view, attr):
            #     msg = f"\'{type(view).__name__}\' don't have attribute \'{attr}\'"
            #     raise MapperException(msg)

            setattr(view, attr, value)

        return view

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def convert(self, from_this, to_obj):
        pass


class MapperModelListToObjectList(MapperBase):
    __result_list = []

    def convert(self, model_list, adapter):
        if not isinstance(model_list, list) and not isinstance(model_list, peewee.ModelSelect):
            raise MapperAttributeException(f"model_list type is not List or peewee ModelSelect. Provide a list or peewee ModelSelect")

        i = 0

        for m in model_list:

            if not isinstance(m, peewee.Model):
                raise MapperAttributeException(f"An object in model_list (index: {i}) is not a peewee.Model type")

            fields = self.extract_properties(m)

            obj = super().do_object(adapter, fields)

            self.__add_view(obj)

            i += 1

        return self

    def extract_properties(self, m):
        return m.__data__

    def __add_view(self, view):
        self.__result_list.append(view)

    def get_result(self):
        return self.__result_list



class MapperModelToObject(MapperBase):

    __result = None

    def convert(self, peewee_model, adapter=object):

        if not isinstance(peewee_model, peewee.Model):
            raise MapperAttributeException(f"model type is not peewee ModelSelect. Provide a list or peewee ModelSelect")

        fields = self.extract_properties(peewee_model)

        obj = super().do_object(adapter, fields)

        self.__result = obj

        return self

    def extract_properties(self, m):
        return m.__data__

    def get_result(self):
        return self.__result


class MapperSpiderLinkToObject(MapperBase):

    __result = None

    def convert(self, link, adapter=object):

        if not isinstance(link, scrapy.link.Link):
            raise MapperAttributeException(f"model type is not scrapy.link.Link. Provide a scrapy's link type")

        fields = self.extract_properties(link)

        obj = super().do_object(adapter, fields)

        self.__result = obj

        return self

    def extract_properties(self, m):
        values = {}
        for slot in m.__slots__:
            values[slot] = m.__getattribute__(slot)
        return values

    def get_result(self):
        return self.__result


class MapperException(Exception):
    pass


class MapperAttributeException(Exception):
    pass


# if __name__ == "__main__":
#     model = SiteToSearch()
#     item = model.get_by_id(1)
#
#     class View(ViewModel):
#         id = None
#         # url = None
#         # first_inclusion = None
#         # last_updated = None
#
#         @property
#         def link(self):
#             return f"<a href\'{self.url}\'>{self.url}</a>"
#
#     # mapper = MapperModelListToObjectList()
#     mapper = MapperModelToObject()
#     mapper.convert(item, View)
#     view = mapper.get_result()
#     print(view.link)
#
#     mapper_list = MapperModelListToObjectList()
#
#     items = model.select()
#     mapper_list.convert(items, View)
#     list_result = mapper_list.get_result()
#     for v in list_result:
#         print(v.link)


# if __name__ == '__main__':
#     link = Link(url='http://www.terra.com.br')
#     mapper = MapperSpiderLinkToObject()
#     mapper.convert(link, UrlFound)
#
#     result = mapper.get_result()
#
#     print(result.url)
#     print(type(result))
