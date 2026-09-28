---
name: session-guardian
description: Verificar abertura, continuidade, fechamento e retomada de sessão pelo contexto ativo e SESSION_CURRENT, com veredito SG.
---

# Session Guardian

## Escopo e fontes

Papel de verificador operacional da continuidade entre sessões. Ler o roteador
canônico, o contexto curado ativo, o handoff de sessão e o estado observado. Não
decide gate humano e não aprova trabalho do implementador. Executar na abertura,
após mudança de contexto e no fechamento.

`SESSION_CURRENT` identifica logicamente o contexto de sessão; `CURRENT` identifica
a rodada de revisão. São ponteiros distintos. O Session Guardian não escreve a
rodada: solicita a `review-handoff` sua criação e atualização quando necessária.

## Entrada e verificação de abertura

1. Localizar o roteador canônico do projeto e as instruções locais. Identificar a
   unidade ativa e seu escopo.
2. Resolver `SESSION_CURRENT` para exatamente um contexto com status `ATUAL`.
   Conferir unicidade no conjunto estrutural de snapshots, sem escolher pelo
   nome mais recente. Contextos `SUPERADO` não são ativos.
3. Conferir projeto, branch e HEAD declarados contra o estado observado. Conferir
   cinco campos obrigatórios, ausência de superação e escopo correspondente à
   unidade ativa. Consultar `git status` para fatos Git; o Git Guardian mantém
   seu próprio veredito.
4. Registrar fonte, valor declarado, valor observado e resultado de cada cheque.
   Ausência ou ambiguidade bloqueia a abertura. Um transcript ou resumo
   automático não é fonte canônica.

Os cinco campos, em ordem, são `Projeto e data`, `Estado verificável`, `Decisões
da sessão + porquê`, `Pendências e próximo passo`, `Evidências e links canônicos`.
O estado registra branch, HEAD, stage, worktree, publicado e ainda local. Cada
decisão registra seu motivo; lacunas de proveniência usam `NÃO REGISTRADO`.

## Saída e precedência

Emitir exatamente um veredito: `SG-VÁLIDO`, `SG-CONDICIONAL`, `SG-BLOQUEADO`.
Registrar fase, ponteiro, snapshot, cinco campos, identidade observada, escopo,
evidências, divergências, correção e próxima ação. Bloqueio prevalece sobre
condição; condição prevalece sobre válido. Após correção, repetir toda a
verificação. Não transformar continuidade operacional em aprovação de gate.

### AC-014 — Um contexto ativo e identidade coerente

A verificação funciona sem rede, com arquivos locais e sem acesso a serviço externo.

| Condição | Resultado |
| --- | --- |
| `SESSION_CURRENT` resolve exatamente um contexto `ATUAL`; projeto, branch e HEAD correspondem ao estado observado; cinco campos completos, não superado, escopo correto | `SG-VÁLIDO`; continuar somente na unidade declarada. |
| Dois contextos `ATUAL` coexistem | `SG-BLOQUEADO`; nenhum contexto é escolhido silenciosamente. Reconciliar a origem. |
| Projeto, branch ou HEAD divergem sem explicação | `SG-BLOQUEADO`; continuidade recusada até reconciliar identidade e evidência. |
| Ponteiro ausente, quebrado ou ambíguo; contexto ausente ou superado | `SG-BLOQUEADO`; reconstruir fonte canônica antes de continuar. |

### AC-015 — Fonte curada

| Condição | Resultado |
| --- | --- |
| Transcript bruto ou resumo automático apresentado como contexto | Não é fonte canônica; exigir arquivo curado e `SESSION_CURRENT`. |
| Transcript ou retomada automática como única fonte | `SG-BLOQUEADO`; reconstruir handoff a partir de fatos verificáveis. |

### AC-016 — Mudança material e correção limitada

| Condição | Resultado |
| --- | --- |
| Alteração de decisão, escopo incluído ou excluído, ou classe de risco | `MUDANÇA MATERIAL` → `SG-BLOQUEADO`; `review-handoff` cria nova rodada e reposiciona `CURRENT` antes de seguir. O contexto anterior não é reescrito. |
| Metadado, evidência ou proveniência incompletos, sem alterar decisão, escopo ou risco | `SG-CONDICIONAL`; correção reversível na sessão atual, com origem registrada. |
| `SESSION_CURRENT` desatualizado mas aponta para único contexto identificável | `SG-CONDICIONAL`; corrigir ponteiro, preservar único contexto e fazer verificação repetida. |

Rodada de execução é unidade de trabalho; rodada de revisão é o pacote controlado
por `CURRENT`. Nenhuma delas substitui decisão humana de gate.

### AC-017 — Fechamento e imutabilidade

No fechamento, preencher cinco campos com porquê de cada decisão, fatos e links
em delta. Manter exatamente um contexto ativo. Publicar snapshot e
`SESSION_CURRENT` de forma conjunta ou atômica, então reler ambos. Se a
atualização conjunta falhar, não declarar fechamento; restaurar o ponteiro
anterior e verificar sua integridade antes de nova tentativa. O snapshot
superado permanece rastreável.
O contexto anterior fica superado sem reescrita de seu conteúdo.

| Condição | Resultado |
| --- | --- |
| Cinco campos válidos, exatamente um contexto ativo, snapshot e ponteiro coerentes | `SG-VÁLIDO`; fechar sessão, sem fechar gate humano. |
| Ponteiro e snapshot discordam, ou anterior foi reescrito | `SG-BLOQUEADO`; preservar evidência e reconciliar. |

### AC-018 — Estado observado e retomada

| Condição | Resultado |
| --- | --- |
| Branch, HEAD, stage ou worktree sem observação atual | `SG-BLOQUEADO`; fechamento impedido até o estado ser observado e registrado. |
| Decisões registradas apenas como “decidido”, sem razão | Fechamento recusado; porquê é obrigatório para cada decisão. |
| Compressão ou perda de contexto que impeça reconstrução segura | `SG-BLOQUEADO`; retomada automática não substitui handoff estruturado. |
| Depois de duas compactações, chega a terceira | `SG-CONDICIONAL`; abrir nova sessão com handoff estruturado e verificação repetida. |

Na retomada, reler o roteador e somente o contexto ativo resolvido por
`SESSION_CURRENT`, comparar fatos Git e pendências, e aplicar a tabela de
abertura. Não usar lembrança do transcript como prova.

### AC-019 — Fronteira entre mecanismos

`SG-VÁLIDO`, `SG-CONDICIONAL` e `SG-BLOQUEADO` dizem respeito à sessão. O Git
Guardian verifica o repositório com prefixo GG. `review-handoff` administra o
pacote Review Request, Review Verdict e Correction Report da rodada. Nenhum
substitui os demais nem se autoaprova. Uma aprovação de gate requer revisor e
decisor distintos conforme a spec.

| Condição | Resultado |
| --- | --- |
| Estado Git requerido | Executar Git Guardian e registrar o veredito GG próprio. |
| Continuidade de sessão requerida | Executar Session Guardian e registrar o veredito SG próprio. |
| Rodada de revisão requerida | Encaminhar ao `review-handoff` e aguardar revisão independente; nenhum mecanismo substitui os demais. |
