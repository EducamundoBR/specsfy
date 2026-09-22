# Reconferência independente — Plan Gate consolidado SPEC-0001 + SPEC-0002

Rodada única de reconferência sobre o lote consolidado, confrontada achado a
achado com o [Review Verdict](review-verdict.md) original. O parecer original
**não foi alterado** (`sha256 ac088a1f…`, 474 linhas, intacto).

## 1. Veredito

> ### `APROVADO COM CONDIÇÕES` — recomendado para decisão humana
>
> Os dois achados `P0` e os quatro `P1` do parecer original estão
> **integralmente resolvidos**, verificados contra os arquivos e não contra a
> declaração do executor. Os três `P2` e os quatro `P3` também. **Nenhuma
> condição pré-Plan Gate permanece aberta.**
>
> As condições restantes pertencem à **execução e ao Delivery Gate**, não ao
> plano. Registro **um achado novo `P2`** — uma falha preexistente do módulo
> `deco/` que bloqueia o Delivery Gate e ainda não tem tarefa dona.
>
> **O Plan Gate NÃO foi marcado e permanece `Pending` nas duas specs.** Esta
> aprovação significa apenas "recomendado para decisão humana de Deco". Nenhum
> arquivo foi editado; a única escrita foi a criação desta página.

## 2. Identidade do revisor e estado Git observado

| Campo | Valor |
| --- | --- |
| Tipo | Reconferência única do lote consolidado |
| Data | 21/09/2026 |
| Revisor | Claude Code / **Opus 5** (`claude-opus-5`) |
| Effort solicitado / observado | `NÃO REGISTRADO` — o pedido não declarou effort |
| Session ID do revisor | `NÃO REGISTRADO` |
| Autoria da correção | Codex; modelo, effort e session ID `NÃO REGISTRADO` |
| Risco | Alto documental e operacional |
| Base da conferência | Arquivos atuais. O Correction Report **não** foi aceito como prova de si mesmo. |
| Autoaprovação | Nenhuma realizada |

Recaptura Git read-only, anterior à análise:

| Item | Esperado | Observado | Resultado |
| --- | --- | --- | --- |
| cwd e raiz Git | `…/14-SpecsFy-Deco` | idêntico | ✅ |
| Branch | `deco/v0.2` | `deco/v0.2` | ✅ |
| HEAD | `2ff940a…` | `2ff940a3885c020db8b019c23c91fc7c82e45037` | ✅ |
| Upstream | `origin/deco/v0.2` | `origin/deco/v0.2` | ✅ |
| Divergência | `0 0` | `0	0` | ✅ |
| Stage | vazio | sem saída | ✅ |
| Status | 2 `M` · 1 `??` | ` M 0001/spec.md`, ` M 0002/spec.md`, `?? …/reviews/` | ✅ |
| `docs/sessoes/` | ausente | **removido** — `docs/` tem só `README.md`, `develop/`, `user/` | ✅ |
| `git diff --check` | limpo | exit 0 | ✅ |
| Gates | Definition `Passed`; Plan e Delivery `Pending`; Status `Defined` | idêntico nas duas specs | ✅ |
| Commit / push / PR | zero | zero | ✅ |

**Nenhuma mudança material foi introduzida nesta rodada de correção.** Censo
contra `HEAD`: SPEC-0001 mantém 3 US, 10 FR, 28 IDs `AC` e 35 blocos `Scenario`;
SPEC-0002 mantém 4 US, 12 FR, 38 IDs `AC` e 56 blocos `Scenario` — idênticos. O
`git diff` toca apenas cabeçalho, §8, §11, §13, §14, §15, §17 e §18: níveis de
plano e entrega, como uma rodada de Plan Gate exige.

## 3. Matriz de reconferência — achado a achado

| Achado | Estado | Evidência verificada por mim |
| --- | --- | --- |
| **`P0-1`** runner e falso verde | **RESOLVIDO** | ver §3.1 |
| **`P0-2`** protocolo do piloto | **RESOLVIDO** | ver §3.2 |
| **`P1-1`** tabela divergente | **RESOLVIDO** | ver §3.3 |
| **`P1-2`** grafo × ordem | **RESOLVIDO** | ver §3.4 |
| **`P1-3`** regressão documental | **RESOLVIDO** | ver §3.5 |
| **`P1-4`** cortes incoerentes | **RESOLVIDO** | ver §3.6 |
| **`P2-1`** DoD de `DEC-006` | **RESOLVIDO** | `0002/spec.md:2023-2025` admite a terceira saída: "**ou** primeira materialização executada e validada pela `T004` desta SPEC-0002 (FR-004, DEC-006)". |
| **`P2-2`** seis nomes de interface | **RESOLVIDO** | `0001/spec.md` `T109` `VERIFY` asseveram "presença e equivalência exata" dos seis nomes, "com falha para nome ausente, divergente ou extra"; `EVIDENCE` registra "comparação 6/6". Conferi os seis literalmente: `Cockpit do projeto` (0001=4 · 0002=1), `Consulta SDD` (40·5), `Relatório Modo B` (9·1), `Limite de interação` (3·1), `Precedência e reconciliação entre repositório e Notion` (2·1), `Permissões MCP e vedações` (2·1). **6/6 resolvem nas duas specs.** |
| **`P2-3`** decisão de stack | **RESOLVIDO** | `T112` `PREP` traz os sete campos da política de 21/09/2026: "tipo de produto, restrições, chassi disponível, competência operacional, testes, deploy e custo de manutenção", com "sem catálogo universal". Censo textual 7/7. |
| **`P3-1`** contagem de erros | **RESOLVIDO** | O Review Request distingue: um erro com `--allow-draft`, "portanto são **dois** erros no modo estrito, não um". Reproduzi: `--allow-draft` → 1 erro (`verify_evidence.mjs`); estrito → 2. |
| **`P3-2`** rótulo do Git Guardian | **RESOLVIDO** | O campo passou a ser "**Preflight manual** desta autoria: `CONDICIONAL` … não houve Git Guardian formal, cuja primeira materialização futura pertence à SPEC-0002/T004". `session-context.md` usa a mesma linguagem. |
| **`P3-3`** `Review state` assimétrico | **RESOLVIDO** | `0001/spec.md:17` e `0002/spec.md:17` ambos `| Review state | APROVADO |`. |
| **`P3-4`** `check_traceability` não reproduzível | **RESOLVIDO** | Linha de comando exata registrada, com raiz `tests`, `--json --full-chain`, exit 1, 22/45 e 25/59 IDs e cadeias incompletas. RED declarado, sem alegação de verde. |
| **§8.10** instância distinta | **RESOLVIDO** | Esta reconferência é instância distinta de quem escreveu e corrigiu. Nem o autor nem eu podemos fechar o gate. |
| **§8.11** evidência de `FR-011` | **PARCIAL — por desenho** | Pertence ao **ato** de fechamento, não ao pacote. Os valores não observados persistem como `NÃO REGISTRADO` em todos os artefatos. Permanece condição pré-Plan Gate do ato humano. |
| **§8.12** mudança material | **RESOLVIDO** | Nenhuma decisão de escopo, risco ou Definition Gate foi alterada; contagens idênticas a `HEAD`. |

### 3.1 `P0-1` — runner, integração à regressão da raiz e ausência de falso verde

Verificado item a item do pedido de reconferência:

- **Runner canônico declarado.** `DEC-009` (`0002/spec.md:1997-2002`): "confirmar
  `python3 -B -m unittest` na raiz para todos os testes `tests/test_deco_*.py`;
  cenários `tests/features/deco_*.feature` participam da regressão BDD… **Não
  adotar `deco/tests/**/*.test.mjs`**". A §11 das duas specs deixou de dizer
  "proposta": `0002:1487` "**Runner TDD confirmado**"; `0001:1269` "**Runner TDD
  confirmado pela decisão humana deste Plan Gate**".
- **Caminhos das tarefas.** Conferi os 32 cabeçalhos. Os seis predecessores TDD
  agora apontam para a raiz: `tests/test_deco_governance_{contracts,rounds,delivery}.py`
  e `tests/test_deco_bridge_{contracts,safety,reconciliation}.py`. **Zero
  ocorrências** de `deco/tests/` ou `.test.mjs` nas tarefas.
- **Integração à regressão da raiz.** `T013` foi reescrita para "Integrar
  validador, fixtures **e regressão da raiz**", com alvo adicional
  `tests/test_deco_regression_contract.py`, e `EXECUTE` cria "contrato de
  regressão da raiz que verifica **presença, descoberta e execução** de todos os
  testes da Camada Potestatem".
- **Validação negativa para ausência, exclusão e não execução.** `T013` `VERIFY`:
  "simular ausência, exclusão e não execução de qualquer suíte da camada e
  **exigir falha não zero em cada caso**". `EVIDENCE`: "os três exits negativos;
  **nenhuma suíte ignorada pode gerar verde**".
- **Ausência de falso verde no Delivery.** `T017` `VERIFY` exige a regressão
  completa, o BDD da raiz, "IDs esperados e executados da camada, negativa de
  ausência/exclusão/não execução e **nenhuma falha mascarada antes de qualquer
  Delivery Gate verde**". Novo item de DoD em `0002/spec.md:2026-2028` e o
  equivalente na SPEC-0001 fecham o mesmo contrato.
- **Coerência entre arquivos previstos, tarefas e evidências.** A contradição
  original — "Arquivos previstos" prometendo `tests/test_deco_*.py` enquanto as
  tarefas criavam `.mjs` — desapareceu: agora os três documentos convergem no
  mesmo harness. `T001` `PREP` já projeta `tests/features/deco_governance_contracts.feature`.

O falso verde que o parecer original apontou está **fechado por desenho**, não
por declaração.

### 3.2 `P0-2` — protocolo do piloto

- **`0001/spec.md:983`** mantém intacto: "Duração: **cinco consultas completas ou
  sete dias, o que ocorrer depois**"; `:982` mantém "Projeto **não crítico**".
- **`M-1` a `M-7` inalteradas**: `M-1` "exatamente 5", `M-2` "≥ 3 de 5", `M-4` e
  `M-5` "5 de 5". Nenhuma meta foi afrouxada.
- **`T111`** `PREP` passa a "certificar projeto não crítico, nunca o legado nem
  projeto com cliente ativo"; `VERIFY` exige "elegibilidade não crítica antes de
  abrir branch ou iniciar piloto".
- **`T114`** foi reescrita para "Executar piloto **medido** e **atualizações** de
  cockpit **por marco**". `EXECUTE`: "executar cinco Consultas SDD completas no
  fluxo real, **aguardar pelo menos sete dias**… a primeira atualização não
  substitui as demais nem a medição". `VERIFY`: "manter piloto aberto até cinco
  consultas completas ou sete dias, o que ocorrer depois; confirmar `M-1`
  exatamente 5, `M-4` e `M-5` 5 de 5, `M-2` pelo menos 3 de 5".
- **`T016`** da SPEC-0002 espelha o protocolo e veda o atalho: "sem usar
  atualização de cockpit como substituto".
- **DoD preservado e reforçado**: novo item em `0001` exige que o piloto tenha
  permanecido aberto pelos dois limiares, com `M-1`=5 e `M-4`/`M-5`=5/5, e que
  "uma atualização do cockpit não substituiu a medição nem os demais marcos".
- **Busca por redução residual**: `1–2 dias`, `12–16 horas` e
  `uma atualização do cockpit` → **zero ocorrências** nas duas specs e no Review
  Request. A estimativa de horas do piloto foi removida do documento.

Nenhuma redução de requisito sobreviveu. A decisão humana foi aplicada na letra.

### 3.3 `P1-1` — tabela derivada das 32 tarefas normativas

Censo próprio: SPEC-0002 tem **17** tarefas (`T001`–`T017`, incluindo `T014`, que
usa "por" e não "em" no cabeçalho) e SPEC-0001 tem **15** (`T101`–`T115`) —
**32** normativas. Executei conferência mecânica read-only comparando cada linha
da tabela com o cabeçalho normativo em quatro colunas (owner, texto, `Refs`,
`Depends`):

```
PASS exit=0 tasks=32 table=32 nodes=32 edges=72 cycles=0 missing=0 cuts=32
```

- `T015`, `T016` e `T017` **presentes**; `T116` e `T117` **ausentes** — zero IDs
  fantasma.
- `Depends` de `T101`–`T103` preservado como `none`, idêntico à spec. A
  precedência cruzada vive no grafo e na §15, não falsificada na coluna.

### 3.4 `P1-2` — grafo, ordem e revalidação da instalação

Auditei as arestas por conta própria: **65** são dependências normativas
(todas presentes, zero faltando) e **7** são pré-condições cruzadas declaradas —
`T015→T101/T102/T103`, `T015→T110`, `T111→T016`, `T016→T112`, `T115→T017`.
**Zero arestas espúrias.** Busca em profundidade: **zero ciclos**, zero
predecessores ausentes.

A lacuna central do parecer original está fechada: `T110` passou a "Integrar a
ponte ao pacote **e revalidar instalação**", e seu `VERIFY` exige "após integrar a
ponte, repetir a instalação sintética da SPEC-0002/T015 e obter GREEN em
instalação, idempotência, conflito, rollback, escopo do manifest e runtime
offline; **o GREEN anterior à ponte não serve ao Delivery Gate**". As duas §15
dizem o mesmo, e a de 0002 acrescenta: "nenhuma evidência anterior a `T110`
valida a instalação final".

Também resolvido o risco residual 7 do parecer original: a propriedade dos
arquivos do piloto foi separada — `T016`/`T017` passam a
`governance-acceptance.md` e `governance-evidence.md`, enquanto `T111`–`T113`
mantêm `acceptance.md` e `T114`–`T115` mantêm `evidence.md`. Sem sobrescrita
entre specs.

### 3.5 `P1-3` — tratamento de `docs/sessoes/`

O contexto foi relocado para `session-context.md` dentro da própria rodada de
revisão e o diretório removido. `docs/` volta a conter exatamente `README.md`,
`develop/` e `user/`, como `AGENTS.md` exige. Reproduzi os dois testes focais:
`test_docs_has_exactly_the_user_and_develop_trees` e
`test_all_documents_are_reachable_from_portal` **passam**. A regressão caiu de 8
para **6** falhas. `T013` `PREP` fixa a regra para o futuro: "guardar o contexto
desta rodada em … `session-context.md`, **nunca em `docs/sessoes/` na raiz do
monorepo**". O Correction Report classifica as duas como falhas do pacote, não
ambientais — correção explícita do erro de classificação original.

### 3.6 `P1-4` — cortes exclusivos

Cortes agora disjuntos e idênticos nos três documentos. SPEC-0002: "mínimo
pilotável = `T001`–`T016` (inclui `T013` e `T015`); necessário para Delivery Gate
= `T017`; pós-piloto = nenhuma tarefa desta spec". SPEC-0001: "mínimo pilotável =
`T101`–`T114`, incluindo `T109` e o piloto completo de `T114`; necessário para
Delivery Gate = `T115`". A conferência mecânica confirma **32 IDs em um corte
cada** e que nenhuma aresta volta de `Delivery` para `Mínimo`. `T013`, `T109` e
`T114` ficam exclusivamente no mínimo, como o pedido exigia. Nenhuma tarefa
normativa pós-piloto — o antigo `T117` deixou de existir.

## 4. Achados novos e regressões

**Nenhuma regressão foi introduzida.** Contagens, cobertura, fronteira de escopo,
gates e obrigações permanecem íntegros. Registro três achados novos, nenhum
bloqueante do Plan Gate.

| ID | Sev. | Local | Achado |
| --- | --- | --- | --- |
| **N-01** | **P2** | `deco/README.md`; `tests/test_brand_icon_adoption.py` | `test_all_tracked_readmes_use_the_canonical_logo_with_png_fallback` falha em `deco/README.md`. É falha **preexistente do módulo**, honestamente declarada no Correction Report, mas **nenhuma das 32 tarefas a assume**. Busca por `logo`/`brand` nas duas specs e no Review Request retorna apenas falsos positivos de substring em "catálogo". O DoD exige "Verificações e checks estáticos disponíveis passam" e a regressão da raiz verde no Delivery Gate; sem dono, esse item não fecha. Não compromete o plano — compromete a chegada ao Delivery Gate. |
| **N-02** | **P3** | `0002/spec.md` `T013` `PREP`; `deco/templates/HANDOFF.md` | `T013` assume "reconciliar `tests/test_references.py` com fixtures negativas sem ocultar links reais quebrados". Das duas quebras atuais, uma é fixture negativa deliberada (`deco/fixtures/handoff/broken-pointer/`) e a outra é **placeholder de template** (`deco/templates/HANDOFF.md -> sessoes/AAAA-MM-DD-handoff.md`), que não é fixture. A redação cobre o primeiro caso com clareza e o segundo por implicação. |
| **N-03** | **P3** | `T016`, `T017` | As pré-condições cruzadas `T111→T016` e `T115→T017` existem no grafo, na §15 e no `PREP` de `T017` ("exigir evidência local da SPEC-0001/T115"), mas não no campo `Depends`, que não cruza specs por limitação do validador. Correto e declarado; apenas invisível a `validate_tasks.mjs`. Vale o verificador cruzado que `T013`/`T109` já preveem. |

## 5. Avaliação da regressão e do BDD indisponível

Executei a regressão por conta própria: **111 testes, 6 falhas, 3 erros**,
exatamente o reportado. Classificação individual:

| Teste | Causa observada | Classificação | Cobertura |
| --- | --- | --- | --- |
| `test_all_authored_markdown_links_and_anchors_resolve` | `deco/fixtures/handoff/broken-pointer/docs/HANDOFF.md`; `deco/templates/HANDOFF.md` | **Preexistente do módulo `deco/`** | `T013` `PREP` (ver `N-02`) |
| `test_all_tracked_readmes_use_the_canonical_logo…` | `deco/README.md` | **Preexistente do módulo `deco/`** | **sem dono** → `N-01` |
| `test_public_origin_is_the_promovaweb_monorepo` | `origin` = `EducamundoBR/specsfy` | **Limitação ambiental (fork)** | estrutural do fork |
| `test_collector_recognizes_the_current_workspace` | mesma causa | **Limitação ambiental (fork)** | estrutural do fork |
| `test_build_manifest_proves_sources_and_artifacts_are_current` | `mapfile: command not found` | **Limitação ambiental** | toolchain local |
| `test_setup_creates_and_preserves_design_system_template` | `template não encontrado: …UserProfile.md` | **Limitação ambiental** | exige `specsfy install` |
| 3 × `test_ebook_usuario` (`ERROR`) | `pdftohtml` / `pdftotext` ausentes | **Limitação ambiental** | toolchain local |

**Falhas introduzidas ou mantidas pelo pacote: zero.** As duas que o parecer
original atribuiu ao pacote foram eliminadas.

**BDD indisponível.** `uv run … behave` → exit 127 (`uv` ausente); o fallback
`python3 -B -m behave` → exit 1 (`No module named behave`). **Limitação
ambiental.** O pacote não reivindicou nenhuma prova BDD a partir disso, e
`DEC-009`, `T013`, `T017` e os dois DoD exigem `deco_*.feature` executados antes
do Delivery Gate — a indisponibilidade atual não vira permissão.

**Nenhuma condição bloqueante do Plan Gate decorre dessas falhas.** Nenhuma é do
plano; todas estão registradas, atribuídas e — com a exceção de `N-01` —
cobertas por tarefa antes do Delivery Gate. **Não declaro a regressão nem o
Delivery Gate verdes**, e o `RED` deliberado das suítes `test_deco_*.py` e
`deco_*.feature` não é evidência de nada além da vedação de implementação.

## 6. Condições restantes

### Pré-Plan Gate

1. **Nenhuma condição técnica permanece aberta.**
2. Procedimental, pertencente ao **ato** de marcar o gate: registrar a evidência
   mínima de `FR-011` — unidade, risco e justificativa, branch e HEAD,
   harness/modelo/effort/session ID do implementador **e** do revisor, escopo,
   verificações e resultado, achados, veredito, correções aplicadas e gate
   resultante —, com todo valor não observado exatamente como `NÃO REGISTRADO`.
3. O fechamento exige **instância distinta** de quem escreveu e de quem corrigiu.
   Nem o autor do plano nem eu podemos marcá-lo: cabe a Deco.

### Execução

4. `T004` materializa o Git Guardian antes de qualquer branch no consumidor
   (`T111` `EXECUTE` já condiciona a criação da branch a isso).
5. `T013` implementa o contrato de regressão da raiz e prova os três negativos —
   ausência, exclusão e não execução.
6. `T110` revalida instalação, idempotência, conflito, rollback e runtime offline
   **após** a integração da ponte; o GREEN de `T015` não substitui.
7. `T114` mantém o piloto aberto pelos dois limiares e mede `M-1` a `M-7`.
8. Prover `uv`/`behave` no ambiente de execução, ou declarar formalmente o
   substituto, antes de reivindicar BDD.

### Pré-Delivery Gate

9. **`N-01`** — atribuir dono à falha de logo de `deco/README.md`, ou registrar
   exceção explícita aprovada por quem orquestra. Sem isso, o item de DoD
   "verificações e checks estáticos disponíveis passam" não fecha.
10. **`N-02`** — ao executar `T013`, cobrir explicitamente o placeholder de
    `deco/templates/HANDOFF.md`, além das fixtures negativas.
11. Regressão da raiz verde, com presença, descoberta e execução comprovadas de
    todas as suítes da camada, sem falha mascarada.
12. Revisão independente do Delivery Gate, por instância distinta, com Contrato
    de Entrega e evidência completa.

## 7. Recomendação objetiva para a decisão humana

**Recomendo aprovar o Plan Gate.**

A rodada de correção tratou os achados na raiz, não na superfície. Os dois `P0`
eram os que importavam, e ambos foram fechados por desenho verificável: o runner
virou decisão registrada (`DEC-009`) com contrato de regressão e três provas
negativas que tornam o falso verde impossível de passar despercebido; e o
protocolo do piloto foi restaurado por inteiro — cinco consultas, sete dias, o
que ocorrer depois, com `M-1` a `M-7` intactas e um item de DoD novo que impede
a atualização de cockpit de substituir a medição. Nenhuma redução de requisito
sobreviveu à busca.

Os quatro `P1` foram resolvidos com rigor acima do pedido: a tabela é hoje
projeção mecanicamente verificável das 32 tarefas normativas em quatro colunas; o
grafo tem 65 arestas normativas e 7 cruzadas declaradas, sem uma única espúria e
sem ciclos; `docs/sessoes/` saiu da raiz e a regressão caiu de 8 para 6 falhas; e
os cortes ficaram disjuntos nos três documentos. A separação de propriedade dos
arquivos do piloto, que eu havia registrado apenas como risco residual, foi
resolvida sem ter sido pedida.

O que resta não é do plano. Das 6 falhas e 3 erros, **nenhuma é do pacote**:
sete são do ambiente e do fork, duas são preexistentes do módulo `deco/`. Só uma
— o logo de `deco/README.md` — carece de dono, e é item de Delivery Gate, não de
Plan Gate; pode ser atribuída no ato do fechamento sem reabrir rodada.

Aprovar aqui significa autorizar a execução, não declarar entrega. O Plan Gate
deve permanecer `Pending` até sua manifestação explícita, e é você quem a
registra — nem o autor do plano nem eu podemos fazê-lo.

## 8. Declaração de nenhuma alteração no repositório

> Durante esta reconferência **nenhum arquivo local foi editado, movido ou
> removido**. Não houve `add`, `commit`, `push`, `fetch`, `pull`, `switch`,
> `stash`, `reset` nem `clean`. Nenhum remote foi alterado. **Nenhum gate foi
> marcado.** Nenhuma spec, plano, tarefa ou código foi tocado. O
> `review-verdict.md` original foi lido e **preservado integralmente**, sem
> sobrescrita. Nenhum mecanismo foi implementado, nenhum subagente foi acionado,
> nenhuma página do Notion foi criada ou modificada, o repositório do Tempus Mind
> Map não foi aberto e nenhum defeito foi corrigido silenciosamente.
>
> Todas as validações foram somente leitura. O único artefato produzido foi esta
> página.
>
> **Estado final, idêntico ao inicial:** branch `deco/v0.2` · HEAD
> `2ff940a3885c020db8b019c23c91fc7c82e45037` · divergência `0 0` · stage vazio ·
> `M deco/specs/0001-ponte-notion-repositorio/spec.md` ·
> `M deco/specs/0002-governanca-sdd/spec.md` ·
> `?? deco/specs/0002-governanca-sdd/reviews/` · zero commit novo, sem push.
