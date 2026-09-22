# Ato humano de aprovação — Plan Gate integrado SPEC-0001 + SPEC-0002

| Campo FR-011 | Evidência deste fechamento |
| --- | --- |
| Unidade revisada | Plano integrado da [SPEC-0001](../../../0001-ponte-notion-repositorio/spec.md) e da [SPEC-0002](../../spec.md), rodada de 21/09/2026 |
| Risco e justificativa | Alto documental e operacional: aprovar o plano de duas specs de governança e ponte, preservando condições de execução, sem afirmar mecanismos ou testes materializados |
| Branch e HEAD de base | `deco/v0.2`; `2ff940a3885c020db8b019c23c91fc7c82e45037`; upstream `origin/deco/v0.2`, divergência `0 0`, stage vazio no preflight |
| Autor do plano | Codex; modelo exposto no Review Request: `gpt-5.6-sol`; effort efetivo e session ID: `NÃO REGISTRADO` |
| Autor da correção | Codex; modelo, effort efetivo e session ID: `NÃO REGISTRADO` |
| Executor deste registro | Codex (harness); modelo, effort efetivo e session ID: `NÃO REGISTRADO` |
| Revisor independente | Claude Code / Claude Opus 5 (`claude-opus-5`); effort solicitado/observado e session ID: `NÃO REGISTRADO` |
| Instância decisora | Deco; decisão humana explícita de 21/09/2026 |
| Separação de papéis | O autor e corretor não se autoaprovaram; o revisor independente recomendou; Deco decidiu |
| Escopo e diff | Pacote documental das duas specs, Review Request, prompt independente, Correction Report, contexto da rodada, parecer original e reconferência; neste ato, apenas estado/evidência do gate nas specs, status no roteador `deco/README.md` e este registro. Nenhum requisito, US, AC, cenário, tarefa normativa ou mecanismo foi alterado |
| Parecer original | [Review Verdict — correções solicitadas](review-verdict.md), imutável neste ato |
| Correções aplicadas | [Correction Report](correction-report.md), com matriz achado → alteração → validação; os P0/P1/P2/P3 da rodada foram reconferidos |
| Veredito independente | [Reconferência](reconference-verdict.md): `APROVADO COM CONDIÇÕES`, recomendado para decisão humana; nenhum bloqueio pré-Plan Gate remanescente |
| Decisão humana | **APROVAR O PLAN GATE COM AS CONDIÇÕES REGISTRADAS** |
| Gate resultante | SPEC-0001 e SPEC-0002: Definition `Passed`, Plan `Passed`, Delivery `Pending`, Status `Defined` |

O registro acima fecha a evidência procedimental de FR-011 para **este Plan
Gate**. “Aprovado com condições” não equivale a regressão verde, implementação,
piloto concluído nem aprovação do Delivery Gate. Valores não observados estão
marcados literalmente como `NÃO REGISTRADO`, sem inferência retroativa.

## Verificações e achados deste ato

Todos os comandos abaixo foram executados na raiz Git. O censo read-only das
fontes normativas, tabela e grafo retornou `PASS`, exit `0`: 32/32 tarefas,
32/32 nós, 72 arestas, zero predecessor ausente, zero ciclo e 32 cortes únicos.
`validate_interface_tasks.mjs` retornou `0` para cada spec. Os dois testes
documentais de topologia `test_docs_has_exactly_the_user_and_develop_trees` e
alcance `test_all_documents_are_reachable_from_portal` retornaram `0` (1/1
cada). `make verify-version` retornou `0` (`0.22.2`), e `git diff --check`
retornou `0`.

`validate_tasks.mjs --allow-draft --json` retornou `1` em ambas as specs,
sem falha de censo: SPEC-0001 tem 15 tarefas, 3 TDD, 90 itens e 45/45 IDs;
SPEC-0002 tem 17 tarefas, 3 TDD, 102 itens e 59/59 IDs. Após a marcação
`Plan Gate: Passed`, o validador passou a exigir os predecessores TDD
**concluídos** para tarefas de código: 21 erros na SPEC-0001 e 33 na
SPEC-0002. Há ainda um erro de caminho `verify_evidence.mjs` em cada uma.
Esses 54 erros de conclusão pertencem à execução futura; nenhuma tarefa foi
marcada como concluída para fabricar verde. O acoplamento de estado do
validador é registrado aqui como achado do ato, não como condição já resolvida.

`validate_spec.mjs --allow-draft` retornou `1` para cada spec pelo falso
positivo conhecido de “Marcadores não resolvidos” sobre vocabulário português.
`check_traceability.mjs ... tests --json --full-chain` retornou `1`:
22/45 IDs cobertos e 45 cadeias incompletas na SPEC-0001; 25/59 e 59 na
SPEC-0002. A regressão da raiz `python3 -B -m unittest discover -s tests -p
'test_*.py'` retornou `1`: 111 testes, 6 falhas e 3 erros. As duas falhas
documentais atribuídas ao pacote pelo parecer original estão corrigidas;
as falhas remanescentes não são declaradas verdes. `uv run --quiet --with
behave behave tests/features --no-capture` não iniciou porque `uv` está
ausente (exit `127` no shell); `python3 -B -m behave ...` retornou `1`
(`No module named behave`). Nenhuma evidência BDD foi reivindicada. A
integração Codacy MCP prevista na instrução local não está disponível nesta
sessão; nenhuma análise Codacy foi alegada.

## Condições preservadas

**Na execução:** T004 materializa Git Guardian; T013 integra os testes da
camada à regressão e prova as negativas; T110 revalida a instalação após
a ponte; T114 mantém o piloto por cinco consultas completas ou sete dias,
o que ocorrer depois, com M-1 exatamente 5 e M-4/M-5 5 de 5. Disponibilizar
`uv` e `behave` antes de reivindicar a evidência BDD correspondente.

**Antes do Delivery Gate:** atribuir dono explícito ao N-01 antes de tratá-lo;
corrigir a referência de logo em `deco/README.md`; cobrir o placeholder de
`deco/templates/HANDOFF.md`; apresentar regressão integral verde, incluindo
presença, descoberta e execução de todas as suítes da camada; obter revisão
independente do Delivery Gate. Nenhuma dessas condições está resolvida por
este ato.

**Rollback e resíduos:** uma eventual revogação exigirá nova decisão humana e
correção documental rastreável, preservando os dois pareceres e o histórico Git;
não há rollback automático ou operação destrutiva. Permanecem vedados nesta
missão implementação, piloto, Delivery Gate, PR, merge, tag, rename técnico e
ampliação de escopo. O próximo passo após a publicação deste pacote é a
execução autorizada em rodada separada, começando pelas dependências do plano.
