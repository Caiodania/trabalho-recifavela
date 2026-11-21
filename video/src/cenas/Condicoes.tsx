import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { camera, kf } from "../tema";
import { CenaSite, cx, pt, unir } from "./comum";
import { R_ANALISE } from "./Analise";
import { CURSOR_EXPLICACAO, FOCO_PROBS } from "./Explicacao";

const R1 = 680; // rolagem até as perguntas
export const R_AVISO = 1180; // rolagem até o resultado com o aviso
export const FOCO_AVISO = (() => {
  const g = unir(cx("condicao", "veredito", R_AVISO), cx("condicao", "aviso", R_AVISO));
  return { z: 1.45, x: g.x + g.w / 2, y: g.y + g.h / 2 };
})();
export const CURSOR_LADO = { x: 1480, y: 640 };

export const Condicoes: React.FC = () => {
  const frame = useCurrentFrame();
  const rolagem = kf(frame, [10, 56, 116, 160], [R_ANALISE, R1, R1, R_AVISO]);
  const perguntas = pt("explicacao", "condicoes", R1);
  const restos = pt("explicacao", "restos", R1, 0.15, 0.5);
  const cam = camera(frame, [
    { f: 0, ...FOCO_PROBS },
    { f: 10, ...FOCO_PROBS },
    { f: 56, z: 1.35, x: 1180, y: perguntas.y + 150 },
    { f: 116, z: 1.35, x: 1180, y: perguntas.y + 150 },
    { f: 160, ...FOCO_AVISO },
  ]);
  return (
    <CenaSite
      passo="3"
      titulo="Perguntas rápidas sobre as condições"
      subtitulo="Aqui, a embalagem ainda tem restos de comida: o site orienta a limpeza"
      {...cam}
    >
      <Tela nome="explicacao" rolagem={rolagem} />
      <Tela nome="condicao" rolagem={rolagem} opacidade={kf(frame, [94, 102], [0, 1])} />
      <Destaque c={cx("explicacao", "restos", R1)} de={66} ate={112} folga={12} />
      <Destaque c={cx("condicao", "aviso", R_AVISO)} de={156} ate={210} escurecer />
      <Cursor
        caminho={[
          { f: 0, x: CURSOR_EXPLICACAO.x, y: CURSOR_EXPLICACAO.y },
          { f: 56, x: CURSOR_EXPLICACAO.x, y: CURSOR_EXPLICACAO.y },
          { f: 88, x: restos.x, y: restos.y },
          { f: 112, x: restos.x, y: restos.y },
          { f: 140, ...CURSOR_LADO },
        ]}
        cliques={[92]}
      />
    </CenaSite>
  );
};
