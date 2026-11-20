# Protocolo de validação do protótipo

**Objetivo:** verificar se o sistema identifica corretamente o material de resíduos reais e se as
orientações de preparo e descarte são adequadas.

**Meta:** pelo menos **80% de acerto** na identificação, ou seja, **24 dos 30** resíduos testados.

## 1. Seleção dos 30 resíduos

Separe resíduos reais, de preferência do próprio fluxo da ReciFavela, distribuídos entre as quatro
categorias. A classificação correta de cada um deve ser definida **antes** do teste e anotada no
gabarito.

Sugestão (8 + 8 + 7 + 7):

| Plástico (8) | Papel e papelão (8) | Metal (7) | Vidro (7) |
|---|---|---|---|
| Garrafa PET de refrigerante | Caixa de papelão | Lata de refrigerante | Garrafa de cerveja |
| Garrafa de água | Folha de caderno | Lata de cerveja amassada | Garrafa de vinho |
| Frasco de detergente | Jornal | Lata de conserva (milho, ervilha) | Pote de conserva |
| Frasco de xampu | Revista | Lata de sardinha | Pote de maionese ou geleia |
| Pote de margarina | Caixa de cereal | Tampa metálica de pote | Copo de vidro |
| Copo descartável | Caixa de ovos (papelão) | Papel-alumínio amassado | Frasco de perfume |
| Sacola plástica | Saco de pão (papel) | Lata de leite em pó | Garrafa de azeite |
| Pote de iogurte | Caixa de sapato | | |

Inclua resíduos em **condições variadas** (limpos, sujos, amassados, com rótulo, quebrados) para
testar também as perguntas sobre as condições e as orientações resultantes.

## 2. Fotografia

- Um resíduo por foto, ocupando boa parte da imagem.
- Boa iluminação, sem contraluz.
- Fundo preferencialmente liso; registre também algumas fotos em situação real (sobre a mesa,
  no chão do galpão) para refletir o uso cotidiano.
- Use o celular que será usado na prática, sem filtros.
- Nomeie os arquivos com a categoria correta: `plastico_01.jpg`, `papel_01.jpg`, `metal_01.jpg`,
  `vidro_01.jpg`… (ou organize em pastas `plastico/`, `papel/`, `metal/`, `vidro/`).

Guarde as fotos em `validacao/fotos/` (pasta ignorada pelo Git).

## 3. Gabarito

Preencha `validacao/gabarito.csv` a partir do modelo `gabarito_modelo.csv`
(colunas `arquivo` e `categoria_correta`; as demais são opcionais). Se os arquivos estiverem
nomeados pela categoria, o gabarito é opcional.

## 4. Execução

**Pelo site:** abra a página *Validação do protótipo*, envie as 30 fotos de uma vez, confira a coluna
*Classificação correta* e baixe a planilha de resultados.

**Pela linha de comando:**

```bash
python avaliar.py validacao/fotos --gabarito validacao/gabarito.csv
```

O relatório mostra os acertos, a taxa de acerto, o acerto por material, a matriz de confusão e
salva um CSV com o resultado de cada foto.

## 5. Avaliação das orientações

Para cada resíduo, abra a página *Analisar resíduo*, envie a foto, responda às perguntas sobre as
condições e verifique, de preferência com a equipe da ReciFavela:

1. A situação indicada (reciclável, com cuidados, não reciclável, descarte especial) está correta?
2. Os passos de preparo são adequados e suficientes?
3. O local de descarte indicado está correto?

Registre *Sim* ou *Não* na coluna **Orientações adequadas?** da página de validação e anote
sugestões de ajuste em **Observações**. Os textos ficam em `recifavela/orientacoes.py`.

## 6. Se a meta não for atingida

- Veja na matriz de confusão quais materiais estão sendo trocados.
- Ajuste ou acrescente descrições dos objetos confundidos em `DESCRICOES`
  (`recifavela/classificador.py`), por exemplo `"a transparent plastic cup"`.
- Refaça as fotos problemáticas seguindo as orientações da seção 2 e repita o teste.
- Registre no relatório o resultado de cada rodada.
