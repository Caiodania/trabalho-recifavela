import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { SEM_ZOOM, camera } from "../tema";
import { CenaSite, cx, pt } from "./comum";

// Ponto final desta cena (reaproveitado no início da próxima, para a câmera não "pular").
export const FOCO_ENVIO = { z: 1.3, x: 640, y: 540 };

export const Inicio: React.FC = () => {
  const frame = useCurrentFrame();
  const cam = camera(frame, [
    { f: 0, ...SEM_ZOOM },
    { f: 70, ...SEM_ZOOM },
    { f: 112, ...FOCO_ENVIO },
  ]);
  const materiais = pt("inicio", "materiais", 0, 0.3, 0.3);
  const upload = pt("inicio", "upload");
  return (
    <CenaSite
      passo="1"
      titulo="Envie uma foto do resíduo"
      subtitulo="Pelo computador ou pela câmera do celular, um item por vez"
      {...cam}
    >
      <Tela nome="inicio" />
      <Destaque c={cx("inicio", "materiais")} de={34} ate={82} />
      <Destaque c={cx("inicio", "dropzone")} de={100} ate={160} />
      <Cursor
        caminho={[
          { f: 0, x: 1380, y: 760 },
          { f: 16, x: 1380, y: 760 },
          { f: 48, x: materiais.x, y: materiais.y },
          { f: 72, x: materiais.x + 40, y: materiais.y + 30 },
          { f: 108, x: upload.x, y: upload.y },
        ]}
      />
    </CenaSite>
  );
};
