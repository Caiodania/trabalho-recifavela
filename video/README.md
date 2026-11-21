# Vídeo de demonstração (Remotion)

Vídeo de ~72 segundos (1920 × 1080, 30 fps) que mostra o site **Descarte Certo** sendo usado:
envio da foto, identificação do material, probabilidades, perguntas sobre as condições,
orientações de preparo e descarte, um segundo exemplo (vidro quebrado), uso no celular,
validação com 30 resíduos e a página sobre o projeto.

As telas em `public/telas/` são capturas reais do site, feitas com um navegador automatizado
(Playwright) percorrendo cada etapa. O cursor, os cliques, o zoom e os destaques são animados
no Remotion. O resultado da validação (28 de 30, 93,3%) é o mesmo da apresentação.

O vídeo final fica em `../apresentacao/ReciFavela_Descarte_Certo_demo.mp4`.

## Comandos

Instalar as dependências:

```console
npm i
```

Abrir o editor (Remotion Studio) para ver e ajustar as cenas:

```console
npm run dev
```

Gerar o vídeo:

```console
npx remotion render DemoDescarteCerto out/ReciFavela_Descarte_Certo_demo.mp4 --crf=18
```

## Estrutura

```
src/
  DemoDescarteCerto.tsx   # sequência das cenas e transições
  tema.ts                 # cores, fontes, tamanho da janela e coordenadas das telas
  componentes/            # fundo, legenda, navegador, câmera, cursor, destaque, tela do site
  cenas/                  # uma cena por arquivo (Abertura, Inicio, Analise, …, Encerramento)
  dados/telas.json        # tamanho de cada captura e posição dos botões e cartões
public/
  telas/                  # capturas do site
  fotos/                  # as 30 fotos usadas na validação
  marca/                  # ícone ReciFavela, logo Mauá e QR code
```

Para mudar o texto de uma legenda, edite a cena correspondente em `src/cenas/`. Para mudar a
duração de uma cena, ajuste o valor em `src/DemoDescarteCerto.tsx` (em `CENAS` e na sequência).

O Remotion é gratuito para equipes de até 3 pessoas
([licença](https://www.remotion.dev/docs/license)).
