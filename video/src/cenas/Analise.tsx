import React from "react";
import { useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { COR, ESCALA, fonteTexto, kf } from "../tema";
import { CenaSite, cx, pt } from "./comum";
import { FOCO_ENVIO } from "./Inicio";

// Rolagem curta para a foto enviada caber inteira na tela (como faria quem usa o site).
export const R_ANALISE = 200;
export const FOCO_MATERIAL = { z: 1.75, ...pt("resultado", "material", R_ANALISE) };
export const CURSOR_MATERIAL = (() => {
  const c = cx("resultado", "material", R_ANALISE);
  return { x: c.x + c.w - 60, y: c.y + c.h - 18 };
})();

/** Linha de varredura sobre a foto enquanto o modelo analisa. */
const Varredura: React.FC<{ de: number; ate: number; rolagem: number }> = ({ de, ate, rolagem }) => {
  const frame = useCurrentFrame();
  const c = cx("analisando", "foto", rolagem);
  const op = kf(frame, [de, de + 8, ate - 8, ate], [0, 1, 1, 0]);
  if (op <= 0) return null;
  const ciclo = ((frame - de) % 36) / 36;
  return (
    <div style={{ position: "absolute", left: c.x, top: c.y, width: c.w, height: c.h, opacity: op, borderRadius: 10, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, background: "rgba(31,111,80,0.12)" }} />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: ciclo * c.h - 40,
          height: 40,
          background: "linear-gradient(180deg, rgba(120,230,170,0) 0%, rgba(120,230,170,0.55) 85%, rgba(200,255,225,0.95) 100%)",
        }}
      />
      {[
        { left: 10, top: 10, borderLeft: "4px solid white", borderTop: "4px solid white" },
        { right: 10, top: 10, borderRight: "4px solid white", borderTop: "4px solid white" },
        { left: 10, bottom: 10, borderLeft: "4px solid white", borderBottom: "4px solid white" },
        { right: 10, bottom: 10, borderRight: "4px solid white", borderBottom: "4px solid white" },
      ].map((s, i) => (
        <div key={i} style={{ position: "absolute", width: 34, height: 34, borderRadius: 4, ...s }} />
      ))}
    </div>
  );
};

/** Estado "Analisando a imagem…" da coluna de resultado (o mesmo aviso que o site mostra). */
const Analisando: React.FC<{ de: number; ate: number; rolagem: number }> = ({ de, ate, rolagem }) => {
  const frame = useCurrentFrame();
  const c = cx("analisando", "direita", rolagem);
  const op = kf(frame, [de, de + 6, ate - 6, ate], [0, 1, 1, 0]);
  if (op <= 0) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: c.x,
        top: c.y,
        width: c.w,
        height: c.h,
        opacity: op,
        borderRadius: 14,
        background: "white",
        border: "2px solid #DCE9E1",
        display: "flex",
        alignItems: "center",
        gap: 18 * ESCALA,
        paddingLeft: 26 * ESCALA,
        fontFamily: fonteTexto,
        color: COR.texto,
      }}
    >
      <div
        style={{
          width: 30,
          height: 30,
          borderRadius: 15,
          border: "4px solid #D5E7DD",
          borderTopColor: COR.verde,
          rotate: `${frame * 14}deg`,
        }}
      />
      <div style={{ fontSize: 19, lineHeight: 1.35 }}>
        <b>Analisando a imagem…</b>
        <br />
        <span style={{ color: "#5B6B64" }}>Comparando a foto com descrições de cada material</span>
      </div>
    </div>
  );
};

export const Analise: React.FC = () => {
  const frame = useCurrentFrame();
  const upload = pt("inicio", "upload");
  const rolagem = kf(frame, [36, 70], [0, R_ANALISE]);
  const foco = {
    zoom: kf(frame, [0, 36, 70, 112, 150], [FOCO_ENVIO.z, FOCO_ENVIO.z, 1.1, 1.1, FOCO_MATERIAL.z]),
    cx: kf(frame, [0, 36, 70, 112, 150], [FOCO_ENVIO.x, FOCO_ENVIO.x, 960, 960, FOCO_MATERIAL.x]),
    cy: kf(frame, [0, 36, 70, 112, 150], [FOCO_ENVIO.y, FOCO_ENVIO.y, 470, 470, FOCO_MATERIAL.y]),
  };
  return (
    <CenaSite
      passo="2"
      titulo="O sistema identifica o material"
      subtitulo="Visão computacional (modelo CLIP): plástico, papel, metal ou vidro"
      {...foco}
    >
      <Tela nome="inicio" rolagem={rolagem} />
      <Tela nome="analisando" rolagem={rolagem} opacidade={kf(frame, [24, 32], [0, 1])} />
      <Tela nome="resultado" rolagem={rolagem} opacidade={kf(frame, [104, 112], [0, 1])} />
      <Varredura de={34} ate={108} rolagem={rolagem} />
      <Analisando de={34} ate={108} rolagem={rolagem} />
      <Destaque c={cx("resultado", "material", R_ANALISE)} de={132} ate={240} escurecer />
      <Cursor
        caminho={[
          { f: 0, x: upload.x, y: upload.y },
          { f: 40, x: upload.x, y: upload.y },
          { f: 72, x: 870, y: 700 },
          { f: 140, x: 870, y: 700 },
          { f: 176, x: CURSOR_MATERIAL.x, y: CURSOR_MATERIAL.y },
        ]}
        cliques={[16]}
      />
    </CenaSite>
  );
};
