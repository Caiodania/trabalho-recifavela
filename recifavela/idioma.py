# O Streamlit gera a página com lang="en", aí o Chrome tenta "traduzir" o site,
# que já está em português. Aqui marcamos a página como pt-BR.
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
    html = html.replace('<html lang="en">', HTML_PORTUGUES, 1)
    if META_SEM_TRADUCAO not in html:
        html = html.replace("<head>", "<head>\n    " + META_SEM_TRADUCAO, 1)
    return html


def ajustar_index_html(caminho: Path | None = None) -> bool:
    caminho = caminho or caminho_index_html()
    try:
        original = caminho.read_text(encoding="utf-8")
        ajustado = marcar_portugues(original)
        if ajustado == original:
            return False
        caminho.write_text(ajustado, encoding="utf-8")
    except OSError as erro:
        # no Streamlit Cloud a pasta é somente leitura; o script da página resolve
        print(f"[recifavela] não foi possível marcar {caminho} como pt-BR: {erro}", file=sys.stderr)
        return False
    return True


@functools.cache
def ajustar_index_html_uma_vez() -> bool:
    return ajustar_index_html()


def declarar_na_pagina() -> None:
    st.html(_SCRIPT_PORTUGUES, unsafe_allow_javascript=True)
