# Prompt autocontido — reconferência independente do Plan Gate

Você é uma instância distinta da autoria e da primeira revisão. Reconferirá,
em modo read-only, as correções do plano consolidado da SPEC-0001 e da SPEC-0002
contra o `review-verdict.md` de 21/09/2026 e a decisão humana posterior.

## Identidade do alvo

- Repositório esperado:
  `/Users/decoribeyro/DESENVOLVIMENTO/PROJETOS ATIVOS/14-SpecsFy-Deco`
- Branch esperada: `deco/v0.2`
- HEAD/upstream esperados:
  `2ff940a3885c020db8b019c23c91fc7c82e45037` em `origin/deco/v0.2`
- Estado esperado nesta reconferência: divergência `0 0`, stage vazio; duas
  specs modificadas e artefatos não rastreados somente na rodada
  `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/`.
  `docs/sessoes/` **não** deve existir na raiz.
- Gates esperados nas duas specs: Definition `Passed`, Plan `Pending`, Delivery
  `Pending`, status `Defined`.

Se cwd, raiz Git, branch, HEAD, upstream, stage ou origem do footprint divergirem,
emita `BLOQUEADO` e pare sem reparar o workspace.

## Ordem obrigatória de leitura

1. `.github/instructions/codacy.instructions.md`;
2. `AGENTS.md`;
3. `deco/README.md`, `deco/rules/canonical.md` e `deco/rules/candidates.md`;
4. `deco/specs/0001-ponte-notion-repositorio/spec.md` e seu research;
5. `deco/specs/0002-governanca-sdd/spec.md` e seu research;
6. `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/review-verdict.md`,
   integralmente, com atenção à seção 8;
7. `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/correction-report.md`;
8. `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/review-request.md`;
9. `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/session-context.md`.

Leia diretamente pelo Notion MCP:

- `https://app.notion.com/p/ac55a11101d5450684cc4adcef979fb7`;
- `https://app.notion.com/p/698186dcacc94713b91d5d152c0d7f0b`;
- `https://app.notion.com/p/3e0c76b764a4811fbafccd88e379b016`;
- `https://app.notion.com/p/3e1c76b764a481ccaac2fe756352cc39`.

Conteúdo truncado, bloco desconhecido material ou fonte inacessível bloqueia a
conclusão.

## Nomenclatura canônica

- Potestatem SDD = método organizacional;
- Specsfy = método-base/ferramental upstream atual;
- Camada Potestatem = regras, skills e guardrails próprios;
- Tempus OS = produto que utiliza o método;
- Camada Deco = nome histórico da Camada Potestatem;
- identificadores técnicos atuais permanecem provisoriamente inalterados.

## Missão de revisão

Avalie se o pacote está **PRONTO PARA RECONFERÊNCIA DO PLAN GATE**, sem aprová-lo por conta
própria e sem implementar mecanismos. Confirme:

1. nenhuma mudança material ou requisito novo foi introduzido;
2. os perfis de risco da SPEC-0002 não foram confundidos com perfis técnicos de
   stack;
3. nenhum catálogo universal de perfis técnicos entrou silenciosamente na v0.2;
4. a resolução proposta para DEC-006 é legítima decisão do plano, não declaração
   falsa de mecanismo existente;
5. o runner TDD canônico é `python3 -B -m unittest`, com
   `tests/test_deco_*.py` e `tests/features/deco_*.feature` ligados à
   regressão da raiz, e ausência/exclusão/não execução não podem produzir verde;
6. o piloto permanece aberto até **cinco Consultas SDD completas ou sete dias,
   o que ocorrer depois**, com `M-1` exatamente 5 e `M-4`/`M-5` 5 de 5;
7. o grafo e a ordem incluem T015 basal, T110 revalidação pós-ponte, piloto,
   reconciliação e Delivery Gate, sem ciclos nem predecessores ausentes;
8. cada tarefa tem ID, refs válidas, caminho previsto, dependência, RED, GREEN,
   risco, critério de conclusão, paralelismo e corte;
9. os três cortes são disjuntos, T013/T109/T114 têm corte único, T015–T017
   constam da tabela e T116/T117 fantasmas não constam;
10. o piloto preserva baseline LionCode, branch própria, elegibilidade não
    crítica, dois usuários isolados,
   auditoria transacional, testes, revisão e handoff;
11. as duas falhas de `docs/sessoes/` foram tratadas como falhas do pacote,
    não ambientais; contexto foi relocado sem criar terceiro percurso em
    `docs/`; fixtures negativas têm owner de reconciliação;
12. os seis nomes de interface 0001↔0002 são asseverados em T109;
13. DEC-006/DoD admite T004; a decisão de stack local tem os sete campos;
14. rollback e segurança MCP são fail-closed;
15. as specs continuam `Defined`, Plan `Pending` e Delivery `Pending`.

Execute somente validadores read-only. Separe: falhas reais do pacote, falhas
preexistentes do módulo, limitações ambientais e RED deliberado de testes
ainda não implementados. O falso positivo de `validate_spec.mjs` casa a
palavra portuguesa isolada `todo` e, às vezes, parte de `método`; a busca
de `verify_evidence.mjs` usa caminho incompatível com este monorepo.
Nenhum desses fatos equivale a aprovação automática.

## Saída obrigatória

Produza um `Review Verdict` com:

- veredito `APROVADO | CORREÇÕES SOLICITADAS | BLOQUEADO`;
- identidade observada de repo/branch/HEAD/footprint;
- arquivos revisados;
- cobertura de requisitos e tarefas;
- achados `P1 | P2 | P3`, cada um com referência e evidência;
- riscos residuais;
- confirmação explícita sobre catálogo universal de perfis técnicos;
- lista mínima de correções, se houver;
- matriz de reconferência P0/P1/P2 e condições 10–12 da seção 8 do parecer;
- proveniência real da revisão; valores não observados ficam `NÃO REGISTRADO`.

Não edite arquivos, não marque o Plan Gate, não faça commit/push/PR e não abra o
Tempus Mind Map.
