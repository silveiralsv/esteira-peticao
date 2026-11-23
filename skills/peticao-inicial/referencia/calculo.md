# Regras de cálculo

Estas regras saem da petição de referência e das 13 petições do banco de teses. O modelo de cálculo do escritório (um só para todos os clientes, link em `config.local.md`) é a fonte das contas de cada bloco (Q1). Quando a planilha e esta página divergirem, vale a planilha e o Validador escreve uma nota.

## Fontes dos parâmetros

| Parâmetro | Fonte | Regra |
|---|---|---|
| Admissão, saída, salário, cargo, CNPJ | CTPS | Q4: a CTPS vence a entrevista. A divergência vai para o log. |
| Jornada, escala, minutos extras, frequência | Entrevista | — |
| Adicional de horas extras, pisos e benefícios | CCT da categoria | Q6: busque na internet (sindicato ou Mediador do MTE) e cite o endereço. Se não achar, use 50% (art. 7º, XVI, CF) e crie uma pergunta. |
| Salário mínimo | Planilha | Use o valor da planilha. Se ele não for o do ano corrente, use o valor oficial e cite a fonte. |
| Data de referência | Dia da rodada | É a data do "SUBTOTAL em ..." e a base da prescrição. |

## Período de cálculo

- **Prescrição bienal:** se a saída foi há mais de 2 anos, não há ação. O veredito é Bloqueado.
- **Prescrição quinquenal:** o período começa no maior entre a admissão e (data de referência − 5 anos).
- **Fim do período:** a saída. Se a pessoa ainda trabalha, a data de referência.
- **Meses:** conte os meses do período. Fração de 15 dias ou mais vale 1 mês.

## Reflexos

Sobre a verba principal X, com 2 casas decimais em cada linha:

| Reflexo | Fórmula |
|---|---|
| Aviso prévio | X / 12 |
| Férias | X / 12 |
| 1/3 das férias | X / 36 |
| 13º salário | X / 12 |
| FGTS | 8% de X |
| Multa de 40% do FGTS | 40% do FGTS acima |
| DSR | 5% de X |

- Insalubridade e periculosidade não têm DSR.
- Sem aviso prévio indenizado (pessoa ainda empregada sem rescisão indireta, ou pedido de demissão mantido), tire a linha do aviso.
- O TOTAL do bloco é a soma exata das linhas escritas, já arredondadas.

## Verbas rescisórias

Use só nas teses que mudam a forma de saída (rescisão indireta, nulidade da justa causa, vínculo) ou quando a rescisão não foi paga.

- **Aviso prévio proporcional:** 30 dias + 3 dias por ano completo de serviço, até 90 dias. O tempo do aviso conta para completar o ano (OJ 82 da SDI-1). Ex.: 3 anos e 11 meses de contrato + 30 dias de aviso = 4 anos completos, então 42 dias.
- **Valor do aviso:** salário / 30 × dias.
- **Reflexos do aviso:** 13º = valor / 12 × (dias / 30); férias e 1/3 da mesma forma.
- **13º proporcional:** avos do ano corrente até a saída projetada pelo aviso. Mês com 15 dias ou mais vale 1 avo.
- **Férias proporcionais:** avos do período aquisitivo corrente até a saída projetada, mais 1/3. Férias vencidas não gozadas entram em dobro se o período concessivo acabou.
- **Saldo de salário:** dias trabalhados no mês da saída, se não foram pagos.
- **FGTS:** só peça "FGTS não depositado" com extrato ou afirmação clara do cliente. A multa de 40% incide sobre os depósitos do contrato inteiro.
- **Rótulos:** o texto de cada linha (datas, avos, dias) tem de bater com o valor. Ex.: "13º salário de 01/01/2026 a 30/09/2026 (9/12 avos)".

## Multas

- **Art. 467:** 50% do TOTAL das verbas rescisórias incontroversas.
- **Art. 477, § 8º:** uma remuneração.

## Valores fixos

| Pedido | Valor |
|---|---|
| Multa diária do PPP | R$ 500,00 |
| Danos morais (Q8) | R$ 10.000,00 |
| Danos materiais | R$ 10.000,00 |
| PLR sem dados | R$ 500,00 |

**Danos morais e o art. 223-G, § 1º:** o inciso tem de comportar o valor. Os tetos são inciso I (leve) 3 salários, II (média) 5, III (grave) 20 e IV (gravíssima) 50. O padrão é o inciso III. Se o texto citar o inciso I, o valor não pode passar de 3 salários.

## Honorários e valor da causa

- **Honorários:** 15% da soma de todos os pedidos com valor, incluindo danos, a multa do PPP e as multas. É o padrão das 13 petições do banco.
- **Valor da causa:** soma dos pedidos + honorários.
- O mesmo valor aparece em "SUBTOTAL em <dia> de <mês por extenso> de <ano>" e no item G das provas, com o valor por extenso.

## Planilha

- Baixe o modelo de cálculo e preencha a cópia local só as células de entrada dos blocos das teses escolhidas. Descubra essas células lendo a planilha com `openpyxl` (rótulos e fórmulas). Registre no log cada célula preenchida.
- Limpe as células de entrada que sobraram de outro caso (nome de paradigma, datas, avos e dias do cabeçalho). Se uma fórmula der `#REF!`, não use o bloco: calcule numa aba extra e registre no log.
- Teses sem bloco no modelo vão numa aba extra `Cálculos extras`, uma linha por item, com a fórmula visível.
- Para ler os totais calculados, suba a planilha (ela vira Google Sheet e calcula as fórmulas) e leia com `read_file_content`.
- Rode o Python com `uv run --with openpyxl python3 ...`. Não instale pacotes no sistema.
