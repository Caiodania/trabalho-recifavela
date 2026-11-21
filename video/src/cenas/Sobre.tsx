import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { SEM_ZOOM, camera, kf } from "../tema";
import { CenaSite, cx, pt } from "./comum";
import { FOCO_MATRIZ, R_MATRIZ } from "./Validacao";

const R_EQUIPE = 1150;

export const Sobre: React.FC = () => {
  const frame = useCurrentFrame();
  // o menu lateral é o mesmo em todas as páginas
  const navSobre = pt("inicio", "navSobre", 0, 0.4, 0.5);
  const cam = camera(frame, [
    { f: 0, ...FOCO_MATRIZ },
    { f: 10, ...FOCO_MATRIZ },
    { f: 34, ...SEM_ZOOM },
  ]);
  return (
    <CenaSite titulo="Sobre o projeto" subtitulo="Problema, solução, tecnologia, validação e a equipe" {...cam}>
      <Tela nome="validacao_resultado" rolagem={R_MATRIZ} />
      <Tela nome="sobre" rolagem={kf(frame, [62, 128], [0, R_EQUIPE])} opacidade={kf(frame, [48, 56], [0, 1])} />
      <Destaque c={cx("sobre", "equipe", R_EQUIPE)} de={122} ate={175} />
      <Cursor
        caminho={[
          { f: 0, x: 1300, y: 560 },
          { f: 14, x: 1300, y: 560 },
          { f: 40, x: navSobre.x, y: navSobre.y },
          { f: 60, x: navSobre.x, y: navSobre.y },
          { f: 90, x: 1460, y: 620 },
        ]}
        cliques={[44]}
        aparece={8}
        some={100}
      />
    </CenaSite>
  );
};
