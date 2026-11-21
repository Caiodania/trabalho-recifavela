import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { ESCALA, SEM_ZOOM, camera, kf } from "../tema";
import { CenaSite, cx, pt, unir } from "./comum";
import { CURSOR_LADO } from "./Condicoes";
import { FOCO_DESCARTE, R_DESCARTE } from "./Orientacoes";

const R1 = 680;
const R2 = 1140;

export const Vidro: React.FC = () => {
  const frame = useCurrentFrame();
  const material = pt("vidro", "material");
  const perguntas = pt("vidro", "condicoes", R1);
  const quebrado = pt("vidro", "quebrado", R1, 0.2, 0.5);
  const grupo = unir(cx("vidro_quebrado", "veredito", R2), cx("vidro_quebrado", "aviso", R2));
  const maisArquivo = { x: 418 * ESCALA, y: 562 * ESCALA }; // botão "+" do envio de arquivo
  const rolagemAntes = kf(frame, [8, 44], [R_DESCARTE, 0]);
  const rolagemDepois = kf(frame, [126, 158, 182, 214], [0, R1, R1, R2]);
  const cam = camera(frame, [
    { f: 0, ...FOCO_DESCARTE },
    { f: 8, ...FOCO_DESCARTE },
    { f: 44, ...SEM_ZOOM },
    { f: 76, ...SEM_ZOOM },
    { f: 104, z: 1.75, x: material.x, y: material.y },
    { f: 126, z: 1.75, x: material.x, y: material.y },
    { f: 158, z: 1.35, x: 1180, y: perguntas.y + 150 },
    { f: 182, z: 1.35, x: 1180, y: perguntas.y + 150 },
    { f: 214, z: 1.42, x: grupo.x + grupo.w / 2, y: grupo.y + grupo.h / 2 },
  ]);
  return (
    <CenaSite
      titulo="Cada material tem as próprias regras"
      subtitulo="Vidro quebrado é reciclável, mas precisa ser embalado com cuidado"
      {...cam}
    >
      <Tela nome="condicao" rolagem={rolagemAntes} />
      <Tela nome="vidro" rolagem={rolagemDepois} opacidade={kf(frame, [66, 74], [0, 1])} />
      <Tela nome="vidro_quebrado" rolagem={rolagemDepois} opacidade={kf(frame, [170, 178], [0, 1])} />
      <Destaque c={cx("vidro", "material")} de={86} ate={128} escurecer />
      <Destaque c={cx("vidro_quebrado", "aviso", R2)} de={208} ate={255} escurecer />
      <Cursor
        caminho={[
          { f: 0, x: 1100, y: 660 },
          { f: 30, x: 1100, y: 660 },
          { f: 58, ...maisArquivo },
          { f: 90, ...maisArquivo },
          { f: 128, x: 1250, y: 760 },
          { f: 160, x: quebrado.x, y: quebrado.y },
          { f: 178, x: quebrado.x, y: quebrado.y },
          { f: 206, ...CURSOR_LADO },
        ]}
        cliques={[62, 166]}
        aparece={28}
      />
    </CenaSite>
  );
};
