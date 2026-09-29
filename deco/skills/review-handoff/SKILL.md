---
name: review-handoff
description: Administrar o pacote de revisão entre implementador e revisor — Review Request, Review Verdict, Correction Report, rodada e ponteiro CURRENT — criando, validando, corrigindo e encerrando rodadas sem reescrever histórico.
---

# Review Handoff

## Escopo e autoridade

Skill de administração da rodada de revisão (SPEC-0002/T011; FR-007, FR-008,
FR-011; AC-020 a AC-026, AC-035 a AC-037). Ela cria a rodada, valida o pacote e
o ponteiro `CURRENT`, conduz correção e reconferência e encerra a rodada. Ela não
revisa conteúdo — isso cabe à skill de gate escolhida pelo `review-router` — e
não aprova gate.

Os campos dos três artefatos e as decisões de AC-020 a AC-026 são normativos em
`deco/templates/review-request.md`, `deco/templates/review-verdict.md` e
`deco/templates/correction-report.md` (T006). Esta skill aplica esses
contratos; não os duplica.

## Layout físico da rodada

Layout aprovado por decisão humana de Deco no adendo de 29/09/2026 ao Plan Gate
(SPEC-0002, §13, Gate do Ato II):

```text
<pasta da spec>/reviews/
  CURRENT                           UTF-8, uma linha: nome da pasta da rodada ativa
  <gate>-<AAAA-MM-DD>[-rNN]/
    estado.md                       - **Estado**: <estado da rodada>
    review-request.md               implementador
    review-verdict.md               revisor
    correction-report.md            implementador, quando houver achados
```

Artefatos exigidos por estado: `review-request.md` a partir de
`PRONTO PARA REVISÃO`; também `review-verdict.md` em `CORREÇÕES SOLICITADAS`,
`APROVADO` e `REPROVADO`; também `correction-report.md` em
`PRONTO PARA RECONFERÊNCIA`. `RASCUNHO` e `ENCERRADA SEM APROVAÇÃO` exigem só
`estado.md`. O pacote é delta: referencia fontes estáveis por caminho e não cola
transcript nem histórico de conversa. A sessão nova recebe apenas o caminho e
`CURRENT`.

Regras fail-closed de `CURRENT`:

| Condição | Resultado |
| --- | --- |
| `CURRENT` ausente, não UTF-8, vazio ou com mais de uma linha útil | Bloquear. |
| Conteúdo com caminho absoluto | Bloquear. |
| Conteúdo com `..` | Bloquear. |
| Conteúdo com separador de caminho que escape da pasta `reviews/` | Bloquear; só um nome relativo dentro de `reviews/`. |
| `CURRENT` ou a pasta de destino é link simbólico | Bloquear. |
| Destino inexistente (ponteiro quebrado) | Bloquear. |
| Destino existe, mas não é pasta | Bloquear. |
| Nome fora de `<gate>-<AAAA-MM-DD>[-rNN]` ou de gate diferente do gate esperado | Bloquear: rodada incompatível com o gate esperado. |
| Artefato exigido pelo estado da rodada ausente | Bloquear. |
| Destino é pasta de rodada ativa do gate esperado, com artefatos completos | Prosseguir, após conferir branch e HEAD. |

Colisão no mesmo dia:

| Condição | Resultado |
| --- | --- |
| Primeira rodada do gate no dia | Pasta `<gate>-<AAAA-MM-DD>`. |
| Nova rodada do mesmo gate no mesmo dia | Sufixo `-r02`, depois `-r03` e assim por diante; `CURRENT` passa a apontar para a nova rodada. |
| Pedido para reutilizar ou sobrescrever pasta existente | Recusar: uma rodada encerrada não pode ser sobrescrita. |

## Ciclo da rodada

Exatamente uma rodada ativa por unidade. Estados:
`RASCUNHO` → `PRONTO PARA REVISÃO` → `EM REVISÃO` → `CORREÇÕES SOLICITADAS` →
`PRONTO PARA RECONFERÊNCIA` → `APROVADO` | `REPROVADO`.
Uma rodada concluída é imutável.

| Condição | Resultado |
| --- | --- |
| Unidade sem rodada ativa e pedido de revisão | Criar pasta da rodada, `estado.md` em `RASCUNHO` e apontar `reviews/CURRENT` para ela. |
| `RASCUNHO` com Review Request completo e base conferida | `PRONTO PARA REVISÃO`. |
| `PRONTO PARA REVISÃO` e revisor distinto em contexto novo, somente leitura | `EM REVISÃO`. |
| `EM REVISÃO` e Verdict com achado bloqueante | `CORREÇÕES SOLICITADAS`. |
| `EM REVISÃO` e Verdict sem achado bloqueante, com proveniência completa | `APROVADO`, recomendação ao decisor do gate. |
| `CORREÇÕES SOLICITADAS` e Correction Report em lote gravado | `PRONTO PARA RECONFERÊNCIA`. |
| `PRONTO PARA RECONFERÊNCIA` e reconferência do mesmo revisor | `APROVADO` ou `REPROVADO`. |
| Pedido de edição em rodada `APROVADO` ou `REPROVADO` | Recusar; revisão adicional exige rodada nova. |

## CURRENT e SESSION_CURRENT

`CURRENT` identifica a rodada ativa e é validado por `review-handoff`; o arquivo
físico é `reviews/CURRENT` na pasta da spec. `SESSION_CURRENT` identifica o
contexto de sessão ativo e é validado pelo Session Guardian, por `docs/HANDOFF.md`.
Um ponteiro não substitui o outro, e nenhum dos dois substitui o veredito `GG-*`
do Git Guardian.

| Condição | Resultado |
| --- | --- |
| `reviews/CURRENT` com uma linha que resolve para uma rodada existente em estado ativo | Prosseguir, após conferir branch e HEAD. |
| `reviews/CURRENT` ausente, vazio ou com mais de uma linha | Bloquear; reconciliar o ponteiro antes de qualquer parecer. |
| `reviews/CURRENT` aponta pasta inexistente (quebrado) | Bloquear; nenhuma rodada é escolhida por dedução. |
| `reviews/CURRENT` aponta rodada `APROVADO`, `REPROVADO` ou `ENCERRADA SEM APROVAÇÃO` | Bloquear; abrir rodada nova se houver revisão a fazer. |
| Mais de uma rodada em estado ativo | Rejeitar a revisão e reportar a ambiguidade. |
| Pedido para usar `SESSION_CURRENT` como `CURRENT`, ou o inverso | Recusar; os identificadores são distintos. |

## Mudança material e nova rodada

Qualquer mudança de decisão, escopo incluído ou excluído ou classe de risco é
`MUDANÇA MATERIAL`. A rodada atual é encerrada como `ENCERRADA SEM APROVAÇÃO`,
com o motivo e a indicação "substituída por <nova rodada>" acrescentados ao
`estado.md`, sem reescrever os artefatos. Abre-se nova rodada em `RASCUNHO` e
`reviews/CURRENT` passa a apontar para ela.

| Condição | Resultado |
| --- | --- |
| `MUDANÇA MATERIAL` em qualquer estado ativo | Encerrar sem aprovação, registrar motivo e sucessora, abrir nova rodada e atualizar `CURRENT`. |
| Correção não material de metadado ou evidência | Permanecer na rodada, com uma reconferência consolidada. |

### AC-035 — Risco alto: plano e resultado em pedidos distintos

Para unidade de risco alto ou crítico, um Review Request do plano é gravado
antes da escrita, e outro Review Request do resultado é gravado
depois da escrita. Os dois pedidos são artefatos em instantes distintos da mesma unidade,
cada um em sua própria rodada.

| Condição | Resultado |
| --- | --- |
| Unidade de risco alto sem Review Request do plano antes da escrita | Bloquear a escrita até o pedido do plano existir. |
| Resultado de risco alto sem Review Request próprio depois da escrita | Recusar o fechamento; gravar o pedido do resultado. |
| Um único Review Request cobrindo plano e resultado | Recusar; separar em dois artefatos. |

### AC-036 — Proveniência insuficiente não fecha a rodada

Review Request e Review Verdict exigem harness, modelo, effort e session ID
observados do implementador e do revisor. Com qualquer valor não observado, a
rodada não fecha. Cada valor ausente persiste exatamente como `NÃO REGISTRADO`;
o relatório pode explicar a ausência, sem substituir o token. Nenhum valor é
inferido de nome, contexto, transcript ou ferramenta.

| Condição | Resultado |
| --- | --- |
| Campo de proveniência com `NÃO REGISTRADO` no fechamento | A rodada não fecha. |
| Valor preenchido por dedução, sem observação | Substituir por `NÃO REGISTRADO` e bloquear o fechamento. |
| Valor observado depois, com fonte e data | Atualizar o campo citando a fonte. |

### AC-037 — Base observada diferente bloqueia a revisão

O Review Request declara branch e HEAD. Se o revisor observa branch ou HEAD
diferente do declarado, a revisão não prossegue como se fosse sobre a mesma
unidade: a rodada passa para `CORREÇÕES SOLICITADAS`, nenhum parecer de aprovação
é emitido e o Review Request precisa ser corrigido. Se a divergência for
`MUDANÇA MATERIAL`, a rodada é encerrada sem aprovação e uma nova rodada é
aberta, com `CURRENT` passando a indicar a nova rodada. Nenhum parecer é aprovado
sobre base diferente da declarada.

| Condição | Resultado |
| --- | --- |
| Branch ou HEAD observado diferente do Review Request | `CORREÇÕES SOLICITADAS`; corrigir o pedido; nenhum parecer de aprovação. |
| Divergência que altera decisão, escopo ou risco | Encerrar sem aprovação, abrir nova rodada e atualizar `CURRENT`. |
| Base observada igual à declarada | Prosseguir com a revisão. |

## Evidência

Fixtures de ponteiro e layout em `deco/fixtures/review-handoff/`. Base
divergente e proveniência ausente são exercitadas pelas fixtures de T006 em
`deco/fixtures/review-round/`: `request-divergent-branch.md` e
`request-divergent-head.md` (AC-037), `request-unregistered-session.md` e
`verdict-unregistered-session.md` (AC-036), todas rejeitadas pelo validador de
`tests/test_deco_governance_rounds.py`.
