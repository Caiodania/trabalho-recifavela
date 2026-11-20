"""Configurações gerais (sem dependências pesadas, para as páginas carregarem rápido)."""

import os

# Modelo CLIP usado na classificação. Pode ser trocado pela variável de ambiente RECIFAVELA_MODELO.
MODELO_PADRAO = os.environ.get("RECIFAVELA_MODELO", "openai/clip-vit-large-patch14")
