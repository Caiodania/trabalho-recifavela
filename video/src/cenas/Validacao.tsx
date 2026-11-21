import React from "react";
import { Audio } from "@remotion/media";
import { ding } from "@remotion/sfx";
import { Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Cursor } from "../componentes/Cursor";
import { Destaque } from "../componentes/Palco";
import { Tela } from "../componentes/Tela";
import { COR, SEM_ZOOM, camera, fonteTexto, kf, saida } from "../tema";
import { CenaSite, cx, pt } from "./comum";

const FOTOS = [
  ...Array.from({ length: 7 }, (_, i) => `metal_0${i + 1}`),
  ...Array.from({ length: 8 }, (_, i) => `papel_0${i + 1}`),
  ...Array.from({ length: 8 }, (_, i) => `plastico_0${i + 1}`),
  ...Array.from({ length: 7 }, (_, i) => `vidro_0${i + 1}`),
];

const R_RESULTADO = 940; // rolagem até as métricas
export const R_MATRIZ = 1290; // rolagem até a matriz de confusão
export const FOCO_MATRIZ = { z: 1.3, ...pt("validacao_resultado", "matriz", R_MATRIZ) };

/** As 30 fotos "voando" para a área de envio. */
const FotosEnviadas: React.FC<{ de: number }> = ({ de }) => {
  const frame = useCurrentFrame();
  const alvo = pt("validacao_inicio", "dropzone");
  return (
    <>
      {FOTOS.map((nome, i) => {
        const ini = de + i * 1.3;
        const p = kf(frame, [ini, ini + 20], [0, 1], saida);
        if (frame < ini || p >= 1) return null;
        const col = i % 6;
        const lin = Math.floor(i / 6);
        const x0 = 1030 + col * 92;
        const y0 = 470 + lin * 70;
        return (
          <Img
            key={nome}
            src={staticFile(`fotos/${nome}.jpg`)}
            style={{
              position: "absolute",
              left: x0 + (alvo.x - 40 - x0) * p,
              top: y0 + (alvo.y - 30 - y0) * p,
              width: 84,
              height: 63,
              borderRadius: 8,
              objectFit: "cover",
              opacity: kf(frame, [ini, ini + 4, ini + 16, ini + 20], [0, 1, 1, 0]),
              scale: 1 - 0.55 * p,
              boxShadow: "0 6px 14px rgba(0,0,0,0.25)",
              border: "2px solid white",
            }}
          />
        );
      })}
    </>
  );
};

/** Barra "Classificando as fotos… (n/30)", como a do site. */
const Progresso: React.FC<{ de: number; ate: number }> = ({ de, ate }) => {
  const frame = useCurrentFrame();
  const c = cx("validacao_inicio", "dropzone");
  const op = kf(frame, [de, de + 6, ate - 6, ate], [0, 1, 1, 0]);
  if (op <= 0) return null;
  const p = kf(frame, [de + 4, ate - 8], [0, 1]);
  return (
    <div
      style={{
        position: "absolute",
        left: c.x - 12,
        top: c.y + c.h + 14,
        width: c.w + 24,
        padding: "12px 12px 18px",
        background: COR.creme,
        opacity: op,
        fontFamily: fonteTexto,
      }}
    >
      <div style={{ fontSize: 20, color: COR.texto, marginBottom: 10 }}>
        Classificando as fotos… ({Math.round(p * 30)}/30)
      </div>
      <div style={{ height: 10, borderRadius: 5, background: "#E6E0D6" }}>
        <div style={{ height: 10, borderRadius: 5, width: `${p * 100}%`, background: COR.verde }} />
      </div>
    </div>
  );
};

export const Validacao: React.FC = () => {
  const frame = useCurrentFrame();
  const nav = pt("inicio", "navValidacao", 0, 0.45, 0.5);
  const upload = pt("validacao_inicio", "upload");
  const zona = pt("validacao_inicio", "dropzone");
  // métricas + faixa "Meta atingida" logo abaixo delas
  const m = cx("validacao_resultado", "metricas", R_RESULTADO);
  const metricas = { ...m, h: m.h + 92 };
  const rolagem = kf(frame, [196, 236, 300, 334], [0, R_RESULTADO, R_RESULTADO, R_MATRIZ]);
  const cam = camera(frame, [
    { f: 0, ...SEM_ZOOM },
    { f: 58, ...SEM_ZOOM },
    { f: 86, z: 1.3, x: zona.x, y: zona.y + 120 },
    { f: 176, z: 1.3, x: zona.x, y: zona.y + 120 },
    { f: 196, ...SEM_ZOOM },
    { f: 236, ...SEM_ZOOM },
    { f: 262, z: 1.45, x: metricas.x + metricas.w / 2, y: metricas.y + metricas.h / 2 },
    { f: 300, z: 1.45, x: metricas.x + metricas.w / 2, y: metricas.y + metricas.h / 2 },
    { f: 334, ...FOCO_MATRIZ },
  ]);
  return (
    <CenaSite
      titulo="Validação com 30 resíduos"
      subtitulo="O site calcula a taxa de acerto, a matriz de confusão e gera a planilha do relatório"
      {...cam}
    >
      <Tela nome="inicio" />
      <Tela nome="validacao_inicio" opacidade={kf(frame, [46, 54], [0, 1])} />
      <Tela nome="validacao_resultado" rolagem={rolagem} opacidade={kf(frame, [172, 180], [0, 1])} />
      <FotosEnviadas de={94} />
      <Progresso de={124} ate={176} />
      <Destaque c={metricas} de={250} ate={306} escurecer />
      <Destaque c={cx("validacao_resultado", "matriz", R_MATRIZ)} de={326} ate={372} escurecer />
      <Cursor
        caminho={[
          { f: 0, x: 900, y: 520 },
          { f: 12, x: 900, y: 520 },
          { f: 38, x: nav.x, y: nav.y },
          { f: 56, x: nav.x, y: nav.y },
          { f: 84, x: upload.x, y: upload.y },
          { f: 110, x: upload.x, y: upload.y },
          { f: 150, x: 1450, y: 700 },
        ]}
        cliques={[42, 88]}
        aparece={4}
      />
      <Sequence from={252} durationInFrames={60} layout="none">
        <Audio src={ding} volume={0.35} />
      </Sequence>
    </CenaSite>
  );
};
