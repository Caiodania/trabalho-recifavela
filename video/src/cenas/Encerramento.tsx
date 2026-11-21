import React from "react";
import { AbsoluteFill, Img, Interactive, staticFile, useCurrentFrame } from "remotion";
import { Fundo } from "../componentes/Palco";
import { COR, fonteTexto, fonteTitulo, kf, saida } from "../tema";

export const Encerramento: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Fundo marca={false} />
      <Interactive.Div
        name="Chamada"
        style={{
          position: "absolute",
          left: 160,
          top: 230,
          width: 1000,
          opacity: kf(frame, [6, 24], [0, 1]),
          translate: `0px ${kf(frame, [6, 30], [36, 0], saida)}px`,
        }}
      >
        <div style={{ fontFamily: fonteTexto, fontWeight: 700, fontSize: 30, letterSpacing: 6, color: COR.laranja }}>
          O SITE ESTÁ NO AR
        </div>
        <div style={{ fontFamily: fonteTitulo, fontWeight: 700, fontSize: 104, lineHeight: 1.08, color: "white", marginTop: 14 }}>
          Experimente agora
        </div>
        <div style={{ fontFamily: fonteTexto, fontWeight: 600, fontSize: 40, color: "white", marginTop: 26 }}>
          recifavela-descarte-certo.streamlit.app
        </div>
        <div style={{ fontFamily: fonteTexto, fontWeight: 400, fontSize: 32, color: COR.verdeClaro, marginTop: 14 }}>
          Aponte a câmera do celular para o QR code
        </div>
      </Interactive.Div>
      <Interactive.Div
        name="QR code"
        style={{
          position: "absolute",
          left: 1280,
          top: 190,
          width: 480,
          height: 480,
          borderRadius: 32,
          background: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "0 40px 80px rgba(0,0,0,0.4)",
          opacity: kf(frame, [14, 30], [0, 1]),
          scale: kf(frame, [14, 40], [0.85, 1], saida),
        }}
      >
        <Img name="QR code do site" src={staticFile("marca/qrcode.png")} style={{ width: 420, height: 420 }} />
      </Interactive.Div>
      <Interactive.Div
        name="Equipe"
        style={{
          position: "absolute",
          left: 160,
          right: 160,
          bottom: 84,
          display: "flex",
          alignItems: "center",
          gap: 40,
          paddingTop: 40,
          borderTop: "2px solid rgba(207,229,218,0.25)",
          opacity: kf(frame, [30, 50], [0, 1]),
        }}
      >
        <Img name="Logo Mauá" src={staticFile("marca/maua-branco.png")} style={{ height: 76 }} />
        <div style={{ fontFamily: fonteTexto, fontSize: 28, color: COR.verdeClaro, lineHeight: 1.45 }}>
          Geórgia Correa Simao · Bianca Las Casas · Maria Clara Meroi
          <br />
          Engenharia · Instituto Mauá de Tecnologia · 2026
        </div>
      </Interactive.Div>
    </AbsoluteFill>
  );
};
