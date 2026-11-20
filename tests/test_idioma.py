from recifavela.idioma import HTML_PORTUGUES, META_SEM_TRADUCAO, ajustar_index_html, marcar_portugues

HTML_STREAMLIT = '<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n  </head>\n</html>\n'


def test_marca_idioma_e_desliga_traducao():
    html = marcar_portugues(HTML_STREAMLIT)
    assert HTML_PORTUGUES in html
    assert 'lang="en"' not in html
    assert html.count(META_SEM_TRADUCAO) == 1


def test_marcacao_e_idempotente():
    uma_vez = marcar_portugues(HTML_STREAMLIT)
    assert marcar_portugues(uma_vez) == uma_vez


def test_ajusta_arquivo_uma_unica_vez(tmp_path):
    arquivo = tmp_path / "index.html"
    arquivo.write_text(HTML_STREAMLIT, encoding="utf-8")
    assert ajustar_index_html(arquivo) is True
    assert HTML_PORTUGUES in arquivo.read_text(encoding="utf-8")
    assert ajustar_index_html(arquivo) is False


def test_arquivo_inexistente_nao_quebra_o_site(tmp_path):
    assert ajustar_index_html(tmp_path / "nao_existe.html") is False
