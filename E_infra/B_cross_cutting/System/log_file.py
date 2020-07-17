import os


def log_file(file_name, link):
    """ Log in file for debug """

    path = os.path.join('..', '..', '..', 'logs', file_name)

    with open(path, 'a+') as file:
        file.write(str(link))
        file.write('\n')
        file.close()