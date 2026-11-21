# Regras de cada material. Cores das lixeiras: Resolução CONAMA 275/2001.
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

PONTO_DE_ENTREGA = "na ReciFavela ou em um Ponto de Entrega Voluntária (PEV) da coleta seletiva"


class Situacao(IntEnum):
    # quanto maior, mais restritivo
    RECICLAVEL = 0
    ATENCAO = 1
    NAO_RECICLAVEL = 2
    DESCARTE_ESPECIAL = 3

    @property
    def rotulo(self) -> str:
        return {
            Situacao.RECICLAVEL: "Reciclável",
            Situacao.ATENCAO: "Reciclável, com cuidados",
            Situacao.NAO_RECICLAVEL: "Não reciclável",
            Situacao.DESCARTE_ESPECIAL: "Descarte especial",
        }[self]

    @property
    def icone(self) -> str:
        return {
            Situacao.RECICLAVEL: "✅",
            Situacao.ATENCAO: "⚠️",
            Situacao.NAO_RECICLAVEL: "🚫",
            Situacao.DESCARTE_ESPECIAL: "☣️",
        }[self]

    @property
    def reciclavel(self) -> bool:
        return self <= Situacao.ATENCAO


@dataclass(frozen=True)
class Pergunta:
    id: str
    texto: str
    situacao: Situacao  # vale quando a resposta é "sim"
    orientacao: str
    exemplo: str = ""


@dataclass(frozen=True)
class Material:
    chave: str
    nome: str
    emoji: str
    cor_lixeira: str
    cor_hex: str
    exemplos: str
    preparo: tuple[str, ...]
    perguntas: tuple[Pergunta, ...]


@dataclass(frozen=True)
class Avaliacao:
    material: Material
    situacao: Situacao
    alertas: tuple[tuple[Situacao, str], ...]
    preparo: tuple[str, ...]
    descarte: str


PLASTICO = Material(
    chave="plastico",
    nome="Plástico",
    emoji="🧴",
    cor_lixeira="vermelha",
    cor_hex="#D32F2F",
    exemplos="garrafas PET, potes, frascos de limpeza e higiene, sacolas, tampas",
    preparo=(
        "Esvazie completamente a embalagem.",
        "Enxágue rapidamente para tirar os restos — dá para reaproveitar a água da louça.",
        "Deixe escorrer e secar para evitar mau cheiro e insetos.",
        "Amasse ou achate garrafas e potes para ocupar menos espaço.",
        "Tampas e rótulos de plástico podem ir junto: também são recicláveis.",
    ),
    perguntas=(
        Pergunta(
            id="sujo",
            texto="Tem restos de comida, gordura ou produto dentro?",
            exemplo="Ex.: pote de margarina com resto, frasco de xampu ainda cheio.",
            situacao=Situacao.RECICLAVEL,
            orientacao=(
                "Retire os restos e lave com água e um pouco de detergente. Material sujo "
                "contamina os outros recicláveis e pode ser descartado na triagem."
            ),
        ),
        Pergunta(
            id="metalizado",
            texto="É uma embalagem metalizada (brilhante por dentro, como papel-alumínio)?",
            exemplo="Ex.: pacote de salgadinho, de biscoito recheado ou de café a vácuo.",
            situacao=Situacao.NAO_RECICLAVEL,
            orientacao=(
                "Embalagens metalizadas misturam plástico e alumínio em camadas finas e "
                "quase nunca são aceitas na reciclagem. Descarte no lixo comum."
            ),
        ),
        Pergunta(
            id="isopor",
            texto="É isopor?",
            exemplo="Ex.: bandeja de frios, copo térmico, proteção de eletrodoméstico.",
            situacao=Situacao.ATENCAO,
            orientacao=(
                "O isopor é reciclável, mas tem pouco valor e nem toda cooperativa recebe. "
                "Se estiver limpo, confirme com a ReciFavela antes de levar; se estiver sujo "
                "de alimento (ex.: bandeja de carne), descarte no lixo comum."
            ),
        ),
        Pergunta(
            id="perigoso",
            texto="Era embalagem de óleo lubrificante, agrotóxico ou outro produto tóxico?",
            situacao=Situacao.DESCARTE_ESPECIAL,
            orientacao=(
                "Embalagens de produtos perigosos não devem ser lavadas nem misturadas aos "
                "recicláveis. Devolva no local de compra (logística reversa) ou leve a um ecoponto."
            ),
        ),
    ),
)

PAPEL = Material(
    chave="papel",
    nome="Papel e papelão",
    emoji="📦",
    cor_lixeira="azul",
    cor_hex="#1976D2",
    exemplos="jornais, revistas, folhas, cadernos, caixas de papelão, embalagens de papel",
    preparo=(
        "Mantenha o papel seco e limpo — guarde longe da chuva e da umidade.",
        "Retire fitas adesivas, grampos e espirais de metal ou de plástico.",
        "Desmonte e achate as caixas de papelão.",
        "Prefira dobrar em vez de amassar ou picar: papel picado demais é difícil de separar.",
    ),
    perguntas=(
        Pergunta(
            id="sujo",
            texto="Está molhado, engordurado ou sujo de comida?",
            exemplo="Ex.: caixa de pizza com gordura, embalagem de lanche.",
            situacao=Situacao.NAO_RECICLAVEL,
            orientacao=(
                "Gordura e umidade estragam as fibras e o papel deixa de ser reciclável. "
                "Se uma parte estiver limpa, recorte-a para reciclar e descarte o restante no lixo comum."
            ),
        ),
        Pergunta(
            id="sanitario",
            texto="É papel higiênico, guardanapo, lenço ou papel-toalha usado?",
            situacao=Situacao.NAO_RECICLAVEL,
            orientacao=(
                "Papéis sanitários usados não são recicláveis por questão de higiene. "
                "Descarte no lixo comum."
            ),
        ),
        Pergunta(
            id="especial",
            texto="É papel térmico, plastificado, adesivo ou fotografia?",
            exemplo="Ex.: cupom fiscal, extrato de caixa eletrônico, etiquetas, papel de presente metalizado.",
            situacao=Situacao.NAO_RECICLAVEL,
            orientacao=(
                "Esses papéis têm químicos ou camadas de plástico que impedem a reciclagem. "
                "Descarte no lixo comum."
            ),
        ),
        Pergunta(
            id="longa_vida",
            texto="É embalagem longa vida (caixa de leite, suco ou molho)?",
            situacao=Situacao.RECICLAVEL,
            orientacao=(
                "Caixas longa vida (cartonadas) são recicláveis: abra, enxágue, deixe secar e achate "
                "antes de entregar junto com os recicláveis secos."
            ),
        ),
    ),
)

METAL = Material(
    chave="metal",
    nome="Metal",
    emoji="🥫",
    cor_lixeira="amarela",
    cor_hex="#F9A825",
    exemplos="latas de refrigerante e cerveja, latas de conserva, tampas, papel-alumínio limpo, panelas velhas",
    preparo=(
        "Esvazie e enxágue as latas.",
        "Amasse as latas de alumínio para ocupar menos espaço.",
        "Em latas de conserva, dobre a tampa para dentro com cuidado para ninguém se cortar.",
        "Junte peças pequenas (tampinhas, lacres) dentro de uma lata maior para não se perderem.",
    ),
    perguntas=(
        Pergunta(
            id="sujo",
            texto="Tem restos de comida ou bebida?",
            situacao=Situacao.RECICLAVEL,
            orientacao=(
                "Lave com água e um pouco de detergente para tirar os restos e evitar mau cheiro e insetos."
            ),
        ),
        Pergunta(
            id="cortante",
            texto="Tem bordas cortantes ou pontas?",
            exemplo="Ex.: tampa de lata de conserva, pregos, arames, lâminas.",
            situacao=Situacao.ATENCAO,
            orientacao=(
                "Proteja quem faz a triagem: dobre as bordas para dentro ou embrulhe as peças em "
                "jornal ou papelão e escreva “CUIDADO – CORTANTE”."
            ),
        ),
        Pergunta(
            id="aerossol",
            texto="É lata de spray (aerossol)?",
            exemplo="Ex.: desodorante, espuma de barbear, purificador de ar.",
            situacao=Situacao.ATENCAO,
            orientacao=(
                "Latas de spray só podem ser recicladas totalmente vazias. Não fure, não amasse e "
                "não coloque no fogo — há risco de explosão."
            ),
        ),
        Pergunta(
            id="quimico",
            texto="Tem resto de tinta, solvente, óleo ou inseticida?",
            situacao=Situacao.DESCARTE_ESPECIAL,
            orientacao=(
                "Restos de produtos químicos são perigosos e contaminam o metal. Leve a um ecoponto "
                "ou ponto de coleta de resíduos perigosos."
            ),
        ),
        Pergunta(
            id="eletronico",
            texto="É pilha, bateria ou parte de aparelho eletrônico?",
            situacao=Situacao.DESCARTE_ESPECIAL,
            orientacao=(
                "Pilhas, baterias e eletrônicos têm metais pesados e não vão para a coleta seletiva "
                "comum. Leve aos coletores de logística reversa (supermercados, lojas de eletrônicos "
                "e assistências técnicas)."
            ),
        ),
    ),
)

VIDRO = Material(
    chave="vidro",
    nome="Vidro",
    emoji="🍾",
    cor_lixeira="verde",
    cor_hex="#388E3C",
    exemplos="garrafas, potes de conserva, frascos de remédio e de perfume, copos",
    preparo=(
        "Esvazie e enxágue para retirar os restos.",
        "Retire tampas e rolhas: tampa de metal vai para o metal; de plástico, para o plástico.",
        "Não precisa tirar o rótulo.",
        "Transporte com cuidado, em caixa de papelão ou embrulhado em jornal.",
    ),
    perguntas=(
        Pergunta(
            id="quebrado",
            texto="Está quebrado ou trincado?",
            situacao=Situacao.ATENCAO,
            orientacao=(
                "Vidro quebrado continua reciclável, mas precisa ser embalado: junte os cacos em uma "
                "caixa de papelão ou garrafa PET cortada, feche bem e escreva “VIDRO QUEBRADO”. "
                "Isso evita acidentes com quem faz a coleta e a triagem."
            ),
        ),
        Pergunta(
            id="plano",
            texto="É espelho, vidro de janela ou box, ou vidro refratário/temperado?",
            exemplo="Ex.: espelho, vidraça, para-brisa, travessa refratária (tipo Pyrex), tampa de panela.",
            situacao=Situacao.NAO_RECICLAVEL,
            orientacao=(
                "Esses vidros têm composição diferente da do vidro de embalagens e não podem ser "
                "misturados a ele. Consulte a ReciFavela ou vidraçarias da região; sem destino, "
                "embrulhe bem e descarte no lixo comum identificando o conteúdo."
            ),
        ),
        Pergunta(
            id="ceramica",
            texto="É cerâmica, porcelana, louça ou cristal?",
            exemplo="Ex.: pratos, xícaras, vasos, taças de cristal.",
            situacao=Situacao.NAO_RECICLAVEL,
            orientacao=(
                "Cerâmica, porcelana e cristal não são vidro de embalagem e contaminam a reciclagem. "
                "Inteiros, podem ser doados; quebrados, embrulhe e descarte no lixo comum ou como entulho."
            ),
        ),
        Pergunta(
            id="lampada",
            texto="É lâmpada?",
            situacao=Situacao.DESCARTE_ESPECIAL,
            orientacao=(
                "Lâmpadas (principalmente as fluorescentes, que contêm mercúrio) não vão para a coleta "
                "de vidro. Leve a pontos de logística reversa em lojas de material de construção e supermercados."
            ),
        ),
    ),
)

MATERIAIS: dict[str, Material] = {m.chave: m for m in (PLASTICO, PAPEL, METAL, VIDRO)}
CATEGORIAS: tuple[str, ...] = tuple(MATERIAIS)


def avaliar(chave_material: str, respostas: dict[str, bool] | None = None) -> Avaliacao:
    material = MATERIAIS[chave_material]
    respostas = respostas or {}

    marcadas = [p for p in material.perguntas if respostas.get(p.id)]
    # vale a resposta mais restritiva
    situacao = max((p.situacao for p in marcadas), default=Situacao.RECICLAVEL)
    alertas = tuple(
        (p.situacao, p.orientacao) for p in sorted(marcadas, key=lambda p: p.situacao, reverse=True)
    )

    if situacao == Situacao.DESCARTE_ESPECIAL:
        descarte = (
            "Não coloque no lixo comum nem junto com os recicláveis: leve a um ponto de "
            "logística reversa ou ecoponto, conforme a orientação acima."
        )
    elif situacao == Situacao.NAO_RECICLAVEL:
        descarte = (
            "Não coloque junto com os recicláveis — esse item contamina o material separado pela "
            "cooperativa. Descarte no lixo comum (rejeito), salvo indicação diferente acima."
        )
    else:
        descarte = (
            f"Separe na lixeira **{material.cor_lixeira}** ({material.nome.lower()}) e entregue "
            f"{PONTO_DE_ENTREGA}."
        )

    preparo = material.preparo if situacao.reciclavel else ()
    return Avaliacao(material, situacao, alertas, preparo, descarte)
