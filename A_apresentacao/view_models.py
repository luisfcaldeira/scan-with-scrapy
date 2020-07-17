from abc import ABCMeta
from E_infra.A_data.model_context import BaseModel


class ViewModel(metaclass=ABCMeta):
    pass


class SiteToSearchViewModel(ViewModel):

    def __str__(self):
        return f"ModelView: {self.url}"
