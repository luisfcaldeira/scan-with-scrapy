from E_infra.A_data.config_db import Config
from E_infra.B_cross_cutting.System.uteis import get_obj_name
import peewee
import datetime
import inspect


config_db = Config()
db = config_db.get_db('varredura_noticias')


def make_table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower() + '_tbl'


def get_table_name(model_class):
    if inspect.isclass(model_class):
        return get_obj_name(model_class()).lower() + '_tbl'

    if isinstance(model_class, object):
        return get_obj_name(model_class).lower() + '_tbl'

    raise AttributeError("The model_class attribute must to be a class or an object. Provide a correct type")

class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = db
        table_function = make_table_name


class SiteToSearch(BaseModel):

    url = peewee.CharField(max_length=2083, unique=True)
    first_inclusion = peewee.DateTimeField(default=datetime.datetime.now)
    last_updated = peewee.DateTimeField(null=True)


class UrlFound(BaseModel):

    url = peewee.CharField(max_length=2083, unique=True)
    first_inclusion = peewee.DateTimeField(default=datetime.datetime.now)
    last_updated = peewee.DateTimeField(null=True)
    referral_url = peewee.CharField(max_length=2083, null=True)


class Page(BaseModel):

    url = peewee.ForeignKeyField(UrlFound)
    date_inclusion = peewee.DateTimeField(default=datetime.datetime.now)
    title = peewee.TextField(null=True)
    content = peewee.TextField(null=True)


if __name__ == '__main__':
    try:
        SiteToSearch.create_table(safe=False)
        # SiteToSearch.get_or_create(url="https://docs.scrapy.org/")
        SiteToSearch.get_or_create(url="https://www.terra.com.br/")
        SiteToSearch.get_or_create(url="https://www.r7.com/")
        UrlFound.create_table(safe=False)
        Page.create_table(safe=False)
        print("Tabelas criadas com sucesso!")

        print(get_table_name(SiteToSearch()))
        print(get_table_name(UrlFound()))
        print(get_table_name(Page()))

    except peewee.OperationalError:
        print("Ocorreu algum erro ou há alguma tabela já existente!")
        print(peewee.OperationalError.with_traceback())
        print(peewee.OperationalError.mro())



