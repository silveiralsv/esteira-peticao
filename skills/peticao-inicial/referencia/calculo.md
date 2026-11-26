# Regras de cálculo

Estas regras saem da petição de referência e das petições do banco de teses. O modelo de cálculo do escritório (um só para todos os clientes, link em `config.local.md`) é a fonte das contas de cada bloco (Q1). Quando a planilha e esta página divergirem, vale a planilha e o Validador escreve uma nota.

## Fontes dos parâmetros

| Parâmetro | Fonte | Regra |
|---|---|---|
| Admissão, saída, salário, cargo, CNPJ | CTPS | Q4: a CTPS vence a entrevista. A divergência vai para o log. |
| Local da prestação de serviços | Entrevista | Sempre o da entrevista, mesmo quando é diferente do endereço do estabelecimento na CTPS. Aqui Q4 não vale. O endereço da reclamada (em face de) continua o da CTPS. |
| Jornada, escala, minutos extras, frequência | Entrevista | Faixa ("15 a 20 minutos"): o maior valor. Data só com o mês: use o mês, sem pergunta. |
| Adicional de horas extras | Função | Enfermagem (auxiliar, técnico ou enfermeiro): 90%. Outras funções: 50%. Não precisa de CCT nem de pergunta. |
| Adicional noturno | Planilha | 20%, fixo no modelo de cálculo. |
| Pisos e benefícios | CCT da categoria | Q6: busque na internet (sindicato ou Mediador do MTE) e cite o endereço. Se não achar, crie uma pergunta (exceto a diferença salarial, na linha abaixo). |
| Diferença salarial sem valor na entrevista (desvio de função e parecidas) | CCT da categoria ou lei | Piso da função exercida − salário, sem pergunta. Se a CCT não tem piso próprio da função, use o salário base da categoria da função exercida (regra da advogada). Sem CCT, use o piso legal da profissão. O pedido nunca sai A APURAR por falta desse valor. |
| Frequência "com frequência" sem número | Regra do escritório | Pelo menos 3 ocorrências, nunca uma só. Exceção expressa à regra 4 de "Horas extras: quanto contar" e a "nunca invente frequência" (`teses.md`). Número dado pela entrevista ou pelo advogado vence o padrão. |
| Salário mínimo | Planilha | Use o valor da planilha. Se ele não for o do ano corrente, use o valor oficial e cite a fonte. |
| Data de referência | Dia da rodada | É a data do "SUBTOTAL em ..." e a base da prescrição bienal. |

## Período de cálculo

- **Prescrição bienal:** se a saída foi há mais de 2 anos, não há ação. O veredito é Bloqueado.
- **Últimos 60 meses (regra do escritório):** a conta usa no máximo 60 meses, os últimos do contrato, terminando no fim do período (abaixo). Contrato com mais de 5 anos: os 60 meses que terminam na saída. Contrato menor: o contrato inteiro. Nunca mais de 60 meses, mesmo com muito mais tempo de registro. O marco não se conta da data de referência (data da rodada − 5 anos).
- **Fim do período:** a saída. Se a pessoa ainda trabalha, a data de referência.
- **Meses:** conte os meses do período. Fração de 15 dias ou mais vale 1 mês.
- **Meses trabalhados:** nas verbas que dependem de trabalho efetivo (horas extras, noturno, feriados, plantões), conte os meses de férias como meses trabalhados (o escritório confirmou esse cálculo). Tire só os meses de afastamento.

## Horas extras: quanto contar

Conte só o tempo extra que a entrevista confirma. Nunca presuma, estime nem invente quantidade.

1. **Minutos todo dia:** "excedia 15 minutos por dia" = 15 minutos em cada dia trabalhado, pela escala informada (6x1, 5x2, 12x36 etc.). Some todos os minutos que a entrevista dá para o mesmo dia ou plantão: chegada antes do horário, saída depois do horário, troca de uniforme ou passagem de plantão depois do ponto.
2. **Só alguns dias:** "2 vezes por semana", "4 dias por mês" = só nessa frequência.
3. **Extra a mais em alguns dias:** "além disso, 2 horas a mais em dois dias por mês" = some essas horas e divida pelos dias trabalhados do mês. O resultado entra na média diária, junto com os minutos de todo dia.
4. **Relato genérico:** extra sem duração ou sem frequência (ex.: "às vezes ficava 2 a 3 horas a mais", sem dizer quantas vezes) fica fora da conta. O fato pode ficar no texto.

## Prorrogação do adicional noturno

- A conta e o pedido são só das horas depois das 05h00: saída − 05h00. Saída às 06h00 = 1 hora por plantão; às 07h00 = 2 horas; às 08h00 = 3 horas.
- Use horas de relógio. Não converta para hora noturna reduzida, mesmo que o texto do modelo cite a hora reduzida.
- Só nos meses de plantão noturno.

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
- Com a reversão do pedido de demissão (rescisão indireta), a saída vale como dispensa sem justa causa: todos os blocos têm as linhas do aviso prévio e da multa de 40% (e o acúmulo usa o ×1,4398).
- O TOTAL do bloco é a soma exata das linhas escritas, já arredondadas.

## Verbas rescisórias

Use só nas teses que mudam a forma de saída (rescisão indireta, nulidade da justa causa, vínculo) ou quando a rescisão não foi paga.

- **Sem TRCT:** calcule só a verba que a entrevista aponta como não paga (ex.: férias vencidas). Não acrescente verba proporcional ou outra verba que a entrevista não cita. Exceção: na tese que muda a forma de saída (reversão do pedido de demissão, rescisão indireta, nulidade da justa causa, vínculo), calcule todos os direitos da dispensa sem justa causa, nas linhas do pedido fixo de `teses.md`, uma vez só.
- **Aviso prévio proporcional:** 30 dias + 3 dias por ano completo de serviço, até 90 dias. O tempo do aviso conta para completar o ano (OJ 82 da SDI-1). Ex.: 3 anos e 11 meses de contrato + 30 dias de aviso = 4 anos completos, então 42 dias.
- **Valor do aviso:** salário / 30 × dias.
- **Reflexos do aviso:** 13º = valor / 12 × (dias / 30); férias e 1/3 da mesma forma.
- **13º proporcional:** avos do ano corrente até a saída projetada pelo aviso. Mês com 15 dias ou mais vale 1 avo. Se o pedido tem as linhas "13º salário sobre o aviso prévio" e "Férias sobre o aviso prévio" (pedido da reversão), os avos do 13º e das férias proporcionais vão só até a saída, sem a projeção: a projeção já está nessas linhas. Não conte o aviso duas vezes.
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

**Danos morais e o art. 223-G, § 1º:** o inciso tem de comportar o valor. Os tetos são inciso I (leve) 3 salários, II (média) 5, III (grave) 20 e IV (gravíssima) 50. Exceção: o pedido só de danos morais é texto fixo da advogada (`teses.md`, "Danos morais (pedido)") e cita o inciso I com R$ 10.000,00. Não troque o inciso nem o valor desse pedido, e não escreva nota sobre o teto. Fora desse texto fixo, o padrão é o inciso III, que comporta os R$ 10.000,00 com qualquer salário a partir do mínimo; se outro texto citar o inciso I (3 salários) ou o II (5 salários), o valor não pode passar desse teto.

## Honorários e valor da causa

- **Honorários:** 15% da soma de todos os pedidos com valor, incluindo danos, a multa do PPP e as multas. É o padrão de todas as petições do banco.
- **Valor da causa:** soma dos pedidos + honorários.
- O mesmo valor aparece em "SUBTOTAL em <dia> de <mês por extenso> de <ano>" e no item G das provas, com o valor por extenso.

## Planilha

- Baixe o modelo de cálculo e preencha a cópia local só as células de entrada dos blocos das teses escolhidas. Descubra essas células lendo a planilha com `openpyxl` (rótulos e fórmulas). Registre no log cada célula preenchida.
- Limpe as células de entrada que sobraram de outro caso (nome de paradigma, datas, avos e dias do cabeçalho). Se uma fórmula der `#REF!`, não use o bloco: calcule numa aba extra e registre no log.
- Teses sem bloco no modelo vão numa aba extra `Cálculos extras`, uma linha por item, com a fórmula visível.
- Para ler os totais calculados, suba a planilha (ela vira Google Sheet e calcula as fórmulas) e baixe o Sheet exportado como xlsx, como diz `drive.md`.
- **Meses de cada bloco (L6 = base de cálculo):** na aba `CALCULO TRABALHISTAS`, `L5` (MESES TRABALHADOS) é o fato do contrato (fórmula com entrada e saída) e `L6` (BASE DE CÁLCULO) é `=MIN(60;L5)`. Cada campo de meses dos blocos é fórmula que lê `L6`, nunca número solto: horas extras `K22`, intervalo `Z20`, adicional noturno `T49`, insalubridade `D36`, periculosidade `S36`, acúmulo `V60`, DSR `D61`, equiparação `H71`, e os meses dos blocos da aba `Cálculos extras` (ex.: desvio de função `='CALCULO TRABALHISTAS'!L6`). Nas verbas de trabalho efetivo com meses de afastamento, use `=L6-<meses de afastamento>` (ex.: `=L6-1`). Os anos de feriados são `AA5 = L6/12`, e `F48` (anos que o bloco de feriados usa) é `=AA5`. Assim o topo mostra o número que a conta usa, e mudar `L6` recalcula tudo. A planilha usa `;` como separador de argumentos.
- **Salário médio no período:** o salário médio ponderado (`Cálculos extras`) cobre só os meses do período de cálculo (os últimos 60, ou o contrato inteiro), com cada faixa salarial da CTPS que cai nele.
- **Salário com várias faixas:** o modelo tem uma célula de salário só. Nos blocos que usam todo o período, preencha o salário médio ponderado pelos meses, calculado na aba `Cálculos extras`. Um bloco com outro período (ex.: só os meses noturnos) é calculado faixa a faixa na aba extra.
- Rode o Python com `uv run --with openpyxl python3 ...`. Não instale pacotes no sistema.
