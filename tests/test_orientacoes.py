import pytest

from recifavela.orientacoes import CATEGORIAS, MATERIAIS, Situacao, avaliar


def test_quatro_categorias():
    assert set(CATEGORIAS) == {"plastico", "papel", "metal", "vidro"}


@pytest.mark.parametrize("chave", CATEGORIAS)
def test_material_completo(chave):
    m = MATERIAIS[chave]
    assert m.preparo and m.perguntas and m.exemplos
    ids = [p.id for p in m.perguntas]
    assert len(ids) == len(set(ids)), "ids de perguntas repetidos"
    assert all(p.orientacao.strip() for p in m.perguntas)


@pytest.mark.parametrize("chave", CATEGORIAS)
def test_sem_respostas_e_reciclavel(chave):
    a = avaliar(chave)
    assert a.situacao == Situacao.RECICLAVEL
    assert a.preparo == MATERIAIS[chave].preparo
    assert a.alertas == ()
    assert f"lixeira **{MATERIAIS[chave].cor_lixeira}**" in a.descarte


def test_sujeira_mantem_reciclavel_com_orientacao_extra():
    a = avaliar("plastico", {"sujo": True})
    assert a.situacao == Situacao.RECICLAVEL
    assert len(a.alertas) == 1 and a.preparo


def test_vidro_quebrado_exige_cuidados():
    a = avaliar("vidro", {"quebrado": True})
    assert a.situacao == Situacao.ATENCAO
    assert a.situacao.reciclavel and a.preparo


def test_situacao_mais_restritiva_prevalece():
    a = avaliar("vidro", {"quebrado": True, "plano": True})
    assert a.situacao == Situacao.NAO_RECICLAVEL
    assert a.preparo == ()  # não reciclável: sem passos de preparo
    assert [s for s, _ in a.alertas] == [Situacao.NAO_RECICLAVEL, Situacao.ATENCAO]
    assert "lixo comum" in a.descarte


@pytest.mark.parametrize(
    ("chave", "pergunta"),
    [("metal", "eletronico"), ("metal", "quimico"), ("vidro", "lampada"), ("plastico", "perigoso")],
)
def test_descarte_especial(chave, pergunta):
    a = avaliar(chave, {pergunta: True})
    assert a.situacao == Situacao.DESCARTE_ESPECIAL
    assert not a.situacao.reciclavel
    assert "logística reversa" in a.descarte


@pytest.mark.parametrize(("chave", "pergunta"), [("papel", "sujo"), ("papel", "sanitario"), ("plastico", "metalizado")])
def test_nao_reciclavel(chave, pergunta):
    assert avaliar(chave, {pergunta: True}).situacao == Situacao.NAO_RECICLAVEL


def test_respostas_desconhecidas_e_negativas_sao_ignoradas():
    a = avaliar("metal", {"inexistente": True, "eletronico": False})
    assert a.situacao == Situacao.RECICLAVEL and a.alertas == ()
