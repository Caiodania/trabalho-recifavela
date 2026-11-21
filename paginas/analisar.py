import hashlib

import streamlit as st
from PIL import UnidentifiedImageError

from recifavela import ui
from recifavela.cache import classificar
from recifavela.imagem import abrir_imagem
from recifavela.orientacoes import CATEGORIAS, MATERIAIS, avaliar

LIMIAR_CONFIANCA = 0.60  # abaixo disso avisamos que a análise ficou em dúvida


def nome_material(chave: str) -> str:
    m = MATERIAIS[chave]
    return f"{m.emoji} {m.nome}"


ui.cabecalho()

col_foto, col_resultado = st.columns([5, 7], gap="large")

# 1. foto
with col_foto:
    with st.container(border=True, key="cartao_foto"):
        ui.secao(1, "Foto do resíduo", "Envie uma imagem ou use a câmera")
        opcoes = ["🖼️ Enviar imagem", "📷 Tirar foto"]
        origem = st.segmented_control(
            "Como enviar a foto",
            opcoes,
            default=opcoes[0],
            required=True,
            label_visibility="collapsed",
            width="stretch",
        ) or opcoes[0]

        if origem == opcoes[1]:
            arquivo = st.camera_input("Aponte a câmera para o resíduo")
        else:
            arquivo = st.file_uploader(
                "Selecione uma foto do resíduo",
                type=["jpg", "jpeg", "png", "webp", "bmp"],
                help="No celular, esta opção também permite usar a câmera.",
            )

        dados = arquivo.getvalue() if arquivo else None
        imagem = None
        if dados:
            try:
                imagem = abrir_imagem(dados)
            except UnidentifiedImageError:
                st.error("Não foi possível abrir este arquivo como imagem. Tente outra foto.")
            else:
                st.image(imagem, width="stretch")

        st.caption(
            "💡 **Dica:** fotografe um item por vez, de perto, com boa luz e, se possível, sobre um fundo liso."
        )

# 2. resultado
with col_resultado:
    with st.container(border=True, key="cartao_2"):
        ui.secao(2, "Material identificado", "Análise feita por visão computacional")

        if imagem is None:
            ui.estado_vazio()
        else:
            with st.spinner("Analisando a imagem… a primeira análise demora mais porque o modelo é carregado."):
                resultado = classificar(dados)

            id_imagem = hashlib.sha1(dados).hexdigest()[:12]
            espaco_cartao = st.container()
            chave = st.selectbox(
                "Não é esse material? Corrija aqui:",
                CATEGORIAS,
                index=CATEGORIAS.index(resultado.categoria),
                format_func=nome_material,
                key=f"material_{id_imagem}",
            )
            corrigido = chave != resultado.categoria
            material = MATERIAIS[chave]

            with espaco_cartao:
                ui.cartao_material(material, resultado.confianca, corrigido)
                if not corrigido and resultado.confianca < LIMIAR_CONFIANCA:
                    segundo = list(resultado.probabilidades)[1]
                    st.warning(
                        f"A análise ficou em dúvida entre **{nome_material(chave)}** e "
                        f"**{nome_material(segundo)}**. Confira o material antes de seguir.",
                        icon="🤔",
                    )

            with st.expander("Como o sistema chegou a esse resultado?"):
                st.caption(
                    "O modelo compara a foto com descrições de objetos de cada material e calcula a "
                    "probabilidade de cada um:"
                )
                ui.barras_probabilidades(resultado.probabilidades)

    if imagem is not None:
        # 3. condições
        with st.container(border=True, key="cartao_3"):
            ui.secao(3, "Condições do resíduo", "Marque o que se aplica — o resultado se ajusta às respostas")
            respostas = {
                p.id: st.checkbox(p.texto, key=f"{id_imagem}_{chave}_{p.id}", help=p.exemplo or None)
                for p in material.perguntas
            }

        # 4. orientações
        avaliacao = avaliar(chave, respostas)
        with st.container(border=True, key="cartao_4"):
            ui.secao(4, "Resultado e orientações")
            ui.cartao_situacao(avaliacao.situacao)
            ui.alertas(avaliacao.alertas)
            if avaliacao.preparo:
                ui.subtitulo("Como preparar")
                ui.lista_passos(avaliacao.preparo)
            ui.subtitulo("Onde descartar")
            ui.cartao_descarte(material, avaliacao.situacao, avaliacao.descarte)

ui.rodape()
