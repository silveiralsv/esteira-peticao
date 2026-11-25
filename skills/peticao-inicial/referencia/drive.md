# Google Drive e log

Todas as operações usam as ferramentas do conector Google Drive (`mcp__claude_ai_Google_Drive__*`). Se estiverem adiadas, carregue com ToolSearch antes de usar.

**Arquivos locais:** grave tudo (downloads, textos extraídos, scripts, HTML) só no diretório de trabalho da rodada. Nunca use outra pasta. A única exceção é a cópia temporária para subir um arquivo (ver "Subir um arquivo"). O orquestrador apaga o diretório de trabalho no fim, e ele tem dados de clientes.

## Ler

- Texto de PDF, docx, xlsx, Google Doc ou Google Sheet: `read_file_content`.
- Listar uma pasta: `search_files` com `parentId = '<ID>'`.

## Baixar um arquivo binário (xlsx)

1. Chame `download_file_content` com o ID.
2. A ferramenta salva o arquivo em disco e mostra o caminho. Copie esse arquivo para o diretório de trabalho.
3. Se em vez disso vier um JSON com base64, decodifique com Python a partir do arquivo do resultado, sem copiar o base64 para o comando.

## Ler os valores calculados de um Google Sheet

`read_file_content` mostra só as primeiras linhas de uma planilha, sem os totais. Para ler os valores:

1. Chame `download_file_content` com o ID do Sheet e `exportMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`.
2. Leia o xlsx baixado com `uv run --with openpyxl python3`, abrindo com `load_workbook(..., data_only=True)`.

## Subir um arquivo

Use `create_file` com `parentId` = ID de `O resultado` e uma referência ao arquivo local no lugar do base64:

```
base64Content: "sha256:<hash>:<caminho absoluto>"
```

Calcule o hash com `shasum -a 256 <arquivo> | cut -d' ' -f1`.

O conector pode recusar a referência a um arquivo em `$TMPDIR` ("Nothing was uploaded"). Nesse caso:

- HTML e texto (relatório, perguntas, `log.txt`): mande o conteúdo em `textContent`.
- Binário (planilha, docx): copie o arquivo para `esteira-<ID da pasta do cliente>/` dentro do scratchpad da sessão (o caminho está no prompt de sistema, em "Scratchpad directory"), calcule o hash da cópia e suba com a referência dela. Apague a cópia logo depois do upload. Registre no log que usou o scratchpad.

| O que | contentMimeType | Conversão |
|---|---|---|
| Petição | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (docx gerado por `scripts/gerar_docx.py`) | deixe converter (vira Google Doc com o papel timbrado) |
| Relatório, Doc de perguntas | `text/html` | deixe converter (vira Google Doc) |
| Planilha | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | deixe converter (vira Google Sheet, que calcula as fórmulas) |
| `log.txt` | `text/plain` | `disableConversionToGoogleType: true` |

O conector Google Drive não edita o conteúdo de um arquivo que já existe. Dentro de uma rodada, para mudar um arquivo que a própria rodada criou, crie a versão nova e só então mande a antiga para a lixeira (`trash_file`).

Depois que a rodada termina, a petição e a planilha podem ter comentários do advogado. Nunca recrie nem mande para a lixeira esses arquivos: os comentários se perdem. Mude no lugar, como diz "Editar no lugar".

## Editar no lugar (Google Docs e Google Sheets)

Os conectores Google Docs (`mcp__claude_ai_Google_Docs__*`) e Google Sheets (`mcp__claude_ai_Google_Sheets__*`) mudam o arquivo que já existe. O link fica o mesmo. Se estiverem adiados, carregue com ToolSearch. Se não existirem, pare e diga ao usuário para ligar o conector Google Workspace.

**Ler comentários.** `read_file_content` com `includeComments: true` dá o texto, as threads (`commentThreads`, com id, autor, texto e status) e o trecho comentado entre `<comment_start id=…>` e `<comment_end id=…>`. Esse texto não serve para índices.

**Ler índices.** `read_doc` dá cada trecho com `startIndex` e `endIndex` e o `revisionId`. A resposta é grande; se for salva em arquivo, use o script `docs_index.py` (`outline` e `find`) da skill `google-workspace` em vez de ler o JSON inteiro.

**Mudar o texto em modo sugestão.** `update_doc` com:

```json
"writeControl": {"writeMode": "SUGGEST", "requiredRevisionId": "<revisionId do último read_doc>"}
```

- Cada mudança fica como sugestão que o advogado aceita ou rejeita. É o registro do que a esteira fez.
- Para trocar um trecho que aparece uma vez: `replaceAllText` com o texto exato. Para os outros casos: `deleteContentRange` e `insertText` nos índices do `read_doc`, do fim do documento para o começo.
- Mude só as palavras que mudam. Apagar o trecho inteiro em que um comentário está ancorado tira o comentário do texto.
- Se o Doc mudou depois da leitura, o conector recusa o lote inteiro. Leia de novo e refaça o lote. Nunca tire o `requiredRevisionId`.
- Texto sugerido e texto com exclusão sugerida ocupam índices até alguém aceitar ou rejeitar. Não escreva dentro deles.
- **Sugestão rejeitada é decisão do advogado.** O log guarda cada sugestão das rodadas anteriores, com o antes e o depois. Se o Doc ainda tem o texto de antes, o advogado rejeitou: não sugira de novo, mesmo que uma regra de `referencia/` mande a troca. Registre no log `rejeitada pelo advogado na rodada N` e cite no relatório.

**Comentar.** `update_doc` com:

```json
{"insertComment": {"content": "[ESTEIRA] ...", "range": {"startIndex": 120, "endIndex": 180}}}
```

O comentário fica ancorado no trecho e aparece com o nome da conta do usuário. Por isso todo comentário da esteira começa com `[ESTEIRA]`. O conector não responde dentro de uma thread que já existe, nem resolve ou apaga comentários.

**Aceitar as sugestões.** O conector não aceita nem rejeita sugestão. Só quando o usuário pedir: no Google Docs, Ferramentas > Rever edições sugeridas > Aceitar tudo (pelo Chrome, se o usuário quiser). Antes, confira que todas as sugestões são da esteira e não do advogado. Os comentários ancorados num trecho apagado ficam no histórico como "conteúdo original eliminado".

**Planilha.** `update_values` muda células do Sheet no lugar; as fórmulas recalculam. Leia o resultado com `get_values`. O Sheets não tem modo sugestão: registre no log cada célula mudada, com o antes e o depois. O histórico de versões do Sheet também guarda a mudança.

## Títulos

- `PERGUNTAS <NOME DO CLIENTE> - rodada N`
- `CÁLCULO <NOME DO CLIENTE>`: um por cliente, criado na primeira rodada e depois mudado no lugar
- `PETIÇÃO INICIAL <NOME DO CLIENTE>`: um por cliente, criado na primeira rodada e depois mudado no lugar
- `RELATÓRIO DE VALIDAÇÃO <NOME DO CLIENTE> - rodada N`
- `log.txt`

Petições e planilhas antigas podem ter ` - rodada 1` no fim do título. O orquestrador tira o sufixo na rodada seguinte.

`<NOME DO CLIENTE>` é o nome da procuração, em maiúsculas.

## log.txt

Um arquivo por cliente, em `O resultado`. Só se acrescentam linhas. Ninguém apaga nem reescreve uma linha antiga.

Formato de cada linha:

```
AAAA-MM-DD HH:MM:SS (GMT-3) | <Agente> | <evento>
```

Gere a hora com `TZ=America/Sao_Paulo date '+%Y-%m-%d %H:%M:%S'`. Durante a rodada, cada agente acrescenta linhas ao `log.txt` do diretório de trabalho:

```bash
echo "$(TZ=America/Sao_Paulo date '+%Y-%m-%d %H:%M:%S') (GMT-3) | Verificador | <evento>" >> "<diretório>/log.txt"
```

O que entra no log:

- início e fim de cada agente;
- cada documento lido (nome do arquivo);
- cada divergência entre documentos e a regra aplicada (ex.: `admissão: entrevista 10/03/2021, CTPS 01/02/2021 → vale CTPS (Q4)`);
- o veredito e o motivo;
- cada pergunta criada ou respondida;
- cada fonte externa consultada, com o endereço;
- cada parâmetro preenchido na planilha (célula e valor);
- cada correção do Validador, com o antes e o depois;
- arquivos criados ou substituídos no Drive (título e ID).

O log não leva CPF, RG nem endereço do cliente. Use o nome do arquivo e o campo, não o dado pessoal.

No fim da rodada, o orquestrador sobe o `log.txt` novo e manda o antigo para a lixeira.
