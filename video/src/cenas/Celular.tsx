import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { Fundo, Legenda } from "../componentes/Palco";
import { COR, fonteTexto, kf, saida } from "../tema";

const TELA_W = 310;
const TELA_H = Math.round((TELA_W * 2532) / 1170);
const BORDA = 14;

const Celular: React.FC<{ src: string; x: number; y: number; de: number; rotulo: string }> = ({ src, x, y, de, rotulo }) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        opacity: kf(frame, [de, de + 14], [0, 1]),
        translate: `0px ${kf(frame, [de, de + 26], [90, 0], saida) + Math.sin((frame + de) / 22) * 5}px`,
      }}
    >
      <div
        style={{
          width: TELA_W + 2 * BORDA,
          height: TELA_H + 2 * BORDA,
          borderRadius: 54,
          background: "#101513",
          padding: BORDA,
          boxShadow: "0 40px 70px rgba(0,0,0,0.5), inset 0 0 0 2px #2B3330",
        }}
      >
        <Img src={staticFile(src)} style={{ width: TELA_W, height: TELA_H, borderRadius: 40, display: "block" }} />
      </div>
      <div
        style={{
          marginTop: 22,
          textAlign: "center",
          fontFamily: fonteTexto,
          fontWeight: 600,
          fontSize: 28,
          color: COR.verdeClaro,
        }}
      >
        {rotulo}
      </div>
    </div>
  );
};

export const CelularCena: React.FC = () => {
  const w = TELA_W + 2 * BORDA;
  const gap = 110;
  const x0 = (1920 - (3 * w + 2 * gap)) / 2;
  return (
    <AbsoluteFill>
      <Fundo />
      <Legenda titulo="Feito para o celular" subtitulo="A câmera abre direto no navegador, sem instalar aplicativo" />
      <Celular src="telas/celular_inicio.png" x={x0} y={206} de={8} rotulo="Tire a foto" />
      <Celular src="telas/celular_material.png" x={x0 + w + gap} y={206} de={22} rotulo="Veja o material" />
      <Celular src="telas/celular_orientacoes.png" x={x0 + 2 * (w + gap)} y={206} de={36} rotulo="Siga as orientações" />
    </AbsoluteFill>
  );
};
