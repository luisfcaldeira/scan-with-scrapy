from peewee import Model, CharField, DateTimeField, ForeignKeyField, TextField, OperationalError, ProgrammingError
import datetime
import inspect

from E_infra.A_data.config_db import Config
from E_infra.B_cross_cutting.System.uteis import get_obj_name

config_db = Config()
db = config_db.get_db('crawling_news')


def make_table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower() + '_tbl'


def get_table_name(model_class):
    if inspect.isclass(model_class):
        return get_obj_name(model_class()).lower() + '_tbl'

    if isinstance(model_class, object):
        return get_obj_name(model_class).lower() + '_tbl'

    raise AttributeError("The model_class attribute must to be a class or an object. Provide a correct type")


class BaseModel(Model):
    """Classe model base"""

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = db
        table_function = make_table_name


class SiteToSearch(BaseModel):

    url = CharField(max_length=2083, unique=True)
    first_inclusion = DateTimeField(default=datetime.datetime.now)
    last_updated = DateTimeField(null=True)


class UrlFound(BaseModel):

    url = CharField(max_length=2083, unique=True)
    first_inclusion = DateTimeField(default=datetime.datetime.now)
    last_updated = DateTimeField(null=True)
    referral_url = CharField(max_length=2083, null=True)


class Page(BaseModel):

    url = ForeignKeyField(UrlFound)
    date_inclusion = DateTimeField(default=datetime.datetime.now)
    title = TextField(null=True)


class PageElement(BaseModel):

    url = ForeignKeyField(UrlFound)
    tag = CharField(max_length=50, null=False)
    classes = CharField(max_length=255, null=True)
    id_attr = CharField(max_length=255, null=True)
    value = TextField(null=False)
    date_inclusion = DateTimeField(default=datetime.datetime.now)


def create_tables():

    try:

        SiteToSearch.create_table(safe=False, )
        # SiteToSearch.get_or_create(url="https://www.terra.com.br/")
        # SiteToSearch.get_or_create(url="https://www.r7.com/")
        SiteToSearch.get_or_create(url="http://g1.globo.com/")
        UrlFound.create_table(safe=False)
        Page.create_table(safe=False)
        PageElement.create_table(safe=False)
        print("Tabelas criadas com sucesso!\n")

        print(get_table_name(SiteToSearch()))
        print(get_table_name(UrlFound()))
        print(get_table_name(Page()))
        print(get_table_name(PageElement()))

        return True
    except ProgrammingError:
        print("A tabela já existe. Dropando tabelas\n")
        delete_tables()
    except OperationalError:
        print("Ocorreu algum erro ou há alguma tabela já existente!")
        print(OperationalError.with_traceback())
        print(OperationalError.mro())

    return False

def delete_tables():

    print(r'======================================== CUIDADO ========================================')
    print(r'Você irá remover as tabelas e essa ação é irreversível! Tem certeza que deseja continuar?')
    resposta = input(r"'s' ou 'n'. Qualquer valor para abortar.")
    print(r'=========================================================================================')

    if resposta != 's':
        exit()

    try:
        print('Prosseguindo...\n')
        SiteToSearch.drop_table(safe=False)
        Page.drop_table(safe=False)
        PageElement.drop_table(safe=False)
        UrlFound.drop_table(safe=False)

    except Exception as e:
        print("Erro ao tentar excluir tabelas", "\n", e)

    finally:
        create_tables()

if __name__ == '__main__':
    # model = SiteToSearch()
    # search_url = f'%terra.com.br%'
    # result = model.select().where(SiteToSearch.url % search_url).get()
    # print(result)

    create_tables()



