---
name: peticao-inicial
description: Gera a petição inicial trabalhista (reclamação trabalhista) a partir da pasta do cliente no Google Drive. Roda três agentes em sequência (Verificador, Redator, Validador), grava o Google Doc da petição, a planilha de cálculo preenchida, o relatório de validação e o log.txt na subpasta "O resultado". Com o link do Google Doc da petição, roda o modo revisão - aplica os comentários do advogado no mesmo Doc, em modo sugestão, sem recriar a petição. Use quando o usuário digitar "/peticao-inicial <link da pasta do cliente ou do Doc da petição>" ou pedir "roda a petição inicial dessa pasta", "gera a inicial do cliente", "faz a reclamação trabalhista desse Drive", "aplica os comentários da advogada na petição", "revisa a petição com os comentários". Com "--learn", roda o modo aprendizado - lê os comentários, as respostas e as edições do advogado, grava as regras gerais na esteira, faz commit e push na main e, na sequência, roda uma rodada de ajuste que aplica as regras novas na mesma petição, em modo sugestão. Use também quando o usuário pedir "aprende com os comentários da advogada", "vê o que a advogada colocou e sobe na main".
argument-hint: [--learn] <link da pasta do cliente, ou do Google Doc da petição>
---

# Petição inicial

Você é o orquestrador. Você não escreve a petição. Você prepara a rodada, chama os três agentes na ordem e grava o log no Drive.

O argumento é o link da **pasta do cliente**. Essa pasta tem duas subpastas: `O que eu recebo` (entrada) e `O resultado` (saída).

Se o link for de um Google Doc (`/document/d/<ID>`), não faça uma rodada nova. Siga a seção "Modo revisão" no fim deste arquivo.

Se o argumento tem `--learn` (antes ou depois do link), siga a seção "Modo aprendizado": ela aprende e, no fim, roda uma rodada de ajuste na mesma pasta. Sem a flag, a esteira só executa: as regras novas ficam como candidatas no log, e só o modo aprendizado grava regras e faz commit.

Responda ao usuário em português.

## Regras que valem para todos

- As regras completas ficam em `referencia/` nesta pasta da skill. Passe o caminho absoluto dessa pasta para cada agente.
- Dados do cliente nunca saem da pasta do cliente, do diretório de trabalho local e dos agentes. Não grave dados de cliente neste repositório.
- Os agentes só leem `O que eu recebo` e a pasta do banco de teses, e só gravam em `O resultado`.
- Nada é apagado no Drive, exceto arquivos que esta mesma rodada criou e substituiu (o `log.txt` e o `texto-da-esteira.txt` antigos e uma planilha refeita).
- Cada cliente tem **uma** petição (`PETIÇÃO INICIAL <NOME>`) e **uma** planilha (`CÁLCULO <NOME>`). A primeira rodada cria as duas. Depois disso a esteira nunca cria outra nem recria: o advogado comenta no Doc, e as rodadas seguintes mudam o mesmo Doc e o mesmo Sheet, em modo sugestão (`referencia/drive.md`, "Editar no lugar"). O link não muda e os comentários ficam.
- Siga `referencia/drive.md` para baixar, subir e substituir arquivos no Drive.

## Passo 1. Preparar a rodada

1. Extraia o ID da pasta do link (`/folders/<ID>`). Se o link não for de pasta, pare e peça o link da pasta do cliente. Se a pasta for a própria `O que eu recebo` ou `O resultado` (compare sem acento e sem maiúsculas), use a pasta-mãe dela como pasta do cliente e registre isso no log.
2. Liste os filhos da pasta (`parentId = '<ID>'`). Ache as subpastas `O que eu recebo` e `O resultado` (compare sem acento e sem maiúsculas).
   - **Falta `O que eu recebo` e a raiz tem arquivos** (pasta montada sem subpastas, na primeira rodada): crie `O que eu recebo` (`create_file` com `contentMimeType: application/vnd.google-apps.folder` e `parentId` = pasta do cliente). Mova para ela cada arquivo da raiz, sem as pastas (`update_file` com `parentId` = ID de `O que eu recebo`). Se o Drive recusar a mudança (a conta não é dona do arquivo), copie o arquivo para `O que eu recebo` com `copy_file` e o mesmo título; o original fica na raiz. Guarde a lista (arquivo, movido ou copiado) e registre no log depois do item 6. Não confira aqui se os documentos estão completos: isso é do Verificador.
   - **Falta `O que eu recebo` e a raiz não tem arquivos:** pare e avise.
   - **Falta `O resultado`:** crie a pasta (`create_file` com `contentMimeType: application/vnd.google-apps.folder` e `parentId` = pasta do cliente).
3. Leia `config.local.md` nesta pasta da skill. Ele tem o link da pasta do banco de teses, o link do modelo de cálculo e o link do modelo de petição em papel timbrado (os dois modelos são os mesmos para todos os clientes). Se o arquivo ou um dos links faltar, pare e diga ao usuário para copiar `config.example.md` para `config.local.md` e preencher.
4. Crie o diretório de trabalho: `${TMPDIR:-/tmp}/esteira-peticao/<ID da pasta do cliente>/`. Se já existir de uma rodada interrompida, apague o conteúdo antes.
5. Se `O resultado` já tem `log.txt`, baixe para o diretório de trabalho. Senão, crie um `log.txt` vazio.
6. A rodada é N = (número de linhas `===== Rodada` no log) + 1. Acrescente:

   ```
   ===== Rodada N =====
   <data e hora> (GMT-3) | Orquestrador | início · pasta <ID> · executado por /peticao-inicial
   ```

   Gere a data e a hora sempre com `TZ=America/Sao_Paulo date '+%Y-%m-%d %H:%M:%S'`.

7. Procure em `O resultado` a petição e a planilha: títulos que começam com `PETIÇÃO INICIAL` (Google Doc) e `CÁLCULO` (Google Sheet), fora da lixeira.
   - **Nenhuma petição:** é a **primeira rodada**. Siga os Passos 2, 3, 4 e 5.
   - **Uma petição:** é uma **rodada de ajuste**. Siga os Passos 2, 3A, 4 e 5. Ache também a planilha. Se faltar a planilha, pare e avise.
   - **Mais de uma petição ou de uma planilha:** pare e pergunte ao usuário qual vale. Não escolha sozinho.

   Na rodada de ajuste, confira que os conectores Google Docs e Google Sheets existem (carregue `mcp__claude_ai_Google_Docs__read_doc` e `mcp__claude_ai_Google_Sheets__get_values` com ToolSearch). Se faltar um deles, pare e diga ao usuário para ligar o conector Google Workspace. Nunca suba uma petição nova no lugar.

   Se o título da petição ou da planilha termina com ` - rodada <n>` (padrão antigo), renomeie com `update_file` para tirar o sufixo. O link não muda. Registre no log.

   Registre no log: `Orquestrador | primeira rodada` ou `Orquestrador | rodada de ajuste · petição <ID> · planilha <ID>`.

## Passo 2. Verificador

Chame o subagente `peticao-verificador`. Passe no prompt:

- o ID da pasta do cliente e os IDs de `O que eu recebo` e `O resultado`;
- o link do banco de teses, o ID do modelo de cálculo e o ID do modelo de papel timbrado;
- o caminho absoluto da pasta `scripts/` desta skill;
- o caminho do diretório de trabalho e o número da rodada;
- o caminho absoluto de `referencia/`;
- na rodada de ajuste, os IDs da petição e da planilha.

Ele grava `dossie.md` no diretório de trabalho e, se precisar, cria o Google Doc de perguntas em `O resultado`. Na rodada de ajuste, grava também `mudancas.md`. A última linha da resposta dele é `VEREDITO: Apto`, `VEREDITO: Apto com ressalvas` ou `VEREDITO: Bloqueado`.

Se o veredito for **Bloqueado**, pule para o Passo 5 e diga ao usuário o link do Doc de perguntas e o motivo do bloqueio.

## Passo 3. Redator

Só na primeira rodada. Chame o subagente `peticao-redator` com os mesmos dados. Ele lê o `dossie.md`, preenche a planilha, sobe a planilha para `O resultado` e grava `peticao.html` no diretório de trabalho. Ele não sobe a petição.

## Passo 3A. Revisor (rodada de ajuste)

No lugar do Redator. Chame o subagente `peticao-revisor` com os mesmos dados, os IDs da petição e da planilha, o número da rodada e o caminho absoluto da pasta `scripts/`. Ele aplica no mesmo Doc e no mesmo Sheet, em modo sugestão, os itens de `mudancas.md` e os comentários abertos do advogado.

## Passo 4. Validador

Chame o subagente `peticao-validador` com os mesmos dados (na rodada de ajuste, com os IDs da petição e da planilha). Ele confere tudo, corrige o que for erro objetivo e sobe o relatório de validação para `O resultado`. Na primeira rodada, ele também sobe a petição. Na rodada de ajuste, ele confere e corrige o Doc que já existe, em modo sugestão.

## Passo 5. Fechar a rodada

1. Se a petição existe, grave o texto que a esteira deixou: leia a petição com `read_doc`, salve no diretório de trabalho e rode `python3 <scripts>/texto_sugerido.py <arquivo> | cut -d' ' -f2- > <diretório>/texto-da-esteira.txt`. Suba para `O resultado` e substitua o antigo, como o `log.txt`. O modo aprendizado compara a petição com esse texto para achar o que o advogado editou depois. Sem o conector Google Docs, pule e registre no log.
2. Acrescente ao log: `<data e hora> (GMT-3) | Orquestrador | fim · veredito <veredito> · arquivos: <títulos criados>`.
3. Suba o `log.txt` para `O resultado` e substitua o antigo, como diz `referencia/drive.md`.
4. Apague o diretório de trabalho (ele tem dados do cliente).
5. Responda ao usuário com:
   - o veredito;
   - os links do que foi criado em `O resultado`. Na rodada de ajuste, o link da petição e da planilha, que são os mesmos, e que as mudanças estão como sugestões para o advogado aceitar ou rejeitar;
   - na rodada de ajuste, a tabela do Revisor e as regras candidatas, que entram na esteira com `/peticao-inicial --learn <link>`;
   - o que o advogado precisa conferir (as notas do Validador e as teses novas);
   - se houver pendências (falta documento, e a petição saiu com o que havia): que cada uma tem um comentário `[ESTEIRA] Pendência` no Doc, e a "Mensagem para o escritório" do relatório, pronta para copiar;
   - se houver Doc de perguntas, que ele responda e rode `/peticao-inicial` de novo com o mesmo link.

Se qualquer agente falhar, não invente o resultado. Registre a falha no log, faça o Passo 5 e diga o que falhou.

## Modo revisão

O advogado revisou a petição no Google Doc e deixou comentários. O modo revisão aplica os comentários no mesmo Doc, em modo sugestão. Ele nunca apaga, recria ou manda para a lixeira a petição ou a planilha: os comentários e o link ficam.

1. Extraia o ID do Doc (`/document/d/<ID>`). Leia os metadados (`get_file_metadata`). O título tem que começar com `PETIÇÃO INICIAL`; senão, pare e peça o link da petição. O `parentId` é `O resultado`, e a pasta-mãe dela é a pasta do cliente.
2. Confira que o conector Google Docs existe (carregue `mcp__claude_ai_Google_Docs__read_doc` com ToolSearch). Se não existir, pare e diga ao usuário para ligar o conector Google Workspace. Não use o conector Drive para substituir o Doc.
3. Ache em `O resultado` o Sheet cujo título começa com `CÁLCULO`. Se houver mais de um, pergunte ao usuário qual vale.
4. Crie o diretório de trabalho e baixe o `log.txt`, como no Passo 1. A revisão é R = (número de linhas `===== Revisão` no log) + 1. Acrescente:

   ```
   ===== Revisão R =====
   <data e hora> (GMT-3) | Orquestrador | início · Doc <ID> · executado por /peticao-inicial
   ```

5. Chame o subagente `peticao-revisor`. Passe: o ID do Doc, o ID do Sheet, os IDs das pastas, o diretório de trabalho, o número da revisão e os caminhos absolutos de `referencia/` e `scripts/`. Não há `mudancas.md`: ele trata só os comentários.
6. Feche como no Passo 5: texto da esteira e log no Drive, diretório de trabalho apagado.
7. Responda ao usuário com:
   - a tabela do Revisor (comentário, tipo, o que foi feito);
   - o link do Doc, que é o mesmo, e que as mudanças estão como sugestões para o advogado aceitar ou rejeitar;
   - as regras candidatas: entram na esteira com `/peticao-inicial --learn <link>`.

## Modo aprendizado (`--learn`)

O advogado já revisou a petição: comentou, respondeu as perguntas, editou o texto. O modo aprendizado transforma o que ele fez em regras gerais da esteira e grava no repositório, com commit e push na `main`. A flag é o pedido do usuário para esse commit e esse push.

Os itens 1 a 9 não mudam a petição, a planilha nem outro arquivo do Drive, exceto o `log.txt`. Depois de aprender, o item 10 roda uma rodada de ajuste na mesma pasta, que aplica as regras novas na petição. O usuário não precisa rodar `/peticao-inicial <link>` de novo.

1. **Pasta do cliente.** O link pode ser da pasta do cliente, de uma subpasta dela ou do Doc da petição. Ache a pasta do cliente e `O resultado` como no Passo 1 (item 1) e no Modo revisão (item 1). Liste `O resultado`: petição, planilha, relatórios, Docs de perguntas, `log.txt` e `texto-da-esteira.txt`.
2. **Repositório.** É `git -C <pasta desta skill> rev-parse --show-toplevel`. O branch tem que ser `main`, sem mudança fora de commit (`git status --porcelain`). Senão, pare e diga ao usuário o que está diferente. Rode `git pull --ff-only`.
3. **Log.** Crie o diretório de trabalho e baixe o `log.txt`, como no Passo 1. A vez é A = (número de linhas `===== Aprendizado` no log) + 1. Acrescente `===== Aprendizado A =====` e `<data e hora> (GMT-3) | Aprendizado | início · executado por /peticao-inicial --learn`.
4. **Juntar o que o advogado fez.** Tudo o que não é da esteira:
   - os comentários da petição, abertos e resolvidos, com todas as respostas (`read_file_content` com `includeComments: true`). Leia também as respostas do advogado dentro de comentários `[ESTEIRA]`. Pule o comentário que já está no log numa linha `Aprendizado | comentário <id>`, exceto as respostas mais novas que essa linha;
   - os comentários da planilha, dos relatórios e dos Docs de perguntas, e as respostas das perguntas;
   - as edições diretas e as sugestões do advogado na petição. Leia a petição com `read_doc`, salve no diretório de trabalho e rode `python3 <scripts>/texto_sugerido.py <arquivo> | cut -d' ' -f2- > texto-atual.txt`. Compare com o `texto-da-esteira.txt` (`diff -u`). Cada trecho diferente foi editado depois da última rodada. `list_file_revisions` diz quem editou e quando. Se o texto da esteira no trecho é o "depois" de uma sugestão da esteira registrada no log, e o texto atual é o "antes", o advogado rejeitou a sugestão;
   - sem `texto-da-esteira.txt` (petição de antes desta regra): compare a petição com o log e com o relatório da última rodada, e diga ao usuário que uma edição direta pode ter ficado de fora;
   - as regras candidatas do Revisor no log (`Revisor | regra candidata`).
5. **Classificar.** Cada item tem um tipo:

   | Tipo | Sinal | O que fazer |
   |---|---|---|
   | Regra geral | "sempre", "nunca", "em todas as petições"; o advogado trocou o texto da esteira por um texto modelo dele; a correção mostra que uma regra de `referencia/` ou um passo de um agente levou ao erro | Gravar (passo 6) |
   | Caso do cliente | fato, data, valor ou nome que só vale para este cliente, e a esteira seguiu as regras | Nada |
   | Confirmação | "está correto", sugestão aceita | Nada |
   | Dúvida | não dá para saber se vale para todos; sugestão da esteira rejeitada sem comentário; o item contradiz outra regra que o advogado já deu | Não gravar. Listar para o usuário perguntar ao advogado |

6. **Gravar.** Leia antes `referencia/` inteira e os arquivos de `agents/` que o item toca.
   - Onde: tese em `teses.md`; conta, percentual ou período em `calculo.md`; forma do texto em `formatacao.md`; Drive e log em `drive.md`; o que um agente faz ou confere em `agents/<agente>.md`; decisão do escritório na tabela do `README.md`.
   - Texto modelo do advogado: copie palavra por palavra como texto fixo em `teses.md`, com `<campo>` no lugar de cada dado do cliente. Ponha o texto fixo na lista do item 5 de `peticao-validador.md`.
   - Escreva em termos gerais. Antes de gravar, procure a regra: se já existe, não repita. Se contradiz uma regra que existe, troque a antiga e diga isso na resposta.
   - Mude só as linhas necessárias.
7. **Dados do cliente.** O repositório é público. Rode `git diff` e confira que nenhuma linha nova tem nome, CPF, RG, endereço, cidade, empresa, data, valor ou número de processo do cliente. Jurisprudência citada no texto modelo do advogado não é dado do cliente. Tire o que tiver. A mensagem de commit também não leva dado do cliente.
8. **Commit e push.** Se nada mudou, não faça commit. Senão, `git add` só nos arquivos mudados, commit `feat: <o que a esteira aprendeu>` com as linhas de atribuição da sessão, e `git push origin main`. Se o push falhar, não force: diga ao usuário.
9. **Fechar.** Acrescente ao log uma linha por item, `Aprendizado | comentário <id> · <tipo> · <regra gravada ou "nada">` (ou `edição · <seção>`, `pergunta <n>`), e `Aprendizado | fim · commit <hash> · <n> regras · <n> dúvidas`. Suba o `log.txt` e substitua o antigo. Apague o diretório de trabalho.
10. **Rodada de ajuste.** Na sequência, rode uma rodada de ajuste na mesma pasta do cliente: Passos 1, 2, 3A, 4 e 5, como sem a flag. Ela roda mesmo sem commit, para aplicar os comentários abertos e as respostas novas.
    - Passe ao Verificador, ao Revisor e ao Validador o hash do commit do item 8 (ou `nenhum`), e diga que esta rodada aplica e confere as regras desse commit.
    - Peça a cada agente que leia antes o próprio arquivo em `agents/` no repositório. O commit pode ter mudado a definição depois que a sessão começou.
    - O Verificador põe em `mudancas.md` um item para cada regra nova do commit que se aplica a esta petição (Passo 8 do `peticao-verificador.md`).
    - As edições diretas do advogado ficam. Se uma contradiz uma regra nova, vale a edição, e o item entra nas dúvidas.
    - Se a pasta não tem petição em `O resultado`, não há o que ajustar: pule e diga isso.
11. **Responder.** Diga ao usuário:
    - uma tabela: origem (comentário, resposta, edição ou pergunta, com autor e primeiras palavras), tipo, o que a esteira aprendeu e o arquivo;
    - o commit, e que as regras já valem para as próximas rodadas, nesta máquina e nas outras depois do `git pull`;
    - as dúvidas para o advogado;
    - o resultado da rodada de ajuste, como no Passo 5: cada regra nova aplicada, já cumprida ou que não se aplica, e as sugestões no Doc.
