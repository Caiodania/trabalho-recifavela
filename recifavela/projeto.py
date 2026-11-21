# Dados do trabalho que aparecem no site. Campo vazio ("") não aparece.

EQUIPE: list[str] = [
    "Geórgia Correa Simao",
    "Bianca Las Casas",
    "Maria Clara Meroi",
]
INSTITUICAO = "Instituto Mauá de Tecnologia"
CURSO = "Engenharia"
DISCIPLINA = ""
ORIENTACAO = ""
ANO = 2026

APRESENTACAO_EQUIPE = (
    "Projeto desenvolvido por estudantes de Engenharia do Instituto Mauá de Tecnologia, "
    "unindo tecnologia e impacto social em parceria com a cooperativa de reciclagem ReciFavela."
)


def linha_academica() -> str:
    return " · ".join(str(p) for p in (CURSO, DISCIPLINA, INSTITUICAO, ANO) if p)
