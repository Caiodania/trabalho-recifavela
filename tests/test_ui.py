"""Testes dos utilitários de formatação da interface."""

from recifavela.ui import pct, texto_html


def test_porcentagem_no_formato_brasileiro():
    assert pct(0.915, 1) == "91,5%"
    assert pct(0.8) == "80%"


def test_texto_html_escapa_e_converte_negrito():
    assert texto_html("Separe na lixeira **azul** <b>") == "Separe na lixeira <b>azul</b> &lt;b&gt;"
