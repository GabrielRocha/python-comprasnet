import logging


log = logging.getLogger('comprasnet')


class BaseDetail:
    DETAIL_URL = None

    def __init__(self, uasg_code, auction_code, *args, **kwargs):
        self.uasg_code = uasg_code
        self.auction_code = auction_code

    def get_params(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def scrap_data(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @property
    def data(self):
        return self.scrap_data()

    def __str__(self):
        return "{}/{}".format(self.uasg_code, self.auction_code)
