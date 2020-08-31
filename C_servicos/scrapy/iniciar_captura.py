import os


class Start:

    def run(self):
        path = os.path.dirname(__file__)
        # navegar o command até a pasta do scrapy
        os.chdir(f'{path}/get_news')
        # rodar scrapy

        os.system(" scrapy crawl news")


# Para testar módulo diretamente
if __name__ == '__main__':
    start = Start()
    start.run()