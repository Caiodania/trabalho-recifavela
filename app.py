"""ReciFavela · Descarte Certo — ponto de entrada do site.

Execute com:  streamlit run app.py
"""

import streamlit as st

from recifavela import idioma, projeto, ui

# Declara a página em português para o navegador não "traduzir" o site (ver recifavela/idioma.py).
idioma.ajustar_index_html()

st.set_page_config(
    page_title="ReciFavela · Descarte Certo",
    page_icon="♻️",
    layout="wide",
    menu_items={"About": "ReciFavela · Descarte Certo — protótipo acadêmico de identificação de resíduos."},
)
ui.aplicar_estilo()
st.logo("assets/logo.svg", size="large", icon_image="assets/icone.svg")

pagina = st.navigation(
    [
        st.Page("paginas/analisar.py", title="Analisar resíduo", icon="♻️", default=True),
        st.Page("paginas/validacao.py", title="Validação do protótipo", icon="📊"),
        st.Page("paginas/sobre.py", title="Sobre o projeto", icon="💡"),
    ]
)

with st.sidebar:
    st.markdown("##### Como usar")
    st.markdown(
        "1. Fotografe **um resíduo por vez**.\n"
        "2. Confira o material identificado.\n"
        "3. Responda às perguntas sobre as condições.\n"
        "4. Siga as orientações de preparo e descarte."
    )
    st.divider()
    st.caption(f"Protótipo acadêmico · {projeto.linha_academica()}")

pagina.run()
