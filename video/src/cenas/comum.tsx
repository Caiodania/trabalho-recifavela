import React from "react";
import { AbsoluteFill } from "remotion";
import { Camera, Fundo, Legenda, Navegador } from "../componentes/Palco";
import { Caixa, NomeTela, caixa, centro, noVisor } from "../tema";

/** Estrutura das cenas que mostram o site: fundo, legenda e navegador com câmera. */
export const CenaSite: React.FC<{
  passo?: string;
  titulo: string;
  subtitulo: string;
  zoom: number;
  cx: number;
  cy: number;
  children: React.ReactNode;
}> = ({ passo, titulo, subtitulo, zoom, cx, cy, children }) => (
  <AbsoluteFill>
    <Fundo />
    <Legenda passo={passo} titulo={titulo} subtitulo={subtitulo} />
    <Navegador>
      <Camera zoom={zoom} cx={cx} cy={cy}>
        {children}
      </Camera>
    </Navegador>
  </AbsoluteFill>
);

/** Caixa de um elemento da tela, já convertida para px do visor. */
export const cx = (tela: NomeTela, nome: string, rolagem = 0): Caixa => noVisor(caixa(tela, nome), rolagem);

/** Ponto de um elemento (fração ax, ay da caixa), em px do visor. */
export const pt = (tela: NomeTela, nome: string, rolagem = 0, ax = 0.5, ay = 0.5) => centro(cx(tela, nome, rolagem), ax, ay);

/** Junta duas caixas numa só (para destacar um grupo). */
export const unir = (a: Caixa, b: Caixa): Caixa => {
  const x = Math.min(a.x, b.x);
  const y = Math.min(a.y, b.y);
  return { x, y, w: Math.max(a.x + a.w, b.x + b.w) - x, h: Math.max(a.y + a.h, b.y + b.h) - y };
};
