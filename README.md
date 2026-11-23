# esteira-peticao

Esteira de agentes do Claude Code que escreve a **petição inicial trabalhista** (reclamação trabalhista) a partir da pasta do cliente no Google Drive. O resultado sai como Google Doc, para um advogado revisar.

## Como usar

```
/peticao-inicial <link da pasta do cliente no Google Drive>
```

A pasta do cliente tem duas subpastas:

- `O que eu recebo`: sempre tem procuração, entrevista e CTPS. Outros documentos são opcionais.
- `O resultado`: onde a esteira grava tudo. Se não existir, a esteira cria.

O modelo de cálculo (xlsx zerado) e o modelo de petição em papel timbrado (docx com o logo e o rodapé do escritório) são os mesmos para todos os clientes e ficam no Drive do escritório. Os links vão em `config.local.md`. A esteira nunca altera os modelos; ela trabalha em cópias.

Se faltar informação, a esteira cria o Doc `PERGUNTAS <NOME DO CLIENTE>`. Você ou o advogado do caso responde o que puder, marca o que vai para o escritório e roda o mesmo comando de novo.

## O fluxo

| Etapa | Quem | Faz | Grava em `O resultado` |
|---|---|---|---|
| 1 | `peticao-verificador` | Confere os documentos, a procuração e a entrevista, identifica as partes, escolhe as teses e dá o veredito: Apto, Apto com ressalvas ou Bloqueado | Doc de perguntas, se precisar |
| 2 | `peticao-redator` | Preenche o modelo de cálculo e escreve a petição com a estrutura e os textos do banco de teses | `CÁLCULO <NOME> - rodada N` |
| 3 | `peticao-validador` | Confere fatos e contas contra os documentos, corrige erros objetivos e deixa notas para o advogado | `PETIÇÃO INICIAL <NOME> - rodada N` e `RELATÓRIO DE VALIDAÇÃO <NOME> - rodada N` |
| — | skill `peticao-inicial` | Orquestra as rodadas | `log.txt` com data e hora de Brasília, agente e evento |

Se o veredito for Bloqueado, a rodada para depois do Verificador.

### Modelo e esforço

| Agente | Modelo | Esforço | Por quê |
|---|---|---|---|
| `peticao-verificador` | Opus (`opus`, hoje Opus 5.5) | `high` | Escolhe as teses e dá o veredito. Uma tese esquecida aqui não é pega depois, porque o Validador só confere o que está na petição. |
| `peticao-redator` | Opus (`opus`, hoje Opus 5.5) | `medium` | Copia e adapta o texto do banco de teses. Os números vêm da planilha, e o Validador corrige o que sair errado. É o agente que mais gasta. |
| `peticao-validador` | Opus (`opus`, hoje Opus 5.5) | `high` | Confere cada fato e procura restos de outro caso. As contas ficam num script Python, não no raciocínio do modelo. |

O alias `opus` sempre aponta para o Opus mais recente. A skill (o orquestrador) roda no modelo e no esforço da sua sessão. Para mudar, edite `model` e `effort` no início de cada arquivo em `agents/`.

## Instalação

Pré-requisitos: Claude Code com o conector Google Drive ligado e `uv` instalado (o Redator usa `openpyxl` com `uv run --with openpyxl`).

```bash
git clone git@github.com:silveiralsv/esteira-peticao.git ~/www/esteira-peticao
cd ~/www/esteira-peticao
./install.sh
cp skills/peticao-inicial/config.example.md skills/peticao-inicial/config.local.md
# preencha em config.local.md os links do banco de teses, do modelo de cálculo e do modelo de papel timbrado
```

O `install.sh` cria links simbólicos em `~/.claude` (ou em `$CLAUDE_CONFIG_DIR`):

```
~/.claude/skills/peticao-inicial             -> skills/peticao-inicial
~/.claude/agents/peticao-verificador.md      -> agents/peticao-verificador.md
~/.claude/agents/peticao-redator.md          -> agents/peticao-redator.md
~/.claude/agents/peticao-validador.md        -> agents/peticao-validador.md
```

Ele não apaga nem substitui nada. Se um destino já existe e não é o link certo, ele avisa e deixa como está. Como são links, um `git pull` já atualiza a esteira.

## Estrutura

```
agents/                              os 3 agentes
skills/peticao-inicial/SKILL.md      o orquestrador
skills/peticao-inicial/referencia/
  teses.md                           quando cada tese entra, fatos mínimos, cálculo
  calculo.md                         reflexos, rescisórias, multas, honorários, valor da causa
  drive.md                           como ler e gravar no Drive, e o formato do log
  formatacao.md                      papéis do HTML da petição e o papel timbrado
skills/peticao-inicial/scripts/gerar_docx.py   gera o docx no papel timbrado a partir do HTML
skills/peticao-inicial/config.example.md
```

## Decisões do escritório

| | Decisão |
|---|---|
| Q1 | Um modelo de cálculo zerado, o mesmo para todos os clientes, é copiado e preenchido a cada petição. |
| Q2 | Tese sem fato do caso não entra e vira pergunta. Só bloqueia se for a tese principal. |
| Q3 | O banco de teses é uma pasta do Drive com petições do escritório. |
| Q4 | Quando a entrevista e a CTPS divergem, vale a CTPS. |
| Q5 | O Validador corrige erros objetivos. Fato sem fonte sai e vira nota para o advogado. |
| Q6 | Os agentes podem buscar dados fora da pasta (CNPJ, vara, CCT, salário mínimo), sempre citando a fonte. |
| Q7 | O escritório autorizou o envio dos dados dos clientes ao modelo. |
| Q8 | Danos morais: R$ 10.000,00 pelo inciso III do art. 223-G, salvo outro critério do advogado. |
| Q12 | A esteira é uma skill: `/peticao-inicial <link>`. |
| Q15 | O Doc de perguntas tem o campo `Responde: eu / escritório`. |

## Privacidade

Este repositório é público. Ele só tem as regras e os prompts.

- Nenhum documento, nome ou dado de cliente entra aqui. O `.gitignore` bloqueia xlsx, docx e pdf.
- Os links das pastas do escritório ficam em `config.local.md`, que fica fora do Git.
- Durante a rodada, os arquivos ficam num diretório temporário, que é apagado no fim.
- O `log.txt` registra nomes de arquivo e campos, não CPF, RG nem endereço.
