---
name: review-plan
description: Revisar o plano no Plan Gate — arquitetura, tarefas, ordem, riscos, rollback e testes previstos, dependências cíclicas, lacunas e escopo adiado — e devolver achados priorizados, sem promover o gate.
---

# Review Plan

## Escopo

Skill de gate selecionada pelo `review-router` quando a unidade está no Plan
Gate (SPEC-0002/T009; FR-006; AC-004, AC-005, AC-020). Revisa se o plano
executa a definição aprovada com rastreabilidade, ordem segura e retorno
possível. Não executa tarefas e não altera o plano revisado.

## Unidade revisada

Um plano integrado — seção de plano técnico, tarefas e ordem de execução de uma
ou mais specs aprovadas no Definition Gate — revisado por um único Review
Request consolidado, com perfis compostos anexos ao mesmo pedido.

## Critérios do Plan Gate

| Condição | Resultado |
| --- | --- |
| Arquitetura, módulos ou artefatos sem dono ou caminho definido | Achado P1. |
| Tarefas sem referência a requisito e AC, ou sem critério de conclusão | Achado P1: rastreabilidade quebrada. |
| Ordem que coloca implementação antes do teste RED ou quebra dependência declarada | Achado P1. |
| Riscos sem mitigação, dono ou condição de parada | Achado P2; P1 se o risco for alto ou crítico. |
| Rollback ausente para tarefa com escrita externa, dados ou histórico | Achado P1. |
| Testes previstos sem comando, nível ou evidência esperada | Achado P2. |
| Tudo verificado com evidência | Veredito `APROVADO`, recomendado ao decisor. |

## Dependências, lacunas e escopo adiado

| Condição | Resultado |
| --- | --- |
| Dependência cíclica entre tarefas ou specs | Achado P1; plano bloqueado até quebrar o ciclo. |
| Lacuna: requisito ou AC sem tarefa ou sem teste que o cubra | Achado P1 por item descoberto. |
| Tarefa sem requisito ou AC de origem | Achado P2: escopo não autorizado. |
| Escopo adiado declarado e registrado com decisão explícita e dono | Aceitar; conferir que nenhuma tarefa depende dele. |
| Escopo adiado implícito ou sem decisão registrada | Achado P1. |

Uma dependência cíclica é P1 e bloqueia o plano. Cada lacuna — requisito ou AC
sem tarefa ou sem teste — também é P1. O escopo adiado só é aceito quando
declarado e registrado com decisão explícita e dono. O revisor não promove o Plan Gate:
recomenda; a marcação cabe ao decisor.

## Achados priorizados

Os achados são listados em ordem de severidade — P0, P1, P2 e P3 —, cada um com
fonte e trecho verificável, evidência, impacto e correção proposta.

| Condição | Resultado |
| --- | --- |
| P0 | Parada imediata da rodada. |
| P1 | `CORREÇÕES SOLICITADAS`; Plan Gate pendente. |
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
| Parecer completo, com evidência e proveniência observada | Recomendar ao decisor; esta skill não promove o Plan Gate. |

## Evidência

Exemplos verificáveis: `deco/fixtures/review-skills/plan-verdict-approved.md` e
`deco/fixtures/review-skills/plan-verdict-corrections.md`.
