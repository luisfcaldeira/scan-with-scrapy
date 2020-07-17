import re


def split_url(url: str):
    """ You must pass a valid url or I`ll raise an exception instead return a tuple """

    compiled = re.compile(
        '(?:https?\:\/\/)?([A-z0-9]+)\.([A-z0-9]+)\.?([A-z0-9]+)?\.?([A-z0-9]{2})?\.?(?:(?:\/[a-z]+)+(?:\/\#.+)?)?')
    match = compiled.match(url)

    if match is None:
        raise AttributeError('The url attribute is not a valid url')

    return match.groups()


if __name__ == '__main__':
    group = split_url('https://www.terra.com.br/#trr-ctn-general')
    print(group)