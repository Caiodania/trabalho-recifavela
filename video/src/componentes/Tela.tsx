import React from "react";
import { Img, staticFile } from "remotion";
import { COR, ESCALA, NomeTela, TELAS, VH, VW } from "../tema";

/**
 * Uma captura real do site. A barra lateral fica fixa e a área principal rola,
 * como no navegador. `rolagem` está em px CSS do site.
 */
export const Tela: React.FC<{ nome: NomeTela; rolagem?: number; opacidade?: number }> = ({
  nome,
  rolagem = 0,
  opacidade = 1,
}) => {
  if (opacidade <= 0) return null;
  const info = TELAS[nome];
  const lateral = info.barraLateral * ESCALA;
  const largura = info.largura * ESCALA;
  const altura = info.altura * ESCALA;
  const src = staticFile(`telas/${nome}.png`);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: opacidade, background: COR.creme }}>
      <div style={{ position: "absolute", left: lateral, top: 0, width: VW - lateral, height: VH, overflow: "hidden" }}>
        <Img
          src={src}
          style={{ position: "absolute", left: -lateral, top: -rolagem * ESCALA, width: largura, height: altura }}
        />
      </div>
      <div style={{ position: "absolute", left: 0, top: 0, width: lateral, height: VH, overflow: "hidden" }}>
        <Img src={src} style={{ position: "absolute", left: 0, top: 0, width: largura, height: altura }} />
      </div>
    </div>
  );
};
