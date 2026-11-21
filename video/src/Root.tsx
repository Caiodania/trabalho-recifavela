import React from "react";
import { Composition, Folder } from "remotion";
import { CENAS, DURACAO_TOTAL, DemoDescarteCerto } from "./DemoDescarteCerto";
import { ALTURA, FPS, LARGURA } from "./tema";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Folder name="Cenas">
        {CENAS.map((c) => (
          <Composition
            key={c.id}
            id={c.id}
            component={c.componente}
            durationInFrames={c.duracao}
            fps={FPS}
            width={LARGURA}
            height={ALTURA}
          />
        ))}
      </Folder>
      <Composition
        id="DemoDescarteCerto"
        component={DemoDescarteCerto}
        durationInFrames={DURACAO_TOTAL}
        fps={FPS}
        width={LARGURA}
        height={ALTURA}
      />
    </>
  );
};
