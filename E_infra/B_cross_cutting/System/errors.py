

class DBNotFound(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class RepeatedUrl(Exception):
    pass

class SiteNotInSearchList(Exception):
    pass


class NoFollowUrl(Exception):
    pass