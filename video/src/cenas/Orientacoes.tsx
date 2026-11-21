import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { camera, kf } from "../tema";
import { CenaSite, cx, pt } from "./comum";
import { CURSOR_LADO, FOCO_AVISO, R_AVISO } from "./Condicoes";

export const R_DESCARTE = 1520;
export const FOCO_DESCARTE = { z: 1.7, ...pt("condicao", "descarte", R_DESCARTE) };

export const Orientacoes: React.FC = () => {
  const frame = useCurrentFrame();
  const rolagem = kf(frame, [8, 62], [R_AVISO, R_DESCARTE]);
  const passos = pt("condicao", "passos", R_DESCARTE);
  const cam = camera(frame, [
    { f: 0, ...FOCO_AVISO },
    { f: 8, ...FOCO_AVISO },
    { f: 62, z: 1.2, x: passos.x, y: passos.y },
    { f: 112, z: 1.2, x: passos.x, y: passos.y },
    { f: 150, ...FOCO_DESCARTE },
  ]);
  return (
    <CenaSite
      passo="4"
      titulo="Como preparar e onde descartar"
      subtitulo="Passo a passo e a cor certa da lixeira (Resolução CONAMA 275/2001)"
      {...cam}
    >
      <Tela nome="condicao" rolagem={rolagem} />
      <Destaque c={cx("condicao", "passos", R_DESCARTE)} de={56} ate={116} />
      <Destaque c={cx("condicao", "descarte", R_DESCARTE)} de={138} ate={210} escurecer />
      <Cursor caminho={[{ f: 0, ...CURSOR_LADO }]} some={4} />
    </CenaSite>
  );
};
