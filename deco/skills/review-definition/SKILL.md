---
name: review-definition
description: Revisar uma spec no Definition Gate — problema, requisitos, escopo, decisões, cenários e dúvidas — e devolver achados priorizados em Review Verdict, sem autoaprovação nem marcação do gate.
---

# Review Definition

## Escopo

Skill de gate selecionada pelo `review-router` quando a unidade está no
Definition Gate (SPEC-0002/T008; FR-006; AC-004, AC-005, AC-020). Revisa se a
definição permite planejar sem inventar comportamento. Não planeja, não
implementa e não altera a spec revisada: devolve achados.

## Unidade revisada

A unidade é uma spec, com seus artefatos de research, revisada a partir de um
único Review Request consolidado da rodada ativa (`CURRENT`). Vários prompts ou
revisões do mesmo gate e da mesma base formam a mesma unidade; perfis de risco
compostos pelo roteador entram como anexos ao mesmo pedido, nunca como revisões
separadas.

## Critérios do Definition Gate

| Condição | Resultado |
| --- | --- |
| Problema e resultado desejado ausentes, vagos ou sem métrica de sucesso | Achado P1: definição não permite planejar. |
| Requisitos funcionais e não funcionais sem identificador, ambíguos ou não verificáveis | Achado P1 por requisito afetado. |
| Escopo incluído sem lista fechada ou escopo excluído implícito | Achado P1: fronteira indefinida. |
| Decisões sem motivo, alternativa considerada ou fonte | Achado P2. |
| Requisito sem cenários BDD de aceite ou AC sem cobertura rastreável | Achado P1. |
| Dúvidas abertas que mudam comportamento, dados ou escopo | Achado P1 até resposta registrada; dúvida não bloqueante vira P3. |
| Contradição entre seções, fontes ou specs relacionadas | Achado P0 se invalida o gate; senão P1. |
| Tudo verificado com evidência | Veredito `APROVADO`, recomendado ao decisor. |

## Achados priorizados

Os achados são listados em ordem de severidade — P0, P1, P2 e P3 —, cada um com
fonte e trecho verificável, evidência, impacto e correção proposta.

| Condição | Resultado |
| --- | --- |
| P0 | Parada imediata da rodada; nada segue ao decisor. |
| P1 | `CORREÇÕES SOLICITADAS`; Definition Gate pendente. |
| P2 | Correção ou justificativa aceita antes do fechamento. |
| P3 | Melhoria registrada, sem aprovação tácita. |
| Achado sem evidência ou correção proposta | Não entra no parecer até ser completado. |

## Separação e fechamento

O revisor abre contexto novo, inicialmente somente leitura, e trata a conclusão
do implementador como alegação. A composição vem do `review-router`: esta skill
mais os perfis indicados; os perfis acrescentam critérios, mas o perfil
não fecha o gate sozinho. O parecer é gravado em arquivo separado a partir de
`deco/templates/review-verdict.md`.

| Condição | Resultado |
| --- | --- |
| Revisor e implementador na mesma instância ou com o mesmo session ID | Recusar o parecer; gate bloqueado até instância distinta. |
| Parecer completo, com evidência e proveniência observada | Recomendar ao decisor; esta skill não marca o Definition Gate. |
| Pedido para registrar `Definition Gate: Passed` pelo revisor | Recusar; a marcação é decisão humana ou da instância decisora designada. |

## Evidência

Exemplo verificável: `deco/fixtures/review-skills/definition-verdict.md`.
