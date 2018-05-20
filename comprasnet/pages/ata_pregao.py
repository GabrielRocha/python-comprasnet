from urllib.parse import urlencode
from . import BaseDetail, log
import requests
import json


class AtaPregao(BaseDetail):
    DETAIL_URL = "http://comprasnet.gov.br/livre/pregao/ata2.asp"

    def __init__(self, co_no_uasg, numprp):
        self.co_no_uasg = co_no_uasg
        self.numprp = numprp

    @property
    def url(self):
        return '{url}?{parameters}'.format(url=self.DETAIL_URL,
                                           parameters=urlencode(self.get_params()))

    def get_params(self):
        params = {"co_no_uasg": self.co_no_uasg,
                  "numprp": self.numprp}
        return self._order_params(params)

    def get_data(self):
        response = requests.get(self.DETAIL_URL, params=self.get_params())
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get "Ata" from "Pregão" {}/{}. Status code: {}'.format(
                self.co_no_uasg, self.numprp, response.status_code
            ))
            return
        return response.text

    def to_json(self):
        return json.dumps({})