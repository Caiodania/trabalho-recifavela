"""Carregamento do modelo e classificação com cache do Streamlit (compartilhado entre páginas).

O modelo (torch/transformers) só é importado na primeira análise, para a página abrir rápido.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from .classificador import ClassificadorMateriais, Resultado


@st.cache_resource(
    show_spinner="Carregando o modelo de visão computacional… (na primeira execução ele é baixado e pode levar alguns minutos)"
)
def obter_classificador() -> ClassificadorMateriais:
    from .classificador import ClassificadorMateriais

    return ClassificadorMateriais()


@st.cache_data(show_spinner=False, max_entries=300)
def classificar(dados: bytes) -> Resultado:
    return obter_classificador().classificar(dados)
