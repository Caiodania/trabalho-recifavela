import React from "react";
import { Audio } from "@remotion/media";
import { mouseClick } from "@remotion/sfx";
import { Sequence, useCurrentFrame } from "remotion";
import { COR, kf, suave } from "../tema";

export type Ponto = { f: number; x: number; y: number };

/** Ponteiro do mouse que segue um caminho (px do visor) e clica nos quadros indicados. */
export const Cursor: React.FC<{ caminho: Ponto[]; cliques?: number[]; aparece?: number; some?: number }> = ({
  caminho,
  cliques = [],
  aparece,
  some,
}) => {
  const frame = useCurrentFrame();
  const fs = caminho.map((p) => p.f);
  const x = kf(frame, fs, caminho.map((p) => p.x), suave);
  const y = kf(frame, fs, caminho.map((p) => p.y), suave);
  const aperto = Math.min(1, ...cliques.map((c) => kf(frame, [c - 3, c, c + 6], [1, 0.8, 1])));
  const opacidade =
    (aparece === undefined ? 1 : kf(frame, [aparece, aparece + 10], [0, 1])) *
    (some === undefined ? 1 : kf(frame, [some, some + 10], [1, 0]));
  if (opacidade <= 0) return null;
  return (
    <>
      {cliques.map((c) => {
        const p = kf(frame, [c, c + 16], [0, 1]);
        if (frame < c || frame > c + 16) return null;
        return (
          <div
            key={c}
            style={{
              position: "absolute",
              left: x - 34,
              top: y - 34,
              width: 68,
              height: 68,
              borderRadius: 34,
              border: `4px solid ${COR.laranja}`,
              opacity: 1 - p,
              scale: 0.3 + p * 0.9,
            }}
          />
        );
      })}
      {cliques.map((c) => (
        <Sequence key={`som-${c}`} from={c - 1} durationInFrames={20} layout="none">
          <Audio src={mouseClick} volume={0.55} />
        </Sequence>
      ))}
      <svg
        width="34"
        height="46"
        viewBox="0 0 20 28"
        style={{
          position: "absolute",
          left: x - 2,
          top: y - 1,
          opacity: opacidade,
          scale: aperto,
          transformOrigin: "2px 1px",
          filter: "drop-shadow(0 3px 4px rgba(0,0,0,0.35))",
        }}
      >
        <path d="M1 1 L1 22 L6.5 17 L10.5 26 L14 24.5 L10 15.8 L17.5 15.8 Z" fill="white" stroke="#1B1B1B" strokeWidth="1.4" strokeLinejoin="round" />
      </svg>
    </>
  );
};
