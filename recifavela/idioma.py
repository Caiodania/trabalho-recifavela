"""Declara a página como português, para o navegador não "traduzir" o site.

O Streamlit serve um ``index.html`` com ``<html lang="en">``. Com isso, navegadores com tradução
automática (como o Chrome) acham que o site está em inglês e "traduzem" um texto que já está em
português ("Fotografe um resíduo" vira "Fotografe uma destruição"), e leitores de tela leem o
conteúdo com pronúncia de inglês. A correção é feita em duas camadas:

1. :func:`ajustar_index_html_uma_vez` grava ``pt-BR`` e o aviso "não traduzir" no próprio
   ``index.html`` (vale desde o carregamento da página; funciona quando a instalação do
   Streamlit permite escrita, como no computador local).
2. :func:`declarar_na_pagina` faz o mesmo na página já aberta, via JavaScript (funciona também
   onde a instalação é somente leitura, como no Streamlit Community Cloud).
"""

import functools
import sys
from pathlib import Path

import streamlit as st

HTML_PORTUGUES = '<html lang="pt-BR" translate="no">'
META_SEM_TRADUCAO = '<meta name="google" content="notranslate" />'

_SCRIPT_PORTUGUES = """<script>
(function () {
  var raiz = document.documentElement;
  raiz.lang = "pt-BR";
  raiz.setAttribute("translate", "no");
  raiz.classList.add("notranslate");
  if (!document.querySelector('meta[name="google"][content="notranslate"]')) {
    var meta = document.createElement("meta");
    meta.name = "google";
    meta.content = "notranslate";
    document.head.appendChild(meta);
  }
})();
</script>"""


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
    except OSError as erro:
        print(f"[recifavela] não foi possível marcar {caminho} como pt-BR: {erro}", file=sys.stderr)
        return False
    print(f"[recifavela] {caminho} marcado como pt-BR (sem tradução automática)", file=sys.stderr)
    return True


@functools.cache
def ajustar_index_html_uma_vez() -> bool:
    """Tenta o ajuste do ``index.html`` só uma vez por processo (o app roda a cada interação)."""
    return ajustar_index_html()


def declarar_na_pagina() -> None:
    """Marca a página aberta como ``pt-BR`` e sem tradução automática (elemento invisível)."""
    st.html(_SCRIPT_PORTUGUES, unsafe_allow_javascript=True)
