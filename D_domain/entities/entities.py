

class UrlFoundEntityDomain:
    url = None
    nofollow = None


class SiteToSearchEntityDomain:
    url = None

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return other == self.url


if __name__ == '__main__':
    site_to_search = SiteToSearchEntityDomain()
    site_to_search.url = 'dsdsdsds'
    sites_list = [site_to_search]
    print('dsdsdsds' in sites_list)
