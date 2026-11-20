"""Testes das métricas da validação (meta de 80% em 30 resíduos)."""

import pandas as pd
import pytest

from recifavela.avaliacao import inferir_categoria, resumir


@pytest.mark.parametrize(
    ("nome", "esperado"),
    [
        ("plastico_01.jpg", "plastico"),
        ("Plástico 2.JPG", "plastico"),
        ("vidro/garrafa.jpg", "vidro"),
        ("papelao3.png", "papel"),
        ("cardboard12.jpg", "papel"),
        ("lata_refrigerante.jpg", "metal"),
        ("metal/IMG_0001.jpg", "metal"),
        ("glass7.jpg", "vidro"),
        ("IMG_0001.jpg", None),
    ],
)
def test_inferir_categoria(nome, esperado):
    assert inferir_categoria(nome) == esperado


def _series(acertos: int, total: int = 30):
    correta = pd.Series(["plastico"] * total)
    sistema = pd.Series(["plastico"] * acertos + ["vidro"] * (total - acertos))
    return correta, sistema


def test_meta_atingida_com_24_de_30():
    r = resumir(*_series(24))
    assert (r.acertos, r.total) == (24, 30)
    assert r.acuracia == pytest.approx(0.8)
    assert r.meta_atingida and r.acertos_necessarios == 24


def test_meta_nao_atingida_com_23_de_30():
    r = resumir(*_series(23))
    assert not r.meta_atingida


def test_linhas_sem_gabarito_sao_ignoradas():
    correta = pd.Series(["papel", None, "metal"])
    sistema = pd.Series(["papel", "vidro", "vidro"])
    r = resumir(correta, sistema)
    assert (r.acertos, r.total) == (1, 2)


def test_matriz_de_confusao_e_acerto_por_material():
    correta = pd.Series(["papel", "papel", "metal", "vidro"])
    sistema = pd.Series(["papel", "plastico", "metal", "vidro"])
    r = resumir(correta, sistema)
    assert r.matriz_confusao.shape == (4, 4)
    assert r.matriz_confusao.loc["Papel e papelão", "Plástico"] == 1
    papel = r.por_categoria.set_index("Material").loc["Papel e papelão"]
    assert (papel["Testados"], papel["Acertos"]) == (2, 1)


def test_sem_dados():
    r = resumir(pd.Series([], dtype=object), pd.Series([], dtype=object))
    assert r.total == 0 and not r.meta_atingida
