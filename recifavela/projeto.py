"""Dados do trabalho acadêmico exibidos no site (página "Sobre o projeto", barra lateral e rodapé).

Campos deixados vazios ("") simplesmente não aparecem no site.
"""

EQUIPE: list[str] = [
    "Geórgia Correa Simao",
    "Bianca Las Casas",
    "Maria Clara Meroi",
]
INSTITUICAO = "Instituto Mauá de Tecnologia"
CURSO = "Engenharia"
DISCIPLINA = ""  # ex.: "Projeto Integrador"
ORIENTACAO = ""  # ex.: "Prof.ª Dra. Fulana de Tal"
ANO = 2026

APRESENTACAO_EQUIPE = (
    "Projeto desenvolvido por estudantes de Engenharia do Instituto Mauá de Tecnologia, "
    "unindo tecnologia e impacto social em parceria com a cooperativa de reciclagem ReciFavela."
)


def linha_academica() -> str:
    """Ex.: "Engenharia · Instituto Mauá de Tecnologia · 2026" (ignora campos vazios)."""
    return " · ".join(str(p) for p in (CURSO, DISCIPLINA, INSTITUICAO, ANO) if p)
