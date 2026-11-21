import { loadFont as carregarInter } from "@remotion/google-fonts/Inter";
import { loadFont as carregarPoppins } from "@remotion/google-fonts/Poppins";
import { Easing, interpolate } from "remotion";
import telasJson from "./dados/telas.json";

// ---------------------------------------------------------------- tipografia e cores (mesmas do site)
export const { fontFamily: fonteTexto } = carregarInter("normal", {
  weights: ["400", "500", "600", "700"],
  subsets: ["latin", "latin-ext"],
});
export const { fontFamily: fonteTitulo } = carregarPoppins("normal", {
  weights: ["600", "700"],
  subsets: ["latin", "latin-ext"],
});

export const COR = {
  verde: "#1F6F50",
  verdeEscuro: "#0F3D2E",
  verdeNoite: "#0A271E",
  verdeClaro: "#CFE5DA",
  creme: "#FBF8F3",
  laranja: "#F2A65A",
  texto: "#1E2A25",
};

export const FPS = 30;
export const LARGURA = 1920;
export const ALTURA = 1080;

// ---------------------------------------------------------------- janela do navegador
// O site foi capturado com 1440 px de largura; dentro da janela ele aparece um pouco ampliado.
export const JANELA = { x: 160, y: 196, w: 1600, h: 844, barra: 48 };
export const VW = JANELA.w; // largura visível do site (px do vídeo)
export const VH = JANELA.h - JANELA.barra; // altura visível do site (px do vídeo)
export const ESCALA = VW / 1440;

// ---------------------------------------------------------------- telas capturadas do site real
export type Caixa = { x: number; y: number; w: number; h: number };
type InfoTela = { largura: number; altura: number; barraLateral: number; caixas: Record<string, Caixa | null> };

const extras: Record<string, InfoTela> = {
  analisando: { largura: 1440, altura: 900, barraLateral: 300, caixas: {} },
};
export const TELAS = { ...(telasJson as unknown as Record<string, InfoTela>), ...extras };
export type NomeTela = keyof typeof TELAS & string;

// Caixas medidas à mão nas capturas (avisos que só aparecem depois de marcar uma condição).
const CAIXAS_EXTRAS: Record<string, Caixa> = {
  "condicao.aviso": { x: 836, y: 1408, w: 508, h: 98 },
  "vidro_quebrado.aviso": { x: 836, y: 1394, w: 508, h: 110 },
  "analisando.direita": { x: 836, y: 412, w: 508, h: 96 },
  "analisando.foto": { x: 396, y: 601, w: 344, h: 258 },
};

export function caixa(tela: NomeTela, nome: string): Caixa {
  const c = CAIXAS_EXTRAS[`${tela}.${nome}`] ?? TELAS[tela].caixas[nome];
  if (!c) throw new Error(`Caixa ${tela}.${nome} não encontrada`);
  return c;
}

/** Converte uma caixa do site (px CSS) para px do visor, considerando a rolagem da área principal. */
export function noVisor(c: Caixa, rolagem = 0): Caixa {
  const naBarraLateral = c.x + c.w <= 300;
  return {
    x: c.x * ESCALA,
    y: (c.y - (naBarraLateral ? 0 : rolagem)) * ESCALA,
    w: c.w * ESCALA,
    h: c.h * ESCALA,
  };
}

export const centro = (c: Caixa, ax = 0.5, ay = 0.5) => ({ x: c.x + c.w * ax, y: c.y + c.h * ay });

// ---------------------------------------------------------------- animação
export const suave = Easing.bezier(0.65, 0, 0.35, 1);
export const saida = Easing.bezier(0.16, 1, 0.3, 1);

/** interpolate() com extrapolação travada e easing suave em cada trecho. */
export function kf(frame: number, quadros: number[], valores: number[], easing = suave) {
  return interpolate(frame, quadros, valores, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });
}

export type Quadro = { f: number; z: number; x: number; y: number };

/** Interpola a câmera (zoom e ponto de foco, em px do visor) ao longo de quadros-chave. */
export function camera(frame: number, chaves: Quadro[]) {
  const fs = chaves.map((c) => c.f);
  return {
    zoom: kf(frame, fs, chaves.map((c) => c.z)),
    cx: kf(frame, fs, chaves.map((c) => c.x)),
    cy: kf(frame, fs, chaves.map((c) => c.y)),
  };
}

/** Foco padrão (sem zoom): centro do visor. */
export const SEM_ZOOM = { z: 1, x: VW / 2, y: VH / 2 };
