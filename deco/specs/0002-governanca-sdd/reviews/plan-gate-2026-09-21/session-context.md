# Contexto da rodada — correção do Plan Gate da Camada Potestatem

**Data:** 21/09/2026
**Estado:** PRONTO PARA RECONFERÊNCIA; Plan Gate `Pending`
**Unidade:** SPEC-0001 + SPEC-0002
**Método:** Potestatem SDD; base atual Specsfy; produto Tempus OS
**Fonte da correção:** [Review Verdict](review-verdict.md) e decisão humana desta rodada.

## Preflight manual antes da correção

- Raiz Git: `14-SpecsFy-Deco`; branch `deco/v0.2`.
- HEAD local e `origin/deco/v0.2`:
  `2ff940a3885c020db8b019c23c91fc7c82e45037`; divergência `0 0`.
- Stage vazio; dois `spec.md` modificados e quatro arquivos não rastreados:
  `review-request.md`, `independent-review-prompt.md`,
  `review-verdict.md` e `docs/sessoes/contexto_sessao_atual.md`.
- Classificação manual: `CONDICIONAL` por footprint conhecido. Não houve
  execução de Git Guardian formal; a primeira materialização está planejada
  na SPEC-0002/T004.

## Fontes normativas

- [Potestatem SDD — glossário e política de stacks](https://app.notion.com/p/ac55a11101d5450684cc4adcef979fb7).
- [Decisão — Fluxo SDD repo-first com ponte Notion MCP](https://app.notion.com/p/698186dcacc94713b91d5d152c0d7f0b).
- [Revisão humana original](https://app.notion.com/p/3e0c76b764a4811fbafccd88e379b016).
- [Reconferência e adendo factual](https://app.notion.com/p/3e1c76b764a481ccaac2fe756352cc39).

## Decisão humana e limites

- Runner TDD da v0.2: `python3 -B -m unittest` na raiz.
- Protocolo do piloto inalterado: cinco Consultas SDD completas ou sete dias,
  o que ocorrer depois; `M-1` exatamente 5 e `M-4`/`M-5` 5 de 5.
- Perfis de risco atuais não são catálogo técnico de stacks; catálogo
  universal permanece pós-piloto.
- Não houve implementação, acesso ao Tempus Mind Map, aprovação de gate,
  stage, commit, push ou PR nesta rodada.

## Topologia e próximo passo

Este contexto é evidência de revisão da própria camada, não handoff de um
projeto consumidor. Por isso foi retirado de `docs/sessoes/`, reservado ao
consumidor por `deco/rules/canonical.md`, e guardado nesta rodada. O
`docs/` da raiz volta a conter apenas os dois percursos oficiais.

Entregar [Correction Report](correction-report.md) e
[Review Request](review-request.md) à instância independente. Só ela pode
emitir novo veredito; a decisão humana de gate continua posterior.
