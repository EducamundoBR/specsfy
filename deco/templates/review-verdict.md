# Review Verdict — modelo da rodada

Responsável: revisor

Preencher em arquivo separado do Review Request, a partir da base e do diff
declarados. Começar em leitura; não aceitar a conclusão do implementador como
evidência. O revisor recomenda, o decisor designado decide o gate. Se revisor e
implementador forem a mesma instância ou tiverem o mesmo session ID, bloquear
a aprovação e pedir revisão independente.

## Identificação e proveniência

- **Unidade**: <preencher>
- **CURRENT**: <preencher>
- **Review Request**: <preencher>
- **Base e HEAD observados**: <preencher>
- **Escopo do diff conferido**: <preencher>
- **Implementador**: <preencher>
- **Revisor**: <preencher>
- **Decisor**: <preencher>
- **Harness**: <preencher>
- **Modelo**: <preencher>
- **Effort**: <preencher>
- **Session ID**: <preencher>

## Evidência e achados

- **Evidências**: <preencher>
- **Achados P0-P3**: <preencher>

| ID | Severidade P0–P3 | Fonte e trecho verificável | Impacto | Correção proposta |
| --- | --- | --- | --- | --- |
| <preencher> | <preencher> | <preencher> | <preencher> | <preencher> |

Usar `Nenhum` somente depois de inspecionar a superfície correspondente; não
deixar uma célula em branco. P0 exige parada imediata, P1 bloqueia o gate, P2
exige correção ou justificativa aceita e P3 registra melhoria. Relatar testes,
diff e evidência que sustentam cada achado ou a ausência deles.

## Parecer e encaminhamento

- **Veredito**: <preencher>
- **Condições**: <preencher>
- **Gate resultante**: <preencher>
- **Decisão humana**: <preencher>

Valores permitidos para `Veredito`: `APROVADO`, `CORREÇÕES SOLICITADAS` ou `REPROVADO`.
O campo `Gate resultante` registra a recomendação do revisor; até decisão
explícita do decisor, o gate permanece pendente. Nenhum parecer favorável sem
teste, diff e evidência fecha gate.

| Condição | Resultado |
| --- | --- |
| Proveniência, base, diff ou evidência ausentes | Devolver o pedido; nenhum veredito aprova gate. |
| Achado P0 ou P1 | Registrar `CORREÇÕES SOLICITADAS` e bloquear fechamento. |
| Parecer completo por instância distinta | Encaminhar recomendação ao decisor, sem autoaprovação. |

Exemplo válido: achado com severidade, fonte, impacto e correção, mais proveniência
do revisor. Exemplo inválido: “aprovado” sem teste, diff, evidência ou identidade
distinta; gate permanece pendente.

## Contrato estrutural

Adendo de 30/09/2026, por decisão humana: o Verdict é conferido pela estrutura,
sem interpretar a apresentação do Markdown.

- A tabela de achados deste modelo é a única fonte de P0, P1, P2 e P3: no máximo
  uma, com o cabeçalho exato, o separador e uma linha por achado, com as cinco
  células preenchidas.
- Fora dela, o Verdict contém somente título `#` na primeira linha, os cabeçalhos
  `##` deste modelo no máximo uma vez e na ordem do modelo, os campos deste modelo
  (uma vez cada), linhas idênticas à prosa e à tabela de condições deste modelo e
  texto simples.
- Texto simples, valores de campo e células usam só letras, números, pontuação,
  símbolos e o espaço comum, e não usam `[`, `]`, `<`, `>`, crase, `*`, `~`, `$`,
  barra invertida, entidade HTML nem `_` fora de palavra; nas células, a única
  barra invertida aceita é a de `\|`.
- A coluna de severidade contém exatamente P0, P1, P2 ou P3. Texto simples,
  valores de campo e as demais células não contêm `P` seguido de dígito em
  nenhuma posição, nem mesmo colado a letras, e não terminam em `P`.
- Texto simples e valores de campo não começam com recuo, citação, marcador de
  lista ou sublinhado de título.
- Qualquer outra linha bloqueia a aprovação e a liberação da escrita.
