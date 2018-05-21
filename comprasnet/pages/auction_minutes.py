from urllib.parse import urlencode
from comprasnet.parser.javascript import JavaScriptParser
from . import BaseDetail, log
from bs4 import BeautifulSoup
import requests
import json


class AtaPregao(BaseDetail):

    ROOT_URL = "http://comprasnet.gov.br/livre/pregao/"
    DETAIL_URL = "{}ata2.asp".format(ROOT_URL)

    def __init__(self, co_no_uasg, numprp):
        self.co_no_uasg = co_no_uasg
        self.numprp = numprp
        self._data = self.get_data()
        self.bs_object = BeautifulSoup(self._data, "html.parser")
        self.js_parser = JavaScriptParser(self._data)

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

    def scrap_data(self):
        return {"result_per_provider": self.get_result_per_provider_url(),
                "declaration": self.get_declaration_url(),
                "terms_of_adjudication": self.get_terms_of_adjudication_url(),
                "clarification": self.get_clarification_url()
                }

    def get_result_per_provider_url(self):
        return "{}{}".format(self.ROOT_URL,
                             self.js_parser.get_onclick_function_link("btnResultadoFornecr"))

    def get_declaration_url(self):
        return "{}{}".format(self.ROOT_URL,
                             self.js_parser.get_onclick_function_link("btnDeclaracoes"))

    def get_terms_of_adjudication_url(self):
        return "{}{}".format(self.ROOT_URL,
                             self.js_parser.get_onclick_function_link("btnTermAdj"))

    def get_clarification_url(self):
        return "{}{}".format(self.ROOT_URL,
                             self.js_parser.get_onclick_function_link("esclarecimento"))

    def to_json(self):
        return json.dumps({})
