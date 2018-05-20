from comprasnet.pages.ata_pregao import AtaPregao
import requests_mock
import pytest


@pytest.fixture
def ata_pregao():
    return AtaPregao(1234, 987)


def test_to_json_should_return_a_dict(ata_pregao):
    assert ata_pregao.to_json() == '{}'


def test_url(ata_pregao):
    expected = "http://comprasnet.gov.br/livre/pregao/ata2.asp?co_no_uasg=1234&numprp=987"
    assert ata_pregao.url == expected


def test_get_params(ata_pregao):
    expected = dict(co_no_uasg=1234, numprp=987)
    assert ata_pregao.get_params() == expected


def test_get_data(ata_pregao):
    with requests_mock.mock() as mock:
        mock.get(ata_pregao.url, text="Success")
        assert ata_pregao.get_data() == "Success"