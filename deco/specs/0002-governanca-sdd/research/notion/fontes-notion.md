# Evidência derivada — fontes da SPEC-0002 (governança do SDD)

Artefato **derivado e enxuto**. Não reproduz as páginas de origem: registra as
cláusulas efetivamente usadas, a natureza de cada uma, o mapeamento para os IDs
da SPEC-0002 e o registro da migração executada a partir da SPEC-0001.

## Declaração de fonte normativa

O Notion permanece a **fonte normativa** das decisões de negócio e de método
aqui citadas, conforme a peça 2 em `deco/rules/canonical.md:45-59`. Este arquivo
é a cópia derivada e autossuficiente prevista por aquela peça: existe para que a
SPEC-0002 seja legível sem MCP, sem rede e sem acesso ao workspace.

Nenhum segredo, credencial, token, dado pessoal ou conteúdo irrelevante foi
transportado para cá.

## Fontes

| # | Título | URL | Status na origem | Data da leitura |
| --- | --- | --- | --- | --- |
| F-1 | Decisão — Fluxo repo-first, dupla validação e Git Guardian | <https://app.notion.com/p/89aafb8557414ba8b2c77ef42a41bff0> | `APROVADA · 28/08/2026`, adendo de 01/09/2026 | 2026-09-16 |
| F-2 | Decisão — Fluxo SDD repo-first com ponte Notion MCP | <https://app.notion.com/p/698186dcacc94713b91d5d152c0d7f0b> | `APROVADA · 16/09/2026`, adendo de skills e repasse de 16/09/2026 | 2026-09-16 |
| F-3 | Convenção handoff × SDD — formato delta e camada agnóstica | <https://app.notion.com/p/4ff22dd2037a4f76a517b065fcdfc652> | `APROVADA · 18/08/2026` | 2026-09-16 |
| F-4 | Handoff — 16/09/2026 · Deco v0.2 | <https://app.notion.com/p/e094d66f42c14e1fbb98150d9a2d6518> | `EM ANDAMENTO · 16/09/2026` | 2026-09-16 |
| F-5 | Modelo de Contrato de Entrega — MusicFlow (Ago/26) | <https://app.notion.com/p/e9555dfab1ce43fab2a4b74110c4617f> | precedente de projeto, sem status normativo transversal | 2026-09-16 |

Todas lidas por Notion MCP em tempo de **autoria**. Nenhuma é dependência de
runtime de qualquer artefato do repositório.

Evidência da rodada, sem natureza de fonte normativa: o pacote documental atual,
a revisão independente original em
<https://app.notion.com/p/3e0c76b764a4811fbafccd88e379b016> e a reconferência
aceita em <https://app.notion.com/p/3e1c76b764a481ccaac2fe756352cc39>
demonstram a decisão operacional, a execução da separação e a resolução integral
de A-01 a A-17; F-4 registrava apenas a proposta.

## Natureza das cláusulas

As cláusulas abaixo estão separadas por natureza, porque tratá-las como
igualmente normativas seria o erro mais caro desta spec:

- **DECISÃO APROVADA** — vinculante; a SPEC-0002 a reproduz por referência.
- **PRECEDENTE** — evidência de que algo funcionou em um projeto; informa o
  desenho, não o obriga.
- **INFERÊNCIA DE ARQUITETURA** — construção desta rodada a partir das fontes;
  **ainda não aprovada** e sujeita ao Definition Gate.
- **QUESTÃO ABERTA** — não resolvida por nenhuma fonte.

## Cláusulas — decisão aprovada

#### G-01

**F-1, seção 4.3 · DECISÃO APROVADA.** Matriz de risco em quatro níveis com
validação por nível: **baixo** — testes e autocheck, segunda LLM opcional;
**médio** — outra família revisa o diff final; **alto** — outra família revisa
**antes e depois**; **crítico** — Git Guardian, segunda LLM antes e depois,
Notion quando pertinente e revisão humana especializada quando irreversível.
Exemplos de crítico: produção, pagamentos, autenticação, LGPD, migração de dados
e Git destrutivo.

#### G-02

**F-1, seção 4.4 · DECISÃO APROVADA.** Quatro proibições permanentes: modelo
novo, barato ou não validado **nunca** é aprovador final de segurança,
autoridade para Git destrutivo, responsável único por deploy ou revisor final de
pagamentos, autenticação ou dados pessoais. Pode atuar em leitura, exploração,
classificação, documentação mecânica, busca e terceira opinião não vinculante.
Promoção exige benchmark documentado e decisão explícita.

#### G-03

**F-1, seção 4.2 · DECISÃO APROVADA.** Implementador e revisor são instâncias
distintas. O revisor abre **contexto novo, inicialmente read-only**, recebe
spec, plano, diff, testes e critérios, e **não recebe a conclusão do
implementador como verdade**. Devolve achados por severidade, com evidência e
correção proposta. **"Uma aprovação sem teste, diff ou evidência não fecha
gate."**

#### G-04

**F-1, seção 3 · DECISÃO APROVADA.** Git Guardian é **papel operacional**, não
produto nem terceira IA. Opera read-only por padrão. Preflight obrigatório antes
de qualquer ação que altere arquivos, histórico, branch, remote ou ambiente.
Saída classificada em `SEGURO | CONDICIONAL | BLOQUEADO`, com operações
permitidas, operações bloqueadas, proteção necessária e próxima ação segura.
Worktree suja de origem desconhecida **bloqueia**, sem `stash`, `reset`,
`switch` ou `checkout` automáticos.

**INFERÊNCIA DECLARADA DA RODADA — dezesseis dimensões operacionais.** F-1
enumera onze itens de inspeção e quatro campos adicionais do contrato de saída.
A composição inicial soma quinze; a normalização desdobra worktrees e stashes,
agrupados na fonte, em duas inspeções (+1), chegando a dezesseis. Aprovação
humana e condutas são explicitadas dentro dessas dimensões normalizadas, não
somadas como novas citações. O número dezesseis não é literal nem herdado
diretamente da fonte.

#### G-05

**F-1, seção 6.2 e adendo 12.4 · DECISÃO APROVADA.** A materialização do Git
Guardian no repositório **não foi executada**; o adendo exige convertê-lo em
script versionado sob a regra "sem saída de script colada no relatório, não
existe veredito". Busca neste repositório em 16/09/2026 não encontrou artefato
correspondente.

#### G-06

**F-1, seções 9 e 12.4 · DECISÃO APROVADA.** Todo planejamento registra
**modelo, effort, risco e exceções**. Papéis são **lógicos** — `planner-strong`,
`implementer`, `reviewer`, `cheap-readonly` — mapeados a modelo concreto, data e
quem promoveu, para que troca de nome ou versão não invalide o processo.

#### G-07

**F-1, seção 10 · DECISÃO APROVADA.** Validação por IA **não equivale** a
revisão humana experiente. Mudanças críticas e irreversíveis preveem revisão
humana especializada quando disponível.

#### G-08

**F-1, seção 5 e F-2, adendo · DECISÃO APROVADA.** O Notion entra como segunda
opinião em seis condições: falta de compreensão segura por quem orquestra;
discordância material entre famílias; ausência de regra de negócio ou contexto
histórico no repositório; mudança de experiência de cliente, política, processo
ou promessa comercial; risco alto ou crítico; decisão de modelo, effort ou
abordagem fora da matriz. **Não** participa quando a tarefa é de baixo risco, o
SDD está completo, o preflight liberou o estado e as evidências bastam.

#### G-09

**F-1, seção 5.1 · DECISÃO APROVADA.** A **unidade preferencial de revisão** é
um Draft PR ou commit contendo spec, plano, diff e testes; na sua ausência, um
pacote compacto. A unidade é sempre um **pacote**, nunca um turno isolado de
conversa.

#### G-10

**F-2, adendo · DECISÃO APROVADA.** Cinco skills mínimas: `review-router`
(classifica gate, risco e perfis), `review-definition`, `review-plan`,
`review-delivery`, `review-handoff`. Quatro perfis de risco complementam as
skills de gate **sem multiplicar skills completas**:
`security-auth-privacy` — segurança/autenticação/privacidade; `data-migration` —
dados/migração; `git-deploy` — Git/deploy; `business-customer` —
negócio/experiência do cliente. O roteador **compõe** gate mais perfis. Os slugs
são identificadores lógicos; caminhos físicos ficam para o Plan Gate.

#### G-11

**F-2, adendo · DECISÃO APROVADA.** Contrato de repasse: o implementador **não
cola histórico de conversa**; grava um **Review Request** em formato delta com
unidade, risco e justificativa, branch/HEAD, base e escopo do diff, arquivos,
testes, decisões, dúvidas, fontes, restrições e harness/modelo/effort/session ID.
O identificador lógico `CURRENT` indica a rodada ativa. O revisor abre contexto novo e grava um
**Review Verdict** separado com identidade, evidências, achados `P0`–`P3`,
veredito, condições e gate resultante. Havendo correções, o implementador grava
um **Correction Report** na mesma rodada e o revisor reconfere **uma vez**.
Mudança material de escopo abre **nova rodada**.

#### G-12

**F-2, adendo · DECISÃO APROVADA.** Estados lógicos da revisão:
`RASCUNHO → PRONTO PARA REVISÃO → EM REVISÃO → CORREÇÕES SOLICITADAS → PRONTO
PARA RECONFERÊNCIA → APROVADO | REPROVADO`. **Exatamente uma rodada ativa.**
Rodadas imutáveis. Caminhos físicos e validação executável ficam para o Plan
Gate.

#### G-13

**F-3, decisão 1 e 2 · DECISÃO APROVADA.** O handoff é obrigatório no
fechamento de sessão, em **formato delta**: só o que a sessão mudou, decisões
**com o porquê**, estado, pendências, próximos passos e evidências. Contexto
estável é linkado, nunca duplicado. **Regra dos 30 segundos.** É o artefato de
validação de quem orquestra, que não lê diff.

#### G-14

**F-3, decisão 3 · DECISÃO APROVADA.** **Um handoff ativo por projeto.** Ao
gravar o novo, o anterior recebe `SUPERADO` e um ponteiro "substituído por". A
abertura lê **apenas o mais recente**; os antigos são rastreabilidade e nunca
são lidos em sequência.

#### G-15

**F-3, contexto e decisão 4 · DECISÃO APROVADA.** Nada sobrevive dentro da LLM
entre sessões: `resume` relê **transcript bruto** e traz becos sem saída e
decisões superadas; `compact` é **compressão com perda** escolhida pela máquina.
A memória entre sessões **sempre** vem de arquivo — a escolha é **quem cura**.
`resume` e `compact` só como atalho intra-tarefa, mesmo dia e mesmo assunto; a
partir da terceira compactação, abrir sessão nova com handoff estruturado rende
mais.

#### G-16

**F-3, decisão 5 · DECISÃO APROVADA.** O handoff é **contrato agnóstico de
harness**: Markdown com cinco campos fixos — projeto e data; estado verificável
(branch, HEAD, o que está no ar, o que não subiu); decisões da sessão + porquê;
pendências e próximo passo; evidências e links canônicos. Um arquivo ativo por
projeto, histórico em subpasta, espelho canônico no Notion e **um único ponto de
acoplamento** com o harness.

#### G-17

**F-3, consequências · DECISÃO APROVADA.** O modo de falha conhecido de um
handoff ruim é registrar **o que** foi decidido sem o **porquê**, fazendo a
sessão seguinte reabrir o que já estava fechado. O porquê é campo obrigatório.

## Cláusulas — precedente

#### G-18

**F-5, "Como funciona um contrato" · PRECEDENTE.** Sete campos obrigatórios, sem
os quais o contrato não dispara: objetivo de uso na voz de quem pede; escopo
incluído (lista fechada); escopo excluído; critérios de aceite verificáveis;
fronteira de autonomia com condições de parada obrigatória; rollback com branch,
commit-base e comando exato; entregável de prova com relatório e evidência.
Na versão anterior da SPEC-0002, **dois desses sete campos gerais estavam
ausentes** do contrato transversal: objetivo de uso e critérios de aceite. A C1
os restitui sem importar regras específicas do domínio MusicFlow.

#### G-19

**F-5, diagnóstico · PRECEDENTE — o achado que justifica os três estados.** Numa
única sessão, **três funcionalidades existiam no código, passavam em teste e não
eram alcançáveis** por quem ia usá-las. O diagnóstico da origem: *"ausência de
critério de aceite sobre alcançabilidade"*. É a prova empírica de que "pronto"
não implica "entregue".

#### G-20

**F-5, entrega do Contrato 01 · PRECEDENTE.** Contrato fechou **12/12 critérios
verdes por automação** e ainda assim registrou pendência explícita: *"verde
automático não garante experiência de uso"*, aguardando validação humana. É a
prova empírica de que "entregue" não implica "aceito".

#### G-21

**F-5, regras permanentes · PRECEDENTE, generalizável.** Quatro regras
transversais, lidas fora do vocabulário de UI da origem: **nome único** — um
recurso, um nome, igual em código, interface e documentação; **sem entregável
inerte** — o que não funciona fica oculto ou explicitamente marcado, nunca
disponível sem efeito; **estado vazio honesto** — nunca mock, nunca dado falso;
**verde antes de voltar** — verificação disponível passando, e falha reportada,
nunca escondida.

#### G-22

**F-5, fronteira de autonomia · PRECEDENTE, generalizável.** Condições de parada
obrigatória: operação que publica ou altera histórico compartilhado; alteração
de schema, migração, política de acesso, segredo ou autenticação; escrita
destrutiva sem backup; **três falhas no mesmo critério**; conclusão de que um
critério exige decisão de produto ou de negócio.

#### G-23

**F-5, rollback do Contrato 02 · PRECEDENTE.** O rollback declarado nomeia
branch, commit-base e comando exato, e registra o backup com caminho, tamanho e
hash verificado. A origem também registra uma armadilha operacional real: um
backup aparentemente criado, porém **vazio**, detectado pelo hash de arquivo
vazio. Generalização: rollback só conta como declarado quando a sua própria
integridade foi verificada.

## Cláusulas — inferência de arquitetura

#### G-24

**INFERÊNCIA DE ARQUITETURA — Session Guardian.** O termo **"Session Guardian"
aparece nominalmente apenas em F-4** (handoff de 16/09/2026), como item a
especificar, **sem definição normativa em nenhuma fonte aprovada**. Sua
definição foi **delimitada nesta rodada** por analogia estrutural com o Git
Guardian (`G-04`) e, sobretudo, pelo conteúdo **já aprovado** da convenção de
handoff (`G-13` a `G-17`): as responsabilidades atribuídas a ele são as
verificações que a convenção já exige — um ativo por projeto, ponteiro
consistente, cinco campos, anterior marcado como superado sem reescrita,
transcript não sendo fonte canônica, estado verificável declarado. Nada foi
inventado além da atribuição dessas verificações a um papel nomeado.
**Pendente de aprovação no Definition Gate.**

#### G-25

**INFERÊNCIA DE ARQUITETURA — Contrato de Entrega transversal.** F-5 é contrato
**de um projeto**, com regras de interface, música, cliques, banco e ferramenta
de teste específicos. A generalização para contrato transversal do SDD — treze
campos, três estados principais, exceções mínimas e vocabulário neutro de
artefato/destino — é construção
desta rodada. **Nenhuma regra específica de UI, música, cliques, banco ou
ferramenta de teste da origem foi importada.** Pendente de aprovação.

#### G-26

**INFERÊNCIA DE ARQUITETURA — vocabulário prefixado.** F-1 define
`SEGURO | CONDICIONAL | BLOQUEADO` para o Git Guardian (`G-04`). A SPEC-0002
prefixa os vereditos de cada verificador — `GG-*` e `SG-*` — para que dois
controles distintos não compartilhem rótulo. Construção desta rodada, sem
respaldo direto em fonte aprovada.

#### G-27

**DECISÃO DA RODADA DOCUMENTAL — separação em duas specs.** F-4 propôs decidir e
executar documentalmente a separação; não registrou aprovação anterior. A
decisão foi tomada e a migração executada nesta sessão de continuação, como
demonstram o pacote atual e a revisão independente. A SPEC-0002 passou a ser a
fonte normativa da governança, enquanto a SPEC-0001 preserva as interfaces da
ponte. Ambas estão `Defined`, com Definition Gate `Passed` e Plan Gate e Delivery
Gate `Pending`; nenhuma implementação foi executada.

## Questões ainda abertas

#### G-28

**QUESTÃO ABERTA — dono do Git Guardian.** `G-05` obriga a localizar a fonte
canônica versionada ou abrir spec própria antes do Plan Gate, mas **nenhuma
fonte define quem faz isso nem em que prazo**. A SPEC-0002 registra a
dependência; não a resolve.

#### G-29

**QUESTÃO ABERTA — aprovador quando não há segunda instância.** `G-03` e `G-07`
exigem revisor distinto e revisão humana em irreversível, mas nenhuma fonte
define o procedimento quando nenhum dos dois está disponível. A SPEC-0002 exige
bloqueio explícito; se isso é sustentável na prática é matéria do piloto.

## Inferências complementares — C1.1

#### G-30

**INFERÊNCIA DECLARADA C1.1 — material × não material.** `G-11` e `G-12` fazem a
mudança material abrir nova rodada, mas nenhuma fonte define o limiar. A
SPEC-0002 adota: **material** altera decisão, escopo incluído ou excluído ou
classe de risco e sempre abre nova rodada; **não material** corrige metadado,
proveniência ou evidência sem alterar esses três elementos e pode receber
correção reversível. A distinção deve ser validada no piloto.

#### G-31

**INFERÊNCIA DECLARADA C1.1 — namespaces de ponteiro.** `CURRENT` identifica
logicamente a rodada ativa de revisão e é validado por `review-handoff`;
`SESSION_CURRENT` identifica logicamente o contexto/handoff ativo e é validado
pelo Session Guardian. Nomes físicos e caminhos permanecem para o Plan Gate.

#### G-32

**INFERÊNCIA DECLARADA C1.1 — domínio provisório e condicional.** Inspeção
manual usa somente `PROVISORIAMENTE SEGURO`, `PROVISORIAMENTE CONDICIONAL` e
`PROVISORIAMENTE BLOQUEADO`; nunca emite `GG-*`. `GG-CONDICIONAL` exige origem
conhecida, proteção reversível verificável e repetição do preflight, sem
contradição ou origem desconhecida.

#### G-33

**INFERÊNCIA DECLARADA C1.1 — saídas dos estados excepcionais de entrega.**
`CORREÇÃO NECESSÁRIA` retorna a `PRONTO` após correção, verificações verdes e
nova evidência; `ENTREGUE COM CORREÇÕES` volta à origem e exige nova entrega;
`ACEITE REVOGADO` reabre como `CORREÇÃO NECESSÁRIA`. Não há atalho direto para
`ACEITO`. A máquina mínima deve ser validada no piloto.

## Mapeamento cláusula → IDs da SPEC-0002

| Cláusula | PR | FR / NFR | AC | DEC | RISK |
| --- | --- | --- | --- | --- | --- |
| G-01 | PR-001 | FR-001, FR-002 | AC-001, AC-002, AC-003, AC-035 | — | RISK-008 |
| G-02 | PR-003 | FR-002 | AC-006 | — | — |
| G-03 | PR-003 | FR-003 | AC-008, AC-009, AC-010 | DEC-002 | RISK-007 |
| G-04 | PR-004 | FR-004 | AC-011, AC-012, AC-013, AC-038 | DEC-006 | — |
| G-05 | PR-004 | FR-004 | AC-011, AC-012, AC-038 | DEC-006 | RISK-012 |
| G-06 | PR-006, PR-008 | FR-002, FR-011, NFR-002 | AC-007, AC-036 | — | — |
| G-07 | — | FR-012 | AC-033 | — | — |
| G-08 | — | FR-012 | AC-032 | — | — |
| G-09 | PR-002 | FR-006, FR-007 | AC-020 | DEC-002 | RISK-006 |
| G-10 | — | FR-006 | AC-004, AC-005 | DEC-003 | RISK-002 |
| G-11 | PR-005 | FR-007, FR-011 | AC-021, AC-022, AC-023, AC-035, AC-036, AC-037 | DEC-004 | RISK-004, RISK-006 |
| G-12 | — | FR-008 | AC-016, AC-024, AC-025, AC-026, AC-037 | DEC-004 | RISK-003, RISK-005 |
| G-13 | PR-005 | FR-005 | AC-017 | DEC-005 | — |
| G-14 | — | FR-005 | AC-014, AC-017 | DEC-005 | RISK-003 |
| G-15 | PR-005 | FR-005, NFR-004 | AC-015 | DEC-005 | — |
| G-16 | PR-008 | FR-005, NFR-004 | AC-017, AC-019 | DEC-005 | — |
| G-17 | — | FR-005, FR-011 | AC-018 | — | — |
| G-18 | — | FR-009 | AC-027 | DEC-007 | — |
| G-19 | — | FR-010 | AC-028, AC-030 | DEC-007 | RISK-009 |
| G-20 | — | FR-010 | AC-029, AC-030 | DEC-007 | RISK-009 |
| G-21 | — | FR-009, FR-011 | AC-030, AC-031 | DEC-008 | — |
| G-22 | PR-003 | FR-012 | AC-033 | DEC-008 | — |
| G-23 | — | FR-011 | AC-031 | DEC-008 | — |
| G-24 | PR-005 | FR-005 | AC-014 a AC-019 | DEC-005 | RISK-010 |
| G-25 | — | FR-009, FR-010 | AC-027 a AC-031 | DEC-007, DEC-008 | — |
| G-26 | — | FR-004, FR-005 | AC-012, AC-013, AC-019, AC-038 | DEC-005, DEC-006 | RISK-010 |
| G-27 | — | — | — | DEC-001 | RISK-001 |
| G-28 | — | FR-004 | — | DEC-006 | RISK-012 |
| G-29 | — | FR-003 | AC-008 | — | RISK-011 |
| G-30 | — | FR-005, FR-008 | AC-016, AC-026 | DEC-004, DEC-005 | RISK-005, RISK-011 |
| G-31 | — | FR-005, FR-007, FR-008 | AC-014, AC-016, AC-017, AC-024, AC-026 | DEC-004, DEC-005 | RISK-003 |
| G-32 | PR-004 | FR-004 | AC-011, AC-012, AC-013, AC-038 | DEC-006 | RISK-012 |
| G-33 | — | FR-010 | AC-028, AC-029, AC-030 | DEC-007 | RISK-009 |

## Registro da migração executada SPEC-0001 → SPEC-0002

Tratamentos: `SAI` (obrigação transversal removida da SPEC-0001) ·
`PERMANECE` (obrigação local da ponte) · `INTERFACE` (permanece local e é
consumida semanticamente) · `DESDOBRADO` · `ADAPTADO` · `NOVO`.

**Migração executada nesta rodada documental.** As linhas preservam o histórico
dos IDs de origem, seus destinos, o tratamento e a evidência de fronteira. A
recomposição ocorreu antes da remoção; a governança transversal saiu da
SPEC-0001 e a parte local sobreposta permaneceu ou foi recomposta.

### Requisitos, princípios, decisões e riscos

| Origem na SPEC-0001 | Destino/conduta | Tratamento | Evidência de fronteira |
| --- | --- | --- | --- |
| FR-011 — roteamento por risco e gate | FR-001, FR-002, FR-003 e FR-008 da SPEC-0002 | `SAI` / `DESDOBRADO` | obrigação transversal |
| FR-012 — skills e repasse | FR-006, FR-007 e FR-008 da SPEC-0002 | `SAI` / `DESDOBRADO` | obrigação transversal |
| FR-013 — Git Guardian | FR-004 da SPEC-0002 | `SAI` / `ADAPTADO` | obrigação transversal removida; parte sobre escrita MCP permaneceu na ponte por interfaces próprias |
| FR-008 — executor e aprovador | permanece na SPEC-0001 e é consumido pela separação transversal | `INTERFACE` | a Consulta SDD ainda exige obrigação local de aprovador distinto |
| PR-008 — texto do Notion não autoriza irreversibilidade | permanece na SPEC-0001; princípio transversal correspondente está na SPEC-0002 | `INTERFACE` | limite específico da fonte Notion não pode desaparecer |
| PR-009 — Git Guardian precede escrita MCP | parte transversal saiu; precedência da escrita externa permaneceu local | `INTERFACE` | obrigação da ponte preservada |
| DEC-008 — política vira requisito | DEC-002 da SPEC-0002 | `SAI` | decisão transversal |
| DEC-009 — Git Guardian como dependência | DEC-006 da SPEC-0002 | `SAI` | dependência transversal |
| DEC-010 — skills, perfis, repasse e caminhos | DEC-003 e DEC-004 da SPEC-0002 | `SAI` / `DESDOBRADO` | caminhos continuam decisão do Plan Gate |
| RISK-010 — explosão de skills | RISK-002 da SPEC-0002 | `SAI` | risco transversal |
| RISK-011 — `CURRENT` ambíguo | RISK-003 da SPEC-0002 | `SAI` | risco da rodada de revisão; não é `SESSION_CURRENT` |
| RISK-012 — branch/HEAD divergente | RISK-004 da SPEC-0002 | `SAI` | objeto correto é o Review Request, não o Session Guardian |
| RISK-013 — rodada reescrita | RISK-005 da SPEC-0002 | `SAI` | risco transversal |
| RISK-014 — pacote excessivo | RISK-006 da SPEC-0002 | `SAI` | risco transversal |
| RISK-015 — ancoragem do revisor | RISK-007 da SPEC-0002 | `SAI` | risco transversal |

### Cenários — uma linha por AC

| AC da SPEC-0001 | Sucessor/conduta | Sobreposição e obrigação local |
| --- | --- | --- |
| AC-022 — Git Guardian precede operação | AC-011 da SPEC-0002 | permaneceu na SPEC-0001 para escrita MCP; a referência transversal a FR-013 foi removida |
| AC-026 — baixo risco | AC-002 | sem obrigação local adicional |
| AC-027 — revisão consolidada | AC-020 | sem obrigação local adicional |
| AC-028 — plano antes da escrita | AC-035 | também cobria Git Guardian; a duplicação foi retirada após a recomposição das ancoragens locais |
| AC-029 — resultado após escrita | AC-035 | também cobre separação local de executor/aprovador |
| AC-030 — dois gates humanos | FR-002 e AC-033 | gate local de escrita externa preservado |
| AC-031 — segurança eleva risco | AC-003 | sem obrigação local adicional |
| AC-032 — correções em lote | AC-023 | sem obrigação local adicional |
| AC-033 — mudança material | AC-026 | também cobria conflito material da ponte; parte local preservada |
| AC-034 — identidades coincidentes | AC-008 | ancoragem explícita do aprovador distinto recomposta antes da remoção |
| AC-035 — parecer sem proveniência | AC-036 | também cobria proveniência local; interface sem inferência mantida |
| AC-036 — modelo não validado | AC-006 | sem obrigação local adicional |
| AC-037 — router escolhe skill | AC-004 | sem obrigação local adicional |
| AC-038 — gate mais perfil | AC-005 | sem obrigação local adicional |
| AC-039 — Review Request consolidado | AC-021 | sem obrigação local adicional |
| AC-040 — rodada por `CURRENT` | AC-024 | ponteiro lógico de revisão, não contexto de sessão |
| AC-041 — `CURRENT` ambíguo | AC-024 | fixture executável ainda futura |
| AC-042 — branch/HEAD divergente | AC-037 | sobrepõe precedência e Git Guardian; sucessor ancora o Review Request |
| AC-043 — revisor igual ao implementador | AC-008 | obrigação local da Consulta SDD preservada por interface |
| AC-044 — Verdict sem proveniência | AC-022 e AC-036 | sobrepõe repasse e proveniência |
| AC-045 — correções na mesma rodada | AC-023 | sem obrigação local adicional |
| AC-046 — mudança material abre rodada | AC-026 | sem obrigação local adicional |
| AC-047 — rodada imutável | AC-025 | sem obrigação local adicional |
| AC-048 — revisão verde sem Consulta SDD | AC-032 | permanece interface com os gatilhos locais da Consulta SDD |
| AC-049 — requests de plano e resultado | AC-035 | sucessor distingue artefatos e instantes |
| AC-050 — perfil não substitui skill | AC-005 | sem obrigação local adicional |

### Cláusulas C-17 a C-29

| Cláusula da SPEC-0001 | Destino auditável | Tratamento executado |
| --- | --- | --- |
| C-17 — contrato do Git Guardian | FR-004; AC-011, AC-012, AC-013 e AC-038 | saiu como norma transversal; escrita MCP manteve interface local |
| C-18 — mecanismo não materializado | FR-004; AC-011, AC-012 e AC-038; DEC-006 | saiu após a dependência ser ancorada |
| C-19 — revisão independente | FR-003 e FR-011; AC-009, AC-010, AC-036 e AC-037 | interface local permaneceu obrigatória |
| C-20 — matriz de risco | FR-001 e FR-002; AC-001, AC-002, AC-003 e AC-035 | duplicação transversal removida |
| C-21 — papéis vedados | FR-002; AC-006 e AC-007 | duplicação transversal removida |
| C-22 — escalonamento externo | FR-012; AC-032 a AC-034 | Consulta SDD permanece local |
| C-23 — pacote de revisão | FR-007 e FR-011; AC-020, AC-021, AC-022, AC-023, AC-035, AC-036 e AC-037 | contrato transversal removido da ponte |
| C-24 — modelo/effort/risco | FR-002 e FR-011; AC-007 e AC-036 | proveniência local permaneceu por interface |
| C-25 — revisão humana | FR-002 e FR-012; AC-006 e AC-033 | gates locais permanecem quando aplicáveis |
| C-26 — cinco skills | FR-006; AC-004 e AC-005 | duplicação transversal removida |
| C-27 — quatro perfis | FR-006; AC-005 | duplicação transversal removida |
| C-28 — Request/Verdict/Correction Report | FR-007, FR-008 e FR-011; AC-020 a AC-026 e AC-035 a AC-037 | pacote transversal removido da ponte |
| C-29 — estados, `CURRENT` e rodada | FR-008; AC-016, AC-024, AC-025, AC-026 e AC-037 | `CURRENT` é da revisão; `SESSION_CURRENT` deriva de G-31; caminhos físicos ficam no Plan Gate |

### Interfaces que permanecem obrigatoriamente na SPEC-0001

| Contrato semântico | Motivo |
| --- | --- |
| Cockpit do projeto | superfície da ponte para marcos, gate e executor/aprovador |
| Consulta SDD | canal de escalonamento e obrigação local de aprovador distinto |
| Relatório Modo B | parecer externo da ponte |
| Limite de interação | regra local de não inferir identidade, estado ou proveniência |
| Precedência e reconciliação entre repositório e Notion | resolução de conflito entre as duas fontes |
| Permissões MCP e vedações | segurança específica da integração externa |

### Contagens e cobertura executadas

| Momento | FR | PR | NFR | AC | Blocos `Scenario` | Resultado |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Baseline anterior à recomposição | 13 | 9 | 4 | 50 | 57 | todos os FR tinham ao menos três ACs |
| Fase 1 — recomposição executada | 13 | 9 | 4 | 53 | 60 | criados AC-051, AC-052 e AC-053 |
| Fase 2 — migração executada | 10 | 9 | 4 | 28 | 35 | removidos FR-011 a FR-013 e AC-026 a AC-050; AC-022 permaneceu local |
| Fase 3 — README e manifesto atualizados | 10 | 9 | 4 | 28 | 35 | sem mudança normativa adicional |

AC-052 recompôs o aprovador distinto e AC-053 recompôs a precedência. O terceiro
cenário, AC-051, foi necessário para preservar margem de cobertura das interfaces
de cockpit e Modo B, em vez de deixar requisitos remanescentes dependentes do
limite mínimo. A projeção histórica de dois ACs e resultado 27/34 foi superada
pelo executado 28/35.

### Referências verificadas após a migração coordenada

- Na SPEC-0001: metadados e métricas; escopo e atores; requisitos e princípios;
  AC-022 e AC-026 a AC-050; artefatos previstos; entidades e transições;
  interfaces; RED-GREEN; matriz de rastreabilidade; gates; ordem de execução;
  dependências, riscos, decisões e Definition of Done.
- No research da SPEC-0001: o mapa cláusula → IDs, especialmente C-17 a C-29.
- Em `deco/README.md`: a seção “Sobre `deco/specs/`” reflete a fronteira final e
  o hash documental correspondente foi atualizado no manifesto.
- `deco/manifest.json` **não inclui `deco/specs/` no escopo de arquivos**; nenhum
  path de spec é instalado; somente o hash do README muda quando essa
  documentação muda.

### Fases documentais executadas nesta rodada

1. Cobertura e ancoragens da SPEC-0001 recompostas, incluindo aprovador distinto
   na Consulta SDD.
2. Duplicação transversal removida depois da validação da recomposição.
3. `deco/README.md` e o hash correspondente no manifesto atualizados.

As duas specs continuam `Draft`, todos os gates permanecem `Pending` e nenhum
mecanismo foi implementado.

### Conteúdo novo na SPEC-0002

| Conteúdo | Destino | Evidência |
| --- | --- | --- |
| Session Guardian | FR-005 | não existe na SPEC-0001; delimitado por G-24 |
| Contrato de Entrega | FR-009 | não existe na SPEC-0001; deriva de G-18 a G-23 |
| Estados `PRONTO` / `ENTREGUE` / `ACEITO` | FR-010 | não existem como máquina de entrega na SPEC-0001 |

## Itens deliberadamente não importados

| Item da origem | Motivo |
| --- | --- |
| F-5, regras de UI: caminho de cliques, ≤ 2 cliques, botão morto na tela, layout v1/v2 | Específicas de interface gráfica de um app; a governança é agnóstica de superfície. `G-21` importa apenas o princípio generalizado. |
| F-5, tudo sobre música: cifra, acorde, karaoke, trilhas, tom, andamento, stems | Domínio do projeto de origem; sem valor transversal. |
| F-5, ferramentas concretas: Playwright, Supabase, `tsc`, Vite, `pg_dump`, RLS | Escolha de stack de um projeto; a governança não fixa ferramenta. |
| F-5, fila de contratos 00 a 06 e seus históricos de entrega | Backlog de produto alheio. |
| F-1, seção 8 (OpenRouter e modelos adicionais) | Política de fornecedor, fora do escopo. |
| F-1, seção 12.1 e 12.2 (achado do preflight em outro piloto) | Estado de outro repositório; importado só o que prova `G-05`. |
| F-1, nomes concretos de modelo por papel | `G-06` importa o mapeamento **lógico**; fixar modelo concreto contrariaria a proibição de inferir valores não observados. |
| F-3, tabelas de consonância e histórico de pendências de 2026 | Governança do workspace Notion, não desta fatia. |
| F-4, seção 2 (estado verificável) e 5 (links) | Estado operacional de sessão; a spec não depende dele. |
| As cinco fontes, na íntegra | PR-005 da SPEC-0001 e a peça 2 exigem referência, não duplicação. |

## Observação sobre autoria versus runtime

A leitura das cinco páginas ocorreu por MCP em **tempo de autoria**. Nada neste
arquivo, na SPEC-0002 ou em qualquer artefato do repositório exige o MCP
conectado para ser lido ou executado. A governança especificada aqui funciona
integralmente sem Notion e sem rede, conforme NFR-005.

Proveniência da SPEC-0002, registrada sem inferência:

| Papel | Identidade | Effort solicitado | Effort efetivo observado | Session ID | Data |
| --- | --- | --- | --- | --- | --- |
| Autoria | Codex/Sol | alto | `NÃO REGISTRADO` | `NÃO REGISTRADO` | 16/09/2026 |
| Revisão independente original | Claude Code/Opus | `NÃO REGISTRADO` | `NÃO REGISTRADO` | `NÃO REGISTRADO` | 19/09/2026 |
| Rodada de correção | Codex/Sol | `NÃO REGISTRADO` | `NÃO REGISTRADO` | `NÃO REGISTRADO` | 19/09/2026 |
| Reconferência aceita | Claude Code/Opus | `NÃO REGISTRADO` | `NÃO REGISTRADO` | `NÃO REGISTRADO` | 19/09/2026 |

Estado terminal da rodada: **APROVADO**. O fechamento de O-01 substitui o ponteiro
desatualizado da rodada de correção pelo resultado da reconferência aceita. A
aprovação dos Definition Gates foi decisão humana explícita de **Deco Ribeyro**,
não ato do revisor. Todo harness, effort ou session ID não observado permanece
`NÃO REGISTRADO`; configuração solicitada não prova configuração efetiva.
