# Uso: python avaliar.py validacao/fotos [--gabarito validacao/gabarito.csv]
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from recifavela.avaliacao import META_ACERTO, TOTAL_PREVISTO, inferir_categoria, listar_imagens, resumir
from recifavela.classificador import MODELO_PADRAO, ClassificadorMateriais
from recifavela.orientacoes import CATEGORIAS


def ler_gabarito(caminho: Path) -> dict[str, str]:
    df = pd.read_csv(caminho, sep=None, engine="python", encoding="utf-8-sig", dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    gabarito = {}
    for _, linha in df.iterrows():
        arquivo, categoria = linha.get("arquivo"), linha.get("categoria_correta")
        if isinstance(arquivo, str) and isinstance(categoria, str) and categoria.strip():
            cat = inferir_categoria(categoria.strip())
            if cat is None:
                sys.exit(f"Categoria inválida no gabarito: {categoria!r} (use: {', '.join(CATEGORIAS)})")
            gabarito[Path(arquivo.strip()).name] = cat
    return gabarito


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida a classificação de materiais do ReciFavela.")
    parser.add_argument("pasta", type=Path, help="pasta com as fotos dos resíduos de teste")
    parser.add_argument("--gabarito", type=Path, help="CSV com as colunas arquivo e categoria_correta")
    parser.add_argument("--saida", type=Path, help="CSV onde salvar os resultados")
    parser.add_argument("--modelo", default=MODELO_PADRAO, help=f"modelo CLIP (padrão: {MODELO_PADRAO})")
    parser.add_argument("--lote", type=int, default=8, help="fotos processadas por vez")
    args = parser.parse_args()

    fotos = listar_imagens(args.pasta)
    if not fotos:
        sys.exit(f"Nenhuma imagem encontrada em {args.pasta}")

    gabarito = ler_gabarito(args.gabarito) if args.gabarito else {}

    print(f"Carregando o modelo {args.modelo}…")
    classificador = ClassificadorMateriais(args.modelo)
    print(f"Classificando {len(fotos)} fotos (dispositivo: {classificador.device})…\n")

    linhas = []
    for inicio in range(0, len(fotos), args.lote):
        grupo = fotos[inicio : inicio + args.lote]
        resultados = classificador.classificar_lote([f.read_bytes() for f in grupo])
        for foto, r in zip(grupo, resultados):
            correta = gabarito.get(foto.name) or inferir_categoria(foto.relative_to(args.pasta))
            linhas.append(
                {
                    "arquivo": str(foto.relative_to(args.pasta)),
                    "correta": correta,
                    "sistema": r.categoria,
                    "confianca": round(r.confianca, 3),
                    "acertou": None if correta is None else correta == r.categoria,
                    **{f"prob_{c}": round(r.probabilidades[c], 3) for c in CATEGORIAS},
                }
            )

    df = pd.DataFrame(linhas)
    resumo = resumir(df["correta"], df["sistema"])

    with pd.option_context("display.max_rows", None, "display.width", 120):
        print(df[["arquivo", "correta", "sistema", "confianca", "acertou"]].to_string(index=False))

    sem_gabarito = int(df["correta"].isna().sum())
    if sem_gabarito:
        print(f"\nAtenção: {sem_gabarito} foto(s) sem categoria correta (ignoradas no cálculo).")

    print("\nAcerto por material:")
    print(resumo.por_categoria.to_string(index=False))
    print("\nMatriz de confusão (linhas: correta · colunas: sistema):")
    print(resumo.matriz_confusao.to_string())

    print(f"\nAcertos: {resumo.acertos} de {resumo.total} ({resumo.acuracia:.1%})")
    if resumo.total != TOTAL_PREVISTO:
        print(f"(o protocolo prevê {TOTAL_PREVISTO} resíduos)")
    status = "ATINGIDA" if resumo.meta_atingida else "NÃO ATINGIDA"
    print(f"Meta de {META_ACERTO:.0%}: {status} (mínimo de {resumo.acertos_necessarios} acertos)")

    saida = args.saida or Path("validacao") / f"resultados_{datetime.now():%Y%m%d_%H%M%S}.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(saida, index=False, sep=";", encoding="utf-8-sig")
    print(f"\nResultados salvos em {saida}")


if __name__ == "__main__":
    main()
