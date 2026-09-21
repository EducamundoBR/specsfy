# Evidência derivada — fontes Notion da SPEC-0001

Artefato **derivado e enxuto**. Não reproduz as páginas de origem: registra apenas
as cláusulas efetivamente utilizadas pela spec, o mapeamento para os IDs e o que
foi deliberadamente não importado.

## Declaração de fonte normativa

O Notion permanece a **fonte normativa** das decisões de negócio aqui citadas,
conforme a peça 2 em `deco/rules/canonical.md:45-59`. Este arquivo é a cópia
derivada e autossuficiente prevista por aquela peça: existe para que a spec e o
repositório sejam legíveis sem MCP, sem rede e sem acesso ao workspace. Em
divergência sobre **regra de negócio**, prevalece a página do Notion; em
divergência sobre **fato operacional** (branch, HEAD, diff, teste), prevalece o
estado observado no repositório.

Nenhum segredo, credencial, token, PII ou dump foi transportado para cá.

## Fontes

| # | Título | URL | Status na origem | Data da leitura |
| --- | --- | --- | --- | --- |
| F-1 | Decisão — Fluxo SDD repo-first com ponte Notion MCP | <https://app.notion.com/p/698186dcacc94713b91d5d152c0d7f0b> | `APROVADA · 16/09/2026`, com adendo de 16/09/2026 sobre skills de revisão e repasse | 2026-09-16 (recarregada após o adendo) |
| F-2 | Handoff — 16/09/2026 · Specsfy/Deco v0.1 documental commitada | <https://app.notion.com/p/d380bfc45b8c4f0db0ea64ac131e29c8> | `ATUAL · 16/09/2026, 09:50 BRT` | 2026-09-16 |
| F-3 | Decisão — Fluxo repo-first, dupla validação e Git Guardian | <https://app.notion.com/p/89aafb8557414ba8b2c77ef42a41bff0> | `APROVADA · 28/08/2026`, adendo 01/09/2026 | 2026-09-16 |

As três fontes, que sustentam as cláusulas `C-01` a `C-29`, foram lidas por
Notion MCP em tempo de **autoria**. Nenhuma delas é
dependência de runtime de qualquer artefato do repositório.

## Cláusulas utilizadas

#### C-01

**Fonte:** F-1, "Princípios" 1-2. VS Code conduz o SDD e a verdade técnica; o
Notion orienta e não intermedeia cada turno, entrando em marcos, dúvidas,
divergências e riscos relevantes.

#### C-02

**Fonte:** F-1, "Princípios" 3-4. Repositório guarda specs, planos, tarefas,
código, testes, ADRs técnicos e evidências versionáveis; o Notion guarda regras
de negócio, decisões, histórico, cockpit, pareceres e contexto transversal.

#### C-03

**Fonte:** F-1, "Princípios" 5-6. Artefatos estruturados substituem copy-paste;
cada consulta tem pergunta única, resposta, no máximo um esclarecimento e
encerramento explícito, sem conversa autônoma infinita entre IAs.

#### C-04

**Fonte:** F-1, "Princípios" 7 e "Fonte da verdade e reconciliação". Estado
técnico observado prevalece para fatos operacionais; decisão aprovada no Notion
prevalece para regra de negócio; conflito explícito bloqueia execução até
reconciliação; nenhuma IA preenche lacuna com suposição silenciosa.

#### C-05

**Fonte:** F-1, "Limite técnico do MCP". Escrever uma pergunta numa página não
dispara por si só o Notion AI. O piloto é humano-no-loop: a IDE cria a consulta,
a pessoa aciona o Notion AI, o parecer é registrado, a IDE relê o registro.

#### C-06

**Fonte:** F-1, "Cockpit do projeto no Notion". Campos mínimos, quatro estados
(`EM ANDAMENTO | AGUARDANDO DECISÃO | BLOQUEADO | CONCLUÍDO`) e seis gatilhos de
atualização. Proibido atualizar por microatividade, comando individual ou
conversa sem mudança de estado.

#### C-07

**Fonte:** F-1, "Modo A — Registro `Consulta SDD`". Identificador
`SDD-AAAAMMDD-NNN`; campos de abertura; campos de resposta; máquina de estados
`RASCUNHO → AGUARDANDO NOTION → RESPONDIDA → APLICADA | DESCARTADA`; `APLICADA`
registra onde a decisão entrou; `DESCARTADA` registra motivo e preserva o
registro.

#### C-08

**Fonte:** F-1, "Modo B — relatório da IDE revisado no Notion". Relatório factual
gravado no Notion separando **observado**, **inferido** e **ainda não
verificado**; parecer independente com fontes, riscos, premissas e recomendação;
a IDE lê apenas o parecer final e registra como foi aplicado. Sete situações
tornam o modo obrigatório: regra de negócio ausente ou ambígua; divergência
material entre famílias de modelo; risco alto ou crítico; mudança de arquitetura
ou processo; experiência ou promessa ao cliente; pagamentos, autenticação,
segurança, LGPD ou dados pessoais; recomendação técnica que a pessoa que
orquestra não compreendeu com segurança.

#### C-09

**Fonte:** F-1, "Permissões e segurança — Escopo recomendado". Leitura nas
páginas canônicas necessárias; escrita somente em cockpit, consultas e relatórios
daquele projeto; sem exclusão, movimento, alteração de permissões ou escrita em
bases alheias; confirmação humana para página normativa; registro de página
alterada, motivo e resultado; acesso proporcional ao blast radius.

#### C-10

**Fonte:** F-1, "Permissões e segurança — Vedações". Não conceder o workspace
inteiro quando uma subárvore resolve; não copiar segredos, tokens, credenciais,
PII ou dumps; **não deixar relatório técnico substituir log ou teste primário**;
**não permitir que o mesmo agente implemente e aprove sozinho**; **não usar o
Notion como canal para ordenar push, deploy ou Git destrutivo sem gate humano**;
não criar loops agente↔agente sem limite, status e encerramento.

#### C-11

**Fonte:** F-1, "Controle de custo e tempo". Notion AI acionado por dúvida, risco
ou marco, nunca por turno; uma pergunta específica com todos os fatos; uma
resposta e no máximo um esclarecimento; contexto estável linkado, não duplicado;
relatórios em formato delta; a IDE lê a resposta diretamente. Seis métricas de
piloto: consultas abertas; consultas respondidas sem esclarecimento; tempo entre
pergunta e aplicação; acionamentos do Notion AI; decisões reabertas por falta de
evidência; episódios de copy-paste evitados.

#### C-12

**Fonte:** F-1, "Baseline verificado". Fornecedor usado: Anthropic no VS Code,
com a nota "testar também com o ChatGPT" — referente ao **fornecedor do lado da
IDE**, não ao consumo do parecer. Capacidade observada na trilha de NFSe. Modelo
exato **não registrado**; proibido inferir.

#### C-13

**Fonte:** F-1, "Plano de adoção — Fase 1" e F-2, pendência 3. Piloto manual em
projeto não crítico, páginas simples antes de qualquer database, medido por
**sete dias ou cinco consultas completas, o que ocorrer depois**.

#### C-14

**Fonte:** F-1, "Limites desta aprovação" e F-2, decisão 7 e pendência 6. Não
criar agora a database `Consultas SDD`, custom agent, trigger ou worker; não
alterar o commit documental da v0.1; não automatizar escrita normativa sem piloto
e confirmação humana.

#### C-15

**Fonte:** F-2, seção 2 "Estado verificável". Branch `deco/v0.1`; HEAD
`71ee8ed350da720dfc5a58971bada7c11ae18bca`; working tree limpa; branch sem
upstream; nenhum push. Delimita a precondição desta frente.

#### C-16

**Fonte:** F-2, pendências 1 e 2. O push de `deco/v0.1` segue em gate separado e
explícito; a v0.2 abre como frente própria começando pela ponte Notion ↔ repo.

#### C-17

**Fonte:** F-3, seção 3. Git Guardian **não é produto nem terceira IA**: é papel
operacional, materializado como skill/subagente do SDD, que atua como porta de
segurança antes de qualquer ação capaz de alterar arquivos, histórico, branch,
remote ou ambiente. Por padrão opera em **somente leitura**. Preflight
obrigatório **antes de qualquer escrita**, com contrato de saída
`SEGURO | CONDICIONAL | BLOQUEADO`, operações permitidas e bloqueadas, proteção
necessária, próxima ação segura e se a aprovação humana é necessária.

#### C-18

**Fonte:** F-3, seção 6.2 e adendo 12.4, item 1. **O mecanismo executável não foi
materializado.** A seção 6.2 lista `.agents/skills/git-guardian/SKILL.md` como
materialização *prevista* e declara que ela "não foi executada nesta sessão". O
adendo corrige o estado anterior — preflight "descrito em markdown e
autorrelatado pelo agente" — para a exigência de `scripts/preflight.sh`
versionado, com a regra: **"sem saída de script colada no relatório, não existe
veredito"**. Verificado em 16/09/2026 neste repositório: nenhum artefato de Git
Guardian, preflight, model-router/roster, independent-review ou
repository-profile existe.

#### C-19

**Fonte:** F-3, seção 4.2. O revisor recebe spec, plano, diff, testes e critérios
de aceite, em **contexto novo e inicialmente read-only**, e **não recebe a
conclusão do implementador como verdade**. Devolve achados por severidade, com
evidência e correção proposta. **"Uma aprovação sem teste, diff ou evidência não
fecha gate."** Baseline: Codex implementa e Claude revisa; quando Claude
implementa, Codex revisa.

#### C-20

**Fonte:** F-3, seção 4.3 (matriz de risco) e seção 7, passos 2, 6 e 8.
Validação exigida por nível: **baixo** — testes e autocheck, segunda LLM
opcional; **médio** — outra família revisa o diff final; **alto** — outra família
revisa **antes e depois**, mais Notion se houver contexto de negócio;
**crítico** — Git Guardian, segunda LLM antes e depois, Notion quando pertinente
e revisão humana especializada quando irreversível. Exemplos de crítico:
produção, pagamentos, autenticação, LGPD, migração de dados e Git destrutivo.
Nenhuma escrita antes do preflight; quem implementou não aprova sozinho.

#### C-21

**Fonte:** F-3, seção 4.4. Um modelo novo, barato ou ainda não validado **nunca**
pode ser: aprovador final de segurança; autoridade para Git destrutivo;
responsável único por deploy; revisor final de pagamentos, autenticação ou dados
pessoais. Pode atuar em tarefas read-only, exploração, classificação,
documentação mecânica, busca e terceira opinião não vinculante. Promoção a papel
crítico exige benchmark documentado, resultado reproduzível e decisão explícita.

#### C-22

**Fonte:** F-3, seção 5. O Notion entra como segunda opinião quando: quem
orquestra não compreende a pergunta, recomendação ou consequência; as duas
famílias discordam em ponto material; falta regra de negócio ou contexto
histórico no repositório; o plano altera experiência de cliente, política,
processo ou promessa comercial; a operação é de risco alto/crítico e uma visão
externa melhora a decisão; é preciso decidir modelo, effort ou abordagem fora da
matriz codificada. **Não** precisa participar quando a tarefa é de baixo risco, o
SDD está completo, o Git Guardian liberou o estado e as evidências bastam.

#### C-23

**Fonte:** F-3, seção 5.1. A **unidade preferencial de revisão** é um Draft PR ou
commit contendo spec, plano, diff e testes; na sua ausência, um pacote compacto
com projeto, branch, objetivo, critérios, modelo e effort, dúvida exata,
proposta ou resultado, estado Git e evidências. A entrega do revisor é
`aprovar | aprovar com condições | rejeitar`, mais riscos não percebidos,
premissas sem evidência, próxima ação mais segura e modelo/effort recomendados.
A unidade é sempre um **pacote**, nunca um turno isolado de conversa.

#### C-24

**Fonte:** F-3, seções 9 e 12.4, item 2. O planejamento registra **modelo,
effort, risco e exceções**. Papéis são lógicos — `planner-strong`,
`implementer`, `reviewer`, `cheap-readonly` — e mapeados a modelo concreto, data
e quem promoveu, para que troca de nome ou versão não invalide o método.
Critério de sucesso: toda tarefa média/alta tem revisão por outra família.

#### C-25

**Fonte:** F-3, seção 10. Validação por IA reduz risco mas **não equivale** a
revisão humana experiente. Mudanças críticas e irreversíveis — segurança,
pagamentos, autenticação, dados pessoais, migrações destrutivas e produção sem
rollback comprovado — preveem revisão humana especializada quando disponível.

#### C-26

**Fonte:** F-1, adendo de 16/09/2026, "Skills mínimas da v0.2". A revisão
independente é operacionalizada por **cinco skills**: `review-router` (classifica
gate, risco e perfis obrigatórios); `review-definition` (problema, requisitos,
escopo, critérios, decisões); `review-plan` (arquitetura, tarefas, ordem, riscos,
rollback, testes previstos); `review-delivery` (diff, testes, evidências,
regressões, aderência à spec); `review-handoff` (cria e valida o pacote de
repasse). Objetivo declarado: revisar **unidades coerentes**, sem pedir segunda
análise depois de cada prompt.

#### C-27

**Fonte:** F-1, adendo, mesmo bloco. Quatro **perfis de risco** complementam as
skills de gate **sem multiplicar skills completas**:
segurança/autenticação/privacidade; dados/migração; Git/deploy;
negócio/experiência do cliente. O `review-router` **compõe** gate mais perfis
aplicáveis — não existe uma skill por combinação.

#### C-28

**Fonte:** F-1, adendo, "Contrato de repasse". O implementador **não cola o
histórico da conversa** na nova sessão: grava um **Review Request** em formato
delta com unidade revisada, risco e justificativa, branch/HEAD, base e escopo do
diff, arquivos, testes, decisões, dúvidas, fontes, restrições e
harness/modelo/effort/session ID do implementador. Um **ponteiro único** indica a
rodada ativa. O revisor abre **contexto novo**, lê o roteador do repositório e o
ponteiro, e grava um **Review Verdict** separado com identidade do revisor,
evidências, achados `P0`–`P3`, veredito, condições e gate resultante. Havendo
correções, o implementador grava um **Correction Report** na **mesma rodada**, e
o revisor reconfere o pacote consolidado **uma vez**. Mudança material de escopo
abre **nova rodada**.

#### C-29

**Fonte:** F-1, adendo, mesmo bloco e "Relação com o Notion". Estados lógicos:
`RASCUNHO → PRONTO PARA REVISÃO → EM REVISÃO → CORREÇÕES SOLICITADAS → PRONTO
PARA RECONFERÊNCIA → APROVADO | REPROVADO`. **Exatamente uma rodada pode estar
ativa.** Caminhos físicos, nomes finais e validação executável **serão definidos
no Plan Gate**; a proposta preferencial é manter pedidos, pareceres e correções
junto à spec correspondente, com ponteiro `CURRENT` e **rodadas imutáveis**.
Revisões técnicas comuns permanecem no repositório e o cockpit recebe apenas o
marco; Consulta SDD segue obrigatória para decisão de negócio,
arquitetura/processo transversal, risco alto/crítico, divergência material ou
falta de compreensão segura por quem orquestra.

## Mapeamento cláusula → IDs da spec

| Cláusula | PR | FR / NFR | AC | DEC |
| --- | --- | --- | --- | --- |
| C-01 | PR-002 | — | — | — |
| C-02 | PR-002 | FR-003, FR-009 | AC-005, AC-014, AC-053 | DEC-002 |
| C-03 | PR-003, PR-004 | FR-006, NFR-002 | AC-002, AC-008, AC-018 | — |
| C-04 | PR-007 | FR-003, FR-010 | AC-005, AC-014, AC-053 | DEC-002 |
| C-05 | PR-004 | FR-006 | AC-008, AC-018 | DEC-004 |
| C-06 | — | FR-001 | AC-009, AC-014, AC-017, AC-051 | — |
| C-07 | PR-003 | FR-002 | AC-002, AC-003, AC-013, AC-052 | — |
| C-08 | PR-003 | FR-007 | AC-011, AC-012, AC-016, AC-051 | DEC-007 |
| C-09 | — | FR-005, NFR-003 | AC-006, AC-007 | DEC-005 |
| C-10 | — | FR-005, FR-008, NFR-003 | AC-007, AC-012, AC-013, AC-017, AC-052 | DEC-007 |
| C-11 | PR-005 | NFR-002 | AC-008, AC-009 | DEC-004 |
| C-12 | — | FR-006 | AC-018 | — |
| C-13 | — | NFR-002 | — | DEC-004 |
| C-14 | PR-006 | NFR-004 | AC-010 | DEC-006 |
| C-15 | — | — | AC-010 | — |
| C-16 | — | NFR-004 | AC-010 | DEC-006 |
| C-17 | PR-009 | FR-005 | AC-022 | — |
| C-18 | PR-009 | FR-005 | AC-022 | — |
| C-19 | — | FR-007, FR-008 | AC-011, AC-013, AC-017, AC-051, AC-052 | DEC-007 |
| C-20 | — | — | — | — |
| C-21 | — | — | — | — |
| C-22 | PR-002 | FR-007 | AC-011 | DEC-007 |
| C-23 | — | — | — | — |
| C-24 | — | FR-006 | AC-018 | — |
| C-25 | — | FR-008 | AC-013, AC-017, AC-052 | DEC-007 |
| C-26 | — | — | — | — |
| C-27 | — | — | — | — |
| C-28 | — | — | — | — |
| C-29 | — | — | — | — |

## Fronteira histórica C-17 a C-29 após a separação

| Cláusula | Parte preservada na ponte | Norma transferida |
| --- | --- | --- |
| C-17, C-18 | escrita MCP consome preflight transversal; alvo, escopo e proveniência permanecem locais | contrato e mecanismo do Git Guardian vivem na spec de governança transversal |
| C-19 | Modo B e aprovador distinto da Consulta SDD permanecem interfaces locais | revisão independente geral vive na spec de governança transversal |
| C-20, C-21 | nenhuma norma local | matriz de risco e papéis vedados vivem na spec de governança transversal |
| C-22 | gatilhos locais do Modo B permanecem em FR-007 | escalonamento transversal vive na spec de governança transversal |
| C-23 | nenhuma norma local | pacote de revisão vive na spec de governança transversal |
| C-24 | proveniência sem inferência permanece em FR-006 e AC-018 | roteamento de modelo e effort vive na spec de governança transversal |
| C-25 | aprovador distinto permanece em FR-008 | revisão humana transversal vive na spec de governança transversal |
| C-26 a C-29 | nenhuma norma local | skills, perfis, artefatos, estados, ponteiros e rodadas vivem na spec de governança transversal |

As cláusulas originais acima permanecem como fotografia histórica da fonte. A
tabela não republica a governança: registra somente a fronteira e aponta sua
fonte normativa na spec de governança transversal.

## Recomposição documental executada antes da migração

| AC novo | Cláusulas de origem | Obrigação recomposta | Por que não amplia escopo |
| --- | --- | --- | --- |
| AC-051 | C-06, C-08, C-10 | cockpit por marco e relatório Modo B factual, com campo `aprovador` explícito | acrescenta e explicita o campo `aprovador`, derivado de C-10 e da obrigação local de FR-008; recompõe uma obrigação já aprovada sem criar novo gatilho ou superfície |
| AC-052 | C-07, C-10 | Consulta SDD e aprovador distinto | torna observável a vedação local já contida em FR-008; não redefine a governança geral |
| AC-053 | C-02, C-04 | precedência e reconciliação Notion ↔ repositório | recompõe FR-009 e FR-010 com regras já aprovadas; não trata de Git Guardian |

A interface semântica com a spec de governança transversal é deliberadamente
estreita: ela fornece a regra geral de separação entre executor e aprovador; a
ponte mantém localmente a transição da Consulta SDD, o cockpit, o Modo B, a
proveniência e a precedência entre Notion e repositório. O corpo da SPEC-0001 não
depende de IDs externos para declarar essas obrigações.

## Itens deliberadamente não importados

| Item da origem | Motivo |
| --- | --- |
| F-1, "Fase 2 — base estruturada": as doze propriedades da database `Consultas SDD` | A database está fora de escopo (C-14). Importar as propriedades agora congelaria um desenho que o piloto existe para validar. |
| F-1, "Fase 3 — automação opcional": custom agent, trigger, worker | Fora de escopo por decisão da própria origem; só é avaliada após o piloto. |
| F-1, "Fontes relacionadas": as três páginas mencionadas e a marcação `SUPERADO` do fluxo anterior | Manutenção do workspace Notion, não contrato da camada. Fora do escopo autorizado desta spec. |
| F-1, "Critérios de sucesso" em prosa | Convertidos em metas numéricas próprias da SPEC-0001 (seção 8). Importar a prosa duplicaria sem tornar verificável. |
| F-2, seções 3 e 5 (decisões A-8/A-9/A-10 e links de evidência) | Pertencem ao fechamento da v0.1, já commitado; não vinculam esta frente. |
| F-2, bloco "Como abrir a próxima thread" | Operação de sessão, sem valor normativo. |
| F-3, seções 1, 2 e 11 (motivação, tabela de camadas, efeito sobre documentos anteriores) | Contexto histórico e governança do workspace Notion; não vinculam o contrato desta fatia. |
| F-3, seção 8 (OpenRouter e modelos adicionais) | Política de fornecedor, fora do escopo da ponte. |
| F-3, seção 12.1 e 12.2 (achado do preflight no `Youtube-TempusOS`) | Estado de outro piloto. Importado apenas o que prova que o mecanismo do Git Guardian não está materializado (`C-18`). |
| F-3, seção 12.4, itens 3, 4 e 5, e seção 12.5 | Métricas de sessão, gatilho de reversão da ADR e prazo de reescrita de documento do Notion: governança do método transversal, não desta fatia. |
| F-3, nomes concretos de modelo e fornecedor por papel | `C-24` importa o mapeamento **lógico**; fixar modelo concreto aqui contrariaria FR-006, que proíbe inferir valores não observados. |
| As três fontes, na íntegra | PR-005 e a peça 2 exigem referência, não duplicação. |

## Observação sobre autoria versus runtime

A leitura destas três páginas ocorreu por MCP em **tempo de autoria**. Nada neste
arquivo, na spec ou em qualquer artefato do repositório exige o MCP conectado
para ser lido ou executado. A distinção está normatizada em PR-001 e verificada
por AC-001, AC-004 e AC-015.
