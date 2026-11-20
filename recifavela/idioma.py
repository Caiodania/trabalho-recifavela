"""Declara a página como português, para o navegador não "traduzir" o site.

O Streamlit serve um ``index.html`` com ``<html lang="en">``. Com isso, navegadores com tradução
automática (como o Chrome) acham que o site está em inglês e "traduzem" um texto que já está em
português ("Fotografe um resíduo" vira "Fotografe uma destruição"), e leitores de tela leem o
conteúdo com pronúncia de inglês. Este módulo ajusta esse arquivo uma única vez: declara o idioma
``pt-BR`` e desliga a tradução automática. O Streamlit lê o arquivo do disco a cada acesso, então
o ajuste vale a partir do carregamento seguinte da página.
"""

from pathlib import Path

HTML_PORTUGUES = '<html lang="pt-BR" translate="no">'
META_SEM_TRADUCAO = '<meta name="google" content="notranslate" />'


def caminho_index_html() -> Path:
    import streamlit

    return Path(streamlit.__file__).parent / "static" / "index.html"


def marcar_portugues(html: str) -> str:
    """Troca o idioma da tag ``<html>`` e acrescenta a meta tag que desliga a tradução."""
    html = html.replace('<html lang="en">', HTML_PORTUGUES, 1)
    if META_SEM_TRADUCAO not in html:
        html = html.replace("<head>", "<head>\n    " + META_SEM_TRADUCAO, 1)
    return html


def ajustar_index_html(caminho: Path | None = None) -> bool:
    """Aplica :func:`marcar_portugues` ao ``index.html`` do Streamlit.

    Retorna ``True`` se o arquivo foi alterado. Falhas de leitura ou escrita são ignoradas:
    o site continua funcionando, apenas sem a marcação de idioma.
    """
    caminho = caminho or caminho_index_html()
    try:
        original = caminho.read_text(encoding="utf-8")
        ajustado = marcar_portugues(original)
        if ajustado == original:
            return False
        caminho.write_text(ajustado, encoding="utf-8")
    except OSError:
        return False
    return True
