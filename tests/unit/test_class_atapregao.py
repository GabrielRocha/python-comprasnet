from collections import namedtuple

from bs4 import BeautifulSoup
from comprasnet.pages.auction_minutes import AtaPregao
from unittest import mock
import requests_mock
import pytest
import os


@mock.patch('comprasnet.pages.auction_minutes.requests.get')
@pytest.fixture
def auction_minute(get):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '../assets/result_minutes_auction.html')
    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = 200
    with open(path) as html:
        MockResponse.text = html.read()
    get.return_value = MockResponse
    return AtaPregao(1234, 987)


def test_to_json_should_return_a_dict(auction_minute):
    assert auction_minute.to_json() == '{}'


def test_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/ata2.asp?co_no_uasg=1234&numprp=987"
    assert auction_minute.url == expected


def test_get_params(auction_minute):
    expected = dict(co_no_uasg=1234, numprp=987)
    assert auction_minute.get_params() == expected


def test_get_data(auction_minute):
    with requests_mock.mock() as mock:
        mock.get(auction_minute.url, text="Success")
        assert auction_minute.get_data() == "Success"


@pytest.mark.xfail(reason="Not Implemented")
def test_get_result_per_provider_link(auction_minute, bs_object):
    expected = "http://comprasnet.gov.br/livre/pregao/FornecedorResultado.asp?\
    prgcod=712965&strTipoPregao=E"
    assert auction_minute.get_result_per_provider_link(bs_object) == expected


def test_clean_onlick_function(auction_minute):
    text = "javascript:resultadoFornecedor(712965);"
    result = auction_minute._clean_onlick_function(text)
    assert result['function_name'] == "resultadoFornecedor"
    assert result['parameters'] == ["712965"]


def test_clean_onlick_function_multiple_parameters(auction_minute):
    text = "javascript:resultadoFornecedor(712965, 123, 9);"
    result = auction_minute._clean_onlick_function(text)
    assert result['function_name'] == "resultadoFornecedor"
    assert result['parameters'] == ["712965", "123", "9"]


def test_find_js_function(auction_minute):
    result = auction_minute._find_js_function("teste")
    expected = 'function teste() { if(true){document.location.href = "Here?parameter=" + coduasg;}}'
    assert result == expected


def test_find_link_inside_function(auction_minute):
    result = auction_minute.find_link_inside_function("teste")
    expected = '"Here?parameter=" + coduasg'
    assert result == expected


def test_get_href_ref(auction_minute):
    result = auction_minute.get_href_ref("teste")
    expected = '"Here?parameter=" + coduasg'
    assert result == expected


def test_get_href_url_var_ref(auction_minute):
    result = auction_minute.get_href_ref("teste_url")
    expected = '"Here?parameter=" + coduasg'
    assert result == expected


def test_get_windows_open_url_var_ref(auction_minute):
    result = auction_minute.get_windows_open_ref("teste_open_url")
    expected = '"here"'
    assert result == expected


def test_get_windows_open_ref(auction_minute):
    result = auction_minute.get_windows_open_ref("teste_open")
    expected = '"path"'
    assert result == expected