"""Página institucional: objetivo, funcionamento, tecnologia, validação e equipe."""

import streamlit as st

from recifavela import projeto, ui
from recifavela.avaliacao import META_ACERTO, TOTAL_PREVISTO
from recifavela.config import MODELO_PADRAO

ui.titulo_pagina(
    "💡",
    "Sobre o projeto",
    "Tecnologia para reduzir dúvidas sobre reciclagem e facilitar a separação dos resíduos na ReciFavela.",
)

with st.container(border=True, key="cartao_8"):
    ui.secao("?", "O problema")
    st.markdown(
        "Muitos resíduos chegam à cooperativa **misturados, sujos ou separados de forma errada**. "
        "Isso reduz o valor do material, aumenta o trabalho de triagem e pode causar acidentes — "
        "como cacos de vidro sem proteção. Boa parte desses erros vem de **dúvidas simples**: "
        "*“isso é reciclável?”*, *“preciso lavar?”*, *“em qual lixeira vai?”*."
    )

with st.container(border=True, key="cartao_9"):
    ui.secao("✓", "A solução", "Um site simples, que funciona no celular")
    ui.fluxo(
        [
            ("📷", "Foto", "A pessoa tira uma foto ou envia uma imagem do resíduo."),
            ("🧠", "Visão computacional", "O modelo identifica o material: plástico, papel, metal ou vidro."),
            ("❓", "Condições", "Perguntas rápidas: está sujo? quebrado? é metalizado? é lâmpada?"),
            ("♻️", "Orientação", "O site diz se é reciclável, como preparar e onde descartar."),
        ]
    )

col_a, col_b = st.columns(2, gap="medium")
with col_a, st.container(border=True, key="cartao_10", height="stretch"):
    ui.secao("⚙", "Tecnologia")
    st.markdown(
        f"""
- **Python** e **Streamlit** na interface web.
- **CLIP** (`{MODELO_PADRAO}`), modelo de visão computacional da OpenAI que relaciona
  imagens e textos. Ele é usado em modo *zero-shot*: a foto é comparada com descrições de
  objetos de cada material, **sem necessidade de treinar o modelo** com fotos próprias.
- **Base de conhecimento** com as regras de reciclabilidade, as perguntas sobre as condições e
  as orientações de preparo e descarte de cada material.
"""
    )
with col_b, st.container(border=True, key="cartao_11", height="stretch"):
    ui.secao("📏", "Validação")
    st.markdown(
        f"""
- **{TOTAL_PREVISTO} resíduos reais** são fotografados e a classificação do sistema é comparada
  com a classificação correta, definida antes do teste.
- **Meta:** pelo menos **{ui.pct(META_ACERTO)} de acerto** (24 de 30).
- As orientações de preparo e descarte também são avaliadas, de preferência com a equipe da
  cooperativa.
- O teste é feito na página *Validação do protótipo*, que gera a taxa de acerto, a matriz de
  confusão e uma planilha para o relatório.
"""
    )

with st.container(border=True, key="cartao_12"):
    ui.secao("🧪", "Teste preliminar", "Antes do teste com resíduos reais")
    st.markdown(
        "O classificador foi conferido com fotos do conjunto público **TrashNet**. Esse resultado "
        "serve apenas como referência: as fotos têm fundo branco e iluminação controlada, diferente "
        "do uso real na cooperativa."
    )
    m1, m2, m3 = st.columns(3)
    m1.metric("Inicial · 200 fotos", "83,0%", border=True)
    m2.metric("Final · 200 fotos", "91,5%", delta="+8,5 p.p.", border=True)
    m3.metric("Protocolo simulado · 30 fotos", "93,3%", delta="28 de 30", border=True)

with st.container(border=True, key="cartao_13"):
    ui.secao("👥", "Equipe")
    ui.equipe()
    orientacao = f" — Orientação: {projeto.ORIENTACAO}" if projeto.ORIENTACAO else ""
    st.caption(projeto.linha_academica() + orientacao)

with st.expander("📚 Referências"):
    st.markdown(
        """
- BRASIL. Conselho Nacional do Meio Ambiente. **Resolução CONAMA nº 275, de 25 de abril de 2001.**
  Estabelece o código de cores para os diferentes tipos de resíduos.
- BRASIL. **Lei nº 12.305, de 2 de agosto de 2010.** Institui a Política Nacional de Resíduos
  Sólidos (logística reversa de pilhas, baterias, lâmpadas, eletrônicos e embalagens de agrotóxicos).
- RADFORD, A. et al. **Learning Transferable Visual Models From Natural Language Supervision.**
  Proceedings of the 38th International Conference on Machine Learning (ICML), 2021.
- YANG, M.; THUNG, G. **Classification of Trash for Recyclability Status.** CS229 Project Report,
  Stanford University, 2016. (Conjunto de dados TrashNet.)
"""
    )

ui.rodape()
