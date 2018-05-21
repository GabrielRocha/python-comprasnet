from urllib.parse import urlencode
from . import BaseDetail, log
from bs4 import BeautifulSoup
import requests
import json
import re


class AtaPregao(BaseDetail):

    REGEX_JS = re.compile("^javascript\:(\w*)\(([\w*| |\,|]*)\)\;$")
    ROOT_URL = "http://comprasnet.gov.br/livre/pregao/"
    DETAIL_URL = "{}ata2.asp".format(ROOT_URL)

    def __init__(self, co_no_uasg, numprp):
        self.co_no_uasg = co_no_uasg
        self.numprp = numprp
        self.bs_object = BeautifulSoup(self.get_data(), "html.parser")

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
        result_per_provider = "{}{}".format(self.ROOT_URL, self.get_link("btnResultadoFornecr"))
        declaration = "{}{}".format(self.ROOT_URL, self.get_link("btnDeclaracoes"))
        return {"result_per_provider": result_per_provider,
                "declaration": declaration}

    def _find_js_code(self):
        try:
            return self.bs_object.find_all('script', src=lambda x: x is None)[0].text
        except IndexError:
            log.error()
            return []

    def _find_js_function(self, function_name):
        js_code = self._find_js_code()
        begin = js_code.find("function {}(".format(function_name))
        br = js_code[begin:].find("{") + 1
        while True:
            next_br = js_code[begin + br:].find("{")
            next_end = js_code[begin + br:].find("}")
            if next_end <= next_br or (next_br or next_end) == -1:
                end = begin + br + next_end + 1
                break
            else:
                br += next_end + 1
        return js_code[begin: end]

    def find_link_inside_function(self, function_name):
        return self.get_href_ref(function_name) or self.get_windows_open_ref(function_name)

    def _build_parameters(self, function_name, parameters):
        try:
            regex = r"function[| ]*(\w*)\(([\w*| |\,|]*)\)"
            text = self._find_js_function(function_name)
            groups = re.search(regex, text).groups()[1]
            parameters_names = [parameter.strip() for parameter in groups.split(",")]
            return dict(zip(parameters_names, parameters))
        except IndexError:
            return {}

    def _create_url_with_parameters(self, url, parameters):
        for name, value in parameters.items():
            regex = "\+[ |]*({})".format(name)
            url = re.sub(regex, str(value), url)
        return re.sub(r"\'|\"|\+| ", "", url)

    def get_href_ref(self, function_name):
        try:
            text = self._find_js_function(function_name)
            regex = r'document\.location\.href[ |]*\=[ |]*([\w|\.\?|\=|\+| |\"|\&]*)'
            match = re.search(regex, text, re.MULTILINE)
            url = match.groups()[0]
            if url == "url":
                return self.get_url_by_variable(text)
            return url
        except (IndexError, AttributeError):
            return

    def get_windows_open_ref(self, function_name):
        try:
            text = self._find_js_function(function_name)
            match = re.search(r'window\.open\(([ |]*([\w|\.\?|\=|\+| |\"|\'|\&]*))',
                              text, re.MULTILINE)
            url = match.groups()[0]
            if url == "url":
                return self.get_url_by_variable(text)
            return url
        except (IndexError, AttributeError):
            return

    def get_url_by_variable(self, text):
        try:
            match = re.search(r'url[ |]*\=([ |]*([\w|\.\?|\=|\+| |\"|\'|\&]*))',
                              text, re.MULTILINE)
            return match.groups()[0].strip()
        except IndexError:
            return

    def _clean_onlick_function(self, function):
        try:
            groups = self.REGEX_JS.match(function).groups()
            function_name = groups[0]
            parameters = [parameter.strip() for parameter in groups[-1].split(",")]
            return {"name": function_name, "parameters": parameters}
        except AttributeError:
            return {"name": "", "parameters": ""}

    def get_link(self, id):
        element = self.bs_object.find(id=id)
        try:
            function = self._clean_onlick_function(element['onclick'])
            url = self.find_link_inside_function(function['name'])
            dict_parameters = self._build_parameters(function['name'],
                                                     function['parameters'])
            return self._create_url_with_parameters(url, dict_parameters)
        except KeyError:
            log.error()

    def to_json(self):
        return json.dumps({})
