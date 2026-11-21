import React from "react";
import { AbsoluteFill, Img, Interactive, staticFile, useCurrentFrame } from "remotion";
import { Fundo } from "../componentes/Palco";
import { COR, fonteTexto, fonteTitulo, kf, saida } from "../tema";

export const Abertura: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Fundo marca={false} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", paddingBottom: 60 }}>
        <Img
          name="Ícone ReciFavela"
          src={staticFile("marca/icone.svg")}
          style={{
            width: 168,
            height: 168,
            opacity: kf(frame, [0, 12], [0, 1]),
            scale: kf(frame, [0, 26], [0.6, 1], saida),
            filter: "drop-shadow(0 18px 30px rgba(0,0,0,0.35))",
          }}
        />
        <Interactive.Div
          name="Rótulo"
          style={{
            marginTop: 40,
            fontFamily: fonteTexto,
            fontWeight: 700,
            fontSize: 30,
            letterSpacing: 8,
            color: COR.laranja,
            opacity: kf(frame, [10, 26], [0, 1]),
          }}
        >
          COOPERATIVA RECIFAVELA
        </Interactive.Div>
        <Interactive.Div
          name="Título"
          style={{
            fontFamily: fonteTitulo,
            fontWeight: 700,
            fontSize: 140,
            lineHeight: 1.1,
            color: "white",
            opacity: kf(frame, [14, 32], [0, 1]),
            translate: `0px ${kf(frame, [14, 36], [40, 0], saida)}px`,
          }}
        >
          Descarte Certo
        </Interactive.Div>
        <Interactive.Div
          name="Subtítulo"
          style={{
            marginTop: 10,
            fontFamily: fonteTexto,
            fontWeight: 400,
            fontSize: 44,
            color: COR.verdeClaro,
            opacity: kf(frame, [26, 44], [0, 1]),
            translate: `0px ${kf(frame, [26, 48], [30, 0], saida)}px`,
          }}
        >
          Demonstração do protótipo: da foto à orientação de descarte
        </Interactive.Div>
      </AbsoluteFill>
      <Interactive.Div
        name="Rodapé"
        style={{
          position: "absolute",
          left: 160,
          right: 160,
          bottom: 72,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          opacity: kf(frame, [36, 56], [0, 1]),
        }}
      >
        <Img name="Logo Mauá" src={staticFile("marca/maua-branco.png")} style={{ height: 76 }} />
        <div style={{ fontFamily: fonteTexto, fontSize: 28, color: COR.verdeClaro, textAlign: "right", lineHeight: 1.4 }}>
          Geórgia Correa Simao · Bianca Las Casas · Maria Clara Meroi
          <br />
          Engenharia · Instituto Mauá de Tecnologia
        </div>
      </Interactive.Div>
    </AbsoluteFill>
  );
};
