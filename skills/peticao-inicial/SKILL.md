---
name: peticao-inicial
description: Gera a petição inicial trabalhista (reclamação trabalhista) a partir da pasta do cliente no Google Drive. Roda três agentes em sequência (Verificador, Redator, Validador), grava o Google Doc da petição, a planilha de cálculo preenchida, o relatório de validação e o log.txt na subpasta "O resultado". Com o link do Google Doc da petição, roda o modo revisão - aplica os comentários do advogado no mesmo Doc, em modo sugestão, sem recriar a petição. Use quando o usuário digitar "/peticao-inicial <link da pasta do cliente ou do Doc da petição>" ou pedir "roda a petição inicial dessa pasta", "gera a inicial do cliente", "faz a reclamação trabalhista desse Drive", "aplica os comentários da advogada na petição", "revisa a petição com os comentários".
argument-hint: <link da pasta do cliente, ou do Google Doc da petição para o modo revisão>
---

# Petição inicial

Você é o orquestrador. Você não escreve a petição. Você prepara a rodada, chama os três agentes na ordem e grava o log no Drive.

O argumento é o link da **pasta do cliente**. Essa pasta tem duas subpastas: `O que eu recebo` (entrada) e `O resultado` (saída).

Se o link for de um Google Doc (`/document/d/<ID>`), não faça uma rodada nova. Siga a seção "Modo revisão" no fim deste arquivo.

Responda ao usuário em português.

## Regras que valem para todos

- As regras completas ficam em `referencia/` nesta pasta da skill. Passe o caminho absoluto dessa pasta para cada agente.
- Dados do cliente nunca saem da pasta do cliente, do diretório de trabalho local e dos agentes. Não grave dados de cliente neste repositório.
- Os agentes só leem `O que eu recebo` e a pasta do banco de teses, e só gravam em `O resultado`.
- Nada é apagado no Drive, exceto arquivos que esta mesma rodada criou e substituiu (o `log.txt` antigo e uma planilha refeita).
- Cada cliente tem **uma** petição (`PETIÇÃO INICIAL <NOME>`) e **uma** planilha (`CÁLCULO <NOME>`). A primeira rodada cria as duas. Depois disso a esteira nunca cria outra nem recria: o advogado comenta no Doc, e as rodadas seguintes mudam o mesmo Doc e o mesmo Sheet, em modo sugestão (`referencia/drive.md`, "Editar no lugar"). O link não muda e os comentários ficam.
- Siga `referencia/drive.md` para baixar, subir e substituir arquivos no Drive.

## Passo 1. Preparar a rodada

1. Extraia o ID da pasta do link (`/folders/<ID>`). Se o link não for de pasta, pare e peça o link da pasta do cliente. Se a pasta for a própria `O que eu recebo` ou `O resultado` (compare sem acento e sem maiúsculas), use a pasta-mãe dela como pasta do cliente e registre isso no log.
2. Liste os filhos da pasta (`parentId = '<ID>'`). Ache as subpastas `O que eu recebo` e `O resultado` (compare sem acento e sem maiúsculas). Se faltar `O que eu recebo`, pare e avise. Se faltar `O resultado`, crie a pasta (`create_file` com `contentMimeType: application/vnd.google-apps.folder` e `parentId` = pasta do cliente).
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

1. Acrescente ao log: `<data e hora> (GMT-3) | Orquestrador | fim · veredito <veredito> · arquivos: <títulos criados>`.
2. Suba o `log.txt` para `O resultado` e substitua o antigo, como diz `referencia/drive.md`.
3. Apague o diretório de trabalho (ele tem dados do cliente).
4. Responda ao usuário com:
   - o veredito;
   - os links do que foi criado em `O resultado`. Na rodada de ajuste, o link da petição e da planilha, que são os mesmos, e que as mudanças estão como sugestões para o advogado aceitar ou rejeitar;
   - na rodada de ajuste, a tabela do Revisor e as regras novas da esteira (confira o `git diff` como no Modo revisão, passo 7);
   - o que o advogado precisa conferir (as notas do Validador e as teses novas);
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
6. Feche como no Passo 5: log no Drive, diretório de trabalho apagado.
7. Se o Revisor gravou regras em `referencia/`, rode `git -C <repositório> diff` e confira que nenhuma linha nova tem nome, CPF, cidade, empresa, data ou valor do cliente. Tire o que tiver. Não faça commit.
8. Responda ao usuário com:
   - a tabela do Revisor (comentário, tipo, o que foi feito);
   - o link do Doc, que é o mesmo, e que as mudanças estão como sugestões para o advogado aceitar ou rejeitar;
   - as regras novas da esteira: já valem nesta máquina para as próximas petições; o commit guarda e leva para as outras.
