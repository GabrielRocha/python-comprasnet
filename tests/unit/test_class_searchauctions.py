import codecs
import os
import pytest
from collections import namedtuple
from datetime import date
from unittest import mock

import requests

from comprasnet.pages.search_auctions import SearchAuctions


def test_class_attributes_and_properties():
    search_auctions = SearchAuctions(date.today())
    assert search_auctions.day == date.today()
    assert search_auctions.total_results == 0
    assert search_auctions.current_page == 1
    assert search_auctions.SEARCH_URL == \
           "http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp"
    assert search_auctions.OFFSET == 10

    assert search_auctions.total_pages == 0
    assert search_auctions.is_done is True

    search_auctions.total_results = 27
    assert search_auctions.total_pages == 3
    assert search_auctions.is_done is False
    search_auctions.current_page = 4
    assert search_auctions.is_done is True


def test_method_get_search_params():
    search_auctions = SearchAuctions()
    expected = ['chkModalidade', 'chkTodos', 'chk_concor', 'chk_concorTodos', 'chk_pregao', 'chk_pregaoTodos',
                'chk_rdc', 'dt_publ_fim', 'dt_publ_ini', 'numpag', 'numprp', 'optTpPesqMat', 'optTpPesqServ',
                'txtObjeto', 'txtlstClasMaterial', 'txtlstGrpMaterial', 'txtlstGrpServico', 'txtlstMaterial',
                'txtlstMunicipio', 'txtlstServico', 'txtlstUasg', 'txtlstUf']
    assert sorted(search_auctions.get_search_params().keys()) == expected


@mock.patch('comprasnet.pages.search_auctions.requests.get')
def test_method_get_search_metadata(get):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/result_page_sample.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_result_content = handle.read()

    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = requests.codes.ok
    MockResponse.text = page_result_content
    get.return_value = MockResponse

    search_auctions = SearchAuctions()
    search_auctions.get_search_metadata()
    assert search_auctions.total_results == 183
    assert search_auctions.total_pages == 19
    assert get.called_with(search_auctions.SEARCH_URL, search_auctions.get_search_params())


@pytest.mark.xfail(reason="Not Implemented")
def test_method_get_search_page_data():
    assert False


@pytest.mark.xfail(reason="Not Implemented")
def test_method_scrap_search_page():
    assert False
