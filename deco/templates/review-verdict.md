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
