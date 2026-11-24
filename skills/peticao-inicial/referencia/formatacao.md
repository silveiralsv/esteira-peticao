# Formatação da petição

A petição sai no papel timbrado do escritório: logo no cabeçalho, endereço e contatos no rodapé, Times New Roman, títulos numerados e os recuos da petição de referência. Quem garante isso é o modelo `Modelo de Petição - papel timbrado.docx` (link em `config.local.md`) e o script `scripts/gerar_docx.py`.

## Como funciona

1. O Redator escreve `peticao.html` só com as marcações abaixo. Nada de CSS, fonte ou cor.
2. O Validador corrige o `peticao.html` e, no fim, gera o docx:

   ```bash
   uv run --with python-docx --with pillow python3 <skill>/scripts/gerar_docx.py modelo.docx peticao.html peticao.docx
   ```

3. O Validador sobe `peticao.docx` com `contentMimeType` de docx, deixando converter. O Google Doc mantém cabeçalho, rodapé e formatação.

O modelo tem um parágrafo de exemplo por papel. Cada bloco do HTML copia a formatação do exemplo do seu papel. O script avisa se usar um papel que o modelo não tem.

## Papéis

| HTML | Papel | Uso |
|---|---|---|
| `<p class="enderecamento">` | endereçamento | `AO JUÍZO DA VARA DO TRABALHO DE ...`, em negrito |
| `<p class="preambulo">` | preâmbulo | qualificação da procuração, com o nome em `<b>` |
| `<h1>` | título | `R E C L A M A Ç Ã O&nbsp;&nbsp;&nbsp;T R A B A L H I S T A` (use `&nbsp;` entre as palavras). Sai com fundo azul-claro na linha inteira (sombreamento do parágrafo), não só atrás das letras |
| `<p class="em-face">` | em face de | reclamadas, com os nomes em `<b>` |
| `<p class="local">` | local da prestação | `<b>Local da prestação de serviços:</b> ...` |
| `<h2>` | seção | títulos das seções. O número (1., 2., 3. ...) é automático; não escreva o número |
| `<h3>` | subseção | uma por tese dentro de "DOS FUNDAMENTOS". O número é automático; não escreva o número |
| `<p>` | corpo | parágrafo comum, com recuo de primeira linha |
| `<blockquote><p>` | citação | lei, súmula, jurisprudência |
| `<li>` | lista | itens da síntese (com marcador) |
| `<p class="pedido">` | pedido | `<b>A-</b> Seja ...`. Pedido sem valor termina com o pontilhado e `DECLARAR;`, `EXPEDIR;`, `DEFERIR.` etc. Pedido de valor fixo (multa do PPP, danos morais) termina com o pontilhado e o valor. O pontilhado e a palavra ou o valor do fim vão em `<b>` |
| `<p class="item">` | linha de valor | `Horas extras ........ R$ 7.338,46;` O script escreve os pontos até perto do valor, e o valor fica alinhado à direita |
| `<p class="total">` | total | `TOTAL DAS HORAS EXTRAS ........ R$ 10.180,98;` em negrito |
| `<p class="subtotal">` | subtotal | `SUBTOTAL em <data> R$ <valor> (<extenso>)` |
| `<p class="nota">` | nota do Validador | `<b>[NOTA DO VALIDADOR]</b> ...`, sai com fundo amarelo |
| `<p class="fecho">` | fecho | "Termos em que, Pede deferimento." e "São Paulo, data e assinatura certificadas." |
| `<p class="assinatura">` | assinatura | duas linhas, em `<b>`: nome com OAB, e CPF |

Dentro de qualquer bloco valem `<b>`, `<i>`, `<u>` e `<br>`.

O endereço, o e-mail e os telefones do escritório já estão no rodapé. Não os repita na assinatura.

## Regras da advogada

- **Linhas de cálculo:** toda linha tem o pontilhado visível até o valor no fim da linha. Isso evita que o juiz se perca entre as linhas. O Google Docs não tem tabulação com pontilhado, então os pontos vão no texto: `scripts/pontilhado.py` dá a linha pronta (rótulo, pontos, tabulação, valor). O `gerar_docx.py` já usa esse script.
- **Negrito:** a linha do TOTAL de cada bloco vai inteira em negrito. No fim de cada pedido, o pontilhado e o valor (ou `DECLARAR;`, `EXPEDIR;`, `DEFERIR.`) vão em negrito, para o juiz achar o valor rápido.
- **Encerramento:** "Termos em que, Pede deferimento.", local e data, e a assinatura saem sempre na formatação do modelo (papéis `fecho` e `assinatura`).

Na rodada de ajuste, o Doc já existe: o pontilhado entra como texto sugerido logo antes da tabulação da linha (`insertText` com os pontos de `pontilhado.py`, precedidos de um espaço), e o negrito como `updateTextStyle` em modo sugestão.
