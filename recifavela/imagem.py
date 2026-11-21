from __future__ import annotations

import io

from PIL import Image, ImageOps


def abrir_imagem(dados: bytes | Image.Image) -> Image.Image:
    imagem = dados if isinstance(dados, Image.Image) else Image.open(io.BytesIO(dados))
    # corrige a rotação das fotos de celular
    return ImageOps.exif_transpose(imagem).convert("RGB")


def quadrada(imagem: Image.Image) -> Image.Image:
    lado = max(imagem.size)
    fundo = Image.new("RGB", (lado, lado), (128, 128, 128))
    fundo.paste(imagem, ((lado - imagem.width) // 2, (lado - imagem.height) // 2))
    return fundo
