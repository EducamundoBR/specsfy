---
name: review-delivery
description: Revisar o resultado no Delivery Gate — Contrato de Entrega, diff, testes, evidências, regressões e aderência — distinguindo PRONTO, ENTREGUE e ACEITO, sem autoaprovação nem marcação do gate.
---

# Review Delivery

## Escopo

Skill de gate selecionada pelo `review-router` quando a unidade está no Delivery
Gate (SPEC-0002/T010; FR-006, FR-009, FR-010, FR-011; AC-027 a AC-031). Revisa
se o resultado cumpre o Contrato de Entrega com evidência material. A regra
completa dos estados e do contrato vive em `deco/rules/delivery-contract.md`
(T012); esta skill aplica essa regra na revisão, sem redefini-la.

### AC-027 — Contrato incompleto não dispara

O Contrato de Entrega tem treze campos obrigatórios, declarados antes da
execução: objetivo de uso; artefato e destino; estado final esperado; escopo
incluído; escopo excluído; critérios de aceite; mecanismo de verificação;
evidência; resíduos proibidos; fronteira de autonomia e condições de parada;
aprovador; atualização documental; rollback. Com um campo ausente, o trabalho
não é iniciado e a revisão não começa. O campo ausente é apontado por nome antes
de qualquer execução ou trabalho.

| Condição | Resultado |
| --- | --- |
| Um dos treze campos ausente ou vazio | Não iniciar; apontar o campo ausente antes da execução. |
| Critério, mecanismo e evidência colapsados em um só campo | Tratar como campo ausente. |
| Treze campos presentes | Prosseguir para os critérios do Delivery Gate. |

## Critérios do Delivery Gate

| Condição | Resultado |
| --- | --- |
| Diff fora do escopo incluído do Contrato de Entrega | Achado P1. |
| Testes declarados não executados, ou execução sem saída registrada | Achado P1. |
| Evidências que não provam cada critério de aceite pelo mecanismo declarado | Achado P1 por critério. |
| Regressão em teste antes verde, inclusive fora do escopo | Achado P1; estado `CORREÇÃO NECESSÁRIA`. |
| Aderência à spec, às decisões e às restrições quebrada | Achado P1. |
| Atualização documental devida ausente | Achado P2. |
| Resíduo proibido presente ou rollback sem ponto de retorno verificado | Achado P1. |

## Estados de entrega

`PRONTO`, `ENTREGUE` e `ACEITO` não são sinônimos e não se colapsam. Qualquer
regressão leva a unidade a `CORREÇÃO NECESSÁRIA`; evidência material ausente
não aprova e resulta em `CORREÇÕES SOLICITADAS`.

| Condição | Resultado |
| --- | --- |
| Verificações internas verdes e evidência produzida, ainda na origem | `PRONTO`; nunca descrito como entregue ou aceito. |
| Presença e alcance comprovados no destino declarado | `ENTREGUE`; ainda sem aceite. |
| Aprovador designado conferiu no destino e registrou aceite explícito | `ACEITO`. |
| Regressão detectada | `CORREÇÃO NECESSÁRIA`, com motivo e nova evidência para voltar a `PRONTO`. |
| Evidência material ausente para qualquer critério | Não aprova: `CORREÇÕES SOLICITADAS`. |
| Validação humana antes do destino | Conta só como autorização para entrega, nunca como `ACEITO`. |

## Achados priorizados

Os achados são listados em ordem de severidade — P0, P1, P2 e P3 —, cada um com
fonte e trecho verificável, evidência, impacto e correção proposta.

| Condição | Resultado |
| --- | --- |
| P0 | Parada imediata; nenhuma ação externa. |
| P1 | `CORREÇÕES SOLICITADAS`; Delivery Gate pendente. |
| P2 | Correção ou justificativa aceita antes do fechamento. |
| P3 | Melhoria registrada, sem aprovação tácita. |

## Separação e fechamento

O revisor abre contexto novo, inicialmente somente leitura, e trata a conclusão
do implementador como alegação. A composição vem do `review-router`: esta skill
mais os perfis indicados; os perfis acrescentam critérios, mas o perfil
não fecha o gate sozinho. O parecer é gravado em arquivo separado a partir de
`deco/templates/review-verdict.md`.

| Condição | Resultado |
| --- | --- |
| Revisor e implementador na mesma instância ou com o mesmo session ID | Recusar o parecer; gate bloqueado até instância distinta. |
| Parecer completo, com evidência e proveniência observada | Recomendar ao decisor; esta skill não marca o Delivery Gate. |

## Evidência

Exemplo verificável: `deco/fixtures/review-skills/delivery-verdict-regression.md`.
