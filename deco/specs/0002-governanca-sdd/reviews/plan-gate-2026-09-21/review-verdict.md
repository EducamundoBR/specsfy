# Review Verdict — Plan Gate consolidado SPEC-0001 + SPEC-0002

## 1. Veredito

> ### `REPROVADO` — equivalente a `CORREÇÕES SOLICITADAS` no vocabulário do prompt
>
> O pacote **não está pronto para o Plan Gate**. Dois achados `P0` atingem a
> cadeia de evidência do plano: o runner de TDD contraria a proposta que a
> própria seção 11 delegou a este gate, e o piloto planejado é estruturalmente
> incapaz de satisfazer o protocolo normativo do piloto já aprovado no
> Definition Gate.
>
> **O Plan Gate NÃO foi marcado e permanece `Pending` nas duas specs. Nenhum
> arquivo do repositório foi criado, editado, movido ou removido, exceto esta
> página de parecer.**

O que está sólido: a fronteira entre perfis de risco e perfis técnicos de stack
está correta; nenhum requisito, US, AC ou cenário foi alterado; o grafo macro não
contém ciclos; o piloto preserva baseline LionCode, censo read-only, branch
própria, isolamento entre dois usuários, auditoria transacional, testes, revisão
e handoff; rollback e segurança MCP são fail-closed; os gates continuam corretos.

## 2. Identidade observada

| Campo | Esperado | Observado | Resultado |
| --- | --- | --- | --- |
| cwd e raiz Git | `…/14-SpecsFy-Deco` | idêntico | ✅ |
| Branch | `deco/v0.2` | `deco/v0.2` | ✅ |
| HEAD | `2ff940a…` | `2ff940a3885c020db8b019c23c91fc7c82e45037` | ✅ |
| Upstream | `origin/deco/v0.2` | `origin/deco/v0.2` | ✅ |
| Divergência | `0 0` | `0	0` | ✅ |
| Stage | vazio | `git diff --cached --name-only` sem saída | ✅ |
| Footprint | autoria + contexto de sessão | ` M 0001/spec.md`, ` M 0002/spec.md`, `?? …/reviews/`, `?? docs/sessoes/` | ✅ coerente com o pós-autoria |
| Gates | Definition `Passed`; Plan e Delivery `Pending`; Status `Defined` | idêntico nas duas specs | ✅ |

`origin` é `EducamundoBR/specsfy` (fork), `upstream` é `promovaweb/specsfy` —
consistente com as rodadas anteriores. Não houve `BLOQUEADO`: a divergência
aparente do footprint é o produto declarado desta autoria, não desvio de
identidade.

## 3. Arquivos e fontes revisados

Locais: `.github/instructions/codacy.instructions.md`; `AGENTS.md`;
`deco/README.md`; `deco/rules/canonical.md`; `deco/rules/candidates.md`;
`deco/specs/0001-ponte-notion-repositorio/spec.md` (1.774 linhas) e seu research
(369); `deco/specs/0002-governanca-sdd/spec.md` (2.026) e seu research (565);
`review-request.md`; `independent-review-prompt.md`;
`docs/sessoes/contexto_sessao_atual.md`; `skills/specsfy-04-validate/scripts/validate_spec.mjs`;
`tests/test_references.py`.

Notion MCP, quatro páginas, **todas carregadas integralmente, sem truncamento e
sem bloco desconhecido**:

1. `ac55a11101d5450684cc4adcef979fb7` — Potestatem SDD — glossário e política de stacks (`Ativo`, 21/09/2026);
2. `698186dcacc94713b91d5d152c0d7f0b` — Decisão — Fluxo SDD repo-first com ponte Notion MCP (`APROVADA · 16/09/2026`);
3. `3e0c76b764a4811fbafccd88e379b016` — Revisão independente final (`CORREÇÕES SOLICITADAS`, executada 19/09/2026);
4. `3e1c76b764a481ccaac2fe756352cc39` — Reconferência Opus A-01 a A-17 (`CORREÇÕES ACEITAS`, 19/09/2026).

## 4. Cobertura de requisitos e tarefas

Censo independente, executado sobre os arquivos atuais e contra `HEAD`:

| Item | SPEC-0001 | SPEC-0002 |
| --- | --- | --- |
| US / FR / NFR | 3 / 10 / 4 | 4 / 12 / 5 |
| IDs `AC` únicos | 28 | 38 |
| Blocos `Scenario` | 35 | 56 |
| Tarefas em §14 | **15** (`T101`–`T115`) | **17** (`T001`–`T017`) |
| Cobertura `validate_tasks` | `45/45` | `59/59` |
| Itens de checklist | 90 | 102 |

**Nenhuma mudança material foi introduzida nas seções 1–7.** `git diff` toca
apenas a data do cabeçalho, um bloco de nomenclatura na seção 8 e as seções 14 e
15. As contagens de US, FR, AC e `Scenario` são idênticas entre `HEAD` e a
árvore de trabalho nas duas specs. Requisito 1 da missão: **atendido**, com a
exceção registrada em `P0-2`, que é redução e não acréscimo.

### Validadores read-only executados

| Comando | Resultado observado |
| --- | --- |
| `validate_tasks.mjs` · 0001 | `NOT READY` — **dois** erros: Plan Gate `Pending` e `verify_evidence.mjs` |
| `validate_tasks.mjs` · 0002 | `NOT READY` — os mesmos dois erros |
| `validate_spec.mjs` · ambas | `NOT READY` — `Marcadores não resolvidos` |
| `validate_interface_tasks.mjs` · ambas | `Interface nas tarefas: OK` |
| `check_traceability.mjs` | `ERRO: spec, raiz de testes, tipos ou mínimo inválidos` — não reproduzido |
| `make verify-version` | ✅ verde — versão única `0.22.2` |
| `python3 -B -m unittest discover -s tests` | 111 testes, **8 falhas e 3 erros** |
| `uv … behave` | não executável — `uv` ausente |

### Separação exigida: falha do pacote × limitação ambiental

Confirmei as duas limitações declaradas e **não as converti em aprovação**:

- **Falso positivo do regex** — legítimo e verificado. O padrão é
  `/\b(?:TODO|TBD|FIXME)\b|\[NEEDS CLARIFICATION/im` (`validate_spec.mjs:103`).
  `\b` é ASCII, então `é` cria fronteira e `mé|todo` casa. Busquei os tokens nas
  duas specs: **8 ocorrências em 0001 e 7 em 0002, todas a palavra portuguesa
  `todo`/`Todo` ou a discussão do próprio defeito**. Zero `TBD`, `FIXME` ou
  `[NEEDS CLARIFICATION` reais. Ressalva de precisão: o Review Request atribui o
  casamento a `todo` *dentro de* `método`; a maioria das ocorrências é a palavra
  isolada. As specs descrevem as duas causas corretamente.
- **`verify_evidence.mjs`** — confirmado. O script existe em
  `skills/specsfy-07-implement/scripts/`; o validador o exige em `.agents/`.
  Incompatibilidade de caminho nesta raiz, não defeito do pacote.
- **`uv` ausente, `pdftohtml`/`pdftotext`/`mapfile` ausentes, `origin` do fork** —
  genuinamente ambientais. Cobrem os 3 erros e 3 das 8 falhas.

**Mas duas falhas não são ambientais nem preexistentes** — ver `P1-3`.

## 5. Achados

### `P0-1` — O runner de TDD contraria a proposta que a seção 11 delegou a este gate

**Referência:** `0001/spec.md:1258-1260`; `0002/spec.md` §11; tarefas `T001`–`T003`,
`T101`–`T103`; `review-request.md`, "Arquivos previstos" e "Testes e evidências
previstos"; `AGENTS.md`, seção "Validação".

**Evidência.** A seção 11 da SPEC-0001 declara, e a da SPEC-0002 repete:

> **Runner TDD**: proposta — `python3 -B -m unittest`, o runner já existente na
> raiz do monorepo (`AGENTS.md:110-118`), **para não introduzir stack nova**. A
> confirmação cabe ao Plan Gate.

O plano fixa o oposto e não registra a decisão: `T001`–`T003` criam
`deco/tests/governance/{contracts,rounds,delivery}.test.mjs` e `T101`–`T103`
criam `deco/tests/notion-bridge/{contracts,safety,reconciliation}.test.mjs` — um
harness Node, isto é, exatamente a stack nova que a seção 11 pedia evitar.
Nenhum `DEC` novo registra a escolha, nenhuma tarefa declara o runner, e nenhuma
tarefa integra esses arquivos à regressão da raiz.

Pior: a tabela "Arquivos previstos" do Review Request promete
`tests/test_deco_*.py` e `tests/features/deco_*.feature` — o harness Python/Behave
da raiz — que **contradiz a própria tabela de tarefas do mesmo documento** e que
**nenhuma tarefa das duas specs cria**. Busca por `tests/test_deco`,
`tests/features` e `behave` nas duas specs retorna apenas linhas da seção 13, que
registram o estado do ambiente.

**Impacto.** A seção 13 e o Review Request declaram a regressão da raiz
(`unittest`, Behave, `make verify-version`) como evidência do Delivery Gate. Com
`.test.mjs` sem runner e fora do `discover`, essa regressão ficaria verde **sem
jamais executar um único teste da Camada Potestatem**. É precisamente o falso
verde que `FR-012` e `AC-032`–`AC-038` existem para impedir, instalado na base do
plano. O Plan Gate era o local designado para confirmar ou rejeitar a proposta da
seção 11; o plano decidiu contra ela em silêncio.

### `P0-2` — O piloto planejado não pode satisfazer o protocolo normativo do piloto

**Referência:** `0001/spec.md:972-975` (protocolo do piloto), `:66-72` (`M-1`–`M-7`),
`:1749` (DoD), `:1323` (`NFR-002` verificado "piloto contra M-1 a M-7");
`review-request.md`, seção "Piloto consumidor" e corte de Delivery; `T114`;
`0002/spec.md:1775`. Fonte primária: Notion `698186dcacc94713b91d5d152c0d7f0b`,
"Fase 1 — piloto manual".

**Evidência.** O texto normativo, aprovado no Definition Gate, é taxativo:

> - Projeto **não crítico**, nunca o legado nem um projeto com cliente ativo.
> - Duração: **cinco consultas completas ou sete dias, o que ocorrer depois**.

E as metas: `M-1` "Consultas completas no piloto — **exatamente 5**"; `M-4` e
`M-5` "**5 de 5**"; `M-2` "≥ 3 de 5". O DoD da SPEC-0001 exige "Piloto foi medido
contra `M-1` a `M-7`". A fonte Notion aprovada em 16/09/2026 diz o mesmo:
"medir por sete dias ou por cinco consultas completas, **o que ocorrer depois**".

O plano fixa: "Meta: **12–16 horas** de execução com IA dentro de **1–2 dias**" e,
como escopo máximo, "**uma** atualização do cockpit por MCP". `T114` é
literalmente "Executar piloto e **uma atualização** de cockpit". O corte de
Delivery repete "**uma** atualização real e escopada do cockpit".

**Impacto.** Uma janela de 1–2 dias não alcança o piso de sete dias, e uma
atualização de cockpit não é cinco Consultas SDD completas. `M-1`, `M-2`, `M-4` e
`M-5` tornam-se inatingíveis por construção, `NFR-002` perde o método de
verificação declarado e o item de DoD nunca fecha. Isto é **redução material de
requisito aprovado, não declarada como tal** — pela regra do próprio pacote
("Mudança material reabre rodada", condição 4 da reconferência aceita), exige
rodada nova, não aprovação condicional. Secundariamente, o plano nunca certifica
explicitamente que o Tempus Mind Map satisfaz "projeto não crítico, nunca o
legado nem um projeto com cliente ativo"; `T111` deveria fazê-lo no censo.

### `P1-1` — A tabela consolidada de tarefas diverge da fonte normativa

**Referência:** `review-request.md`, "Tarefas consolidadas"; `0001/spec.md` §14;
`0002/spec.md` §14.

O Review Request declara a convenção: "Os IDs `T0xx` pertencem à SPEC-0002;
`T1xx`, à SPEC-0001". Contra as specs:

| Divergência | Evidência |
| --- | --- |
| `T116` e `T117` **não existem** | A SPEC-0001 termina em `T115`; `validate_tasks` conta 15 tarefas. Duas linhas da tabela são IDs fantasma no namespace da SPEC-0001. |
| `T015`, `T016` e `T017` **foram omitidos** | Existem na SPEC-0002 (instalação isolada; contrato do piloto; reconciliação e Delivery Gate) e não aparecem na tabela. `validate_tasks` conta 17 tarefas. |
| Dependências reescritas | A tabela dá a `T101`–`T103` "Dependências: `T004`–`T014`"; a spec registra `Depends: none`. |
| Caminho omitido | `T015` prevê `deco/fixtures/consumer/valid/AGENTS.md`; "Arquivos previstos" só declara `deco/fixtures/{governance,notion-bridge}/`. |

**Impacto.** O revisor humano do Plan Gate aprovaria uma tabela que não é projeção
fiel das specs, e três tarefas normativas atravessariam o gate sem revisão.

### `P1-2` — O grafo de dependências contradiz a ordem de execução

**Referência:** `review-request.md`, bloco `mermaid` e "Tarefas consolidadas";
`0002/spec.md` §15, passos 4–6; `0001/spec.md` §15, passo 1.

O grafo ordena `C[Ponte local] → D[Integração] → E[Validadores] → F[Empacotamento]
→ G[Instalação no consumidor]`: a ponte é integrada **antes** do pacote. A ordem
de execução faz o inverso — `T014` (pacote e instalador) e `T015` (instalação
isolada no consumidor) executam no passo 4, e só no passo 5 vêm `T101`–`T110`,
sendo `T110` justamente "Integrar a ponte ao pacote em `deco/manifest.json`".
`T015` depende apenas de `T014`, nunca de `T110`, e **nenhuma tarefa revalida a
instalação depois que a ponte entra no manifesto**.

Não há ciclo — requisito 5 da missão está atendido —, mas há contradição de
ordem com uma lacuna concreta de verificação: o pacote seria validado no
consumidor sem a metade que a SPEC-0001 entrega.

Secundariamente, o nó `A[Git Guardian] → B[Governança transversal]` inverte a
ordem real: `T004` depende de `T001`–`T003`.

### `P1-3` — Duas falhas de regressão são do pacote, não do ambiente

**Referência:** `review-request.md`, "Validação executada nesta sessão";
`0002/spec.md:1602`; `tests/test_documentation_audiences.py:34`;
`tests/test_contexto_projeto.py:192`; `tests/test_references.py:43-49`;
`AGENTS.md`, "Disciplina documental".

O Review Request classifica as 8 falhas e 3 erros como "preexistentes/ambientais".
Isolei cada teste:

```
test_docs_has_exactly_the_user_and_develop_trees
  AssertionError: Items in the second set but not the first: 'sessoes'

test_all_documents_are_reachable_from_portal
  órfãos: {…/docs/sessoes/contexto_sessao_atual.md}
```

As duas falham **exclusivamente** por causa de `docs/sessoes/`, artefato desta
frente de trabalho — não do ambiente. A própria seção 13 das duas specs registra
"111 testes; **6 falhas** e 3 erros" no HEAD `71ee8ed`; hoje são **8**. O delta é
exatamente essas duas. E `AGENTS.md` é explícito: "Na primeira camada, `docs/`
contém somente `docs/README.md`, `docs/user/` e `docs/develop/`" — a raiz do
monorepo não é projeto consumidor, e `deco/rules/canonical.md` coloca
`docs/sessoes/<AAAA-MM-DD>-handoff.md` **no consumidor**. Nenhuma tarefa das duas
specs tem dono para esse item.

Outras duas falhas também não são ambientais, embora sejam preexistentes: são do
módulo `deco/` (`deco/README.md` no teste de logo; `deco/fixtures/handoff/broken-pointer/`
e `deco/templates/HANDOFF.md` no teste de links). Esta última é estrutural e
agrava: `tests/test_references.py` varre a árvore inteira e **não tem exclusão
para fixture negativa**. `T013` e `T109` criam `deco/fixtures/governance/` e
`deco/fixtures/notion-bridge/` cheias de casos negativos, que quebrarão o mesmo
teste. O plano exige regressão da raiz verde no Delivery Gate e simultaneamente
manda criar o que a quebra, sem nenhuma tarefa que reconcilie os dois.

### `P1-4` — Os três cortes não são coerentes entre si nem com as specs

**Referência:** `review-request.md`, "Três cortes" e coluna `Corte`;
`0002/spec.md:1801`; `0001/spec.md:1589-1591`.

- A SPEC-0002 declara "**`T001`–`T016` formam o mínimo pilotável**"; a tabela
  marca `T013` como `Delivery`.
- A SPEC-0001 declara "`T101`–`T114` compõem o mínimo pilotável" e, na mesma
  frase, "`T109` … necessárias ao Delivery Gate" — `T109` está nas duas faixas.
  A tabela marca `T109` e `T114` como `Delivery`, contra o texto da spec.

O requisito 7 da missão — "os três cortes são coerentes" — **não está atendido**.
A parte boa: o pós-piloto **não invade o mínimo pilotável**. Catálogo universal,
rename, database estruturada, custom agent/trigger/worker, automação normativa,
colaboração e produção pública estão consistentemente fora em todos os três
documentos.

### `P2-1` — A resolução de DEC-006 é legítima, mas o DoD não a admite

**Referência:** `0002/spec.md:1939-1948` (`DEC-006`), `:1988-1990` (DoD);
`review-request.md`, decisão 2.

Confirmo o requisito 4 da missão: **não há declaração falsa de mecanismo
existente**. `DEC-006` continua dizendo que o censo não encontrou artefato,
`T004` registra o RED "GG formal inexistente", e a alternativa que `DEC-006`
descartou era fixar a implementação **no Definition Gate** — fazê-lo no Plan Gate
é exatamente o lugar correto. A decisão é legítima.

O defeito é de fechamento: o DoD admite apenas duas saídas — "fonte canônica
versionada localizada e referenciada, **ou** spec própria aberta". A saída
escolhida — materializar em `T004` dentro da SPEC-0002 — não é nenhuma das duas, e
o item de DoD permaneceria insatisfazível como está escrito.

### `P2-2` — O verificador executável dos seis nomes de interface ficou pela metade

**Referência:** `0001/spec.md:1523-1529` (`T109`); revisão independente de
19/09/2026, §11 item 1 e reconferência aceita ("prever verificação executável
desses nomes no Plan Gate").

O `PREP` de `T109` enumera "seis interfaces 0001↔0002", mas o `VERIFY` pede GREEN
apenas em "positivos, negativos, offline e reconciliação" e o `EVIDENCE` registra
"matriz fixture → requisito → resultado". A verificação dos nomes não é asseverada
nem evidenciada. A junta entre as duas specs continua puramente semântica, que é
o ponto fraco que a rodada anterior mandou fechar neste gate.

### `P2-3` — O registro de decisão de stack da política aprovada não tem dono

**Referência:** Notion `ac55a11101d5450684cc4adcef979fb7`, §4 item 6;
`review-request.md`, "Análise de impacto da política de stacks"; `T112`.

A política aprovada em 21/09/2026 exige: "A decisão de stack deve acontecer no
começo da especificação, registrando: tipo de produto, restrições, chassi
disponível, competência operacional, testes, deploy e custo de manutenção". O
Review Request classifica o eixo como "sem requisito de implementação nestas
specs". O `PREP` de `T112` registra apenas "autenticação, dois usuários e
PostgreSQL preferencial". Os sete campos não são exigidos por nenhuma tarefa.

### `P3-1` — "O único erro em ambas" é impreciso

`validate_tasks.mjs` retorna **dois** erros nas duas specs: `Plan Gate precisa
estar Passed para validação estrita` e `Evidence Contract 1 exige
verify_evidence.mjs`. O primeiro é esperado e benigno, mas o pacote afirma que há
um só.

### `P3-2` — Veredito `CONDICIONAL` atribuído a um Git Guardian declaradamente inexistente

`review-request.md` registra "Git Guardian desta autoria: `CONDICIONAL`" e
`docs/sessoes/contexto_sessao_atual.md` repete "veredito Git Guardian:
`CONDICIONAL`", enquanto `DEC-006` e `T004` declaram que o mecanismo não existe.
Não é afirmação falsa — a inexistência está declarada em outro lugar do mesmo
pacote —, mas rotular um julgamento manual com o nome do guardrail não
implementado convida exatamente a confusão que `FR-004` quer evitar. Sugiro
"preflight manual" até `T004` existir.

### `P3-3` — `Review state` assimétrico

A SPEC-0002 tem `| Review state | APROVADO |` (`:17`); a SPEC-0001 não tem a linha.
`O-01` da reconferência foi corretamente fechado na SPEC-0002 — a Proveniência
registra a rodada de correção de 19/09 e o parecer —, mas a SPEC-0001 ficou sem
ponteiro de rodada equivalente.

### `P3-4` — `check_traceability.mjs` não é reproduzível a partir do pacote

O Review Request afirma que o script foi "executado para fotografar o RED", sem
registrar a linha de comando. Minha execução retornou
`ERRO: spec, raiz de testes, tipos ou mínimo inválidos` — consistente com a
inexistência de raiz de testes, mas o resultado alegado não é verificável.

## 6. Confirmação explícita — catálogo universal de perfis técnicos

> **Confirmado: nenhum catálogo universal de perfis técnicos de stack entrou na
> v0.2, nem silenciosa nem explicitamente.**

Verifiquei por busca direta (`laravel|postgres|catálogo universal|perfis técnicos|stack`)
nas duas specs, e requisito por requisito:

- `FR-006` da SPEC-0002 define **quatro perfis de risco** —
  `security-auth-privacy`, `data-migration`, `git-deploy`, `business-customer` —
  e declara que "complementam a skill de gate: não a substituem, não fecham gate
  sozinhos e não geram skill por combinação". São perfis de **risco e domínio**,
  idênticos ao adendo aprovado em 16/09/2026. **Não foram confundidos com perfis
  de stack** (requisito 2 da missão: atendido).
- A tabela de seis perfis técnicos existe **apenas na fonte Notion**
  (§5 de `ac55a11101d5450684cc4adcef979fb7`) e **não foi importada** para
  nenhuma das duas specs.
- `0002/spec.md:1282-1285` e `0001/spec.md:915-917` declaram explicitamente o
  adiamento; `T117` do Review Request e os cortes o confirmam como pós-piloto com
  Definition Gate próprio.
- A menção a Laravel/PostgreSQL é **contrato técnico local do piloto**, sempre
  condicionada ao censo read-only, e ambas as specs afirmam que não acopla o
  método à stack.

Requisito 3 da missão: **atendido**.

## 7. Riscos residuais

1. **`RISK-012` / `G-28`** — a materialização do Git Guardian segue sem prazo. O
   plano lhe dá dono (`T004`), o que é progresso real, mas o caminho crítico
   inteiro depende dela.
2. **Junta semântica entre as duas specs** — permanece sem verificador asseverado
   (`P2-2`). Enquanto as specs evoluírem em rodadas separadas, nada detecta a
   quebra de correspondência.
3. **Regressão da raiz em conflito estrutural com fixtures negativas** (`P1-3`) —
   tende a piorar a cada tarefa de validador.
4. **`G-29`** — ausência de segunda instância bloqueia em vez de liberar; ainda
   não testado em uso, e o piloto de 1–2 dias não o testará.
5. **`RISK-011`** — declarado não plenamente mitigado; permanece aberto.
6. **Modo estrito indisponível** — por desenho do validador enquanto o Plan Gate
   for `Pending`, somado ao falso positivo upstream. Nenhum dos dois é defeito do
   pacote.
7. **Ownership compartilhado de arquivos do piloto** — `deco/pilots/tempus-mind-map/acceptance.md`
   é escrito por `T016` (0002) e por `T111`–`T113` (0001); `evidence.md`, por
   `T017` (0002) e `T114`–`T115` (0001). Nenhuma das specs declara quem é dono.

## 8. Condições mínimas para o Plan Gate

**Bloqueantes — exigem nova rodada de correção antes de qualquer marcação:**

1. **`P0-1`** — Decidir o runner de TDD explicitamente, como `DEC` registrado, já
   que a seção 11 delegou a confirmação a este gate. Se `python3 -B -m unittest`
   for confirmado, reescrever os caminhos de `T001`–`T003` e `T101`–`T103`. Se o
   harness Node for escolhido, registrar a decisão, declarar o runner, justificar
   a stack nova contra a intenção da seção 11 e **acrescentar tarefa que integre
   esses testes à regressão declarada da raiz**. Reconciliar a tabela "Arquivos
   previstos", que hoje promete `tests/test_deco_*.py` e `tests/features/deco_*.feature`
   que nenhuma tarefa cria.
2. **`P0-2`** — Reconciliar o piloto com o protocolo normativo: ou o plano adota
   "cinco consultas completas ou sete dias, o que ocorrer depois" e ajusta o
   timebox e `T114`, ou a redução é declarada como **mudança material**, abre
   rodada nova e reabre os Atos I–III da SPEC-0001, alterando `M-1`–`M-7`,
   `NFR-002` e o DoD sob decisão humana explícita. Acrescentar a `T111` a
   certificação de "projeto não crítico, nunca o legado nem projeto com cliente
   ativo".

**Necessários antes do fechamento:**

3. **`P1-1`** — Reemitir a tabela consolidada como projeção fiel das specs:
   remover `T116`/`T117` ou criá-los nas specs; incluir `T015`, `T016` e `T017`;
   alinhar as dependências de `T101`–`T103`; declarar `deco/fixtures/consumer/`.
4. **`P1-2`** — Alinhar grafo e ordem de execução, e fazer `T015` depender de
   `T110` ou criar tarefa que revalide a instalação após a integração da ponte.
5. **`P1-3`** — Reclassificar as duas falhas como do pacote; criar tarefa dona da
   remoção ou relocação de `docs/sessoes/` conforme `AGENTS.md`; criar tarefa que
   reconcilie `tests/test_references.py` com as fixtures negativas previstas.
6. **`P1-4`** — Tornar os três cortes idênticos entre Review Request e as duas
   seções 15.
7. **`P2-1`** — Ajustar o item de DoD de `DEC-006` para admitir a terceira saída.
8. **`P2-2`** — Assevere a verificação dos seis nomes no `VERIFY` e no `EVIDENCE`
   de `T109`.
9. **`P2-3`** — Dar dono aos sete campos do registro de decisão de stack.

**Recomendados, não bloqueantes:** `P3-1` a `P3-4`.

**Procedimentais:**

10. O fechamento exige **instância distinta** de quem escreveu o plano
    (`FR-003` da SPEC-0002, Guardrail A de `deco/rules/canonical.md`). Este
    parecer **não fecha o gate**; o autor do plano também não pode.
11. Registrar a evidência mínima de `FR-011` no ato do fechamento, com todo valor
    não observado exatamente como `NÃO REGISTRADO`.
12. Qualquer alteração de decisão, escopo ou classe de risco a partir daqui é
    `MUDANÇA MATERIAL` e abre rodada nova.

## 9. Proveniência desta revisão

| Campo | Valor |
| --- | --- |
| Unidade revisada | Plano integrado da SPEC-0001 e da SPEC-0002 |
| Risco | Alto documental e operacional |
| Data de execução | 2026-09-21 |
| Papel | Revisor independente, read-only |
| Harness | Claude Code (CLI), macOS Darwin 24.5.0 |
| Modelo do revisor | `claude-opus-5` (Opus 5) |
| Effort solicitado ao revisor | `NÃO REGISTRADO` — o pedido não declarou effort |
| Effort efetivamente observado | `NÃO REGISTRADO` |
| Session ID do revisor | `NÃO REGISTRADO` |
| Autoria revisada | Codex; modelo exposto pela sessão `gpt-5.6-sol`; effort e session ID `NÃO REGISTRADO` |
| Branch e HEAD | `deco/v0.2` · `2ff940a3885c020db8b019c23c91fc7c82e45037` |
| Rodada anterior | Definition Gate `Passed`, `APROVADO`, fechamento humano de Deco Ribeyro em 19/09/2026 |
| Autoaprovação | Nenhuma realizada |
| Base da conferência | Arquivos atuais e quatro páginas Notion carregadas integralmente. O Review Request **não** foi aceito como prova de si mesmo. |

## 10. Declaração de nenhuma alteração no repositório

> Durante esta revisão **nenhum arquivo local foi editado, movido ou removido**.
> Não houve `add`, `commit`, `push`, `fetch`, `pull`, `switch`, `stash`, `reset`
> nem `clean`. Nenhum remote foi alterado. **Nenhum gate foi marcado.** Nenhuma
> spec, plano, tarefa ou código foi tocado. Nenhum mecanismo foi implementado.
> Nenhum subagente foi acionado. Nenhuma página do Notion foi criada ou
> modificada — as quatro fontes foram apenas lidas. O repositório do Tempus Mind
> Map não foi aberto. Nenhum defeito foi corrigido silenciosamente.
>
> A única escrita executada foi a criação deste arquivo,
> `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/review-verdict.md`,
> que é o artefato separado exigido por `FR-007`.
>
> **Estado final, idêntico ao inicial:** branch `deco/v0.2` · HEAD
> `2ff940a3885c020db8b019c23c91fc7c82e45037` · divergência `0 0` · stage vazio ·
> `M deco/specs/0001-ponte-notion-repositorio/spec.md` ·
> `M deco/specs/0002-governanca-sdd/spec.md` · `?? deco/specs/0002-governanca-sdd/reviews/` ·
> `?? docs/sessoes/` · zero commit novo, sem push.
