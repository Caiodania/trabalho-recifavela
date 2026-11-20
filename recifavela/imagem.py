"""Funções leves de imagem (sem dependência do modelo, para a página carregar rápido)."""

from __future__ import annotations

import io

from PIL import Image, ImageOps


def abrir_imagem(dados: bytes | Image.Image) -> Image.Image:
    """Abre a imagem corrigindo a rotação de fotos de celular (EXIF)."""
    imagem = dados if isinstance(dados, Image.Image) else Image.open(io.BytesIO(dados))
    return ImageOps.exif_transpose(imagem).convert("RGB")


def quadrada(imagem: Image.Image) -> Image.Image:
    """Completa a imagem com bordas até ficar quadrada (evita cortar o objeto)."""
    lado = max(imagem.size)
    fundo = Image.new("RGB", (lado, lado), (128, 128, 128))
    fundo.paste(imagem, ((lado - imagem.width) // 2, (lado - imagem.height) // 2))
    return fundo
