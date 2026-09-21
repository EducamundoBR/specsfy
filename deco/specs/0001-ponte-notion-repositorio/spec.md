# Especificação integrada: Ponte Notion ↔ repositório da camada Deco

| Campo | Valor |
| --- | --- |
| Formato | Specsfy/2.0 |
| ID | SPEC-0001 |
| Slug | 0001-ponte-notion-repositorio |
| Status | Defined |
| Effort | 3 |
| Effort updated at | 2026-09-19 |
| Effort rationale | Contrato de processo ainda complexo, embora com fronteira reduzida após a separação: dez requisitos funcionais, vinte e oito IDs AC, trinta e cinco blocos `Scenario`, cinco artefatos documentais previstos e piloto especificado, ainda não executado; não contém catálogo de skills nem código de produto. O nível 3 permanece pela integração entre Notion, repositório, segurança da escrita e reconciliação de fontes, não pelo tamanho anterior. Revisar após o Definition Gate. |
| ClickUp Task | |
| Milestones | |
| Definition Gate | Passed |
| Plan Gate | Pending |
| Delivery Gate | Pending |
| Evidence Contract | 1 |
| Interface para pessoas | Sim — páginas Notion (cockpit e Consulta SDD); nenhuma superfície web criada no repositório |
| Atualizada em | 2026-09-19 |

> **Decisão local de roteamento.** As specs de definição da própria camada
> distribuível vivem em `deco/specs/<NNNN>-<slug>/`; o estado permanece no
> cabeçalho e nos gates, sem segmento físico de estado nesta versão. Esta exceção
> local foi aprovada no Definition Gate e não altera o roteamento de projetos
> consumidores.

## Ato I — Definir

### 1. Problema e resultado

#### Problema

O contexto de negócio, as decisões humanas e o histórico do projeto vivem no
Notion; a verdade técnica vive no repositório. A passagem entre os dois é manual
— cada rodada nasce no Notion, vira prompt copiado para a IDE, volta como
relatório colado e exige nova mediação — o que consome créditos, atrasa cada
passagem e mantém o Notion no caminho crítico mesmo quando o repositório já tem
contexto suficiente; trabalhar só na IDE também não resolve, porque sem contexto
de negócio e sem parecer externo quem orquestra não valida decisões técnicas com
segurança. A camada Deco v0.1 já normatizou o princípio (peça 2 em
`deco/rules/canonical.md:45-59`), mas não definiu mecanismo, artefatos, escopo de
permissão nem limite de interação.

#### Resultado desejado

Um contrato que permita à LLM da IDE ler e escrever no Notion por MCP dentro de
um escopo restrito — eliminando o transporte manual — sem que o projeto
consumidor passe a depender de Notion, MCP ou rede para funcionar. O trabalho
técnico continua no repositório; o Notion entra em marcos, dúvidas, divergências
e riscos relevantes.

#### Métricas de sucesso

Das seis medidas da decisão de origem, cinco foram numeradas aqui como `M-1`,
`M-2`, `M-3`, `M-5` e `M-7`; a sexta, tempo entre pergunta e aplicação, é
registrada descritivamente por não haver baseline.
`M-4` e `M-6` são métricas novas acrescentadas por esta spec para tornar
observáveis o encerramento da Consulta SDD e a vedação de aplicação sem
evidência. As metas das sete métricas são **experimentais e próprias desta
spec**: não são decisão histórica e o piloto existe para confirmá-las ou
refutá-las. Definição operacional, coleta e registro em `#### Piloto manual e
metas experimentais` (seção 8).

| # | Métrica | Meta experimental da SPEC-0001 |
| --- | --- | --- |
| M-1 | Consultas completas no piloto | exatamente 5 |
| M-2 | Consultas respondidas sem esclarecimento | ≥ 3 de 5 |
| M-3 | Acionamentos do Notion AI por consulta | ≤ 2 |
| M-4 | Consultas encerradas em `APLICADA` ou `DESCARTADA`, com destino ou motivo | 5 de 5 |
| M-5 | Consultas relidas diretamente pela IDE, sem copy-paste de retorno | 5 de 5 |
| M-6 | Decisões aplicadas sem evidência registrada | 0 |
| M-7 | Decisões reabertas por falta de evidência | ≤ 1 |

`M-1` materializa "consultas abertas" e `M-5` materializa "episódios de
copy-paste evitados".

### 2. Research e esclarecimentos

#### Researchs executados

- **R-001** [critical] A proibição da peça 2 alcança apenas o runtime do
  consumidor, não o tempo de autoria — Verdict: verified — Confidence: high —
  Evidence: research/notion/fontes-notion.md#c-01 — Budget: 1/2
- **R-002** [critical] A decisão aprovada exige o Modo B (relatório revisado) em
  sete situações, incluindo risco alto, segurança e LGPD — Verdict: verified —
  Confidence: high — Evidence: research/notion/fontes-notion.md#c-08 — Budget: 1/2
- **R-003** [critical] A decisão aprovada veda usar o Notion como canal para
  ordenar push, deploy ou Git destrutivo sem gate humano — Verdict: verified —
  Confidence: high — Evidence: research/notion/fontes-notion.md#c-10 — Budget: 1/2
- **R-004** [material] A nota "testar também com o ChatGPT" refere-se ao
  fornecedor do lado da IDE, não ao consumo do parecer — Verdict: verified —
  Confidence: medium — Evidence: research/notion/fontes-notion.md#c-12 — Budget: 1/2

#### Fontes e contexto consultados

- Notion — "Decisão — Fluxo SDD repo-first com ponte Notion MCP"
  (`APROVADA · 16/09/2026`), `698186dcacc94713b91d5d152c0d7f0b`: princípios,
  arquitetura de papéis, modos A e B, cockpit, permissões, controle de custo e
  plano de adoção em fases.
- Notion — "Handoff — 16/09/2026 · Specsfy/Deco v0.1 documental commitada"
  (`ATUAL`), `d380bfc45b8c4f0db0ea64ac131e29c8`: estado verificável do
  repositório e pendências que delimitam esta frente.
- Notion — "Decisão — Fluxo repo-first, dupla validação e Git Guardian"
  (`APROVADA · 28/08/2026`, adendo `01/09/2026`),
  <https://app.notion.com/p/89aafb8557414ba8b2c77ef42a41bff0>: sustenta
  `C-17` a `C-25` e as obrigações locais derivadas preservadas na ponte.
- Repositório — `deco/rules/canonical.md:45-59` (peça 2) e `:136-139`
  (proveniência); `deco/rules/canonical.md:121-132` (guardrails A e B);
  `deco/skills/fechar-sessao-deco/SKILL.md:63-64` (a camada não escreve no
  Notion); `deco/README.md:104-117` (fonte, instalação, lock).
- Repositório — `AGENTS.md:35-62` (fonte da verdade do monorepo; limites do
  módulo `deco/`) e `AGENTS.md:88-95` (precedente de **regra** de MCP local ao
  monorepo, não publicável em consumidores).
- Repositório — `docs/develop/context/README.md:44-56` (regra de divergência
  entre fontes) e `docs/develop/context/README.md:72-81` (tabela de precedência
  das fontes, reaproveitada por esta spec).

#### Documentação consultada

- Notion MCP — Help Center, consultado em 16/09/2026,
  <https://www.notion.so/help/notion-mcp>: natureza do canal de leitura e escrita
  escopadas; base de FR-005.
- Notion — Security best practices for agent connections, consultado em
  16/09/2026, <https://www.notion.so/help/security-best-practices-for-agent-connections>:
  princípio de acesso proporcional ao blast radius; base de NFR-003.
- Specsfy — `skills/templates/Spec.md` (formato Specsfy/2.0) e
  `skills/specsfy-04-validate/scripts/validate_spec.mjs`, lidos em 16/09/2026:
  contrato estrutural e regra de cobertura mínima de três cenários por
  identificador.

#### Artefatos de pesquisa armazenados

- `deco/specs/0001-ponte-notion-repositorio/research/notion/fontes-notion.md`:
  evidência derivada das três páginas Notion — título, URL, data de leitura,
  cláusulas `C-01` a `C-29` efetivamente usadas, mapeamento cláusula → ID, itens
  deliberadamente não importados e declaração de que o Notion permanece fonte
  normativa. Sem reprodução integral, sem segredo e sem PII.
- Nenhum outro artefato externo. As fontes do repositório não geram cópia em
  `research/`: são citadas por caminho e linha, conforme PR-005.

#### Dúvidas respondidas

- **Q**: escrever uma pergunta numa página do Notion dispara o Notion AI?
  → **A**: não. O MCP transporta leitura e escrita; o acionamento do Notion AI é
  humano no piloto. Registrado na decisão de 16/09/2026 (`C-05`).
- **Q**: qual fornecedor/modelo sustenta o baseline observado?
  → **A**: Anthropic no VS Code, observado na trilha de NFSe. O modelo exato
  **não foi registrado** e não deve ser inferido (`C-12`).
- **Q-001**: a proibição de dependência de MCP alcança o tempo de autoria ou só o
  runtime do consumidor? → **A**: só o runtime do consumidor. A peça 2 é
  explícita nos dois qualificadores — *"nada **dentro do repositório** pode
  depender do MCP do Notion estar conectado **em tempo de execução**"*
  (`deco/rules/canonical.md:47-49`), justificada por *"sem transformar uma
  conveniência em dependência de runtime"* (`:57-59`). Três confirmações
  independentes: a decisão aprovada constrói o fluxo inteiro sobre MCP em autoria e
  foi aprovada sob a mesma peça 2; `AGENTS.md:88-95` já estabelece o precedente de
  regra de MCP local ao monorepo e não publicável em consumidores;
  `deco/skills/fechar-sessao-deco/SKILL.md:63-64` restringe a escrita no Notion
  no **consumidor**, sem tocar a autoria. PR-001 deixa de ser leitura adotada e
  passa a norma derivada.
- **Q-002**: a nota "testar também com o ChatGPT" impõe que o parecer do Notion AI
  seja acionável por outro fornecedor? → **A**: não; a pergunta original invertia
  o lado da ponte. A nota está no bloco "Baseline verificado", junto de
  *"Fornecedor usado: Anthropic no VS Code"*, e trata do **fornecedor do lado da
  IDE** que opera o MCP, não de quem consome o parecer (`C-12`). Consequência
  normativa: nenhum requisito de multifornecedor entra neste contrato; o teste com
  outro fornecedor vira observação secundária e não bloqueante do piloto
  (seção 8), sob a proibição de inferir modelo não observado de FR-006.

#### Dúvidas abertas

- Nenhuma.

### 3. Escopo e atores

#### Incluído

Contratos documentais da ponte: cockpit do projeto; registro `Consulta SDD`;
relatório de revisão independente (Modo B); fonte da verdade e reconciliação;
cópia derivada por categoria; permissões e protocolo de escrita MCP; limite de
interação; obrigação local de aprovador distinto na transição de Consulta SDD de
risco alto ou crítico; registro de decisão de negócio originada na IDE; piloto
manual, metas experimentais e protocolo de segurança.

A spec de governança transversal fornece classificação de risco, gates,
preflight, continuidade de sessão e repasse entre agentes. Esta spec somente
consome essas garantias como precondições sem duplicar seus contratos.

Escopo de entrega: camada Deco v0.2, módulo `deco/` deste fork.

#### Fora de escopo

- Implementar skills, scripts, verificadores, banco, trigger, worker ou automação.
- Redefinir classificação de risco, gates, preflight, continuidade de sessão,
  catálogo de skills, perfis ou contrato de repasse da governança transversal.
- Autorizar Git, push, deploy, alteração de remote, segredo ou ação irreversível
  por conteúdo vindo do Notion.
- Criar superfície web, componente, rota ou dependência de runtime do Notion.
- Fixar caminhos físicos antes do Plan Gate.
- Alterar componentes fora de `deco/`, a integração ClickUp, o Hub ou o website.

#### Atores

- **Pessoa que orquestra**: aciona o Notion AI, decide regra de negócio e registra
  aprovação explícita quando o contrato exigir.
- **Agente da IDE**: lê estado técnico, cria e relê registros pelo MCP, produz
  cópias derivadas e não aprova sozinho a própria aplicação de alto risco.
- **Notion AI**: responde à consulta acionada pela pessoa; não executa operações.
- **Aprovador distinto**: valida a transição da Consulta SDD e o parecer de Modo
  B quando aplicável, sem substituir a governança transversal.

### 4. Princípios e restrições do projeto

- **PR-001**: dois planos separados. Autoria/operação pode usar MCP; o runtime do
  consumidor funciona integralmente sem Notion, MCP ou rede.
- **PR-002**: a IDE conduz; o Notion orienta. O Notion não intermedeia cada turno.
- **PR-003**: artefatos estruturados substituem copy-paste.
- **PR-004**: sem conversa autônoma entre agentes; toda consulta tem encerramento
  explícito.
- **PR-005**: contexto estável é linkado, não duplicado, inclusive entre
  documentos do próprio repositório.
- **PR-006**: cópia derivada é ato explícito, nunca sincronização automática.
- **PR-007**: a precedência entre fontes reaproveita a regra vigente em
  `docs/develop/context/README.md`; nenhuma lacuna é preenchida por suposição.
- **PR-008**: nenhum texto lido do Notion autoriza ação irreversível sobre Git,
  produção ou permissões.
- **PR-009**: toda escrita MCP ou derivada da ponte consome como precondição a
  liberação do contrato transversal de preflight. Esta spec valida somente alvo,
  escopo e proveniência locais; não emite nem redefine o veredito transversal.

### 5. Histórias de usuário

#### US-001 — Consultar o Notion sem transportar texto à mão (P1)

Como pessoa que orquestra, quero que a IDE registre a dúvida no Notion e releia a
resposta de lá, para obter parecer de negócio sem copiar prompt nem relatório.

**Por que P1**: é a dor que originou a decisão aprovada — o transporte manual
consome créditos, atrasa cada passagem e é o único custo que a ponte elimina de
imediato. Sem ela, as demais histórias não têm uso.
**Teste independente**: abrir uma consulta, responder no Notion e ver a IDE
continuar a partir do registro, sem cópia manual.
**Requisitos**: FR-002, FR-006, FR-007

#### US-002 — Enxergar o estado do projeto sem ler diff (P1)

Como pessoa que orquestra, quero uma página curta com objetivo, marco, estado,
decisão aberta e próximo gate, para acompanhar sem abrir o repositório.

**Por que P1**: materializa a peça 4 (régua de validação do orquestrador,
`deco/rules/canonical.md:77-87`). Sem o cockpit, aprovar um gate vira confiança no
agente em vez de verificação.
**Teste independente**: após um marco, conferir que o cockpit reflete o novo
estado e que nenhuma microatividade gerou atualização.
**Requisitos**: FR-001, FR-003

#### US-003 — Trabalhar com o Notion fora do ar (P1)

Como desenvolvedor, quero continuar quando o Notion ou o MCP estiverem
indisponíveis, desde que o repositório já contenha o necessário.

**Por que P1**: é a invariante que impede a conveniência de virar dependência. Se
falhar, a camada contradiz a peça 2 e o projeto deixa de ser legível sem rede.
**Teste independente**: desligar o MCP e concluir uma fatia cujo contexto já
esteja versionado.
**Requisitos**: FR-004, NFR-001

### 6. Cenários BDD de aceite

#### AC-001 — Consumidor opera sem MCP

**Cobre**: US-003, FR-004, NFR-001

```gherkin
@US-003 @FR-004 @NFR-001 @AC-001
Feature: Autossuficiência do projeto consumidor

  Scenario: Fluxo completo com MCP desconectado
    Given um projeto consumidor com a camada Deco instalada
    And o Notion MCP desconectado e sem acesso à rede
    When a equipe executa o fluxo de trabalho do projeto
    Then nenhuma etapa falha por ausência de Notion, MCP ou rede
    And nenhum artefato do repositório exige resolução remota para ser lido
```

#### AC-002 — Consulta ponta a ponta sem copy-paste de retorno

**Cobre**: US-001, FR-002, NFR-002

```gherkin
@US-001 @FR-002 @NFR-002 @AC-002
Feature: Consulta SDD sem transporte manual

  Scenario: Pergunta publicada e resposta relida pela IDE
    Given uma dúvida de negócio durante o desenvolvimento
    When a IDE cria uma Consulta SDD no Notion com pergunta única e evidências
    And a pessoa aciona o Notion AI para responder
    Then a IDE relê a resposta diretamente do Notion pelo identificador da consulta
    And o registro da consulta comprova que nenhum trecho foi recolado na IDE
```

#### AC-003 — Aplicação ou descarte rastreável

**Cobre**: US-001, FR-002, FR-003

```gherkin
@US-001 @FR-002 @FR-003 @AC-003
Feature: Encerramento rastreável da Consulta SDD

  Scenario: Decisão incorporada é marcada como aplicada
    Given uma Consulta SDD com status RESPONDIDA
    When a decisão é incorporada ao trabalho
    Then o status passa a APLICADA e registra onde entrou no repositório

  Scenario: Decisão recusada preserva o registro
    Given uma Consulta SDD com status RESPONDIDA
    When a decisão é recusada
    Then o status passa a DESCARTADA com o motivo registrado
    And a consulta não é apagada
```

#### AC-004 — Indisponibilidade do Notion não bloqueia trabalho autossuficiente

**Cobre**: US-003, FR-006, NFR-001

```gherkin
@US-003 @FR-006 @NFR-001 @AC-004
Feature: Degradação sem bloqueio

  Scenario: Repositório já contém a decisão necessária
    Given que o repositório já contém a decisão necessária como cópia derivada
    When o Notion ou o MCP está indisponível
    Then o desenvolvimento prossegue sem abrir consulta
    And a indisponibilidade só é registrada quando há dúvida que impede concluir a fatia
```

#### AC-005 — Conflito entre Notion e repositório bloqueia explicitamente

**Cobre**: US-002, FR-003, NFR-004

```gherkin
@US-002 @FR-003 @NFR-004 @AC-005
Feature: Reconciliação de fontes divergentes

  Scenario: Divergência material interrompe a execução
    Given uma divergência material entre decisão do Notion e estado do repositório
    And material significa divergência que altera decisão, escopo ou risco
    When a divergência é detectada
    Then a execução é bloqueada e o conflito é declarado
    And nenhuma das fontes é escolhida silenciosamente
    And nenhuma lacuna é preenchida por suposição
```

#### AC-006 — Escrita fora do escopo é recusada

**Cobre**: FR-005, NFR-003

```gherkin
@FR-005 @NFR-003 @AC-006
Feature: Escopo de escrita do MCP

  Scenario: Destino fora da subárvore autorizada
    Given uma tentativa de escrever fora de cockpit, Consulta SDD ou relatório do projeto
    When a operação é solicitada pelo agente
    Then a operação é recusada
    And exclusão, movimentação e alteração de permissões permanecem indisponíveis
    And a atualização de página normativa exige confirmação humana explícita
```

#### AC-007 — Segredo e PII não são transportados

**Cobre**: FR-005, NFR-003

```gherkin
@FR-005 @NFR-003 @AC-007
Feature: Barreira de dados sensíveis

  Scenario: Conteúdo sensível na preparação da escrita
    Given um conteúdo com segredo, token, credencial, dado pessoal sob a LGPD ou dump
    When o agente prepara escrita no Notion
    Then o conteúdo não é transportado
    And o registro da operação preserva motivo e resultado sem expor o dado
```

#### AC-008 — Limite de um esclarecimento

**Cobre**: FR-006, NFR-002

```gherkin
@FR-006 @NFR-002 @AC-008
Feature: Limite de interação entre agentes

  Scenario: Resposta insuficiente esgota o único esclarecimento
    Given uma Consulta SDD respondida que não resolveu a dúvida
    When a IDE solicita esclarecimento
    Then é permitido no máximo um esclarecimento
    And persistindo a dúvida, a consulta é encerrada e a pessoa define o próximo gate
    And nenhum ciclo adicional entre agentes é iniciado automaticamente
```

#### AC-009 — Cockpit atualizado somente por marco

**Cobre**: US-002, FR-001, NFR-002

```gherkin
@US-002 @FR-001 @NFR-002 @AC-009
Feature: Disciplina de atualização do cockpit

  Scenario: Marco produz atualização
    Given um dos seis gatilhos de marco definidos em FR-001
    When o marco ocorre
    Then o cockpit é atualizado com data e agente da atualização

  Scenario: Microatividade não produz atualização
    Given uma atividade que não altera estado, decisão, escopo ou risco
    When a atividade termina
    Then o cockpit permanece inalterado
```

#### AC-010 — Componentes fora de escopo permanecem intactos

**Cobre**: FR-004, NFR-004

```gherkin
@FR-004 @NFR-004 @AC-010
Feature: Preservação dos artefatos da v0.1

  Scenario: Diff da entrega não alcança artefatos excluídos
    Given a entrega desta spec
    When o diff é revisado
    Then AGENTS.md, deco/rules/, deco/manifest.json, deco/skills/, deco/templates/ e as fixtures da v0.1 permanecem inalterados
    And nenhum instalador, verifier da camada, database, agent, trigger ou worker é criado
```

#### AC-011 — Modo B é obrigatório nos gatilhos declarados

**Cobre**: US-001, FR-007, NFR-003

```gherkin
@US-001 @FR-007 @NFR-003 @AC-011
Feature: Revisão independente obrigatória

  Scenario: Risco alto exige relatório revisado
    Given uma entrega que toca autenticação, pagamento, segurança ou dado pessoal
    When a IDE conclui a análise técnica
    Then um relatório de revisão independente é publicado no Notion antes do gate
    And prosseguir sem esse relatório é recusado com o gatilho apontado
```

#### AC-012 — Notion não autoriza Git, push ou deploy

**Cobre**: FR-005, FR-007, NFR-003

```gherkin
@FR-005 @FR-007 @NFR-003 @AC-012
Feature: Vedação de comando irreversível por texto remoto

  Scenario: Parecer instrui operação destrutiva
    Given um parecer ou relatório no Notion que instrui push, deploy, merge, rebase ou Git destrutivo
    When a IDE lê esse conteúdo
    Then a operação não é executada a partir do texto lido
    And a execução exige gate humano explícito registrado na IDE
    And a recusa aponta a cláusula violada antes de propor ajuste
```

#### AC-013 — Quem abre a consulta não aprova sozinho a aplicação

**Cobre**: FR-002, FR-008, NFR-004

```gherkin
@FR-002 @FR-008 @NFR-004 @AC-013
Feature: Separação entre executor e aprovador

  Scenario: Executor tenta encerrar a própria consulta de risco alto
    Given uma Consulta SDD de risco alto ou crítico aberta pela LLM da IDE
    When a mesma LLM tenta marcar a consulta como APLICADA
    Then a transição é recusada
    And a aplicação exige aprovador distinto do executor, identificado no registro
```

#### AC-014 — Divergência de branch ou HEAD resolve pelo estado observado

**Cobre**: US-002, FR-001, FR-003

```gherkin
@US-002 @FR-001 @FR-003 @AC-014
Feature: Precedência do estado técnico observado

  Scenario: Cockpit desatualizado em relação ao repositório
    Given um cockpit cujo branch ou HEAD difere do repositório
    When a divergência é observada
    Then prevalece o estado observado no repositório
    And o cockpit é corrigido no próximo marco, sem reescrever o histórico da página
```

#### AC-015 — Cópia derivada por categoria com proveniência

**Cobre**: US-003, FR-004, NFR-001

```gherkin
@US-003 @FR-004 @NFR-001 @AC-015
Feature: Destino da cópia derivada

  Scenario: Decisão do Notion necessária ao trabalho técnico
    Given uma decisão aprovada no Notion necessária a uma fatia
    When ela é trazida para o repositório
    Then o destino segue a natureza: ADR, spec, tarefa ou handoff
    And a URL ou o identificador entram como proveniência, nunca como dependência de leitura
    And nenhum arquivo genérico único concentra decisões de naturezas distintas
```

#### AC-016 — Relatório Modo B separa observado, inferido e não verificado

**Cobre**: US-001, FR-007, NFR-002

```gherkin
@US-001 @FR-007 @NFR-002 @AC-016
Feature: Estrutura do relatório de revisão independente

  Scenario: Relatório publicado sem separação das três classes
    Given um relatório da IDE preparado para revisão no Notion
    When ele não separa observado, inferido e ainda não verificado
    Then a publicação é recusada até a separação existir
    And o relatório não substitui log ou teste primário como evidência
```

#### AC-017 — Coincidência entre executor e aprovador bloqueia o gate

**Cobre**: FR-001, FR-008, NFR-004

```gherkin
@FR-001 @FR-008 @NFR-004 @AC-017
Feature: Separação obrigatória na aprovação de gate

  Scenario: Aprovador distinto assina o fechamento
    Given um gate prestes a ser fechado
    And um aprovador distinto de quem executou
    When o cockpit é atualizado com o resultado
    Then o registro identifica nominalmente quem executou e quem aprovou
    And o gate pode passar a Passed

  Scenario: Executor e aprovador coincidem
    Given um gate cujo executor é também o único aprovador disponível
    When o fechamento é tentado
    Then o fechamento é recusado
    And o gate permanece Pending
    And o cockpit permanece BLOQUEADO até revisão por instância distinta
    And sinalizar a coincidência não libera a passagem
```

#### AC-018 — Encerramento explícito da consulta

**Cobre**: FR-006, FR-008, NFR-002

```gherkin
@FR-006 @FR-008 @NFR-002 @AC-018
Feature: Encerramento e registro de participação

  Scenario: Consulta encerrada com procedência registrada
    Given uma Consulta SDD que chegou a APLICADA ou DESCARTADA
    When ela é encerrada
    Then o encerramento é explícito e datado
    And fornecedor, modelo, effort e papel são registrados quando relevantes para a decisão
    And valores não observados são registrados como NÃO REGISTRADO, nunca inferidos
```

#### AC-019 — Decisão de negócio da IDE não vale sem registro no Notion

**Cobre**: US-001, FR-009, NFR-004

```gherkin
@US-001 @FR-009 @NFR-004 @AC-019
Feature: Registro obrigatório da decisão de negócio

  Scenario: Decisão aceita no chat da IDE e ainda não registrada
    Given uma decisão de negócio aceita durante o trabalho na IDE
    And nenhum registro correspondente no Notion
    When a decisão é invocada como norma ou para fechar um gate
    Then a invocação é recusada
    And a decisão consta como PENDENTE DE REGISTRO
    And o registro no Notion é exigido antes de considerá-la aplicada
```

#### AC-020 — Notion indisponível mantém a decisão pendente sem parar o trabalho

**Cobre**: US-003, FR-009, FR-006, NFR-001

```gherkin
@US-003 @FR-009 @FR-006 @NFR-001 @AC-020
Feature: Degradação sem promoção silenciosa

  Scenario: Decisão de negócio aceita com MCP fora do ar
    Given uma decisão de negócio aceita na IDE
    And o Notion ou o MCP indisponível
    When o trabalho técnico independente dessa decisão prossegue
    Then o trabalho técnico não é bloqueado
    And a decisão de negócio permanece PENDENTE DE REGISTRO
    And a pendência é registrada no repositório
    And a decisão não é promovida a aplicada por decurso de tempo
```

#### AC-021 — Decisão registrada gera cópia derivada por categoria

**Cobre**: FR-009, FR-004, NFR-002

```gherkin
@FR-009 @FR-004 @NFR-002 @AC-021
Feature: Retorno da decisão ao repositório

  Scenario: Decisão registrada no Notion volta como cópia derivada
    Given uma decisão de negócio já registrada no Notion
    When ela passa a ser necessária ao trabalho técnico
    Then o repositório recebe a cópia derivada autossuficiente pertinente
    And o destino segue a categoria definida em FR-004
    And o identificador da página entra como proveniência, nunca como dependência de leitura
```

#### AC-022 — Escrita MCP consome o preflight transversal

**Cobre**: FR-005, NFR-003

```gherkin
@FR-005 @NFR-003 @AC-022
Feature: Escrita da ponte condicionada e escopada

  Scenario: Escrita solicitada em superfície autorizada do projeto
    Given uma escrita em cockpit, Consulta SDD ou relatório Modo B do projeto
    And a governança transversal ainda não liberou a operação
    When o agente tenta iniciar a escrita MCP
    Then a escrita permanece bloqueada
    And esta spec não emite veredito substituto
    And após a liberação transversal o alvo, o escopo e a proveniência locais são verificados antes da escrita
```

#### AC-023 — Conflito material mantém o gate bloqueado

**Cobre**: FR-010, FR-003, NFR-004

```gherkin
@FR-010 @FR-003 @NFR-004 @AC-023
Feature: Bloqueio por conflito material

  Scenario: Notion e repositório em conflito material
    Given um conflito material entre decisão aprovada no Notion e estado do repositório
    When um gate é submetido a fechamento
    Then o gate permanece bloqueado até reconciliação explícita
    And nenhuma das fontes é escolhida em silêncio
    And nenhuma lacuna é preenchida por suposição
```

#### AC-024 — Precedência distinta para fato técnico e regra de negócio

**Cobre**: US-002, FR-010, FR-003

```gherkin
@US-002 @FR-010 @FR-003 @AC-024
Feature: Duas precedências, dois domínios

  Scenario: Divergência sobre fato técnico
    Given uma divergência sobre branch, HEAD, diff ou resultado de teste
    When a divergência é avaliada
    Then prevalece o estado observado no repositório

  Scenario: Divergência sobre regra de negócio
    Given uma divergência sobre regra de negócio
    When a divergência é avaliada
    Then prevalece a decisão aprovada no Notion
```

#### AC-025 — Escopo concedido é auditado por teste negativo, não por declaração

**Cobre**: FR-005, NFR-003

```gherkin
@FR-005 @NFR-003 @AC-025
Feature: Verificação empírica do blast radius sem ampliar o raio

  Scenario: Auditoria precede qualquer escrita
    Given a conexão MCP autorizada para o projeto do piloto
    When o protocolo de segurança do piloto é iniciado
    Then o escopo OAuth efetivamente concedido é auditado antes de qualquer tentativa de escrita
    And o escopo observado é registrado e comparado ao escopo pretendido em FR-005

  Scenario: Acesso inesperado a conteúdo real interrompe o protocolo
    Given uma auditoria que revela acesso a conteúdo real fora da página-canário
    When o protocolo chega à etapa de escrita
    Then nenhuma escrita é tentada
    And o gate é classificado como BLOQUEADO
    And o escopo é corrigido antes de qualquer retomada

  Scenario: Teste negativo restrito à página-canário
    Given uma página-canário isolada, criada para o piloto, sem conteúdo real, sem relação com bases operacionais, descartável e com rollback conhecido
    And um payload exclusivamente sintético representando classes proibidas
    When a escrita é tentada contra essa página-canário
    Then o resultado é registrado com alvo, tentativa e confirmação de ausência de efeito fora do canário
    And nenhum segredo, token, credencial ou dado pessoal real é usado

  Scenario: Tentativa contra página real é recusada pelo próprio protocolo
    Given a intenção de comprovar permissão excessiva gravando em uma página real
    When o teste é proposto
    Then o teste é recusado por desenho
    And a expectativa de que a escrita seria negada não autoriza a tentativa
```

#### AC-051 — Marco de reconciliação atualiza cockpit e Modo B

**Cobre**: FR-001, FR-007

```gherkin
@FR-001 @FR-007 @AC-051
Feature: Interface auditável entre parecer e cockpit

  Scenario: Parecer de Modo B conclui uma reconciliação material
    Given um parecer de Modo B que separa observado, inferido e ainda não verificado
    And a reconciliação altera estado, decisão, escopo ou risco do projeto
    When o parecer final é aplicado
    Then o cockpit é atualizado como marco com data, agente, aprovador e links de evidência
    And o cockpit referencia o parecer sem duplicar o relatório completo
    And a atualização não substitui as fontes primárias do parecer
```

#### AC-052 — Consulta de alto risco exige aprovador distinto

**Cobre**: FR-002, FR-008

```gherkin
@FR-002 @FR-008 @AC-052
Feature: Aprovação local da transição da Consulta SDD

  Scenario: Executor é a única instância aprovadora disponível
    Given uma Consulta SDD de risco alto ou crítico no estado RESPONDIDA
    And o executor é a única instância aprovadora disponível
    When a transição para APLICADA é solicitada
    Then a transição é recusada
    And a consulta permanece RESPONDIDA
    And a aplicação aguarda aprovador distinto identificado no registro
```

#### AC-053 — Reconciliação preserva a precedência das duas fontes

**Cobre**: FR-003, FR-009, FR-010

```gherkin
@FR-003 @FR-009 @FR-010 @AC-053
Feature: Reconciliação da ponte sem promoção silenciosa

  Scenario: Fato técnico e decisão de negócio divergem entre as fontes
    Given um fato técnico observado no repositório
    And uma regra de negócio aprovada no Notion
    And uma decisão originada na IDE ainda sem registro no Notion
    When a reconciliação da ponte é registrada
    Then o fato técnico observado prevalece no seu domínio
    And a regra de negócio aprovada prevalece no seu domínio
    And a decisão sem registro permanece PENDENTE DE REGISTRO
    And o conflito continua bloqueado até reconciliação explícita e cópia derivada pertinente
```

### 7. Requisitos

#### Funcionais

- **FR-001**: **Cockpit do projeto.** Deve existir, por projeto, uma página curta
  no Notion com os campos mínimos: projeto; objetivo atual; último marco
  concluído; branch e HEAD relevantes; estado; decisão em aberto;
  riscos/bloqueios; próximo gate; links de evidência (spec, ADR, PR, testes,
  consulta); data, agente e aprovador da última atualização. Estados admitidos:
  `EM ANDAMENTO | AGUARDANDO DECISÃO | BLOQUEADO | CONCLUÍDO`. Gatilhos de
  atualização: spec aprovada; implementação concluída; revisão independente
  encerrada; commit ou PR criado; deploy, incidente ou fechamento de sessão;
  mudança material de decisão, escopo ou risco. Fora desses gatilhos, não
  atualizar.
- **FR-002**: **Registro `Consulta SDD`.** Identificador `SDD-AAAAMMDD-NNN`. A
  consulta declara projeto, branch/HEAD, tipo, risco, **uma** pergunta, motivo da
  necessidade, opções, trade-offs, recomendação da IDE e evidências. A resposta
  separa: fontes consultadas; premissas confirmadas; premissas sem evidência;
  riscos não percebidos; recomendação; condições; decisão de quem orquestra,
  quando necessária. Estados:
  `RASCUNHO → AGUARDANDO NOTION → RESPONDIDA → APLICADA | DESCARTADA`.
  `APLICADA` exige registrar onde a decisão entrou no repositório; `DESCARTADA`
  exige motivo e preserva o registro.
- **FR-003**: **Fonte da verdade e reconciliação.** Repositório é fonte primária
  de código, testes, estado Git, specs, planos e evidências versionáveis; o Notion
  é fonte primária de regras e decisões humanas/de negócio, cockpit, consulta e
  parecer. Em divergência: estado técnico observado prevalece para fatos
  operacionais; decisão aprovada no Notion prevalece para regra de negócio;
  conflito explícito bloqueia execução até reconciliação; nenhuma lacuna é
  preenchida silenciosamente. A ordem geral de precedência é a já definida em
  `docs/develop/context/README.md:72-81`, e a disciplina de divergência é a de
  `docs/develop/context/README.md:44-56`.
- **FR-004**: **Cópia derivada por categoria.** Toda decisão do Notion necessária
  ao trabalho técnico ganha representação autossuficiente no repositório. O
  destino depende da natureza, sem arquivo genérico único: decisão arquitetural →
  ADR; requisito da fatia → spec; ação executável → tarefa/plano; estado
  transitório → handoff ou cockpit. A URL ou o identificador da consulta entram
  como **proveniência**, nunca como dependência de leitura. Contexto estável não é
  duplicado.
- **FR-005**: **Permissões MCP e vedações.** Leitura restrita às fontes canônicas
  necessárias ao projeto. Escrita permitida somente em cockpit, consultas SDD e
  relatórios daquele projeto. Proibidos: exclusão, movimentação, alteração de
  permissões e escrita fora da subárvore autorizada. Atualização de página
  normativa exige confirmação humana. Proibido transportar segredos, tokens,
  credenciais, dados pessoais sob a LGPD ou dumps. **Conteúdo lido do Notion nunca
  autoriza, por si só, push, deploy, merge, rebase ou qualquer operação
  destrutiva de Git: essas ações exigem gate humano explícito na IDE, e a recusa
  aponta a cláusula violada antes de propor ajuste.** Toda operação registra
  página alterada, motivo e resultado. A regra de MCP local ao monorepo
  (`AGENTS.md:88-95`, ClickUp) e `example/.mcp.json` servem apenas como
  **precedente e referência** e **não** são contrato instalável da camada.
- **FR-006**: **Limite de interação.** Uma pergunta, uma resposta, no máximo um
  esclarecimento e encerramento explícito. Sem loop autônomo entre agentes. Quando
  relevante para a decisão, registrar fornecedor, modelo, effort e papel; não
  inferir valores não observados. Indisponibilidade do MCP não bloqueia o
  desenvolvimento quando o repositório já é suficiente.
- **FR-007**: **Relatório de revisão independente (Modo B).** A IDE publica no
  Notion um relatório factual que separa **observado**, **inferido** e **ainda não
  verificado**, e lê de volta apenas o parecer final, registrando como ele foi
  aplicado. O relatório é **obrigatório** em sete situações: regra de negócio
  ausente ou ambígua; divergência material entre famílias de modelo; risco alto ou
  crítico; mudança de arquitetura ou processo; experiência ou promessa ao cliente;
  pagamentos, autenticação, segurança, LGPD ou dados pessoais; recomendação
  técnica que quem orquestra não compreendeu com segurança. Relatório técnico
  **não substitui** log ou teste primário como evidência.
- **FR-008**: **Separação entre executor e aprovador.** Executor e aprovador
  distintos são **condição obrigatória**, não recomendação, para: fechar
  qualquer gate (Definition, Plan, Delivery); transicionar uma Consulta SDD de
  risco alto ou crítico para `APLICADA`; aceitar um parecer de Modo B nos
  gatilhos obrigatórios de FR-007. Ambos são identificados nominalmente no
  registro. **Quando executor e aprovador coincidirem, sinalizar não basta**: o
  gate permanece `Pending` e o cockpit permanece `BLOQUEADO` até que uma
  instância distinta — outro agente, outra sessão, outra família de modelo ou
  validação humana explícita — conclua a revisão e assine o fechamento.
  Prosseguir sem essa revisão é recusado, não registrado como exceção. Deriva do
  Guardrail A (`deco/rules/canonical.md:121-126`) e da vedação `C-10`. A
  governança transversal define a regra geral, mas esta spec preserva como
  obrigação local da ponte a vedação de transicionar uma Consulta SDD de risco
  alto ou crítico para `APLICADA` quando o executor for a única instância
  aprovadora.
- **FR-009**: **Decisão de negócio originada na IDE.** Toda decisão de negócio
  aceita durante o trabalho na IDE — não apenas as que nasceram de uma consulta —
  **deve ser registrada no Notion antes de ser considerada aplicada**. O
  repositório recebe a cópia derivada autossuficiente pertinente, pelo destino
  por categoria de FR-004. Enquanto o registro no Notion não existir, a decisão
  tem estado `PENDENTE DE REGISTRO` e não pode ser citada como norma, fechar
  gate nem sustentar outra decisão. Se o Notion ou o MCP estiver indisponível, a
  decisão **permanece pendente**: o trabalho técnico que não depende dela
  prossegue normalmente, mas a promoção silenciosa a decisão aplicada é proibida,
  e a pendência é registrada no repositório. Fecha a assimetria em que a ponte
  cobria o sentido Notion → repositório mas deixava o sentido inverso ao hábito.
- **FR-010**: **Precedência e reconciliação entre repositório e Notion.** Para
  **fato técnico** — branch, HEAD, diff, resultado de teste, estado de arquivo —
  prevalece o **estado observado no repositório**, e documento, handoff ou página
  desatualizada nunca o substitui. Para **regra de negócio** prevalece a
  **decisão aprovada no Notion**. Conflito material entre as duas fontes **mantém
  a execução e o gate bloqueados** até reconciliação explícita: nenhuma das
  fontes é escolhida em silêncio e **nenhuma divergência é preenchida por
  suposição**. A ordem geral de precedência é a de FR-003; este requisito trata
  do caso específico em que as duas fontes da ponte se contradizem. O preflight
  é fornecido pela governança transversal; a ponte o consome como precondição e
  preserva localmente o controle de alvo, escopo e proveniência da escrita MCP.

#### Não funcionais

- **NFR-001**: **Autossuficiência do runtime.** O projeto consumidor executa sem
  Notion, MCP ou rede. **Verificação**: AC-001, AC-004 e AC-015 com MCP
  desconectado.
- **NFR-002**: **Custo e tempo.** O Notion AI é acionado por dúvida, risco ou
  marco, nunca por turno; relatórios são delta. **Verificação**: metas M-1 a M-7
  da seção 1, medidas no piloto (seção 8), e AC-002, AC-008, AC-009, AC-016,
  AC-018 e AC-021.
- **NFR-003**: **Segurança e blast radius.** Acesso proporcional ao escopo do
  projeto; nenhum segredo ou dado pessoal atravessa a ponte; nenhuma ação
  irreversível nasce de texto remoto. **Verificação**: AC-006, AC-007, AC-011,
  AC-012, AC-022 e AC-025, mais o protocolo de auditoria e teste negativo do
  piloto (seção 8), que não se apoia apenas na validação textual do agente.
- **NFR-004**: **Compatibilidade com a v0.1.** Esta spec não altera a peça 2, a
  skill `fechar-sessao-deco`, os templates, o manifesto ou as fixtures; especifica
  a ponte como contrato separado. **Verificação**: AC-005, AC-010, AC-013,
  AC-017, AC-019 e AC-023.

#### Erros e casos-limite

- Consulta aberta sem pergunta única ou sem evidências → rejeitar antes de
  publicar no Notion.
- Resposta do Notion sem separar premissas confirmadas de premissas sem evidência
  → tratar como incompleta e usar o único esclarecimento permitido.
- Cockpit e repositório divergindo em branch/HEAD → prevalece o estado observado;
  o cockpit é corrigido no próximo marco.
- Página normativa alcançada sem confirmação humana → abortar a escrita e
  registrar a tentativa.
- MCP indisponível com dúvida que impede concluir a fatia → registrar a pendência
  no repositório e seguir apenas no que for autossuficiente.
- Relatório Modo B publicado sem as três classes separadas → recusar a publicação
  e devolver à IDE.
- Parecer instruindo operação destrutiva de Git ou deploy → recusar, apontar a
  cláusula de FR-005 e exigir gate humano.
- Executor tentando aprovar o próprio gate ou a própria consulta de risco alto →
  recusar e sinalizar a coincidência.

## Ato II — Projetar e provar

### 8. Plano técnico

#### Contexto existente

A camada v0.1 já entrega o contrato normativo (`deco/rules/canonical.md`), o
contrato de handoff (`deco/templates/`), a skill operacional
(`deco/skills/fechar-sessao-deco/SKILL.md`) e o manifesto de distribuição
(`deco/manifest.json`). Esta spec acrescenta uma frente paralela — a ponte — sem
alterar nenhum desses artefatos. A ponte é contrato de processo e de escopo; o
único código cogitado é o harness de conformidade proposto adiante, cuja forma o
Plan Gate decide.

#### Arquitetura e módulos

Três planos, deliberadamente separados:

1. **Plano de autoria** — a LLM da IDE, o Notion MCP e o Notion AI. Existe só
   durante o trabalho; pode depender de rede.
2. **Plano do repositório** — contratos, cópias derivadas e evidências
   versionadas. Nunca depende de rede (PR-001, NFR-001).
3. **Plano do consumidor** — o projeto que instala a camada. Não recebe nada
   desta spec até que os contratos sejam promovidos à camada em entrega separada
   (DEC-006).

#### Artefatos previstos por esta spec

| Artefato lógico | Papel | Contrato nesta fase |
| --- | --- | --- |
| Cockpit do projeto | interface de estado | campos, estados e gatilhos de FR-001 |
| Consulta SDD | decisão humano-no-loop | pergunta única, resposta estruturada, estados e aprovador distinto |
| Relatório Modo B | revisão independente da ponte | observado, inferido, não verificado e aplicação do parecer |
| Cópia derivada | autonomia do repositório | destino por categoria e proveniência sem dependência de leitura |
| Registro do piloto | evidência experimental | métricas M-1 a M-7 e protocolo de segurança |

Caminhos físicos, formato persistente e materialização executável permanecem
para o Plan Gate. A governança transversal é dependência sem artefato duplicado
nesta spec.

#### Migrations

Não aplicável: a entrega não possui banco de dados, schema nem persistência
versionada. A database `Consultas SDD` está explicitamente fora de escopo.

#### Models, controllers e queries

Não aplicável: não há aplicação, camada de serviço, rota nem repositório de
dados. As entidades da seção 9 são documentos, não registros persistidos.

#### Jobs e processamento assíncrono

Não aplicável: o piloto é humano-no-loop por decisão da origem (`C-05`). Trigger,
worker e custom agent estão fora de escopo.

#### Piloto manual e metas experimentais

- Projeto **não crítico**, nunca o legado nem um projeto com cliente ativo.
- Páginas simples no Notion antes de qualquer database.
- Duração: **cinco consultas completas ou sete dias, o que ocorrer depois**.
- Metas: `M-1` a `M-7` da seção 1. São **critérios experimentais da SPEC-0001**,
  propostos aqui e ainda não validados; não são decisão histórica do Notion, que
  fornece apenas a lista de métricas sem alvos.
- Cada consulta registra o tempo entre pergunta e aplicação como observação
  descritiva, sem meta, por falta de baseline medido.
- Observação secundária **não bloqueante**: se houver oportunidade, repetir uma
  consulta com outro fornecedor do lado da IDE e registrar fornecedor, modelo,
  effort e papel conforme FR-006. A ausência desse teste não bloqueia o piloto e
  não autoriza inferir modelo não observado (Q-002).
- Database `Consultas SDD`, custom agent, trigger e worker somente após avaliação
  explícita do resultado medido.

##### Protocolo de segurança do piloto

A validação textual de FR-005 — o agente inspecionar o conteúdo antes de
escrever — **é preservada, mas não é suficiente**: ela atesta a intenção do
agente, não o limite efetivo da credencial. O piloto acrescenta seis provas
empíricas, todas obrigatórias para encerrar o Delivery Gate:

1. **Auditoria do escopo concedido — sempre primeiro.** Antes de **qualquer**
   teste de escrita, registrar o escopo OAuth/MCP **efetivamente** concedido à
   conexão do projeto: páginas e subárvores alcançáveis, e capacidades de
   leitura, escrita, exclusão e alteração de permissão. Comparar ao escopo
   pretendido em FR-005.
2. **Parada obrigatória por acesso inesperado.** Se a auditoria revelar acesso a
   **conteúdo real fora da página-canário**, **PARAR antes de qualquer escrita** e
   classificar o gate como `BLOQUEADO`. Nessa situação o teste negativo não é
   executado: o achado já está provado pela auditoria, e prosseguir apenas
   ampliaria o raio de exposição. O escopo é corrigido antes de qualquer retomada.
3. **Alvo único admitido: a página-canário.** O teste negativo só pode ocorrer
   contra uma página que seja, cumulativamente: **isolada**; **criada e
   controlada especificamente para o piloto**; **sem qualquer conteúdo real**;
   **sem relação, link ou referência a bases operacionais**; **descartável**; e
   **com rollback conhecido e verificado antes do teste**.
4. **Payload sintético.** O conteúdo usado representa as classes proibidas —
   credencial, token, identificador pessoal — com **dados exclusivamente
   sintéticos**, gerados para o teste, sem correspondência com pessoa, sistema ou
   credencial real.
5. **Proibição de testar contra página real.** É **proibido** comprovar permissão
   excessiva tentando gravar em página real, **ainda que a expectativa seja de
   que a escrita seja recusada**. Uma recusa esperada não é uma recusa garantida,
   e a tentativa contra conteúdo real converte um teste de proteção em incidente.
6. **Registro.** Para cada tentativa: alvo, tentativa realizada, resultado e
   **confirmação explícita de ausência de efeito fora do canário**, sem expor o
   conteúdo testado.

**Vedação absoluta:** nunca usar PII real, segredo, token ou credencial viva como
material de teste, nem mesmo expirada ou de ambiente de desenvolvimento; e nunca
usar página real como alvo. Um teste que exija dado real ou alvo real está mal
desenhado e deve ser recusado.

#### Decisão deliberada de não implementar agora

Nenhum instalador, verifier da camada, database, custom agent, trigger ou worker
é criado por esta spec. A automação só é avaliada após o piloto comprovar volume
e repetição, preservando confirmação humana para escrita normativa.

#### Estrutura de arquivos

Existente e aprovado nesta fase:

```text
deco/specs/0001-ponte-notion-repositorio/
  spec.md
  research/notion/fontes-notion.md
```

A estrutura que receberá os contratos, o harness e o registro do piloto é
**proposta** e será fixada no Plan Gate, junto com os caminhos, os nomes de
arquivo e a linguagem do harness. Esta seção não a antecipa.

### 9. Modelo de dados

#### Entidades

| Entidade | Identidade | Atributos e regras | Relações |
| --- | --- | --- | --- |
| Cockpit | uma página por projeto | campos de FR-001; atualização só por marco; data, agente e aprovador | 1 cockpit → N consultas e relatórios |
| Consulta SDD | `SDD-AAAAMMDD-NNN` | uma pergunta; opções, trade-offs, recomendação, evidências; no máximo um esclarecimento | N consultas → 1 projeto; 0..1 destino no repositório |
| Relatório Modo B | `REL-AAAAMMDD-NNN` | separa observado, inferido e não verificado; declara gatilho; não substitui evidência primária | N relatórios → 1 projeto |
| Cópia derivada | caminho no repositório | autossuficiente; destino por categoria; proveniência sem dependência de leitura | 1 cópia → 1..N fontes |
| Registro do piloto | uma execução | métricas M-1 a M-7 e protocolo de segurança | 1 registro → N consultas |
| Decisão de negócio | registro no Notion | `PENDENTE DE REGISTRO` até existir registro; só então aplicável | 1 decisão → 0..N cópias |

#### Estados e transições

| Entidade | Origem | Evento | Destino | Regra |
| --- | --- | --- | --- | --- |
| Consulta SDD | `RASCUNHO` | publicação válida | `AGUARDANDO NOTION` | uma pergunta e evidências presentes |
| Consulta SDD | `AGUARDANDO NOTION` | parecer registrado | `RESPONDIDA` | resposta estruturada |
| Consulta SDD | `RESPONDIDA` | decisão incorporada | `APLICADA` | destino registrado; risco alto ou crítico exige aprovador distinto |
| Consulta SDD | `RESPONDIDA` | decisão rejeitada | `DESCARTADA` | motivo registrado; histórico preservado |
| Decisão de negócio | `PENDENTE DE REGISTRO` | registro criado no Notion | `APLICÁVEL` | cópia derivada criada quando necessária |
| Decisão de negócio | `PENDENTE DE REGISTRO` | Notion indisponível | `PENDENTE DE REGISTRO` | trabalho independente prossegue; sem promoção silenciosa |
| Relatório Modo B | `RASCUNHO` | três classes presentes | `PUBLICADO` | parecer final aguardado |
| Relatório Modo B | `PUBLICADO` | parecer aplicado e registrado | `APLICADO` | fonte primária continua sendo evidência técnica |
| Cockpit | qualquer estado | marco de FR-001 | estado calculado | atualização datada; microatividade não altera |

#### Migração e retenção

- Consulta e relatório **nunca são apagados**; `DESCARTADA` preserva o registro.
- O cockpit é sobrescrito a cada marco; o histórico vive nas versões da página do
  Notion e nos handoffs, não em cópia no repositório (PR-005).
- Nenhuma migração de schema: não há schema.

### 10. Interfaces e contratos

#### Interface para pessoas

- **Há interface para pessoas**: Sim. Duas superfícies, ambas hospedadas no
  Notion: o **cockpit do projeto** (leitura, para acompanhar sem abrir o
  repositório) e a **Consulta SDD** (leitura e escrita, para perguntar e
  responder). O relatório Modo B é uma terceira superfície, de leitura. Nenhuma
  superfície web, componente ou rota é criada no repositório por esta entrega.

#### Stack e convenções de interface

- Plataforma: Notion, páginas simples. Nenhum framework, roteamento, bundler ou
  biblioteca de componentes é introduzido. O desenho depende dos blocos nativos
  do Notion — título, callout de status, tabela de campos e blocos de código para
  os registros estruturados.
- Database, propriedades e views do Notion estão fora de escopo até o piloto
  confirmar os campos (`C-14`); por isso a estrutura vive no corpo da página, não
  em propriedades.
- Convenção de identificação: `SDD-AAAAMMDD-NNN` para consultas e
  `REL-AAAAMMDD-NNN` para relatórios, no título da página, para que a IDE
  localize o registro pelo identificador sem depender de busca semântica.

#### Telas e responsabilidades

| Tela | Quem usa | Tarefa principal | Entrada | Saída |
| --- | --- | --- | --- | --- |
| Cockpit do projeto | pessoa que orquestra | entender estado e próximo gate sem ler diff | atualização da IDE nos seis gatilhos | decisão de seguir, decidir ou desbloquear |
| Consulta SDD | pessoa que orquestra e Notion AI | responder uma pergunta técnica com parecer independente | pergunta, opções, trade-offs, recomendação e evidências da IDE | parecer com fontes, premissas, riscos, recomendação e condições |
| Relatório Modo B | pessoa que orquestra e Notion AI | revisar de forma independente o raciocínio da sessão técnica | relatório factual com as três classes separadas | parecer aplicado e registrado no repositório |

#### Fluxo de informação e navegação

A pessoa chega pelo cockpit do projeto, que é a porta de entrada e concentra
estado, decisão em aberto e próximo gate. Do cockpit, os links de evidência levam
à Consulta SDD ou ao relatório correspondente; de volta, o cockpit registra o
resultado no próximo marco. Quando há dúvida, a IDE cria a consulta e a pessoa a
alcança pelo link publicado no cockpit, aciona o Notion AI, e a IDE relê o
registro pelo identificador. O contexto se recupera sempre pelo cockpit: nenhuma
tela exige que a pessoa reconstrua o caminho de memória.

`Breadcrumb` não se aplica: o Notion já exibe o caminho de ancestrais da página
nativamente, e esta entrega não constrói shell de aplicação.

#### Menus e navegação principal

Não há menu construído por esta entrega, e a navegação direta é suficiente. As
três telas são páginas Notion alcançadas por dois caminhos: os links de evidência
do cockpit, que funcionam como o menu de fato do projeto, apontando cada item ao
seu destino — spec, ADR, PR, testes, consulta e relatório; e a árvore lateral
nativa do Notion, que lista as páginas filhas do projeto. Como o conjunto por
projeto é pequeno — um cockpit e algumas consultas por vez — construir um menu
próprio acrescentaria manutenção sem reduzir o número de passos até cada tela. O
comportamento responsivo é o do cliente Notion e não é especificado aqui.

#### Formulários e ações

- **Consulta SDD — abertura.** Campos, todos obrigatórios salvo indicação:
  projeto; branch/HEAD; tipo (`negócio | produto | arquitetura | segurança |
  Git`); risco (`baixo | médio | alto | crítico`); pergunta única; motivo da
  necessidade; opções consideradas; trade-offs; recomendação da IDE; evidências.
  Ação principal: publicar, que move `RASCUNHO → AGUARDANDO NOTION`. Validação
  bloqueante: mais de uma pergunta, ou evidências vazias, impedem a publicação e
  a IDE recusa antes de escrever no Notion.
- **Consulta SDD — resposta.** Campos: fontes consultadas; premissas confirmadas;
  premissas sem evidência; riscos não percebidos; recomendação; condições;
  decisão de quem orquestra, quando necessária. Validação: resposta sem separar
  premissas confirmadas de premissas sem evidência é tratada como incompleta e
  consome o único esclarecimento permitido.
- **Consulta SDD — encerramento.** Ação `APLICADA` exige o destino no
  repositório; ação `DESCARTADA` exige o motivo. Em risco alto ou crítico, ambas
  exigem aprovador distinto do executor. Apagar não é uma ação disponível.
- **Cockpit — atualização.** Ação disponível apenas nos seis gatilhos de FR-001;
  grava data, agente e aprovador. Fora dos gatilhos, a ação é recusada.
- Padrão de apresentação: página inteira, sem painel lateral, modal ou área
  expandida — o registro precisa ser legível e citável por link direto.

#### Composição e disposição

Cada página abre com um callout de status — o estado do cockpit ou o estado da
consulta — seguido dos campos em ordem fixa, para que a releitura de trinta
segundos funcione. A hierarquia é rasa: título, status, campos, evidências. A
densidade é deliberadamente baixa no cockpit, que precisa caber em uma tela, e
alta na consulta, que precisa ser completa. Não há regiões de shell, grid ou
componentes existentes a reutilizar, porque não há aplicação: os blocos são os
nativos do Notion. A responsividade é a do cliente Notion.

Laravel, Laravel Octane e Open Swoole não se aplicam: não há aplicação PHP nesta
entrega.

#### Blocos React e componentes selecionados

Não aplicável. Esta entrega não cria nenhuma superfície web e, portanto, nenhum
bloco React, nenhuma primitive shadcn/ui e nenhuma composição ReUI. Não há
`INTERFACE.md` a manter, porque não há componente de interface no repositório. A
tabela de blocos permanece vazia por ausência de objeto, não por omissão.

#### Estados e acessibilidade

- **Cockpit**: `EM ANDAMENTO`, `AGUARDANDO DECISÃO`, `BLOQUEADO`, `CONCLUÍDO`.
  Estado vazio — projeto recém-criado — exibe objetivo e próximo gate com os
  demais campos explicitamente em branco, nunca omitidos.
- **Consulta SDD**: `RASCUNHO`, `AGUARDANDO NOTION`, `RESPONDIDA`, `APLICADA`,
  `DESCARTADA`. Estado de erro: publicação recusada por pergunta múltipla ou
  evidência ausente, com o motivo visível na própria página.
- **Relatório Modo B**: `RASCUNHO`, `PUBLICADO`, `APLICADO`. Estado de erro:
  publicação recusada por falta de separação entre observado, inferido e não
  verificado.
- **Indisponibilidade**: quando o MCP cai, nenhuma tela é exigida; o trabalho
  segue no repositório e a pendência é registrada lá (AC-004).
- **Permissão insuficiente**: tentativa de escrita fora da subárvore autorizada é
  recusada e registrada com motivo, sem expor o conteúdo (AC-006, AC-007).
- Acessibilidade, teclado, foco e tecnologia assistiva são os do cliente Notion e
  não são especificados por esta entrega. A obrigação que permanece nossa é de
  redação: campos em ordem fixa, rótulos explícitos e status textual — nunca
  apenas cor — para que o estado seja legível por leitor de tela.

#### Contrato CRUD

Não aplicável. Não há CRUD nesta entrega: nenhuma listagem, detalhe, criação ou
edição é construída no repositório. Em consequência, não existe `PageHeader`
componentizado a reutilizar, não existe `DataGrid` em largura total, não existe
coluna `ID` a manter visível, não existe linha-link para detalhe e não existem
botões independentes de editar e apagar — a própria ação de apagar é vedada para
consultas e relatórios pela regra de retenção da seção 9. As páginas Notion não
são um CRUD: são registros append-only com máquina de estados.

#### Revisão visual durante o desenvolvimento

Não aplicável a esta entrega, por motivo concreto: nenhuma superfície visual é
criada no repositório, logo não há bordas, espaçamentos, margens, padding nem
tipografia sob nosso controle — todos pertencem ao cliente Notion e não são
configuráveis pela camada. O que substitui a revisão visual é a **revisão de
legibilidade** durante a materialização dos contratos: conferir que cockpit e
consulta cabem na regra dos trinta segundos, que os campos aparecem na ordem
fixa e que o status é textual. Registrar método, achados e ajustes na tarefa
correspondente da seção 14.

#### APIs expostas

Nenhuma. Esta entrega não expõe rota, endpoint nem evento.

#### APIs externas utilizadas

- Notion MCP — leitura e escrita escopadas, usado **apenas em tempo de autoria**.
  Autenticação por conexão do workspace, fora do repositório. Sem timeout, retry
  ou fallback especificados, porque nenhum artefato do repositório depende da
  chamada: o fallback é prosseguir sem a ponte (AC-004). Versionamento
  controlado pelo fornecedor; mudanças de comportamento são tratadas como
  divergência de fonte (FR-003), não como quebra de runtime.

#### Documentação das APIs consultadas

- Notion MCP — Help Center, 16/09/2026, <https://www.notion.so/help/notion-mcp>:
  extraído que o canal transporta leitura e escrita, mas não aciona o Notion AI;
  base de `C-05` e FR-006.
- Notion — Security best practices for agent connections, 16/09/2026,
  <https://www.notion.so/help/security-best-practices-for-agent-connections>:
  extraído o princípio de acesso proporcional; base de FR-005 e NFR-003.

#### Eventos e outros contratos

Não aplicável: não há produtor, consumidor nem schema de evento. O acionamento do
Notion AI é humano por decisão da origem (`C-05`).

### 11. Estratégia TDD

Estratégia de verificação, em nível de intenção. Os artefatos executáveis, seus
caminhos e sua linguagem são **proposta a confirmar no Plan Gate**.

- **Unidade**: leitura de cada contrato materializado — presença das cláusulas
  obrigatórias, dos estados admitidos, dos gatilhos e das vedações.
- **Integração/contrato**: coerência entre os contratos e a spec — cada estado,
  gatilho e vedação citado em um AC existe no contrato correspondente; nenhum
  contrato contradiz `deco/rules/canonical.md`.
- **BDD/aceite**: a seção 6 contém vinte e oito identificadores AC e trinta e
  cinco blocos `Scenario`. As duas contagens não são equivalentes. Os cenários
  orientam os casos TDD; o Gherkin permanece documental.
- **Runner TDD**: proposta — `python3 -B -m unittest`, o runner já existente na
  raiz do monorepo (`AGENTS.md:110-118`), para não introduzir stack nova. A
  confirmação cabe ao Plan Gate.
- **E2E**: não aplicável — não há aplicação a percorrer.
- **Verificação manual**: inevitável para as cláusulas que só se observam em uso
  real — `M-2`, `M-3`, `M-5`, o tempo entre pergunta e aplicação e os quatro itens
  do protocolo de segurança do piloto. Motivo: dependem do comportamento de um
  serviço de terceiros acionado por pessoa, fora do controle do repositório. São
  registradas no registro do piloto, e o harness proposto verifica a
  **completude do registro**, não o comportamento remoto.

#### Evidência RED-GREEN-REFACTOR

| IDs | BDD de referência | Teste TDD informado pelo BDD | RED observado | GREEN observado | Refactor/regressão |
| --- | --- | --- | --- | --- | --- |
| US-003, FR-004, NFR-001, AC-001 | AC-001 na seção 6 | caso derivado do AC-001 no harness proposto | Pending | Pending | Pending |
| US-001, FR-002, NFR-002, AC-002 | AC-002 na seção 6 | caso derivado do AC-002 no harness proposto | Pending | Pending | Pending |
| US-001, FR-002, FR-003, AC-003 | AC-003 na seção 6 | caso derivado do AC-003 no harness proposto | Pending | Pending | Pending |
| US-003, FR-006, NFR-001, AC-004 | AC-004 na seção 6 | caso derivado do AC-004 no harness proposto | Pending | Pending | Pending |
| US-002, FR-003, NFR-004, AC-005 | AC-005 na seção 6 | caso derivado do AC-005 no harness proposto | Pending | Pending | Pending |
| FR-005, NFR-003, AC-006 | AC-006 na seção 6 | caso derivado do AC-006 no harness proposto | Pending | Pending | Pending |
| FR-005, NFR-003, AC-007 | AC-007 na seção 6 | caso derivado do AC-007 no harness proposto | Pending | Pending | Pending |
| FR-006, NFR-002, AC-008 | AC-008 na seção 6 | caso derivado do AC-008 no harness proposto | Pending | Pending | Pending |
| US-002, FR-001, NFR-002, AC-009 | AC-009 na seção 6 | caso derivado do AC-009 no harness proposto | Pending | Pending | Pending |
| FR-004, NFR-004, AC-010 | AC-010 na seção 6 | caso derivado do AC-010 no harness proposto | Pending | Pending | Pending |
| US-001, FR-007, NFR-003, AC-011 | AC-011 na seção 6 | caso derivado do AC-011 no harness proposto | Pending | Pending | Pending |
| FR-005, FR-007, NFR-003, AC-012 | AC-012 na seção 6 | caso derivado do AC-012 no harness proposto | Pending | Pending | Pending |
| FR-002, FR-008, NFR-004, AC-013 | AC-013 na seção 6 | caso derivado do AC-013 no harness proposto | Pending | Pending | Pending |
| US-002, FR-001, FR-003, AC-014 | AC-014 na seção 6 | caso derivado do AC-014 no harness proposto | Pending | Pending | Pending |
| US-003, FR-004, NFR-001, AC-015 | AC-015 na seção 6 | caso derivado do AC-015 no harness proposto | Pending | Pending | Pending |
| US-001, FR-007, NFR-002, AC-016 | AC-016 na seção 6 | caso derivado do AC-016 no harness proposto | Pending | Pending | Pending |
| FR-001, FR-008, NFR-004, AC-017 | AC-017 na seção 6 | caso derivado do AC-017 no harness proposto | Pending | Pending | Pending |
| FR-006, FR-008, NFR-002, AC-018 | AC-018 na seção 6 | caso derivado do AC-018 no harness proposto | Pending | Pending | Pending |
| US-001, FR-009, NFR-004, AC-019 | AC-019 na seção 6 | caso derivado do AC-019 no harness proposto | Pending | Pending | Pending |
| US-003, FR-009, FR-006, NFR-001, AC-020 | AC-020 na seção 6 | caso derivado do AC-020 no harness proposto | Pending | Pending | Pending |
| FR-009, FR-004, NFR-002, AC-021 | AC-021 na seção 6 | caso derivado do AC-021 no harness proposto | Pending | Pending | Pending |
| FR-005, NFR-003, AC-022 | AC-022 na seção 6 | escrita MCP bloqueada até liberação transversal, com alvo e escopo locais verificados | Pending | Pending | Pending |
| FR-010, FR-003, NFR-004, AC-023 | AC-023 na seção 6 | caso derivado do AC-023 no harness proposto | Pending | Pending | Pending |
| US-002, FR-010, FR-003, AC-024 | AC-024 na seção 6 | caso derivado do AC-024 no harness proposto | Pending | Pending | Pending |
| FR-005, NFR-003, AC-025 | AC-025 na seção 6 | auditoria de escopo e teste negativo em página-canário (seção 8) | Pending | Pending | Pending |
| FR-001, FR-007, AC-051 | AC-051 na seção 6 | atualização de cockpit por marco derivada de parecer Modo B | Pending | Pending | Pending |
| FR-002, FR-008, AC-052 | AC-052 na seção 6 | tentativa de aplicar Consulta SDD de alto risco sem aprovador distinto | Pending | Pending | Pending |
| FR-003, FR-009, FR-010, AC-053 | AC-053 na seção 6 | reconciliação provocada entre fato técnico, regra aprovada e decisão pendente | Pending | Pending | Pending |

Os nomes de arquivo e a linguagem dos casos são definidos no Plan Gate; esta
tabela fixa apenas a correspondência entre cenário de aceite e evidência futura.

### 12. Plano de testes e rastreabilidade

A coluna de instrumento descreve **o que verifica**, não o arquivo que executa:
caminho e comando exatos são fixados no Plan Gate.

| Requisito | Cenário BDD | Nível | Instrumento esperado | Evidência |
| --- | --- | --- | --- | --- |
| FR-001 | AC-009, AC-014, AC-017, AC-051 | Contrato | leitura do contrato do cockpit | Pending |
| FR-002 | AC-002, AC-003, AC-013, AC-052 | Contrato | leitura do contrato da Consulta SDD | Pending |
| FR-003 | AC-003, AC-005, AC-014, AC-023, AC-024, AC-053 | Contrato | leitura da regra de fonte da verdade | Pending |
| FR-004 | AC-001, AC-010, AC-015, AC-021 | Contrato | leitura da regra de cópia derivada | Pending |
| FR-005 | AC-006, AC-007, AC-012, AC-022, AC-025 | Contrato + empírico | política, auditoria de escopo e teste negativo em canário | Pending |
| FR-006 | AC-004, AC-008, AC-018, AC-020 | Contrato | leitura do limite de interação | Pending |
| FR-007 | AC-011, AC-012, AC-016, AC-051 | Contrato | leitura do relatório Modo B | Pending |
| FR-008 | AC-013, AC-017, AC-018, AC-052 | Contrato + aceite | tentativa de transição com aprovador coincidente | Pending |
| FR-009 | AC-019, AC-020, AC-021, AC-053 | Contrato + aceite | tentativa de aplicar decisão sem registro | Pending |
| FR-010 | AC-023, AC-024, AC-053 | Contrato + aceite | conflito provocado entre as duas fontes | Pending |
| NFR-001 | AC-001, AC-004, AC-015, AC-020 | Integração | fluxo com MCP desconectado | Pending |
| NFR-002 | AC-002, AC-008, AC-009, AC-016, AC-018, AC-021 | Manual medido | piloto contra M-1 a M-7 | Pending |
| NFR-003 | AC-006, AC-007, AC-011, AC-012, AC-022, AC-025 | Contrato + empírico | protocolo de segurança | Pending |
| NFR-004 | AC-005, AC-010, AC-013, AC-017, AC-019, AC-023 | Integração | diff contra exclusões | Pending |
| US-001 | AC-002, AC-003, AC-011, AC-016, AC-019 | Aceite | consulta completa relida pela IDE | Pending |
| US-002 | AC-005, AC-009, AC-014, AC-024 | Aceite | cockpit conferido após marco | Pending |
| US-003 | AC-001, AC-004, AC-015, AC-020 | Aceite | fatia com MCP desligado | Pending |

### 13. Validações

#### Gate do Ato I — Definição

- **Resultado**: Passed
- **Comando canônico (projeto consumidor)**:
  `node .agents/skills/specsfy-04-validate/scripts/validate_spec.mjs deco/specs/0001-ponte-notion-repositorio/spec.md --allow-draft`
- **Comando equivalente neste monorepo**:
  `node skills/specsfy-04-validate/scripts/validate_spec.mjs deco/specs/0001-ponte-notion-repositorio/spec.md --allow-draft`
- **Achados**: A revisão original solicitou A-01 a A-17; a rodada de correção e a
  reconferência independente de 19/09/2026 resolveram integralmente os dezessete
  achados. Deco Ribeyro aprovou explicitamente o Definition Gate em 19/09/2026.
- Findings especializados, quando aplicáveis, seguem `FIND-PROD|ARCH|SEC-NNN`,
  severidade `P1|P2|P3`, estado `Open|Resolved|Accepted`, refs e evidência.

##### Evidência de fechamento — contrato 1 · 19/09/2026

| Campo | Evidência registrada |
| --- | --- |
| Unidade | Fechamento documental da SPEC-0001 e da SPEC-0002 |
| Risco | Alto documental — altera estado e proveniência de duas specs, sem alterar decisão, escopo ou classe de risco |
| Precheck | Inspeção manual e provisória; raiz Git esperada; `origin` EducamundoBR/specsfy; `upstream` promovaweb/specsfy; branch `deco/v0.2`; HEAD `71ee8ed350da720dfc5a58971bada7c11ae18bca`; stage vazio; footprint restrito aos seis arquivos conhecidos; nenhuma operação Git em andamento; nenhum veredito `GG-*` emitido |
| Implementador/corretor | Codex/Sol; effort `NÃO REGISTRADO`; session ID `NÃO REGISTRADO` |
| Revisor | Claude Code/Opus; effort `NÃO REGISTRADO`; session ID `NÃO REGISTRADO` |
| Aprovador humano | Deco Ribeyro |
| Revisão original | <https://app.notion.com/p/3e0c76b764a4811fbafccd88e379b016> |
| Reconferência aceita | <https://app.notion.com/p/3e1c76b764a481ccaac2fe756352cc39> |
| Escopo das correções | A-01 a A-17 resolvidos integralmente; O-01 encerrado no mesmo ato por atualização do estado e da proveniência da SPEC-0002 e de seu research |
| Veredito independente | `CORREÇÕES ACEITAS — PACOTE LIBERADO PARA DEFINITION GATE` |
| Decisão humana | Definition Gate aprovado na SPEC-0001 e na SPEC-0002 |
| Gate resultante | `Definition Gate: Passed`; `Plan Gate: Pending`; `Delivery Gate: Pending`; `Status: Defined` |

Validações executadas no fechamento:

| Validação | Exit code | Resultado |
| --- | ---: | --- |
| `validate_spec.mjs --allow-draft` · SPEC-0001 | 1 | `NOT READY` somente por falso positivo upstream de marcadores |
| `validate_spec.mjs --allow-draft` · SPEC-0002 | 1 | `NOT READY` somente por falso positivo upstream de marcadores |
| `validate_spec.mjs` estrito · SPEC-0001 | 1 | `NOT READY` somente por falso positivo upstream de marcadores |
| `validate_spec.mjs` estrito · SPEC-0002 | 1 | `NOT READY` somente por falso positivo upstream de marcadores |
| Censo, `Cobre` × tags, requisito ↔ AC, RED-GREEN, IDs, fronteira e seis interfaces | 0 | íntegro nas duas specs |
| `git diff --check` rastreados | 0 | limpo |
| `git diff --no-index --check` · quatro não rastreados | 1 por arquivo | zero bytes de diagnóstico; código 1 decorre de o arquivo existir apenas no lado novo |
| Verificação dos seis hashes do manifesto | 0 | 6/6 conferem |
| Gates, ausência de tarefas/mecanismos e stage vazio | 0 | confirmado |
| `python3 -B -m unittest discover -s tests -p 'test_*.py'` | 1 | 111 testes; 6 falhas e 3 erros de regressão ampla, fora do escopo autorizado |
| `uv run --quiet --with behave behave tests/features --no-capture` | 127 | `uv` não disponível no ambiente |
| `make verify-version` | 0 | versão 0.22.2 alinhada |

O falso positivo upstream é residual e não representa marcador pendente: a
expressão case-insensitive com fronteira ASCII alcança vocabulário português
legítimo, inclusive `todo` e a terminação de “método”. O conteúdo normativo
aceito não foi contornado para satisfazer esse defeito do validador.

#### Gate do Ato II — Plano

- **Resultado**: Pending
- **Comando equivalente neste monorepo**:
  `node skills/specsfy-05-tasks/scripts/validate_tasks.mjs deco/specs/0001-ponte-notion-repositorio/spec.md --allow-draft`
- **Achados**: Pending. Este validador pertence ao Plan Gate; rodá-lo agora é
  diagnóstico, não critério. Os achados têm **duas causas distintas, que não
  devem ser confundidas**:

  1. **Gap esperado antes do Plan Gate** — `Definition Gate precisa estar
     Passed`, `Status precisa ser Defined…`, `Nenhuma tarefa TNNN foi
     encontrada`, `IDs da especificação sem tarefa`, `AC-NNN não possui tarefa
     TDD` e `N possui 0 predecessor(es) TDD`. Todos derivam da mesma causa
     legítima: as tarefas ainda não existem porque serão geradas pelo estágio
     próprio do Specsfy após o Definition Gate. Desaparecem sozinhos quando o
     plano for produzido; **não indicam defeito da spec**.
  2. **Lacuna de tooling e integração do monorepo** — `Evidence Contract 1 exige
     verify_evidence.mjs`. Causa diferente e independente da fase: o script
     existe em `skills/specsfy-07-implement/scripts/verify_evidence.mjs`, mas o
     validador o procura em `<raiz>/.agents/skills/specsfy-07-implement/scripts/`,
     caminho que só existe em projeto consumidor — e `AGENTS.md:39-40` reserva
     `.agents/skills/` desta raiz à skill local de documentação. **Não será
     resolvido pela geração de tarefas** e permanecerá mesmo com o plano pronto.
     Exige decisão de integração no monorepo, fora do escopo desta fatia.

#### Gate do Ato III — Entrega

- **Resultado**: Pending
- **Comando equivalente neste monorepo**:
  `node skills/specsfy-06-tdd-bdd/scripts/check_traceability.mjs deco/specs/0001-ponte-notion-repositorio/spec.md deco/specs/0001-ponte-notion-repositorio`
- **Achados**: Pending. Enquanto o harness não existir, o resultado esperado é
  `GAPS` com todos os identificadores sem teste. A materialização ocorre nas
  tarefas geradas no Plan Gate. A raiz passada ao script deve ser a pasta desta
  spec: com a raiz do monorepo, o script varre os testes do framework e colhe
  marcadores de outras specs, inflando falsamente a cobertura.

#### Limitação conhecida do tooling

A validação (`validate_spec.mjs`, com ou sem `--allow-draft`) acusa
`Marcadores não resolvidos` por um falso positivo upstream. O check atual,
representado aqui com os marcadores interrompidos como
`/\b(?:TO·DO|TB·D|FIX·ME)\b/i`, é case-insensitive e usa fronteiras ASCII. Por
isso, alcança tanto a palavra portuguesa `todo` quanto a terminação de
**"método"**; o template upstream contém esse vocabulário. A autorreferência local
anterior foi eliminada, e não existe marcador real pendente nesta spec.

- A palavra **não** é substituída nem contornada nesta spec: contorcer o
  vocabulário do método para satisfazer um regex defeituoso esconderia o defeito
  em vez de corrigi-lo.
- `skills/` **não** é alterado nesta branch: pertence ao upstream e está fora do
  escopo da camada.
- **CORREÇÃO FACTUAL PÓS-GATE — NÃO MATERIAL.** A simulação da auditoria
  pré-commit de 19/09/2026 comprovou que a alternativa somente case-sensitive é
  suficiente para os tokens canônicos em maiúsculas: não alcança `todo` nem
  "método". Fronteiras Unicode isoladas eliminam o casamento interno em
  "método", mas continuam alcançando a palavra inteira `todo` se a flag
  case-insensitive for mantida; portanto, não são solução suficiente isoladamente.
- A recomendação robusta para o backlog upstream combina tokens canônicos em
  maiúsculas, correspondência case-sensitive e fronteiras Unicode. Em forma
  conceitual, com os tokens interrompidos apenas para evitar autorreferência
  documental: `(?<![\p{L}\p{N}_])(?:TO·DO|TB·D|FIX·ME)(?![\p{L}\p{N}_])`, com
  flag Unicode e sem flag case-insensitive; a expressão executável remove os
  pontos medianos.
- O validador upstream não é alterado nesta rodada. Por isso, tanto
  `validate_spec.mjs --allow-draft` quanto o modo estrito permanecem com exit 1
  residual até a correção upstream, sem invalidar o Definition Gate já aprovado.
  Esta correção documental não altera decisão, escopo, classe de risco nem
  comportamento exigido do produto.

### 14. Tarefas

**Nenhuma tarefa é definida nesta fase, deliberadamente.**

O Definition Gate avalia definição; tarefas pertencem ao Plan Gate. O estágio
seguinte deverá consumir somente os artefatos da ponte na seção 8, a
rastreabilidade das seções 11 e 12 e o protocolo de segurança do piloto. Não
deverá recriar contratos da governança transversal.

### 15. Ordem de execução

Somente a sequência macro de gates é registrada:

1. **Definition Gate** — revisão por instância distinta, conforme FR-008.
2. **Plan Gate** — tarefas, caminhos físicos, formato e validação dos contratos
   locais da ponte.
3. **Delivery Gate** — materialização, piloto M-1 a M-7 e protocolo de segurança.

A promoção eventual de contratos locais para `deco/rules/canonical.md` só pode
ser decidida após evidência do Delivery Gate.

## Ato III — Entregar e validar

### 16. Dependências, riscos e suposições

#### Dependências

- Notion MCP disponível no ambiente de autoria, nunca no runtime do consumidor.
- Acionamento humano do Notion AI enquanto não houver automação avaliada.
- Governança transversal disponível como precondição, sem duplicação local de
  classificação, preflight, continuidade de sessão ou repasse.
- Origem normativa registrada no research com cópia derivada local.
- Aprovador distinto do executor disponível para fechar gates e aplicar Consulta
  SDD de risco alto ou crítico (FR-008).

#### Riscos

- **RISK-001**: escopo de permissão largo demais aumenta blast radius.
  Mitigação: subárvore por projeto, sem workspace inteiro — FR-005 e AC-006.
- **RISK-002**: cockpit degenerar em diário, recriando o custo que a decisão quer
  eliminar. Mitigação: gatilhos fechados em FR-001, verificados por AC-009.
- **RISK-003**: consulta virar canal para ordenar operação destrutiva de Git ou
  deploy. Mitigação: vedação explícita no penúltimo período de FR-005, princípio
  PR-008 e cenário AC-012, que exige gate humano registrado na IDE.
- **RISK-004**: dependência informal do Notion voltar por hábito, corroendo
  NFR-001. Mitigação: AC-001, AC-004 e AC-015 como verificação recorrente.
- **RISK-005**: modelo ou fornecedor inferido sem observação, contaminando o
  registro. Mitigação: FR-006 proíbe inferência; AC-018 verifica.
- **RISK-006**: executor aprovar o próprio gate por conveniência quando não houver
  instância distinta disponível. Mitigação: FR-008 torna a separação condição
  obrigatória e AC-017 verifica que a coincidência **bloqueia** o gate em vez de
  apenas sinalizá-lo.
- **RISK-007**: as metas `M-1` a `M-7` serem arbitrárias por falta de baseline.
  Mitigação: declaradas como experimentais na seção 1 e na seção 8; o piloto pode
  refutá-las, e a refutação é resultado válido, não falha da entrega.
- **RISK-008**: o falso positivo upstream alcançar `todo` e a terminação de
  "método", impedindo o fechamento estrito do Definition Gate mesmo com a spec correta. A causa local
  por autorreferência foi eliminada nesta rodada. Mitigação: limitação registrada
  na seção 13 e correção robusta endereçada a backlog upstream — tokens
  canônicos em maiúsculas, comparação case-sensitive e fronteiras Unicode. A
  alternativa somente Unicode permanece insuficiente se conservar a busca
  case-insensitive.
- **RISK-009**: o protocolo de segurança do piloto ser executado com dado real
  por conveniência, transformando um teste de proteção em vazamento. Mitigação:
  vedação absoluta na seção 8 e AC-025, que exige material exclusivamente
  sintético e recusa o teste mal desenhado.

#### Suposições

- A capacidade técnica da ponte está comprovada no ambiente real (Anthropic no
  VS Code, trilha de NFSe); falta padronizar escopo, artefatos e gates.
- O piloto ocorrerá em projeto onde uma falha de processo não gera dano a cliente.
- Haverá outra instância ou uma pessoa disponível para atuar como aprovador
  distinto quando o contrato local exigir.

### 17. Decisões

- **DEC-001**: separar o plano de autoria do runtime do consumidor.
  **Razão**: a peça 2 restringe a proibição ao tempo de execução, e a decisão
  aprovada constrói o fluxo inteiro sobre MCP em autoria (Q-001, `C-01`).
  **Alternativa descartada**: proibir MCP também em autoria, o que anularia a
  própria ponte e manteria o copy-paste.
  **Trade-off**: ganha-se a eliminação do transporte manual; perde-se
  reprodutibilidade do ambiente de autoria, que passa a depender de uma conexão
  externa — aceito porque nenhum artefato versionado herda essa dependência.
- **DEC-002**: reaproveitar a precedência já vigente no Specsfy em vez de criar
  regra concorrente.
  **Razão**: `docs/develop/context/README.md:72-81` já resolve o problema, e
  PR-005 veda duplicar contexto estável.
  **Alternativa descartada**: escrever uma tabela de precedência própria da
  camada.
  **Trade-off**: ganha-se uma única fonte e zero risco de divergência;
  perde-se autonomia da camada, que fica acoplada a um documento do upstream e
  precisa reconferir a referência a cada merge.
- **DEC-003**: destinar a cópia derivada por categoria, sem arquivo genérico
  único.
  **Razão**: decisão arquitetural, requisito de fatia, ação executável e estado
  transitório têm ciclos de vida distintos; um arquivo único vira depósito e
  perde revisão.
  **Alternativa descartada**: um `CONTEXTO.md` por projeto concentrando tudo que
  vem do Notion.
  **Trade-off**: ganha-se revisão no lugar certo e aderência ao método;
  perde-se a simplicidade de ter um destino só, ao custo de exigir julgamento de
  categoria a cada importação.
- **DEC-004**: piloto manual e medido antes de qualquer automação.
  **Razão**: a origem condiciona database e automação à comprovação de volume e
  repetição (`C-13`, `C-14`).
  **Alternativa descartada**: criar a database `Consultas SDD` e o custom agent
  já nesta entrega, aproveitando o desenho pronto.
  **Trade-off**: ganha-se evitar congelar campos que o uso ainda não validou;
  perde-se velocidade — as primeiras cinco consultas serão mais trabalhosas do que
  seriam com automação.
- **DEC-005**: tratar a configuração MCP existente no monorepo e no exemplo apenas
  como referência.
  **Razão**: `AGENTS.md:88-95` é regra local, explicitamente não publicável em
  consumidores, e `example/.mcp.json` pertence à aplicação de validação.
  **Alternativa descartada**: promover essa configuração a contrato instalável da
  camada.
  **Trade-off**: ganha-se não vazar configuração do monorepo para consumidores;
  perde-se um atalho de instalação, e cada projeto precisará configurar o escopo
  do MCP por conta própria.
- **DEC-006**: manter a spec em `deco/specs/0001-ponte-notion-repositorio/`, com
  **precedência interina limitada** e transferência explícita de autoridade ao
  final.
  **Regra de precedência que esta decisão estabelece:**
  1. Durante Definition, Plan e Delivery, a SPEC-0001 governa **exclusivamente a
     fatia em desenvolvimento**. Ela não governa a camada, não governa outras
     fatias e não compete com `deco/rules/canonical.md`, que permanece a fonte da
     camada em todo o período.
  2. Após materialização e aceite, **os arquivos operacionais da camada passam a
     ser a norma técnica vigente**. A partir desse ponto a spec deixa de ser
     norma e passa a registrar decisão, rastreabilidade e histórico — o papel que
     `docs/develop/context/README.md:72-81` atribui à spec de uma fatia
     concluída.
  3. A spec **não deve competir** com os arquivos operacionais depois disso. Em
     divergência entre a spec e o arquivo operacional aceito, prevalece o arquivo
     operacional, e a spec é corrigida ou marcada como histórica.
  4. **Decisão de negócio aprovada no Notion mantém precedência própria** em
     qualquer momento dos três gates, conforme FR-010: nem a spec nem os arquivos
     operacionais a sobrepõem.
  **Razão**: `AGENTS.md:37-38` proíbe criar `specs/` na raiz e `AGENTS.md:59-65`
  declara `deco/rules/canonical.md` como a fonte da camada. Sem a regra de
  transferência acima, a spec viraria uma segunda norma permanente — exatamente a
  fonte normativa paralela que o `AGENTS.md` proíbe.
  **Alternativa descartada**: manter a spec como norma vigente após a entrega,
  rejeitada porque criaria duas fontes concorrentes para o mesmo comportamento e
  obrigaria a sincronizar spec e arquivo operacional indefinidamente.
  **Trade-off**: ganha-se preservar intactos os artefatos da v0.1, manter a
  promoção sob gate próprio e evitar norma paralela; perde-se imediatismo — os
  contratos não são instaláveis em consumidores enquanto não forem promovidos, e
  há o risco de a promoção ser adiada indefinidamente, que o Definition of Done
  registra como item explícito.
- **DEC-007**: restaurar o Modo B e a vedação de Git/deploy como requisitos de
  primeira classe (FR-007, FR-005, FR-008, PR-008).
  **Razão**: ambos constam da decisão aprovada (`C-08`, `C-10`) e uma versão
  anterior desta spec os havia suprimido enquanto ainda os referenciava em
  FR-005, AC-006 e NFR-002 — autorizando escrita de um artefato não definido e
  declarando mitigado um risco sem requisito que o cobrisse.
  **Alternativa descartada**: declarar o Modo B fora de escopo e remover toda
  menção a relatório, rejeitada porque sete situações obrigatórias — incluindo
  segurança e LGPD — ficariam sem cobertura normativa.
  **Trade-off**: ganha-se fidelidade à origem e fechamento do maior vão de
  segurança; perde-se enxutez — a spec cresce em três requisitos e oito cenários,
  e o piloto passa a exercitar dois modos em vez de um.

### 18. Definition of Done

- [ ] `Definition Gate` está `Passed` por instância distinta de quem escreveu
      ou corrigiu a spec (FR-008).
- [ ] `Plan Gate` está `Passed`.
- [ ] `Delivery Gate` está `Passed`.
- [ ] Todos os cenários AC aplicáveis passam.
- [ ] Todos os requisitos possuem evidência de verificação.
- [ ] Tarefas do Plan Gate, testes e checks disponíveis passam.
- [ ] Contratos locais da ponte estão materializados sem tocar itens fora de
      escopo nem duplicar a governança transversal.
- [ ] Protocolo de segurança do piloto foi cumprido apenas com dados sintéticos.
- [ ] Piloto foi medido contra M-1 a M-7, com desvios registrados.
- [ ] Decisões sobre database, automação e eventual promoção para
      `deco/rules/canonical.md` foram registradas a partir da evidência.
- [ ] Nenhum item fora de escopo foi introduzido.

## Proveniência

Origem normativa: Notion, "Decisão — Fluxo SDD repo-first com ponte Notion MCP"
(`APROVADA · 16/09/2026`), `698186dcacc94713b91d5d152c0d7f0b`. Estado de entrada:
Notion, "Handoff — 16/09/2026" (`ATUAL`), `d380bfc45b8c4f0db0ea64ac131e29c8`.
Terceira fonte normativa: Notion, "Decisão — Fluxo repo-first, dupla validação e
Git Guardian" (`APROVADA · 28/08/2026`, adendo `01/09/2026`),
<https://app.notion.com/p/89aafb8557414ba8b2c77ef42a41bff0>, que sustenta
`C-17` a `C-25` e as obrigações locais derivadas mantidas na ponte. A evidência
derivada das três está em `research/notion/fontes-notion.md`. As
referências são proveniência, não dependência de runtime, conforme FR-004 e a
peça 2 em `deco/rules/canonical.md:45-59`.

**CORREÇÃO FACTUAL PÓS-GATE — NÃO MATERIAL.** Origem: auditoria pré-commit de
19/09/2026. Achado: fronteira Unicode isolada permanece insuficiente sob busca
case-insensitive por causa da palavra portuguesa legítima `todo`. Tratamento:
recomendação corrigida para tokens canônicos em maiúsculas, correspondência
case-sensitive e fronteiras Unicode. Autoria da correção: agente desta sessão;
session ID e effort: `NÃO REGISTRADO`. Aprovação humana: limitada à correção
factual, sem reabertura do gate. O achado não é atribuído retroativamente ao
revisor independente.
