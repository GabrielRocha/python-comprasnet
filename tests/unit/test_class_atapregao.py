import requests_mock


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


def test_result_per_provider_scrap_data(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/FornecedorResultado.asp?prgcod=712965&strTipoPregao=E"
    result = auction_minute.scrap_data()
    assert "result_per_provider" in result
    assert result["result_per_provider"] == expected


def test_declaration_scrap_data(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/declaracoesProposta.asp?prgCod=712965"
    result = auction_minute.scrap_data()
    assert "declaration" in result
    assert result["declaration"] == expected


def test_get_result_per_provider_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/FornecedorResultado.asp?prgcod=712965&strTipoPregao=E"
    result = auction_minute.get_result_per_provider_url()
    assert result == expected


def test_get_declaration_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/declaracoesProposta.asp?prgCod=712965"
    result = auction_minute.get_declaration_url()
    assert result == expected
