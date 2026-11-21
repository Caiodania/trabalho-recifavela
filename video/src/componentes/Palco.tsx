import React from "react";
import { AbsoluteFill, Img, Interactive, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { COR, Caixa, JANELA, VH, VW, fonteTexto, fonteTitulo, kf, saida } from "../tema";

/** Fundo verde da marca ReciFavela, com um brilho que se move devagar. */
export const Fundo: React.FC<{ marca?: boolean }> = ({ marca = true }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill
      name="Fundo"
      style={{
        background: `radial-gradient(circle at ${interpolate(frame, [0, durationInFrames], [78, 70])}% 0%, #2A8A63 0%, ${COR.verdeEscuro} 42%, ${COR.verdeNoite} 100%)`,
      }}
    >
      {marca ? (
        <Interactive.Div
          name="Marca"
          style={{
            position: "absolute",
            right: 160,
            top: 64,
            display: "flex",
            alignItems: "center",
            gap: 14,
            opacity: 0.9,
          }}
        >
          <Img name="Ícone ReciFavela" src={staticFile("marca/icone.svg")} style={{ width: 52, height: 52 }} />
          <div style={{ fontFamily: fonteTitulo, fontWeight: 700, fontSize: 30, color: "white", lineHeight: 1.05 }}>
            Descarte Certo
            <div style={{ fontFamily: fonteTexto, fontWeight: 500, fontSize: 18, color: COR.verdeClaro, letterSpacing: 2 }}>
              RECIFAVELA
            </div>
          </div>
        </Interactive.Div>
      ) : null}
    </AbsoluteFill>
  );
};

/** Legenda de cada etapa, no alto do vídeo. */
export const Legenda: React.FC<{ passo?: string; titulo: string; subtitulo: string }> = ({ passo, titulo, subtitulo }) => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="Legenda"
      style={{
        position: "absolute",
        left: JANELA.x,
        top: 44,
        width: 1330,
        display: "flex",
        alignItems: "flex-start",
        gap: 26,
        opacity: kf(frame, [4, 22], [0, 1], saida),
        translate: `0px ${kf(frame, [4, 26], [24, 0], saida)}px`,
      }}
    >
      {passo ? (
        <div
          style={{
            flex: "0 0 auto",
            width: 68,
            height: 68,
            marginTop: 4,
            borderRadius: 34,
            background: COR.laranja,
            color: COR.verdeNoite,
            fontFamily: fonteTitulo,
            fontWeight: 700,
            fontSize: 36,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {passo}
        </div>
      ) : null}
      <div>
        <div style={{ fontFamily: fonteTitulo, fontWeight: 700, fontSize: 56, lineHeight: 1.12, color: "white" }}>
          {titulo}
        </div>
        <div style={{ fontFamily: fonteTexto, fontWeight: 400, fontSize: 32, lineHeight: 1.3, color: COR.verdeClaro, marginTop: 6 }}>
          {subtitulo}
        </div>
      </div>
    </Interactive.Div>
  );
};

/** Janela de navegador com o endereço público do site. */
export const Navegador: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div
      style={{
        position: "absolute",
        left: JANELA.x,
        top: JANELA.y,
        width: JANELA.w,
        height: JANELA.h,
        borderRadius: 18,
        overflow: "hidden",
        background: COR.creme,
        boxShadow: "0 40px 90px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.08)",
      }}
    >
      <div
        style={{
          height: JANELA.barra,
          background: "#ECE8E1",
          borderBottom: "1px solid #DDD6CB",
          display: "flex",
          alignItems: "center",
          paddingLeft: 22,
          gap: 10,
        }}
      >
        {["#EC6A5E", "#F4BF4F", "#61C554"].map((c) => (
          <div key={c} style={{ width: 14, height: 14, borderRadius: 7, background: c }} />
        ))}
        <div
          style={{
            marginLeft: 40,
            height: 32,
            width: 620,
            borderRadius: 16,
            background: "white",
            display: "flex",
            alignItems: "center",
            gap: 10,
            paddingLeft: 16,
            fontFamily: fonteTexto,
            fontSize: 18,
            color: "#3C4A43",
          }}
        >
          <svg width="14" height="16" viewBox="0 0 14 16">
            <rect x="1" y="7" width="12" height="9" rx="2" fill="#5E6B64" />
            <path d="M4 7V5a3 3 0 0 1 6 0v2" stroke="#5E6B64" strokeWidth="2" fill="none" />
          </svg>
          recifavela-descarte-certo.streamlit.app
        </div>
      </div>
      <div style={{ position: "relative", width: VW, height: VH, overflow: "hidden" }}>{children}</div>
    </div>
  );
};

/** Câmera dentro do visor: zoom em torno de um ponto (em px do visor), sem sair da tela. */
export const Camera: React.FC<{ zoom: number; cx: number; cy: number; children: React.ReactNode }> = ({
  zoom,
  cx,
  cy,
  children,
}) => {
  const mx = VW / (2 * zoom);
  const my = VH / (2 * zoom);
  const x = Math.min(Math.max(cx, mx), VW - mx);
  const y = Math.min(Math.max(cy, my), VH - my);
  return (
    <AbsoluteFill
      style={{
        transformOrigin: "0 0",
        transform: `translate(${VW / 2 - x * zoom}px, ${VH / 2 - y * zoom}px) scale(${zoom})`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

/** Moldura laranja que chama a atenção para uma área (opcionalmente escurecendo o resto). */
export const Destaque: React.FC<{ c: Caixa; de: number; ate: number; escurecer?: boolean; folga?: number }> = ({
  c,
  de,
  ate,
  escurecer = false,
  folga = 10,
}) => {
  const frame = useCurrentFrame();
  const opacidade = kf(frame, [de, de + 10, ate - 10, ate], [0, 1, 1, 0]);
  if (opacidade <= 0) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: c.x - folga,
        top: c.y - folga,
        width: c.w + 2 * folga,
        height: c.h + 2 * folga,
        borderRadius: 18,
        border: `4px solid ${COR.laranja}`,
        opacity: opacidade,
        scale: kf(frame, [de, de + 14], [1.05, 1], saida),
        boxShadow: escurecer
          ? `0 0 0 3000px rgba(8, 28, 21, ${0.38 * opacidade}), 0 0 30px rgba(242,166,90,0.55)`
          : "0 0 30px rgba(242,166,90,0.55)",
      }}
    />
  );
};
