"""Classificação do material do resíduo com visão computacional.

Usa o modelo CLIP (OpenAI) em modo *zero-shot*: a imagem é comparada com
descrições em texto de cada material ("a photo of a plastic bottle", "a photo of
a cardboard box"...). Não é preciso treinar o modelo com fotos próprias — basta
ajustar as descrições abaixo se algum tipo de resíduo for confundido com
frequência nos testes.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from .config import MODELO_PADRAO
from .imagem import abrir_imagem, quadrada

# Descrições (em inglês, idioma em que o CLIP foi treinado) dos objetos mais
# comuns de cada categoria. A média das descrições forma o "protótipo" do material.
DESCRICOES: dict[str, list[str]] = {
    "plastico": [
        "a plastic bottle",
        "a PET soda bottle",
        "a plastic container",
        "a plastic food packaging",
        "a plastic bag",
        "a plastic cup",
        "a plastic detergent bottle",
        "a plastic shampoo bottle",
        "a plastic lid",
        "a yogurt cup",
        "a styrofoam tray",
        "a crumpled plastic wrapper",
        "a transparent plastic bottle",
        "a white plastic bottle",
        "a plastic jug",
        "a clear plastic clamshell container",
    ],
    "papel": [
        "a sheet of paper",
        "crumpled paper",
        "a cardboard box",
        "a piece of corrugated cardboard",
        "a newspaper",
        "a magazine",
        "a paper bag",
        "an egg carton",
        "a cereal box",
        "a notebook",
        "a paper cup",
        "a milk carton",
        "a white sheet of printer paper",
        "a crumpled ball of paper",
        "a paper envelope",
        "a stack of printed documents",
        "a torn piece of paper",
        "a flattened brown cardboard box",
    ],
    "metal": [
        "an aluminum soda can",
        "a beer can",
        "a tin can",
        "a steel food can",
        "a crushed aluminum can",
        "aluminum foil",
        "a metal bottle cap",
        "a metal lid",
        "scrap metal",
        "a metal pot",
        "an aerosol spray can",
        "metal wire and nails",
        "a shiny metal object",
        "a rusty metal can",
    ],
    "vidro": [
        "a glass bottle",
        "a green glass beer bottle",
        "a wine bottle",
        "a glass jar",
        "a clear glass jar with a lid",
        "a drinking glass",
        "broken glass shards",
        "a glass perfume bottle",
        "a small glass medicine bottle",
        "a brown glass bottle",
        "a transparent glass container",
        "a glass sauce bottle",
        "a transparent glass bottle",
        "a glass bottle with a label",
    ],
}

TEMPLATES = (
    "a photo of {}.",
    "a close-up photo of {}.",
    "a photo of {}, household waste for recycling.",
    "a photo of a used {}.",
)


@dataclass(frozen=True)
class Resultado:
    categoria: str
    confianca: float
    probabilidades: dict[str, float]  # da mais provável para a menos provável


def _como_tensor(saida) -> torch.Tensor:
    # Versões novas do transformers podem devolver um objeto em vez do tensor.
    return saida if isinstance(saida, torch.Tensor) else saida.pooler_output


class ClassificadorMateriais:
    def __init__(self, modelo: str = MODELO_PADRAO, device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.nome_modelo = modelo
        self.modelo = CLIPModel.from_pretrained(modelo).to(self.device).eval()
        self.processador = CLIPProcessor.from_pretrained(modelo)
        self.categorias = tuple(DESCRICOES)
        self._preparar_textos()

    @torch.inference_mode()
    def _preparar_textos(self) -> None:
        prototipos = []
        for categoria in self.categorias:
            descricoes = []
            for descricao in DESCRICOES[categoria]:
                frases = [t.format(descricao) for t in TEMPLATES]
                tokens = self.processador(text=frases, return_tensors="pt", padding=True).to(self.device)
                emb = _como_tensor(self.modelo.get_text_features(**tokens))
                emb = emb / emb.norm(dim=-1, keepdim=True)
                media = emb.mean(dim=0)
                descricoes.append(media / media.norm())
            # Média das descrições: equivale a tirar a média da similaridade da foto
            # com cada descrição do material.
            prototipos.append(torch.stack(descricoes).mean(dim=0))
        self._prototipos = torch.stack(prototipos)  # [n_categorias, dim]

    @torch.inference_mode()
    def _embeddings_imagens(self, imagens: list[Image.Image]) -> torch.Tensor:
        entrada = self.processador(images=imagens, return_tensors="pt").to(self.device)
        emb = _como_tensor(self.modelo.get_image_features(**entrada))
        return emb / emb.norm(dim=-1, keepdim=True)

    @torch.inference_mode()
    def classificar_lote(self, imagens: list[bytes | Image.Image]) -> list[Resultado]:
        imagens = [abrir_imagem(img) for img in imagens]
        # Duas vistas por foto: recorte central (padrão do CLIP) e foto inteira com bordas.
        emb_centro = self._embeddings_imagens(imagens)
        emb_inteira = self._embeddings_imagens([quadrada(img) for img in imagens])
        emb = emb_centro + emb_inteira
        emb = emb / emb.norm(dim=-1, keepdim=True)

        escala = self.modelo.logit_scale.exp()
        logits = escala * emb @ self._prototipos.T  # [n_imagens, n_categorias]
        probs = logits.softmax(dim=1).cpu()

        resultados = []
        for linha in probs:
            ordem = sorted(zip(self.categorias, linha.tolist()), key=lambda x: x[1], reverse=True)
            resultados.append(
                Resultado(categoria=ordem[0][0], confianca=ordem[0][1], probabilidades=dict(ordem))
            )
        return resultados

    def classificar(self, imagem: bytes | Image.Image) -> Resultado:
        return self.classificar_lote([imagem])[0]
