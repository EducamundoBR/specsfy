# Correction Report — Plan Gate consolidado SPEC-0001 + SPEC-0002

**Rodada:** 21/09/2026, após [Review Verdict](review-verdict.md) independente.
**Decisão humana:** `python3 -B -m unittest` é o runner TDD canônico da v0.2;
o protocolo do piloto **não** foi reduzido.
**Estado:** PRONTO PARA RECONFERÊNCIA; ambas as specs permanecem `Defined`,
Definition `Passed`, Plan `Pending`, Delivery `Pending`.
**Autoria desta correção:** Codex; modelo, effort efetivo e session ID:
`NÃO REGISTRADO`. **Revisor e aprovador desta rodada:** `NÃO REGISTRADO`.
Este relatório não é Review Verdict nem aprovação de gate.

## Identidade e escopo

Preflight manual anterior à escrita: raiz
`/Users/decoribeyro/DESENVOLVIMENTO/PROJETOS ATIVOS/14-SpecsFy-Deco`;
branch `deco/v0.2`; HEAD local e `origin/deco/v0.2`
`2ff940a3885c020db8b019c23c91fc7c82e45037`; divergência `0 0`;
stage vazio. Footprint conhecido: dois `spec.md` modificados, três artefatos
de revisão não rastreados e um contexto não rastreado em `docs/sessoes/`.
Classificação manual `CONDICIONAL`; o Git Guardian formal ainda não existe
e continua sendo T004 futura.

Foram alterados apenas plano/tarefas nas duas specs, Review Request,
prompt de reconferência e evidências desta rodada. O contexto foi relocado
de `docs/sessoes/contexto_sessao_atual.md` para [session-context.md](session-context.md);
o diretório vazio `docs/sessoes/` foi removido. O
`review-verdict.md` não foi alterado. Nenhum mecanismo, teste de produto
ou perfil técnico universal foi implementado. O Tempus Mind Map não foi aberto.

## Matriz achado → alteração → arquivo/linha → validação

| Achado | Alteração desta rodada | Arquivo/linha | Validação |
| --- | --- | --- | --- |
| P0-1 · runner e falso verde | DEC-009 registra `unittest`; T001–T003/T101–T103 usam `tests/test_deco_*.py` e PREP prevê `tests/features/deco_*.feature`; T013 integra descoberta/execução da camada à regressão da raiz e exige três negativas; T017 impede Delivery verde sem a suíte executada | [SPEC-0002 §8](../../spec.md), [T001–T003](../../spec.md), [T013](../../spec.md), [DEC-009](../../spec.md), [SPEC-0001 T101–T103](../../../0001-ponte-notion-repositorio/spec.md) — linhas: 0002/spec.md:1678–1692,1762,1790,1997; 0001/spec.md:1471–1485 | `validate_tasks --allow-draft`: TDD 3+3; 45/45 e 59/59 IDs. Testes negativos ainda são plano, não implementação |
| P0-2 · protocolo do piloto | T111 certifica projeto não crítico; T114 mantém cinco consultas completas ou sete dias, o que ocorrer depois; M-1 exatamente 5 e M-4/M-5 5/5; T016, T115/T017, cockpit, DoD e estimativa alinhados; removido timebox de 1–2 dias | [SPEC-0001 T111–T115](../../../0001-ponte-notion-repositorio/spec.md), [§15/DoD](../../../0001-ponte-notion-repositorio/spec.md), [SPEC-0002 T016–T017](../../spec.md), [piloto](review-request.md) — linhas: 0001/spec.md:1550–1578,1586,1766; 0002/spec.md:1783–1790; review-request.md:266 | Busca `1–2 dias` e `uma atualização` no plano atual: zero redução normativa; protocolo e metas continuam na seção 1 da SPEC-0001 |
| P1-1 · tabela divergente | Tabela reconstruída dos 32 cabeçalhos normativos; T015–T017 incluídas, T116/T117 removidas; texto, refs, deps e ownership literais | [tabela](review-request.md) — linhas: review-request.md:220–264 | Conferência mecânica: 32/32 linhas e zero fantasmas/drift |
| P1-2 · grafo/ordem | Grafo contém 32 nós/72 arestas; T015 é baseline antes da ponte; T110 revalida instalação pós-integração; T111→T016→T112 e T115→T017 são pré-condições cruzadas | [grafo](review-request.md), [SPEC-0001 T110](../../../0001-ponte-notion-repositorio/spec.md), [SPEC-0002 §15](../../spec.md) — linhas: review-request.md:94–211; 0001/spec.md:1543; 0002/spec.md:1798 | Conferência mecânica: zero arestas normativas ausentes, zero predecessores fantasmas e zero ciclos |
| P1-3 · regressão documental | Contexto movido para esta rodada, sem terceiro percurso em `docs/`; T013 assume topologia e reconciliação de `tests/test_references.py` com fixtures negativas | [contexto](session-context.md), [SPEC-0002 T013](../../spec.md) — linhas: session-context.md:1; 0002/spec.md:1762 | Os dois testes focais `test_docs_has_exactly_the_user_and_develop_trees` e `test_all_documents_are_reachable_from_portal`: 1/1 OK cada. Nunca foram classificados como ambientais |
| P1-4 · cortes | Cada tarefa tem um corte: T001–T016 e T101–T114 no mínimo; T017 e T115 no Delivery; nenhuma tarefa normativa pós-piloto. T013/T109/T114 permanecem somente no mínimo | [SPEC-0001 §15](../../../0001-ponte-notion-repositorio/spec.md), [SPEC-0002 §15](../../spec.md), [cortes/tabela](review-request.md) — linhas: 0001/spec.md:1586; 0002/spec.md:1798; review-request.md:212–264 | 32 IDs em um corte cada; arestas nunca voltam de Delivery ao mínimo |
| P2-1 · DEC-006/DoD | DoD admite terceira saída: materializar e validar Git Guardian por T004 na SPEC-0002 | [SPEC-0002 DoD](../../spec.md) — linhas: 0002/spec.md:2010–2030 | Censo literal da terceira saída; T004 ainda aberta |
| P2-2 · seis nomes | VERIFY e EVIDENCE de T109 asseveram os seis nomes exatos, equivalência 6/6 e negativas para ausência/divergência/excesso | [SPEC-0001 T109](../../../0001-ponte-notion-repositorio/spec.md) — linhas: 0001/spec.md:1536–1542 | Seis nomes conferidos contra tabela de interfaces da SPEC-0002 §10; testes futuros permanecem RED |
| P2-3 · decisão de stack | T112 possui os sete campos: tipo de produto, restrições, chassi, competência operacional, testes, deploy e custo de manutenção, em contrato local | [SPEC-0001 T112](../../../0001-ponte-notion-repositorio/spec.md) — linhas: 0001/spec.md:1557–1563 | Censo textual 7/7; sem catálogo universal |
| P3-1 · erro contado | Review Request distingue um erro com `--allow-draft` e dois no modo estrito | [validação](review-request.md) — linhas: review-request.md:348–370 | Saídas dos validadores registradas abaixo |
| P3-2 · Git Guardian ainda inexistente | `CONDICIONAL` atribuído somente a preflight manual, não ao mecanismo T004 | [identidade](review-request.md), [contexto](session-context.md) — linhas: review-request.md:13; session-context.md:1–21 | T004 aberta; nenhuma afirmação de mecanismo executado |
| P3-3 · Review state | SPEC-0001 recebeu `Review state: APROVADO`, simétrico ao fechamento humano já documentado na SPEC-0002 | [SPEC-0001 cabeçalho](../../../0001-ponte-notion-repositorio/spec.md) — linhas: 0001/spec.md:17 | Censo dos cabeçalhos: Definition `Passed`, Plan/Delivery `Pending` |
| P3-4 · traceability | Comandos exatos e saídas RED reproduzíveis registrados abaixo; não alegar verde sem testes materializados | [validação](review-request.md) — linhas: review-request.md:348–370 | SPEC-0001 22/45 IDs, 45 cadeias incompletas; SPEC-0002 25/59 IDs, 59 cadeias incompletas; exit 1 esperado |
| §8.10–12 · independência/proveniência/mudança material | Instância distinta fará reconferência; valores não observados ficam `NÃO REGISTRADO`; nenhuma decisão de escopo, risco ou Definition Gate foi alterada | [prompt](independent-review-prompt.md), este relatório — linhas: independent-review-prompt.md:1–110; correction-report.md:1–30 | Plan Gate `Pending`; nenhuma autoaprovação |

Os links de arquivo acima identificam ownership; as linhas exatas foram
recapturadas ao fim da rodada e aparecem no anexo de evidência abaixo.

## Evidência de validação

| Comando, na raiz do monorepo | Código | Resultado |
| --- | ---: | --- |
| `node skills/specsfy-05-tasks/scripts/validate_tasks.mjs deco/specs/0001-ponte-notion-repositorio/spec.md --allow-draft --json` | 1 | 15 tarefas, 3 TDD, 45/45 IDs, 90 checklists; erro único de caminho `verify_evidence.mjs` |
| Mesmo comando para `0002-governanca-sdd/spec.md` | 1 | 17 tarefas, 3 TDD, 59/59 IDs, 102 checklists; mesmo erro de caminho |
| Os mesmos validadores de tarefas sem `--allow-draft` | 1 em cada | Os erros incluem Plan Gate ainda `Pending`, como deve permanecer, além do caminho `verify_evidence.mjs` |
| `node skills/specsfy-05-tasks/scripts/validate_interface_tasks.mjs <spec>` | 0 em cada | Interface nas tarefas: OK nas duas specs |
| `node skills/specsfy-04-validate/scripts/validate_spec.mjs <spec> --allow-draft` | 1 em cada | `Marcadores não resolvidos`: falso positivo do regex upstream sobre `todo` |
| `python3 -B -m unittest tests.test_documentation_audiences.DocumentationAudienceContractTests.test_docs_has_exactly_the_user_and_develop_trees` | 0 | 1 teste OK |
| `python3 -B -m unittest tests.test_contexto_projeto.ProjectContextContractTests.test_all_documents_are_reachable_from_portal` | 0 | 1 teste OK |
| `python3 -B -m unittest discover -s tests -p 'test_*.py'` | 1 | 111 testes; 6 falhas, 3 erros; ver classificação abaixo |
| `python3 -B -m unittest tests.test_references.RepositoryReferenceTests.test_all_authored_markdown_links_and_anchors_resolve` | 1 | Somente 2 links preexistentes quebrados em fixture/template da camada; nenhum link novo do pacote |
| `uv run --quiet --with behave behave tests/features --no-capture` | 127 | `uv` ausente; BDD não executado |
| `python3 -B -m behave tests/features --no-capture` | 1 | fallback tentado; `No module named behave`; BDD não executado |
| `make verify-version` | 0 | versão única `0.22.2` |
| `node skills/specsfy-setup/scripts/monitor_context.mjs --project .` | 0 | `CURRENT`; documentação compatível com os caminhos alterados |
| `git diff --check` | 0 | sem whitespace inválido |

`check_traceability.mjs` foi executado de forma reproduzível, sem criar
testes: `node skills/specsfy-06-tdd-bdd/scripts/check_traceability.mjs
deco/specs/0001-ponte-notion-repositorio/spec.md tests --json --full-chain`
teve exit 1, 22/45 IDs e 45 cadeias incompletas; o equivalente da SPEC-0002
teve exit 1, 25/59 IDs e 59 cadeias incompletas. A raiz de testes usada foi
`tests`; os arquivos TDD/BDD previstos ainda não existem por vedação de
implementação.

**Conferência mecânica read-only:** extraí os cabeçalhos de §14 de ambas as
specs e comparei `ID`, owner, texto, `Refs` e `Depends` com cada linha da
tabela; comparei os 32 nós e 72 arestas Mermaid com os predecessores normativos,
as pré-condições cruzadas e a atribuição única de corte; uma busca em
profundidade rejeitou ciclos. Resultado: `PASS`, exit 0, 32/32 tarefas,
32/32 nós, zero divergências, zero predecessores ausentes e zero ciclos.
O procedimento é read-only e repetível contra os três arquivos do pacote.

Executar na **raiz Git**; saída esperada: `PASS exit=0 tasks=32 table=32
nodes=32 edges=72 cycles=0 missing=0 cuts=32`. Rollback: não aplicável;
somente leitura, sem arquivo temporário ou mudança de estado.

```bash
python3 -B -c '
import re
from pathlib import Path
specs = {"0002": Path("deco/specs/0002-governanca-sdd/spec.md"), "0001": Path("deco/specs/0001-ponte-notion-repositorio/spec.md")}
tasks = {}
for owner, path in specs.items():
    body = path.read_text().split("### 14. Tarefas", 1)[1].split("### 15.", 1)[0]
    for m in re.finditer(r"^- \[ \] (T\d{3}) (.*?) — Refs: (.*?) — Depends: (.*)$", body, re.M):
        tasks[m[1]] = (owner, m[2], m[3], m[4])
report = Path("deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/review-request.md").read_text()
table = report.split("## Tarefas consolidadas", 1)[1].split("## Piloto consumidor", 1)[0]
rows = [line.strip(" |").split(" | ") for line in table.splitlines() if re.match(r"^\| T\d{3} \|", line)]
assert len(rows) == len(tasks) == 32
assert len({r[0] for r in rows}) == 32
for r in rows:
    assert tasks[r[0]] == tuple(r[1:5]), r[0]
    assert r[10] == ("Delivery" if r[0] in {"T017", "T115"} else "Mínimo"), r[0]
graph = report.split("## Grafo de dependências", 1)[1].split("## Três cortes", 1)[0]
nodes = set(re.findall(r"^\s*(T\d{3})\[", graph, re.M))
edges = set(re.findall(r"^\s*(T\d{3}) --> (T\d{3})\s*$", graph, re.M))
assert nodes == set(tasks)
assert all((p, k) in edges for k, t in tasks.items() for p in re.findall(r"T\d{3}", t[3]))
cross = {("T015","T101"),("T015","T102"),("T015","T103"),("T015","T110"),("T111","T016"),("T016","T112"),("T115","T017")}
assert cross <= edges
cut = {r[0]: r[10] for r in rows}
rank = {"Mínimo": 0, "Delivery": 1, "Pós-piloto": 2}
assert all(rank[cut[a]] <= rank[cut[b]] for a, b in edges), "backward cut edge"
adj = {k: [] for k in tasks}
for a, b in edges:
    assert a in adj and b in adj
    adj[a].append(b)
seen, active = set(), set()
def visit(n):
    assert n not in active, "cycle"
    if n in seen: return
    active.add(n)
    for x in adj[n]: visit(x)
    active.remove(n)
    seen.add(n)
for n in tasks: visit(n)
print(f"PASS exit=0 tasks={len(tasks)} table={len(rows)} nodes={len(nodes)} edges={len(edges)} cycles=0 missing=0 cuts=32")
'
```

### Falha do pacote × preexistente × ambiente

- **Falhas desta rodada corrigidas:** as duas falhas de `docs/sessoes/`
  foram introduzidas pelo pacote anterior; ambas passaram após relocação.
  O diretório removido estava vazio e não continha outro dado.
- **Falhas preexistentes do repositório/módulo, não ambientais nem verdes:**
  `deco/README.md` não atende ao teste de logo; `deco/fixtures/handoff/broken-pointer/`
  e `deco/templates/HANDOFF.md` quebram `test_references.py`;
  `setup_context.mjs` não encontra `UserProfile.md` no teste de template.
  T013 assume impedir agravamento por futuras fixtures negativas, sem
  declarar essas falhas resolvidas agora.
- **Limitações do ambiente/fork:** `origin` é o fork EducamundoBR, enquanto
  testes do upstream exigem `promovaweb/specsfy`; `uv` e o módulo Python
  `behave` não existem;
  `mapfile`, `pdftohtml` e `pdftotext` não estão disponíveis neste
  ambiente. Isso não substitui regressão verde no Delivery Gate.
- **RED deliberado:** as suítes `test_deco_*.py` e
  `deco_*.feature` são arquivos previstos, não criados nesta missão.
  Sua ausência não é evidência GREEN; T013/T109/T017 exigem fechamento futuro.

## Rollback, riscos e handoff

O rollback desta rodada é documental e recuperável: restaurar os dois
`spec.md` a partir do diff sem operar Git destrutivo; preservar o parecer
independente e este relatório; se a relocação do contexto for rejeitada,
escolher em nova revisão um destino compatível com `AGENTS.md`, nunca recriar
`docs/sessoes/` na raiz sem aprovação normativa. Não se realiza rollback
automático nem se altera a baseline LionCode.

Riscos residuais: runner/BDD ainda não implementados; regressão da raiz não
verde por falhas preexistentes; `uv` ausente; Git Guardian formal T004 ainda
aberto; janela do piloto futura de no mínimo sete dias; propriedade dos
arquivos do piloto agora separada por spec, mas precisa ser exercitada.

**Próximo passo único:** entregar este Correction Report, as specs corrigidas e
o Review Request atualizado a uma instância independente para novo Review
Verdict. Só após essa reconferência e decisão humana o Plan Gate poderá mudar
de `Pending`.
