import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { Abertura } from "./cenas/Abertura";
import { Analise } from "./cenas/Analise";
import { CelularCena } from "./cenas/Celular";
import { Condicoes } from "./cenas/Condicoes";
import { Encerramento } from "./cenas/Encerramento";
import { Explicacao } from "./cenas/Explicacao";
import { Inicio } from "./cenas/Inicio";
import { Orientacoes } from "./cenas/Orientacoes";
import { Sobre } from "./cenas/Sobre";
import { Validacao } from "./cenas/Validacao";
import { Vidro } from "./cenas/Vidro";

// Duração de cada cena (quadros a 30 fps). A transição entre cenas é um esmaecimento de 12 quadros.
export const CENAS = [
  { id: "Abertura", componente: Abertura, duracao: 120 },
  { id: "Inicio", componente: Inicio, duracao: 150 },
  { id: "Analise", componente: Analise, duracao: 240 },
  { id: "Explicacao", componente: Explicacao, duracao: 180 },
  { id: "Condicoes", componente: Condicoes, duracao: 210 },
  { id: "Orientacoes", componente: Orientacoes, duracao: 210 },
  { id: "Vidro", componente: Vidro, duracao: 255 },
  { id: "Celular", componente: CelularCena, duracao: 180 },
  { id: "Validacao", componente: Validacao, duracao: 380 },
  { id: "Sobre", componente: Sobre, duracao: 165 },
  { id: "Encerramento", componente: Encerramento, duracao: 210 },
] as const;

export const TRANSICAO = 12;
export const DURACAO_TOTAL = CENAS.reduce((s, c) => s + c.duracao, 0) - TRANSICAO * (CENAS.length - 1);

export const DemoDescarteCerto: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence name="Abertura" durationInFrames={120}>
      <Abertura />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="1 · Envio da foto" durationInFrames={150}>
      <Inicio />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="2 · Identificação" durationInFrames={240}>
      <Analise />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="2 · Transparência" durationInFrames={180}>
      <Explicacao />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="3 · Condições" durationInFrames={210}>
      <Condicoes />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="4 · Orientações" durationInFrames={210}>
      <Orientacoes />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="Vidro quebrado" durationInFrames={255}>
      <Vidro />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="Celular" durationInFrames={180}>
      <CelularCena />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="Validação" durationInFrames={380}>
      <Validacao />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="Sobre" durationInFrames={165}>
      <Sobre />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSICAO })} />
    <TransitionSeries.Sequence name="Encerramento" durationInFrames={210}>
      <Encerramento />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
