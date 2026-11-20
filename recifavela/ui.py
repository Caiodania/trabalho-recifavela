"""Identidade visual do site: estilos globais e componentes em HTML.

Cores da marca: verde (sustentabilidade), areia (fundo acolhedor) e laranja-terracota
(o sol de Recife). As cores das lixeiras seguem a Resolução CONAMA nº 275/2001.
"""

from __future__ import annotations

import base64
import html
import re
from collections.abc import Iterable

import streamlit as st

from . import projeto
from .orientacoes import CATEGORIAS, MATERIAIS, Material, Situacao

VERDE = "#1F6F50"
VERDE_ESCURO = "#17573F"
TERRACOTA = "#D9773E"
TEXTO_SUAVE = "#5B6863"

ESTILO_SITUACAO = {
    # fundo, borda, texto do título
    Situacao.RECICLAVEL: ("#E7F4EC", "#A9D5BB", "#17573F"),
    Situacao.ATENCAO: ("#FFF4E0", "#F0C483", "#8A5300"),
    Situacao.NAO_RECICLAVEL: ("#FDECEA", "#F0B4AD", "#A1271B"),
    Situacao.DESCARTE_ESPECIAL: ("#F1EAFB", "#CDB6F0", "#5B3596"),
}

EXPLICACAO_SITUACAO = {
    Situacao.RECICLAVEL: "Pode ir para a coleta seletiva depois do preparo indicado.",
    Situacao.ATENCAO: "Pode ir para a coleta seletiva, mas exige cuidados especiais.",
    Situacao.NAO_RECICLAVEL: "Não deve ir para a coleta seletiva.",
    Situacao.DESCARTE_ESPECIAL: "Precisa de descarte especial: não vai para o lixo comum nem para a reciclagem.",
}

_CSS = f"""
<style>
[data-testid="stMainBlockContainer"] {{ padding-top: 4.4rem; max-width: 1180px; }}
div[class*="st-key-cartao"] {{
  background: #FFFFFF; border-radius: 20px; box-shadow: 0 2px 12px rgba(30,42,37,.05);
}}
.rf-hero {{
  position: relative; overflow: hidden; border-radius: 24px; padding: 28px 32px; color: #fff;
  background:
    radial-gradient(circle at 88% 15%, rgba(242,166,90,.40), transparent 38%),
    radial-gradient(circle at 10% 110%, rgba(255,255,255,.10), transparent 40%),
    linear-gradient(135deg, #154F39 0%, {VERDE} 55%, #2F8A5F 100%);
  display: flex; flex-wrap: wrap; gap: 20px 32px; align-items: center; justify-content: space-between;
  box-shadow: 0 10px 30px rgba(23,87,63,.18); margin-bottom: 6px;
}}
.rf-hero-marca {{ display: flex; align-items: center; gap: 18px; }}
.rf-hero-marca img {{ filter: drop-shadow(0 6px 12px rgba(0,0,0,.18)); }}
.rf-kicker {{ font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; font-weight: 700; opacity: .85; }}
.rf-hero-titulo {{ font-family: Poppins, sans-serif; font-weight: 700; font-size: 2.3rem; line-height: 1.08; }}
.rf-hero-texto {{ max-width: 33rem; opacity: .93; margin-top: 6px; font-size: 1rem; line-height: 1.5; }}
.rf-pills {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.rf-pill {{
  background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.28); border-radius: 999px;
  padding: 8px 14px; font-size: .88rem; font-weight: 600; white-space: nowrap;
}}
.rf-pill b {{ color: #FFD7AE; margin-right: 4px; }}
.rf-titulo-pagina {{ display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }}
.rf-titulo-pagina .i {{
  width: 56px; height: 56px; border-radius: 16px; display: grid; place-items: center; font-size: 1.7rem;
  background: #E7F4EC; flex: none;
}}
.rf-titulo-pagina h1 {{ font-family: Poppins, sans-serif; font-size: 2rem; margin: 0; padding: 0; color: #1E2A25; }}
.rf-titulo-pagina p {{ margin: 2px 0 0; color: {TEXTO_SUAVE}; }}
.rf-secao {{ display: flex; align-items: center; gap: 12px; margin: 2px 0 12px; }}
.rf-secao-num {{
  width: 34px; height: 34px; border-radius: 50%; background: {VERDE}; color: #fff; flex: none;
  display: grid; place-items: center; font-weight: 700; font-family: Poppins, sans-serif;
}}
.rf-secao-titulo {{ font-family: Poppins, sans-serif; font-weight: 600; font-size: 1.22rem; color: #1E2A25; line-height: 1.2; }}
.rf-secao-sub {{ font-size: .86rem; color: {TEXTO_SUAVE}; }}
.rf-subtitulo {{ font-family: Poppins, sans-serif; font-weight: 600; font-size: 1.02rem; color: #1E2A25; margin: 16px 0 8px; }}
.rf-material {{
  display: flex; gap: 16px; align-items: center; padding: 16px 18px; border-radius: 18px; background: #fff;
  border: 1px solid #E3DCD0; border-left: 8px solid var(--cor);
}}
.rf-material-icone {{
  width: 62px; height: 62px; border-radius: 16px; display: grid; place-items: center; font-size: 2rem; flex: none;
  background: color-mix(in srgb, var(--cor) 14%, white);
}}
.rf-rotulo {{ font-size: .74rem; text-transform: uppercase; letter-spacing: .09em; color: {TEXTO_SUAVE}; font-weight: 700; }}
.rf-material-nome {{ font-family: Poppins, sans-serif; font-weight: 700; font-size: 1.75rem; line-height: 1.15; color: #1E2A25; }}
.rf-conf {{ display: flex; align-items: center; gap: 10px; margin-top: 6px; font-size: .85rem; color: {TEXTO_SUAVE}; }}
.rf-conf > span {{ white-space: nowrap; }}
.rf-barra {{ flex: 1; height: 8px; border-radius: 99px; background: #EEE9E0; overflow: hidden; min-width: 70px; max-width: 200px; }}
.rf-barra > span {{ display: block; height: 100%; border-radius: 99px; background: var(--cor); }}
.rf-probs {{ display: grid; gap: 10px; }}
.rf-prob {{ display: grid; grid-template-columns: 9.5rem 1fr 3.2rem; align-items: center; gap: 10px; font-size: .9rem; }}
.rf-prob .rf-barra {{ max-width: none; }}
.rf-prob-val {{ text-align: right; font-variant-numeric: tabular-nums; color: {TEXTO_SUAVE}; }}
.rf-veredito {{
  display: flex; gap: 14px; align-items: center; padding: 16px 18px; border-radius: 18px;
  background: var(--fundo); border: 1px solid var(--borda);
}}
.rf-veredito-icone {{ font-size: 2rem; flex: none; }}
.rf-veredito-titulo {{ font-family: Poppins, sans-serif; font-weight: 700; font-size: 1.35rem; color: var(--texto); line-height: 1.2; }}
.rf-veredito-texto {{ color: #33403B; font-size: .95rem; }}
.rf-alerta {{
  display: flex; gap: 10px; align-items: flex-start; padding: 12px 14px; border-radius: 14px; margin-top: 8px;
  background: var(--fundo); border-left: 5px solid var(--borda); font-size: .93rem; color: #2A3631; line-height: 1.45;
}}
.rf-passos {{ list-style: none; margin: 0 !important; padding: 0 !important; display: grid; gap: 8px; }}
.rf-passos li {{
  display: flex; gap: 12px; align-items: flex-start; background: #FBF8F3; border: 1px solid #ECE6DB;
  border-radius: 14px; padding: 10px 14px; line-height: 1.45; margin: 0;
}}
.rf-passos .n {{
  width: 26px; height: 26px; border-radius: 50%; background: #E7F4EC; color: {VERDE_ESCURO}; font-weight: 700;
  display: grid; place-items: center; flex: none; font-size: .85rem;
}}
.rf-descarte {{
  display: flex; gap: 16px; align-items: center; padding: 14px 18px; border-radius: 18px;
  background: #FBF8F3; border: 1px solid #ECE6DB; line-height: 1.45;
}}
.rf-chip {{
  display: inline-block; padding: 3px 12px; border-radius: 999px; font-weight: 700; font-size: .8rem;
  background: var(--cor); color: var(--cor-texto); margin-bottom: 4px;
}}
.rf-vazio {{
  display: flex; gap: 14px; align-items: center; padding: 18px; border-radius: 18px; margin-bottom: 14px;
  border: 2px dashed #D5E6DB; background: #F4FAF6; color: #2A3631;
}}
.rf-vazio .i {{ font-size: 2rem; }}
.rf-grade {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
.rf-card-mat {{
  background: #fff; border: 1px solid #E3DCD0; border-top: 5px solid var(--cor); border-radius: 16px;
  padding: 14px 16px; display: flex; gap: 12px; align-items: flex-start; line-height: 1.4;
}}
.rf-card-mat b {{ font-family: Poppins, sans-serif; font-size: 1rem; }}
.rf-card-mat small {{ color: {TEXTO_SUAVE}; font-size: .82rem; }}
.rf-fluxo {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 6px 0 4px; }}
.rf-etapa {{
  background: #fff; border: 1px solid #E3DCD0; border-radius: 18px; padding: 16px; position: relative; line-height: 1.4;
}}
.rf-etapa .i {{ font-size: 1.6rem; }}
.rf-etapa b {{ display: block; font-family: Poppins, sans-serif; margin: 6px 0 2px; }}
.rf-etapa small {{ color: {TEXTO_SUAVE}; }}
.rf-etapa .k {{ position: absolute; top: 12px; right: 14px; font-weight: 700; color: #C9D9CF; font-family: Poppins, sans-serif; font-size: 1.4rem; }}
.rf-equipe {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 12px; }}
.rf-pessoa {{ display: flex; gap: 12px; align-items: center; background: #fff; border: 1px solid #E3DCD0; border-radius: 16px; padding: 12px 14px; }}
.rf-avatar {{
  width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; flex: none; color: #fff;
  font-weight: 700; font-family: Poppins, sans-serif; background: linear-gradient(135deg, {VERDE}, #2F8A5F);
}}
.rf-selo {{
  display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 999px;
  background: #FCEBDD; color: #8A4416; font-weight: 700; font-size: .85rem; margin-bottom: 10px;
}}
.rf-rodape {{
  margin-top: 36px; padding: 18px 0 6px; border-top: 1px solid #E3DCD0; color: {TEXTO_SUAVE}; font-size: .84rem;
  display: flex; flex-wrap: wrap; gap: 6px 24px; justify-content: space-between;
}}
.rf-rodape b {{ color: {VERDE}; }}
@media (min-width: 761px) {{
  div.st-key-cartao_foto {{ position: sticky; top: 4.5rem; }}
}}
@media (max-width: 760px) {{
  .rf-hero {{ padding: 22px 20px; border-radius: 20px; }}
  .rf-hero-titulo {{ font-size: 1.8rem; }}
  .rf-hero-marca {{ flex-direction: column; align-items: flex-start; gap: 12px; }}
  .rf-hero-marca img {{ width: 48px; height: 48px; }}
  .rf-grade, .rf-fluxo {{ grid-template-columns: 1fr; }}
  .rf-material-nome {{ font-size: 1.45rem; }}
  .rf-prob {{ grid-template-columns: 7.5rem 1fr 3rem; }}
  .rf-titulo-pagina h1 {{ font-size: 1.6rem; }}
}}
</style>
"""


def aplicar_estilo() -> None:
    st.html(_CSS)


def pct(valor: float, casas: int = 0) -> str:
    """Porcentagem no formato brasileiro (vírgula decimal)."""
    return f"{100 * valor:.{casas}f}%".replace(".", ",")


def texto_html(texto: str) -> str:
    """Escapa o texto e converte **negrito** do Markdown em <b>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(texto, quote=False))


def _svg_img(svg: str, largura: int, altura: int) -> str:
    """O st.html remove <svg> embutido; por isso o desenho vai como imagem (data URI)."""
    codigo = base64.b64encode(svg.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{codigo}" width="{largura}" height="{altura}" alt="" style="flex:none">'


def _icone_marca(claro: bool = False, tamanho: int = 68) -> str:
    fundo, traco = ("#FBF8F3", VERDE) if claro else (VERDE, "#FBF8F3")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="18" fill="{fundo}"/>
  <path d="M46.7 23.5A17 17 0 1 0 49 32" fill="none" stroke="{traco}" stroke-width="5" stroke-linecap="round"/>
  <path d="M49.5 18.4L47.7 25.2L40.9 23.4" fill="none" stroke="{traco}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M24 40C24 30 30 24 40 24C40 34 34 40 24 40Z" fill="#F2A65A"/>
  <path d="M26 38L35 29" stroke="{fundo}" stroke-width="2.2" stroke-linecap="round"/>
</svg>"""
    return _svg_img(svg, tamanho, tamanho)


def lixeira_svg(cor: str, largura: int = 46) -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 48">
  <rect x="5" y="11" width="30" height="35" rx="5" fill="{cor}"/>
  <rect x="2" y="6" width="36" height="7" rx="3" fill="{cor}"/>
  <rect x="2" y="6" width="36" height="7" rx="3" fill="#000" fill-opacity=".18"/>
  <rect x="14" y="1.5" width="12" height="6" rx="2.5" fill="none" stroke="{cor}" stroke-width="2.5"/>
  <path d="M14 20v18M20 20v18M26 20v18" stroke="#fff" stroke-opacity=".6" stroke-width="2.6" stroke-linecap="round"/>
</svg>"""
    return _svg_img(svg, largura, round(largura * 1.2))


def cor_texto_sobre(material: Material) -> str:
    return "#2B2100" if material.chave == "metal" else "#FFFFFF"


def cabecalho() -> None:
    st.html(
        f"""
<div class="rf-hero">
  <div class="rf-hero-marca">
    {_icone_marca(claro=True)}
    <div>
      <div class="rf-kicker">Cooperativa ReciFavela</div>
      <div class="rf-hero-titulo">Descarte Certo</div>
      <div class="rf-hero-texto">Fotografe um resíduo e descubra, em segundos, se ele é reciclável
      e como prepará-lo para a coleta seletiva.</div>
    </div>
  </div>
  <div class="rf-pills">
    <span class="rf-pill"><b>1</b>📷 Fotografe</span>
    <span class="rf-pill"><b>2</b>🔎 Identifique</span>
    <span class="rf-pill"><b>3</b>♻️ Descarte certo</span>
  </div>
</div>
"""
    )


def titulo_pagina(icone: str, titulo: str, texto: str) -> None:
    st.html(
        f"""<div class="rf-titulo-pagina"><div class="i">{icone}</div>
<div><h1>{html.escape(titulo)}</h1><p>{texto_html(texto)}</p></div></div>"""
    )


def secao(numero: int | str, titulo: str, subtitulo: str | None = None) -> None:
    sub = f'<div class="rf-secao-sub">{texto_html(subtitulo)}</div>' if subtitulo else ""
    st.html(
        f"""<div class="rf-secao"><div class="rf-secao-num">{numero}</div>
<div><div class="rf-secao-titulo">{html.escape(titulo)}</div>{sub}</div></div>"""
    )


def subtitulo(texto: str) -> None:
    st.html(f'<div class="rf-subtitulo">{html.escape(texto)}</div>')


def estado_vazio() -> None:
    cartoes = "".join(
        f"""<div class="rf-card-mat" style="--cor:{m.cor_hex}">{lixeira_svg(m.cor_hex, 34)}
<div><b>{m.emoji} {m.nome}</b><br><small>Lixeira {m.cor_lixeira} · {html.escape(m.exemplos)}</small></div></div>"""
        for m in (MATERIAIS[c] for c in CATEGORIAS)
    )
    st.html(
        f"""<div class="rf-vazio"><div class="i">📷</div>
<div><b>Envie uma foto para começar.</b><br>O resultado da análise aparecerá aqui.</div></div>
<div class="rf-rotulo" style="margin:4px 0 10px">Materiais reconhecidos</div>
<div class="rf-grade">{cartoes}</div>"""
    )


def cartao_material(material: Material, confianca: float, corrigido: bool) -> None:
    if corrigido:
        detalhe = "Corrigido manualmente por você"
    else:
        detalhe = (
            f'<div class="rf-barra"><span style="width:{100 * confianca:.0f}%"></span></div>'
            f"<span>{pct(confianca)} de confiança</span>"
        )
    st.html(
        f"""<div class="rf-material" style="--cor:{material.cor_hex}">
  <div class="rf-material-icone">{material.emoji}</div>
  <div style="flex:1;min-width:0">
    <div class="rf-rotulo">Material identificado</div>
    <div class="rf-material-nome">{material.nome}</div>
    <div class="rf-conf">{detalhe}</div>
  </div>
</div>"""
    )


def barras_probabilidades(probabilidades: dict[str, float]) -> None:
    linhas = "".join(
        f"""<div class="rf-prob"><span>{MATERIAIS[c].emoji} {MATERIAIS[c].nome}</span>
<div class="rf-barra" style="--cor:{MATERIAIS[c].cor_hex}"><span style="width:{100 * p:.1f}%"></span></div>
<span class="rf-prob-val">{pct(p, 1)}</span></div>"""
        for c, p in probabilidades.items()
    )
    st.html(f'<div class="rf-probs">{linhas}</div>')


def cartao_situacao(situacao: Situacao) -> None:
    fundo, borda, texto = ESTILO_SITUACAO[situacao]
    st.html(
        f"""<div class="rf-veredito" style="--fundo:{fundo};--borda:{borda};--texto:{texto}">
  <div class="rf-veredito-icone">{situacao.icone}</div>
  <div><div class="rf-veredito-titulo">{situacao.rotulo}</div>
  <div class="rf-veredito-texto">{EXPLICACAO_SITUACAO[situacao]}</div></div>
</div>"""
    )


def destaque(icone: str, titulo: str, texto: str, tom: Situacao = Situacao.RECICLAVEL) -> None:
    """Faixa de destaque no estilo do veredito (verde, laranja, vermelho ou roxo)."""
    fundo, borda, cor = ESTILO_SITUACAO[tom]
    st.html(
        f"""<div class="rf-veredito" style="--fundo:{fundo};--borda:{borda};--texto:{cor}">
  <div class="rf-veredito-icone">{icone}</div>
  <div><div class="rf-veredito-titulo">{html.escape(titulo)}</div>
  <div class="rf-veredito-texto">{texto_html(texto)}</div></div>
</div>"""
    )


def alertas(itens: Iterable[tuple[Situacao, str]]) -> None:
    icones = {
        Situacao.RECICLAVEL: "🧽",
        Situacao.ATENCAO: "⚠️",
        Situacao.NAO_RECICLAVEL: "🚫",
        Situacao.DESCARTE_ESPECIAL: "☣️",
    }
    blocos = "".join(
        f"""<div class="rf-alerta" style="--fundo:{ESTILO_SITUACAO[s][0]};--borda:{ESTILO_SITUACAO[s][1]}">
<span>{icones[s]}</span><span>{texto_html(t)}</span></div>"""
        for s, t in itens
    )
    if blocos:
        st.html(blocos)


def lista_passos(passos: Iterable[str]) -> None:
    itens = "".join(
        f'<li><span class="n">{i}</span><span>{texto_html(p)}</span></li>' for i, p in enumerate(passos, 1)
    )
    st.html(f'<ol class="rf-passos">{itens}</ol>')


def cartao_descarte(material: Material, situacao: Situacao, texto: str) -> None:
    if situacao.reciclavel:
        icone = lixeira_svg(material.cor_hex)
        chip = (
            f'<span class="rf-chip" style="--cor:{material.cor_hex};--cor-texto:{cor_texto_sobre(material)}">'
            f"Lixeira {material.cor_lixeira}</span><br>"
        )
    elif situacao == Situacao.DESCARTE_ESPECIAL:
        icone = lixeira_svg("#7A5BB5")
        chip = '<span class="rf-chip" style="--cor:#7A5BB5;--cor-texto:#fff">Ponto de coleta especial</span><br>'
    else:
        icone = lixeira_svg("#8A8F8C")
        chip = '<span class="rf-chip" style="--cor:#8A8F8C;--cor-texto:#fff">Lixo comum (rejeito)</span><br>'
    st.html(f'<div class="rf-descarte">{icone}<div>{chip}{texto_html(texto)}</div></div>')


def fluxo(etapas: Iterable[tuple[str, str, str]]) -> None:
    cartoes = "".join(
        f'<div class="rf-etapa"><span class="k">{i}</span><div class="i">{icone}</div>'
        f"<b>{html.escape(t)}</b><small>{texto_html(d)}</small></div>"
        for i, (icone, t, d) in enumerate(etapas, 1)
    )
    st.html(f'<div class="rf-fluxo">{cartoes}</div>')


def equipe() -> None:
    def iniciais(nome: str) -> str:
        partes = [p for p in nome.split() if p[:1].isalpha()]
        return (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper() if partes else "?"

    pessoas = "".join(
        f'<div class="rf-pessoa"><div class="rf-avatar">{iniciais(n)}</div><div>{html.escape(n)}</div></div>'
        for n in projeto.EQUIPE
    )
    st.html(
        f"""<div class="rf-selo">👩‍🔬 Mulheres na engenharia</div>
<p style="margin:0 0 12px;color:#33403B">{html.escape(projeto.APRESENTACAO_EQUIPE)}</p>
<div class="rf-equipe">{pessoas}</div>"""
    )


def rodape() -> None:
    st.html(
        f"""<div class="rf-rodape">
  <span><b>ReciFavela · Descarte Certo</b> — protótipo acadêmico ·
  {html.escape(projeto.linha_academica())}</span>
  <span>A análise é uma sugestão automática. Em caso de dúvida, consulte a equipe da cooperativa.</span>
</div>"""
    )
