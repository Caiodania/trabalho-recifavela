import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { camera, kf } from "../tema";
import { CURSOR_MATERIAL, FOCO_MATERIAL, R_ANALISE } from "./Analise";
import { CenaSite, cx, pt } from "./comum";

export const FOCO_PROBS = { z: 1.85, ...pt("explicacao", "probs", R_ANALISE) };
export const CURSOR_EXPLICACAO = pt("resultado", "explicacao", R_ANALISE, 0.12, 0.5);

export const Explicacao: React.FC = () => {
  const frame = useCurrentFrame();
  const link = pt("resultado", "explicacao", R_ANALISE, 0.5, 0.5);
  const cam = camera(frame, [
    { f: 0, ...FOCO_MATERIAL },
    { f: 14, ...FOCO_MATERIAL },
    { f: 46, z: 1.5, x: link.x, y: link.y - 60 },
    { f: 70, z: 1.5, x: link.x, y: link.y - 60 },
    { f: 108, ...FOCO_PROBS },
  ]);
  return (
    <CenaSite
      passo="2"
      titulo="Transparência na decisão"
      subtitulo="O site mostra a probabilidade de cada material e permite corrigir se errar"
      {...cam}
    >
      <Tela nome="resultado" rolagem={R_ANALISE} />
      <Tela nome="explicacao" rolagem={R_ANALISE} opacidade={kf(frame, [56, 64], [0, 1])} />
      <Destaque c={cx("explicacao", "probs", R_ANALISE)} de={96} ate={185} escurecer />
      <Cursor
        caminho={[
          { f: 0, x: CURSOR_MATERIAL.x, y: CURSOR_MATERIAL.y },
          { f: 18, x: CURSOR_MATERIAL.x, y: CURSOR_MATERIAL.y },
          { f: 48, x: CURSOR_EXPLICACAO.x, y: CURSOR_EXPLICACAO.y },
        ]}
        cliques={[53]}
      />
    </CenaSite>
  );
};
