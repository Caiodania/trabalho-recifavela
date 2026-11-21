# ♻️ ReciFavela · Descarte Certo

Protótipo de site para a **ReciFavela**, cooperativa de reciclagem, que usa visão computacional
para facilitar a identificação e o descarte correto de resíduos.

## Como funciona

1. O usuário **tira uma foto** ou **envia uma imagem** do resíduo.
2. Um modelo de visão computacional (**CLIP**, da OpenAI) identifica o material.
3. O material é classificado em **plástico, papel, metal ou vidro** — o usuário pode corrigir se
   a identificação estiver errada.
4. O site informa se o resíduo é **reciclável** e faz **perguntas sobre as condições**
   (está sujo? quebrado? é metalizado? é lâmpada?…), que podem mudar o resultado para
   *reciclável com cuidados*, *não reciclável* ou *descarte especial*.
5. São apresentadas as **orientações de preparo** e o **local de descarte** (com a cor da
   lixeira da coleta seletiva, conforme a Resolução CONAMA 275/2001).

O site tem três páginas:

| Página | Conteúdo |
|---|---|
| **Analisar resíduo** | Duas áreas: à esquerda, o envio da foto; à direita, o resultado da análise em etapas numeradas (material → condições → resultado e orientações). |
| **Validação do protótipo** | Teste com os 30 resíduos reais: taxa de acerto, meta de 80%, matriz de confusão e planilha de resultados. |
| **Sobre o projeto** | Problema, solução, tecnologia, método de validação, resultados preliminares, equipe e referências. |

### Identidade visual

- **Cores:** verde (sustentabilidade), areia (fundo acolhedor) e laranja-terracota (o sol de
  Recife). As cores das lixeiras seguem o padrão CONAMA: vermelho (plástico), azul (papel),
  amarelo (metal) e verde (vidro).
- **Tipografia:** Poppins nos títulos e Inter no texto (Google Fonts).
- **Acessibilidade:** a situação do resíduo é indicada por texto e ícone, não só pela cor;
  layout responsivo para celular.
- Estilos e componentes visuais ficam em `recifavela/ui.py`; o tema do Streamlit, em
  `.streamlit/config.toml`; o logotipo, em `assets/`.

### Dados da equipe

Os nomes das integrantes, curso, disciplina, instituição e orientação aparecem na página
*Sobre o projeto* e no rodapé. Edite-os em [`recifavela/projeto.py`](recifavela/projeto.py).

## Instalação

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

(No Linux/macOS: `source .venv/bin/activate`.)

```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

O site abre em `http://localhost:8501`. Na **primeira análise** o modelo (≈1,7 GB) é baixado do
Hugging Face e carregado; depois disso cada foto leva cerca de 1 a 3 segundos em CPU.

Para usar o site no celular (e tirar fotos com a câmera dele), acesse o endereço *Network URL*
mostrado no terminal estando na mesma rede Wi-Fi. A câmera do navegador exige HTTPS fora do
`localhost`; se ela não abrir, use a opção **Enviar imagem**, que no celular também permite
fotografar.

### Modelo mais leve

Em computadores com pouca memória, use uma versão menor do CLIP (mais rápida, porém menos
precisa):

```bash
set RECIFAVELA_MODELO=openai/clip-vit-base-patch16
```

(No Linux/macOS: `export RECIFAVELA_MODELO=openai/clip-vit-base-patch16`.)

## Publicação (Streamlit Community Cloud)

**Site publicado:** <https://recifavela-descarte-certo.streamlit.app>

O site é publicado gratuitamente no [Streamlit Community Cloud](https://share.streamlit.io), a
partir deste repositório: branch `main`, arquivo principal `app.py`, Python 3.13. Cada `git push`
na `main` atualiza o site automaticamente. Mudanças nos módulos de `recifavela/` (como `ui.py` ou
`projeto.py`) só aparecem depois de reiniciar o app no painel: *Manage app → ⋮ → Reboot app*.

- O `requirements.txt` instala o PyTorch **somente para CPU**, evitando baixar as bibliotecas de
  GPU, que o servidor não usa.
- O modelo ocupa cerca de 2,1 GB de memória, dentro do limite do plano gratuito (≈2,7 GB).
- Depois de um período sem acessos, o app "dorme"; o primeiro acesso seguinte leva alguns minutos
  para acordar e baixar o modelo de novo.
- No endereço publicado (HTTPS), a câmera do celular funciona direto pelo navegador.
- O Streamlit declara as páginas como inglês (`lang="en"`), o que faz o Chrome "traduzir" o
  site, que já está em português. O `recifavela/idioma.py` corrige isso declarando `pt-BR` e
  desligando a tradução automática. Divulgue sempre o endereço principal acima: o link interno
  (`…streamlit.app/~/+/`) ainda pode ser traduzido por navegadores que traduzem inglês
  automaticamente, porque a decisão de traduzir acontece antes de o app carregar.

## Validação do protótipo

O protocolo completo está em [validacao/PROTOCOLO.md](validacao/PROTOCOLO.md). Resumo:

- 30 resíduos reais são fotografados e a classificação do sistema é comparada com a
  classificação correta definida antes do teste.
- **Meta: pelo menos 80% de acerto (24 de 30).**
- As orientações de preparo e descarte também são avaliadas para cada resíduo.

O teste pode ser feito pela página **Validação do protótipo** do site ou pela linha de comando:

```bash
python avaliar.py validacao/fotos --gabarito validacao/gabarito.csv
```

Sem gabarito, a categoria correta é deduzida do nome do arquivo ou da pasta
(`plastico_01.jpg`, `vidro/garrafa.jpg`…).

### Teste preliminar

Antes do teste com resíduos reais, o classificador foi conferido com 200 fotos do conjunto
público [TrashNet](https://huggingface.co/datasets/garythung/trashnet) (50 por material, papel e
papelão juntos). O resultado serve só como referência: as fotos do TrashNet têm fundo branco e
iluminação controlada, diferente do uso real na cooperativa.

| Configuração | Acerto |
|---|---|
| Versão inicial das descrições | 83,0% |
| Versão atual (descrições ampliadas + protótipo médio por material) | **91,5%** (183 de 200) |
| Versão atual, simulação do protocolo com 30 fotos não usadas nos ajustes (8/8/7/7) | **93,3%** (28 de 30) |

## Testes automatizados

As regras de reciclabilidade, as métricas da validação e a formatação são cobertas por testes:

```bash
pip install -r requirements-dev.txt
```

```bash
python -m pytest
```

## Estrutura do projeto

```
app.py                     # ponto de entrada (navegação, tema, barra lateral)
paginas/
  analisar.py              # envio da foto e resultado da análise
  validacao.py             # validação com os 30 resíduos de teste
  sobre.py                 # apresentação do projeto e da equipe
recifavela/
  classificador.py         # visão computacional (CLIP zero-shot)
  orientacoes.py           # reciclabilidade, perguntas, preparo e descarte por material
  avaliacao.py             # métricas da validação (acerto, matriz de confusão)
  ui.py                    # identidade visual: estilos e componentes
  projeto.py               # dados da equipe e do trabalho acadêmico
  config.py                # modelo de visão computacional usado
  imagem.py                # abertura e ajuste das fotos
  cache.py                 # cache do modelo no Streamlit
  idioma.py                # declara a página em português (evita tradução automática)
assets/                    # logotipo
apresentacao/              # slides (PowerPoint) e vídeo de demonstração (MP4)
video/                     # projeto Remotion que gera o vídeo de demonstração
tests/                     # testes automatizados (pytest)
avaliar.py                 # validação pela linha de comando
validacao/
  PROTOCOLO.md             # roteiro do teste com 30 resíduos
  gabarito_modelo.csv      # modelo de planilha com a classificação correta
```

## Como ajustar

- **Orientações e perguntas:** edite `recifavela/orientacoes.py`. Cada pergunta define a
  situação resultante (reciclável, com cuidados, não reciclável, descarte especial) e o texto da
  orientação. O local de entrega fica na constante `PONTO_DE_ENTREGA`.
- **Classificação:** o modelo não precisa de treinamento. Se algum objeto for confundido com
  frequência, acrescente descrições dele em `DESCRICOES` (`recifavela/classificador.py`), em
  inglês, e repita a validação.

## Limitações

- O sistema reconhece apenas quatro materiais; resíduos orgânicos, eletrônicos e outros serão
  classificados como o material mais parecido. As perguntas sobre as condições e a opção de
  corrigir o material ajudam a evitar erros de orientação.
- Embalagens mistas (longa vida, metalizadas) são tratadas pelas perguntas, não pela foto.
- A análise é uma sugestão automática; em caso de dúvida, a equipe da ReciFavela deve ser
  consultada.
