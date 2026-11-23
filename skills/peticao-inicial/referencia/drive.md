# Google Drive e log

Todas as operações usam as ferramentas do conector Google Drive (`mcp__claude_ai_Google_Drive__*`). Se estiverem adiadas, carregue com ToolSearch antes de usar.

## Ler

- Texto de PDF, docx, xlsx, Google Doc ou Google Sheet: `read_file_content`.
- Listar uma pasta: `search_files` com `parentId = '<ID>'`.

## Baixar um arquivo binário (xlsx)

1. Chame `download_file_content` com o ID.
2. O resultado é JSON com o conteúdo em base64. Quando ele é grande, a ferramenta salva o resultado num arquivo e mostra o caminho. Use esse arquivo.
3. Decodifique com Python, sem copiar o base64 para o comando:

   ```bash
   python3 -c "import json,base64,sys;d=json.load(open(sys.argv[1]));open(sys.argv[2],'wb').write(base64.b64decode(d.get('content') or d.get('base64Content') or d['data']))" <arquivo do resultado> <destino>.xlsx
   ```

   Se a chave for outra, abra o JSON e veja o nome do campo.

## Subir um arquivo

Use `create_file` com `parentId` = ID de `O resultado` e uma referência ao arquivo local no lugar do base64:

```
base64Content: "sha256:<hash>:<caminho absoluto>"
```

Calcule o hash com `shasum -a 256 <arquivo> | cut -d' ' -f1`.

| O que | contentMimeType | Conversão |
|---|---|---|
| Petição, relatório, Doc de perguntas | `text/html` | deixe converter (vira Google Doc) |
| Planilha | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | deixe converter (vira Google Sheet, que calcula as fórmulas) |
| `log.txt` | `text/plain` | `disableConversionToGoogleType: true` |

O conector não edita o conteúdo de um arquivo que já existe. Para mudar um arquivo, crie a versão nova e só então mande a antiga para a lixeira (`trash_file`). Só faça isso com arquivos que o fluxo criou.

## Títulos

- `PERGUNTAS <NOME DO CLIENTE> - rodada N`
- `CÁLCULO <NOME DO CLIENTE> - rodada N`
- `PETIÇÃO INICIAL <NOME DO CLIENTE> - rodada N`
- `RELATÓRIO DE VALIDAÇÃO <NOME DO CLIENTE> - rodada N`
- `log.txt`

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
