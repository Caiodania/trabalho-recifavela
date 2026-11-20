"""Cálculo das métricas da validação do protótipo (meta: 80% de acerto em 30 resíduos)."""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .orientacoes import CATEGORIAS, MATERIAIS

META_ACERTO = 0.80
TOTAL_PREVISTO = 30
EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# Palavras que, no nome do arquivo ou da pasta, indicam a categoria correta.
_PALAVRAS = {
    "plastico": ("plastico", "plastic", "pet"),
    "papel": ("papel", "papelao", "paper", "cardboard"),
    "metal": ("metal", "lata", "aluminio"),
    "vidro": ("vidro", "glass"),
}


def _normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def inferir_categoria(caminho: str | Path) -> str | None:
    """Deduz a categoria correta pelo nome do arquivo ou da pasta (ex.: vidro/garrafa.jpg, papel_03.jpg)."""
    partes = [_normalizar(p) for p in Path(caminho).parts]
    for parte in reversed(partes):  # o nome do arquivo tem prioridade sobre as pastas
        for token in _tokens(parte):
            for categoria, palavras in _PALAVRAS.items():
                if token in palavras:
                    return categoria
    return None


def _tokens(texto: str) -> list[str]:
    limpo = "".join(c if c.isalnum() else " " for c in texto)
    return [t.rstrip("0123456789") for t in limpo.split()]


def listar_imagens(pasta: str | Path) -> list[Path]:
    return sorted(p for p in Path(pasta).rglob("*") if p.suffix.lower() in EXTENSOES_IMAGEM)


@dataclass(frozen=True)
class Resumo:
    total: int
    acertos: int
    acuracia: float
    meta_atingida: bool
    matriz_confusao: pd.DataFrame
    por_categoria: pd.DataFrame

    @property
    def acertos_necessarios(self) -> int:
        """Acertos mínimos para a meta considerando o total testado."""
        return math.ceil(META_ACERTO * self.total - 1e-9)


def resumir(correta: pd.Series, sistema: pd.Series) -> Resumo:
    """Compara a classificação correta com a do sistema (linhas sem categoria correta são ignoradas)."""
    dados = pd.DataFrame({"correta": correta, "sistema": sistema}).dropna()
    total = len(dados)
    acertos = int((dados["correta"] == dados["sistema"]).sum())
    acuracia = acertos / total if total else 0.0

    nomes = {c: MATERIAIS[c].nome for c in CATEGORIAS}
    matriz = pd.crosstab(
        pd.Categorical(dados["correta"].map(nomes), categories=list(nomes.values())),
        pd.Categorical(dados["sistema"].map(nomes), categories=list(nomes.values())),
        rownames=["Correta"],
        colnames=["Sistema"],
        dropna=False,
    )

    linhas = []
    for c in CATEGORIAS:
        sub = dados[dados["correta"] == c]
        n = len(sub)
        a = int((sub["sistema"] == c).sum())
        linhas.append({"Material": nomes[c], "Testados": n, "Acertos": a, "Acerto (%)": round(100 * a / n, 1) if n else None})
    por_categoria = pd.DataFrame(linhas)

    return Resumo(total, acertos, acuracia, total > 0 and acuracia >= META_ACERTO, matriz, por_categoria)
