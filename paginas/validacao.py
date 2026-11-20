"""Página de validação: compara a classificação do sistema com a classificação correta."""

import base64
import hashlib
import io

import pandas as pd
import streamlit as st
from PIL import UnidentifiedImageError

from recifavela import ui
from recifavela.avaliacao import EXTENSOES_IMAGEM, META_ACERTO, TOTAL_PREVISTO, inferir_categoria, resumir
from recifavela.cache import classificar
from recifavela.imagem import abrir_imagem
from recifavela.orientacoes import CATEGORIAS, MATERIAIS, Situacao

ROTULOS = {c: f"{MATERIAIS[c].emoji} {MATERIAIS[c].nome}" for c in CATEGORIAS}
CHAVE_POR_ROTULO = {v: k for k, v in ROTULOS.items()}


@st.cache_data(show_spinner=False, max_entries=300)
def miniatura(dados: bytes) -> str:
    imagem = abrir_imagem(dados)
    imagem.thumbnail((160, 160))
    buffer = io.BytesIO()
    imagem.save(buffer, format="JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()


def classificar_fotos(arquivos) -> tuple[list[dict], list[str]]:
    linhas, ignorados = [], []
    barra = st.progress(0.0, text="Classificando as fotos…")
    for i, arquivo in enumerate(arquivos, 1):
        dados = arquivo.getvalue()
        try:
            resultado = classificar(dados)
            foto = miniatura(dados)
        except UnidentifiedImageError:
            ignorados.append(arquivo.name)
            continue
        finally:
            barra.progress(i / len(arquivos), text=f"Classificando as fotos… ({i}/{len(arquivos)})")
        linhas.append(
            {
                "Foto": foto,
                "Arquivo": arquivo.name,
                "Correta": ROTULOS.get(inferir_categoria(arquivo.name)),
                "Sistema": ROTULOS[resultado.categoria],
                "Confiança": round(100 * resultado.confianca, 1),
                "Orientações adequadas?": None,
                "Observações": "",
            }
        )
    barra.empty()
    return linhas, ignorados


ui.titulo_pagina(
    "📊",
    "Validação do protótipo",
    f"Compare a classificação do sistema com a classificação correta de {TOTAL_PREVISTO} resíduos reais. "
    f"Meta: **{ui.pct(META_ACERTO)} de acerto** (24 de 30).",
)

with st.expander("📋 Como realizar o teste"):
    st.markdown(
        """
1. Separe 30 resíduos reais e defina **antes** a categoria correta de cada um
   (sugestão: 7 a 8 de cada material — plástico, papel, metal e vidro).
2. Fotografe cada resíduo individualmente.
3. Nomeie os arquivos com a categoria correta para que ela seja preenchida automaticamente
   (ex.: `plastico_01.jpg`, `vidro_garrafa.jpg`) — ou escolha a categoria na tabela.
4. Envie todas as fotos de uma vez. O sistema classifica cada uma e calcula a taxa de acerto.
5. Para avaliar as **orientações**, abra cada resíduo na página *Analisar resíduo*, responda às
   perguntas sobre as condições e registre na coluna *Orientações adequadas?* se o preparo e o
   descarte indicados estão corretos.
6. Baixe a planilha de resultados ao final para anexar ao relatório.
"""
    )

with st.container(border=True, key="cartao_5"):
    ui.secao(
        1,
        "Fotos dos resíduos de teste",
        "Dica: nomeie os arquivos com o material (ex.: plastico_01.jpg) para preencher a classificação correta",
    )
    arquivos = st.file_uploader(
        "Fotos dos resíduos de teste",
        type=[e.lstrip(".") for e in sorted(EXTENSOES_IMAGEM)],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

linhas, ignorados = classificar_fotos(arquivos) if arquivos else ([], [])
if ignorados:
    st.warning("Não foi possível abrir como imagem: " + ", ".join(ignorados))

if linhas:
    assinatura = hashlib.sha1("|".join(f"{a.name}:{a.size}" for a in arquivos).encode()).hexdigest()[:12]

    with st.container(border=True, key="cartao_6"):
        ui.secao(2, "Confira cada resíduo", "Preencha ou corrija a classificação correta e avalie as orientações")
        editado = st.data_editor(
            pd.DataFrame(linhas),
            key=f"editor_{assinatura}",
            hide_index=True,
            width="stretch",
            disabled=["Foto", "Arquivo", "Sistema", "Confiança"],
            column_config={
                "Foto": st.column_config.ImageColumn("Foto", width="small"),
                "Arquivo": st.column_config.TextColumn("Arquivo"),
                "Correta": st.column_config.SelectboxColumn(
                    "Classificação correta", options=list(ROTULOS.values())
                ),
                "Sistema": st.column_config.TextColumn("Classificação do sistema"),
                "Confiança": st.column_config.ProgressColumn(
                    "Confiança", min_value=0, max_value=100, format="%.0f%%"
                ),
                "Orientações adequadas?": st.column_config.SelectboxColumn(
                    "Orientações adequadas?", options=["Sim", "Não"]
                ),
                "Observações": st.column_config.TextColumn("Observações"),
            },
        )

    correta = editado["Correta"].map(CHAVE_POR_ROTULO)
    sistema = editado["Sistema"].map(CHAVE_POR_ROTULO)
    resumo = resumir(correta, sistema)

    with st.container(border=True, key="cartao_7"):
        ui.secao(3, "Resultado da validação")

        sem_gabarito = int(correta.isna().sum())
        if sem_gabarito:
            st.warning(
                f"{sem_gabarito} foto(s) sem classificação correta definida. Preencha a coluna "
                "**Classificação correta** para incluí-las no cálculo."
            )

        if resumo.total:
            avaliadas = editado["Orientações adequadas?"].dropna()
            c1, c2, c3 = st.columns(3)
            c1.metric("Acertos", f"{resumo.acertos} de {resumo.total}", border=True)
            c2.metric(
                "Taxa de acerto",
                ui.pct(resumo.acuracia, 1),
                delta=f"{100 * (resumo.acuracia - META_ACERTO):+.1f}".replace(".", ",") + " p.p. da meta",
                border=True,
            )
            c3.metric(
                "Orientações adequadas",
                f"{(avaliadas == 'Sim').sum()} de {len(avaliadas)}" if len(avaliadas) else "—",
                help="Quantos resíduos avaliados receberam orientações de preparo e descarte adequadas.",
                border=True,
            )

            if resumo.meta_atingida:
                ui.destaque(
                    "🎯",
                    "Meta atingida",
                    f"{ui.pct(resumo.acuracia, 1)} de acerto — o mínimo exigido é {ui.pct(META_ACERTO)}.",
                )
            else:
                faltam = resumo.acertos_necessarios - resumo.acertos
                ui.destaque(
                    "📉",
                    "Meta não atingida",
                    f"{ui.pct(resumo.acuracia, 1)} de acerto. Seriam necessários "
                    f"{resumo.acertos_necessarios} acertos em {resumo.total} ({faltam} a mais).",
                    Situacao.NAO_RECICLAVEL,
                )
            if resumo.total != TOTAL_PREVISTO:
                st.caption(f"O protocolo prevê {TOTAL_PREVISTO} resíduos; foram considerados {resumo.total}.")

            por_categoria = resumo.por_categoria.assign(
                **{"Acerto (%)": lambda d: d["Acerto (%)"].map(lambda v: "—" if pd.isna(v) else f"{v:.1f}%".replace(".", ","))}
            )
            ui.subtitulo("Acerto por material")
            st.dataframe(por_categoria, hide_index=True, width="stretch")
            ui.subtitulo("Matriz de confusão")
            st.caption("Linhas: classificação correta · colunas: classificação do sistema")
            st.dataframe(resumo.matriz_confusao, width="stretch")

            erros = editado[correta.notna() & (correta != sistema)]
            if len(erros):
                ui.subtitulo("Resíduos classificados incorretamente")
                st.dataframe(
                    erros[["Foto", "Arquivo", "Correta", "Sistema", "Confiança"]],
                    hide_index=True,
                    width="stretch",
                    column_config={
                        "Foto": st.column_config.ImageColumn("Foto", width="small"),
                        "Confiança": st.column_config.NumberColumn("Confiança", format="%.0f%%"),
                    },
                )

        planilha = editado.drop(columns=["Foto"]).assign(
            Acertou=(correta == sistema).where(correta.notna()).map({True: "Sim", False: "Não"})
        )
        st.download_button(
            "Baixar resultados (CSV)",
            planilha.to_csv(index=False, sep=";").encode("utf-8-sig"),
            file_name="validacao_recifavela.csv",
            mime="text/csv",
            icon=":material/download:",
            type="primary",
        )
elif not arquivos:
    st.info("Envie as fotos para iniciar a validação.", icon="📁")

ui.rodape()
