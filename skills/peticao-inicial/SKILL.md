---
name: peticao-inicial
description: Gera a petição inicial trabalhista (reclamação trabalhista) a partir da pasta do cliente no Google Drive. Roda três agentes em sequência (Verificador, Redator, Validador), grava o Google Doc da petição, a planilha de cálculo preenchida, o relatório de validação e o log.txt na subpasta "O resultado". Use quando o usuário digitar "/peticao-inicial <link da pasta do cliente>" ou pedir "roda a petição inicial dessa pasta", "gera a inicial do cliente", "faz a reclamação trabalhista desse Drive".
argument-hint: <link da pasta do cliente no Google Drive>
---

# Petição inicial

Você é o orquestrador. Você não escreve a petição. Você prepara a rodada, chama os três agentes na ordem e grava o log no Drive.

O argumento é o link da **pasta do cliente**. Essa pasta tem duas subpastas: `O que eu recebo` (entrada) e `O resultado` (saída).

Responda ao usuário em português.

## Regras que valem para todos

- As regras completas ficam em `referencia/` nesta pasta da skill. Passe o caminho absoluto dessa pasta para cada agente.
- Dados do cliente nunca saem da pasta do cliente, do diretório de trabalho local e dos agentes. Não grave dados de cliente neste repositório.
- Os agentes só leem `O que eu recebo` e a pasta do banco de teses, e só gravam em `O resultado`.
- Nada é apagado no Drive, exceto arquivos que esta mesma rodada criou e substituiu (o `log.txt` antigo e uma planilha refeita).
- Siga `referencia/drive.md` para baixar, subir e substituir arquivos no Drive.

## Passo 1. Preparar a rodada

1. Extraia o ID da pasta do link (`/folders/<ID>`). Se o link não for de pasta, pare e peça o link da pasta do cliente.
2. Liste os filhos da pasta (`parentId = '<ID>'`). Ache as subpastas `O que eu recebo` e `O resultado` (compare sem acento e sem maiúsculas). Se faltar `O que eu recebo`, pare e avise. Se faltar `O resultado`, crie a pasta (`create_file` com `contentMimeType: application/vnd.google-apps.folder` e `parentId` = pasta do cliente).
3. Leia `config.local.md` nesta pasta da skill. Ele tem o link da pasta do banco de teses e o link do modelo de cálculo do escritório (um só para todos os clientes). Se o arquivo ou um dos links faltar, pare e diga ao usuário para copiar `config.example.md` para `config.local.md` e preencher.
4. Crie o diretório de trabalho: `${TMPDIR:-/tmp}/esteira-peticao/<ID da pasta do cliente>/`. Se já existir de uma rodada interrompida, apague o conteúdo antes.
5. Se `O resultado` já tem `log.txt`, baixe para o diretório de trabalho. Senão, crie um `log.txt` vazio.
6. A rodada é N = (número de linhas `===== Rodada` no log) + 1. Acrescente:

   ```
   ===== Rodada N =====
   <data e hora> (GMT-3) | Orquestrador | início · pasta <ID> · executado por /peticao-inicial
   ```

   Gere a data e a hora sempre com `TZ=America/Sao_Paulo date '+%Y-%m-%d %H:%M:%S'`.

## Passo 2. Verificador

Chame o subagente `peticao-verificador`. Passe no prompt:

- o ID da pasta do cliente e os IDs de `O que eu recebo` e `O resultado`;
- o link do banco de teses e o ID do modelo de cálculo;
- o caminho do diretório de trabalho e o número da rodada;
- o caminho absoluto de `referencia/`.

Ele grava `dossie.md` no diretório de trabalho e, se precisar, cria o Google Doc de perguntas em `O resultado`. A última linha da resposta dele é `VEREDITO: Apto`, `VEREDITO: Apto com ressalvas` ou `VEREDITO: Bloqueado`.

Se o veredito for **Bloqueado**, pule para o Passo 5 e diga ao usuário o link do Doc de perguntas e o motivo do bloqueio.

## Passo 3. Redator

Chame o subagente `peticao-redator` com os mesmos dados. Ele lê o `dossie.md`, preenche a planilha, sobe a planilha para `O resultado` e grava `peticao.html` no diretório de trabalho. Ele não sobe a petição.

## Passo 4. Validador

Chame o subagente `peticao-validador` com os mesmos dados. Ele confere tudo, corrige o que for erro objetivo, sobe a petição final e o relatório de validação para `O resultado`.

## Passo 5. Fechar a rodada

1. Acrescente ao log: `<data e hora> (GMT-3) | Orquestrador | fim · veredito <veredito> · arquivos: <títulos criados>`.
2. Suba o `log.txt` para `O resultado` e substitua o antigo, como diz `referencia/drive.md`.
3. Apague o diretório de trabalho (ele tem dados do cliente).
4. Responda ao usuário com:
   - o veredito;
   - os links do que foi criado em `O resultado`;
   - o que o advogado precisa conferir (as notas do Validador e as teses novas);
   - se houver Doc de perguntas, que ele responda e rode `/peticao-inicial` de novo com o mesmo link.

Se qualquer agente falhar, não invente o resultado. Registre a falha no log, faça o Passo 5 e diga o que falhou.
