# Especificação integrada: Governança transversal do SDD assistido por IA

| Campo | Valor |
| --- | --- |
| Formato | Specsfy/2.0 |
| ID | SPEC-0002 |
| Slug | 0002-governanca-sdd |
| Status | Defined |
| Effort | 3 |
| Effort updated at | 2026-09-16 |
| Effort rationale | Contrato de processo transversal com doze requisitos funcionais, trinta e oito identificadores AC e cinquenta e seis blocos `Scenario`; sem código de produto. Revisar após o Definition Gate. |
| ClickUp Task | |
| Milestones | |
| Definition Gate | Passed |
| Plan Gate | Passed |
| Delivery Gate | Pending |
| Review state | APROVADO |
| Evidence Contract | 1 |
| Interface para pessoas | Não — a governança é processo e não cria superfície própria; cockpit e Consulta SDD pertencem à SPEC-0001 e são consumidos como interface declarada |
| Atualizada em | 2026-09-21 |

> **Decisão da rodada documental, Definition Gate aprovado.** A separação entre
> a ponte Notion ↔ repositório e a governança transversal foi proposta no handoff
> anterior, decidida e executada documentalmente nesta sessão de continuação. A
> decisão operacional é evidenciada pelo pacote atual e pela revisão independente,
> não pelo handoff anterior. Ambas as specs estão `Defined`, com Definition Gate
> `Passed`, Plan Gate `Passed` por decisão humana de Deco em 21/09/2026 e
> Delivery Gate `Pending`.
>
> **Migração documental executada.** A recomposição da ponte e a retirada da
> governança transversal da SPEC-0001 foram concluídas; esta spec tornou-se a
> fonte normativa da governança, preservadas as interfaces semânticas da ponte.
> O registro histórico, com IDs de origem, destino, tratamento, evidências e
> contagens, está no research. O README e seu hash no manifesto foram atualizados.
>
> **Nada aqui está implementado.** Git Guardian, Session Guardian, skills de
> revisão, artefatos de repasse e Contrato de Entrega são **especificados**, não
> construídos. Nenhum existe como arquivo, script ou skill neste repositório.
>
> **Decisão local de roteamento.** Estas specs de definição da camada distribuível
> vivem em `deco/specs/<NNNN>-<slug>/`; o estado está no cabeçalho e nos gates,
> sem segmento físico de estado nesta versão. A exceção local foi aprovada no
> Definition Gate e não altera o roteamento de projetos consumidores.

## Ato I — Definir

### 1. Problema e resultado

#### Problema

O trabalho assistido por IA nesta organização já tem regras — revisão cruzada
entre famílias de modelo, preflight antes de operação de Git, handoff em formato
delta, proibição de modelos não validados em papéis críticos — mas elas vivem
espalhadas entre decisões do Notion, conversas de sessão e uma spec de produto
que as absorveu por falta de lugar melhor. O efeito prático é triplo: cada
sessão renegocia quando revisar e quem aprova; o custo de revisão cresce com o
número de prompts em vez de com o risco; e não há critério verificável para
dizer que algo terminou — "pronto" é usado indistintamente para código que
passou no teste, artefato que chegou ao destino e trabalho que alguém conferiu.
Três funcionalidades já foram declaradas prontas e eram inalcançáveis por quem
ia usá-las (`G-19`).

#### Resultado desejado

Uma governança transversal, verificável e agnóstica de harness e de fornecedor,
que determine: quanto de revisão cada mudança merece; quem pode aprovar o quê;
qual controle precede a escrita; como o contexto atravessa sessões sem
transcript; e quando um trabalho está `PRONTO`, `ENTREGUE` ou `ACEITO`, sem que
uma palavra esconda as outras duas.

#### Métricas de sucesso

Metas **experimentais desta spec**, propostas aqui e ainda não validadas. Não são
decisão histórica de nenhuma fonte; existem para o piloto confirmar ou refutar.

| # | Métrica | Meta experimental |
| --- | --- | --- |
| M-1 | Unidades revisadas cuja classificação de risco foi registrada antes da execução | 100% |
| M-2 | Revisões disparadas por prompt isolado em vez de por pacote | 0 |
| M-3 | Gates fechados sem a evidência mínima de FR-011 | 0 |
| M-4 | Sessões abertas sem contexto ativo localizável por `SESSION_CURRENT` | 0 |
| M-5 | Entregas declaradas `PRONTO` que não alcançaram `ENTREGUE` na mesma rodada | registrar e explicar cada caso |
| M-6 | Ações irreversíveis executadas sem gate humano declarado | 0 |
| M-7 | Rodadas de revisão por unidade até aprovação | mediana ≤ 2 |

### 2. Research e esclarecimentos

#### Researchs executados

- **R-001** [critical] A matriz de risco de quatro níveis e a exigência de
  revisão antes e depois no risco alto são decisão aprovada, não proposta —
  Verdict: verified — Confidence: high — Evidence: research/notion/fontes-notion.md#g-01 — Budget: 1/2
- **R-002** [critical] O termo "Session Guardian" não tem definição normativa em
  nenhuma fonte aprovada; aparece apenas no handoff — Verdict: verified —
  Confidence: high — Evidence: research/notion/fontes-notion.md#g-24 — Budget: 1/2
- **R-003** [critical] Existe evidência empírica de que "pronto" não implica
  "entregue" nem "aceito" — Verdict: verified — Confidence: high —
  Evidence: research/notion/fontes-notion.md#g-19 — Budget: 1/2
- **R-004** [material] O mecanismo executável do Git Guardian não está
  materializado em nenhum repositório conhecido — Verdict: verified —
  Confidence: high — Evidence: research/notion/fontes-notion.md#g-05 — Budget: 1/2
- **R-005** [material] O contrato do MusicFlow é precedente de projeto, com
  regras de interface e stack que não se generalizam — Verdict: verified —
  Confidence: medium — Evidence: research/notion/fontes-notion.md#g-25 — Budget: 1/2

#### Fontes e contexto consultados

- Notion — cinco páginas registradas em `research/notion/fontes-notion.md`,
  tabela "Fontes", com título, URL, status e data de leitura.
- Repositório — `deco/rules/canonical.md:15-43` (peça 1, contrato de handoff),
  `:61-75` (peça 3, protocolo de decisão), `:77-87` (peça 4, régua de validação),
  `:121-132` (guardrails A e B).
- Repositório — `deco/templates/HANDOFF.md` e `deco/templates/session-handoff.md`
  (ponteiro e snapshot de cinco campos); `deco/fixtures/handoff/valid/`,
  `missing-field/` e `broken-pointer/` (fixtures que materializam somente
  contexto válido, campo ausente e ponteiro quebrado; não cobrem todas as
  verificações do Session Guardian).
- Repositório — `deco/specs/0001-ponte-notion-repositorio/spec.md`, integralmente,
  e seu research derivado.
- Repositório — `AGENTS.md:35-65` e `docs/develop/context/README.md:72-81`
  (precedência das fontes).

#### Documentação consultada

- Specsfy — `skills/templates/Spec.md` e
  `skills/specsfy-04-validate/scripts/validate_spec.mjs`, lidos em 16/09/2026:
  contrato estrutural Specsfy/2.0 e regra de cobertura mínima de três cenários
  por identificador.
- Nenhuma documentação de fornecedor externo foi consultada para esta spec.

#### Artefatos de pesquisa armazenados

- `deco/specs/0002-governanca-sdd/research/notion/fontes-notion.md`: cinco
  fontes, cláusulas `G-01` a `G-33` separadas por natureza (decisão aprovada,
  precedente, inferência de arquitetura, questão aberta), mapeamento
  cláusula → ID, registro da migração executada SPEC-0001 → SPEC-0002 e lista de itens
  deliberadamente não importados. Sem reprodução integral, sem segredo, sem dado
  pessoal.
- Nenhum outro artefato externo. Fontes do repositório são citadas por caminho e
  linha, não copiadas.

#### Dúvidas respondidas

- **Q**: o Session Guardian já está definido em alguma decisão aprovada?
  → **A**: não. O termo aparece nominalmente apenas no handoff de 16/09/2026.
  Sua definição foi **delimitada nesta rodada** pelas verificações que a
  convenção de handoff já aprovada exige (`G-24`), sem inventar
  responsabilidades novas.
- **Q**: o contrato do MusicFlow pode ser adotado como norma transversal?
  → **A**: não. É precedente de um projeto, com regras de interface gráfica,
  domínio musical e stack específicos. Foram generalizados apenas os sete campos,
  as condições de parada, o rollback verificado e as quatro regras permanentes
  em vocabulário neutro (`G-21`, `G-25`).
- **Q**: por que prefixar os vereditos dos dois verificadores?
  → **A**: porque Git Guardian e Session Guardian respondem perguntas diferentes
  sobre objetos diferentes. Compartilhar o rótulo `BLOQUEADO` faria um relatório
  ambíguo sobre qual controle barrou o quê (`G-26`).

#### Dúvidas abertas

- Nenhuma bloqueante para o Definition Gate. Três questões permanecem abertas nas
  fontes e estão registradas como tal, com o tratamento adotado declarado:
  dono e prazo da materialização do Git Guardian (`G-28`, tratado por RISK-012);
  procedimento quando não há segunda instância disponível para aprovar (`G-29`,
  tratado por FR-003, que bloqueia em vez de liberar); limiar objetivo de
  "mudança material" (`G-30`, adotado por analogia e não validado em uso).

### 3. Escopo e atores

#### Incluído

Classificação de risco; roteamento de modelo, effort e revisão; separação entre
implementador e aprovador; Git Guardian e preflight; Session Guardian; catálogo
de skills de revisão e perfis; contrato de repasse entre agentes com Review
Request, Review Verdict e Correction Report; `CURRENT` da rodada ativa; máquina de
estados da revisão; Contrato de Entrega; estados `PRONTO`, `ENTREGUE` e `ACEITO`;
evidência, proveniência, rollback e resíduos proibidos; critérios de escalonamento
ao Notion ou ao humano; limites de autonomia e tratamento de ações irreversíveis;
interfaces com a SPEC-0001 e com specs de produto.

#### Fora de escopo

- **Implementação** de qualquer mecanismo aqui especificado: skills, scripts,
  ponteiros, diretórios de rodada, verificadores. Esta spec define contratos.
- **Materialização do Git Guardian.** Permanece dependência externa (DEC-006).
- **Cockpit, Consulta SDD, Modo B e protocolo de escrita escopada no Notion.**
  São da SPEC-0001 e consumidos como interface; esta spec não os redefine.
- **Escolha de fornecedor ou modelo concreto.** Apenas papéis lógicos (`G-06`).
- **Regras de interface gráfica, domínio de produto ou stack de teste.** Não são
  transversais (`G-25`).
- **Tarefas e ordem de execução detalhada.** Matéria do Plan Gate.
- **Redesenho da separação ou nova migração normativa.** A migração documental
  desta rodada já foi executada; qualquer mudança material permanece sujeita a
  nova rodada e ao Definition Gate.

#### Atores

- **Implementador**: executa a unidade de trabalho, classifica o risco inicial,
  grava o Review Request e o Correction Report. Não aprova o próprio trabalho.
- **Revisor**: instância distinta, em contexto novo e inicialmente read-only.
  Recebe o pacote, não a conclusão do implementador. Grava o Review Verdict.
- **Git Guardian**: papel verificador do estado do repositório antes de escrita.
  Read-only por padrão. Não implementa nem executa a operação que autoriza.
- **Session Guardian**: papel verificador do contexto de sessão na abertura,
  durante e no fechamento. Não guarda memória própria, não substitui o Git
  Guardian e não decide conteúdo técnico.
- **Pessoa que orquestra**: decide negócio, aprova risco alto e irreversibilidade,
  e é o aprovador declarado do Contrato de Entrega quando o aceite é humano. Não
  precisa ler diff para exercer esse papel.

### 4. Princípios e restrições do projeto

- **PR-001**: revisão proporcional ao risco. O custo de verificação acompanha a
  consequência da mudança, não o seu tamanho nem o número de interações.
- **PR-002**: a unidade de revisão é um artefato coerente — spec, plano, ADR,
  diff, pacote de correções, testes ou gate. **Prompt individual nunca é unidade
  obrigatória de revisão** (`G-09`).
- **PR-003**: quem executa não aprova sozinho. O fechamento exige instância
  distinta da execução (`G-03`).
- **PR-004**: nenhuma escrita antes do preflight. O controle precede a ação, não
  a acompanha (`G-04`).
- **PR-005**: memória entre sessões vem de **arquivo curado por humano**, nunca
  de transcript bruto ou de compressão automática (`G-15`).
- **PR-006**: proveniência é **declarada, nunca inferida**. Harness, modelo,
  effort e session ID não observados persistem como `NÃO REGISTRADO`. O relatório
  pode explicar a ausência, mas não substituir esse token.
- **PR-007**: estado observado prevalece sobre documento. Handoff, registro ou
  página desatualizada nunca substitui o estado real verificado.
- **PR-008**: a governança é agnóstica de harness e de fornecedor. Papéis são
  lógicos e mapeados a implementações concretas fora desta spec (`G-06`, `G-16`).

### 5. Histórias de usuário

#### US-001 — Revisar na medida do risco (P1)

Como pessoa que orquestra, quero que cada mudança receba a revisão proporcional
ao seu risco, para não pagar revisão dupla em correção editorial nem aprovar uma
mudança de autenticação com autoverificação.

**Por que P1**: é a dor que originou a governança. Sem a matriz, ou se revisa
tudo — e o custo inviabiliza — ou não se revisa nada, e o risco aparece em
produção.
**Teste independente**: submeter duas mudanças, uma editorial e uma de
autenticação, e observar que só a segunda exige segunda família e gate humano.
**Requisitos**: FR-001, FR-002, FR-003

#### US-002 — Retomar uma sessão sem reconstruir contexto à mão (P1)

Como desenvolvedor, quero abrir uma sessão nova e encontrar o contexto ativo
íntegro e verificável, para não reconstruir o estado a partir de transcript nem
herdar decisões já superadas.

**Por que P1**: a amnésia entre sessões é o único modo de falha que o método base
não cobre sozinho (`deco/rules/canonical.md:38-40`). Sem o verificador, o
contrato de handoff existe mas ninguém garante que foi cumprido.
**Teste independente**: abrir sessão em um projeto com `SESSION_CURRENT` válido e
concluir a leitura de contexto sem abrir transcript.
**Requisitos**: FR-005, FR-008

#### US-003 — Saber se algo está realmente entregue (P1)

Como pessoa que orquestra, quero distinguir o que foi concluído, o que chegou ao
destino e o que foi conferido, para não descobrir depois que a entrega verde era
inalcançável.

**Por que P1**: há prova empírica de falha — três funcionalidades prontas em
código, verdes em teste e inalcançáveis por quem ia usá-las (`G-19`).
**Teste independente**: percorrer um contrato até `PRONTO` e confirmar que a
transição para `ENTREGUE` exige comprovação de alcance no destino.
**Requisitos**: FR-009, FR-010

#### US-004 — Não sofrer ação irreversível não autorizada (P1)

Como pessoa que orquestra, quero que nenhuma ação destrutiva ou externa aconteça
sem preflight e sem gate humano explícito, para que um engano de contexto não
vire perda de trabalho ou incidente.

**Por que P1**: o custo é assimétrico — uma revisão a mais custa minutos, um
`reset --hard` sobre trabalho de origem desconhecida custa a sessão inteira.
**Teste independente**: solicitar uma operação destrutiva com worktree suja de
origem desconhecida e observar o bloqueio.
**Requisitos**: FR-004, FR-012

### 6. Cenários BDD de aceite

#### AC-001 — Classificação de risco precede a execução

**Cobre**: FR-001, US-001, NFR-001

```gherkin
@FR-001 @US-001 @NFR-001 @AC-001
Feature: Risco declarado antes do trabalho

  Scenario: Unidade iniciada sem classificação
    Given uma unidade de trabalho prestes a ser executada
    And nenhuma classificação de risco registrada
    When a execução é iniciada
    Then a execução é recusada até o risco ser classificado e justificado
    And a classificação fica registrada junto da unidade
```

#### AC-002 — Risco baixo não exige segunda família

**Cobre**: FR-001, FR-002, NFR-001

```gherkin
@FR-001 @FR-002 @NFR-001 @AC-002
Feature: Proporcionalidade no risco baixo

  Scenario: Correção editorial sem alteração de comportamento
    Given uma leitura, formatação, correção editorial ou recálculo mecânico
    And nenhum gatilho de elevação automática presente
    When o executor conclui e roda as verificações existentes
    Then a autoverificação do executor basta
    And nenhuma revisão por segunda família é exigida
```

#### AC-003 — Elevação automática por natureza do assunto

**Cobre**: FR-001, NFR-003, US-004

```gherkin
@FR-001 @NFR-003 @US-004 @AC-003
Feature: Natureza eleva o risco, tamanho não o rebaixa

  Scenario: Mudança de uma linha que toca autenticação
    Given uma mudança pequena que altera permissão, autenticação, segredo, dado pessoal, migração de dados, produção ou histórico de Git
    When o risco é classificado
    Then a classificação é elevada automaticamente para alto ou crítico
    And o tamanho reduzido da mudança não rebaixa a classificação
```

#### AC-004 — Roteador seleciona a skill do gate corrente

**Cobre**: FR-002, FR-006, US-001

```gherkin
@FR-002 @FR-006 @US-001 @AC-004
Feature: Seleção da skill de gate

  Scenario: Unidade submetida no gate de definição
    Given uma spec submetida a revisão no gate de definição
    When o roteador classifica a unidade
    Then a skill selecionada é a de revisão de definição
    And o roteador declara se a revisão exigida é prévia, posterior ou ambas
```

#### AC-005 — Perfil compõe com o gate, sem criar skill nova

**Cobre**: FR-002, FR-006, NFR-001

```gherkin
@FR-002 @FR-006 @NFR-001 @AC-005
Feature: Composição em vez de multiplicação

  Scenario: Entrega que altera autenticação
    Given uma unidade no gate de entrega que altera autenticação
    When o roteador classifica a unidade
    Then a composição é a skill de entrega somada ao perfil de segurança, autenticação e privacidade
    And nenhuma skill nova é criada para essa combinação
    And o perfil não fecha o gate sozinho
```

#### AC-006 — Papel crítico é vedado a modelo não validado

**Cobre**: FR-002, FR-003, NFR-003

```gherkin
@FR-002 @FR-003 @NFR-003 @AC-006
Feature: Papéis vedados

  Scenario: Modelo não validado indicado para papel crítico
    Given um modelo novo, barato ou ainda não validado
    When ele é indicado como aprovador final de segurança, autoridade para operação destrutiva de histórico, responsável único por publicação ou revisor final de pagamento, autenticação ou dado pessoal
    Then a indicação é recusada
    And ele permanece autorizado para leitura, exploração, classificação, documentação mecânica, busca e terceira opinião não vinculante
    And a promoção exige benchmark documentado e decisão explícita
```

#### AC-007 — Papel lógico é mapeado a implementação concreta

**Cobre**: FR-002, NFR-002, NFR-004

```gherkin
@FR-002 @NFR-002 @NFR-004 @AC-007
Feature: Agnosticismo com rastreabilidade

  Scenario: Registro do roteamento de uma unidade
    Given uma unidade cujo trabalho foi roteado a papéis lógicos
    When o roteamento é registrado
    Then cada papel lógico aparece mapeado a harness, modelo, effort e data
    And a troca de nome ou versão do modelo não invalida o processo
    And todo valor não observado persiste como NÃO REGISTRADO, nunca inferido
```

#### AC-008 — Executor e aprovador coincidentes bloqueiam o gate

**Cobre**: FR-003, US-001, NFR-002

```gherkin
@FR-003 @US-001 @NFR-002 @AC-008
Feature: Separação obrigatória

  Scenario: Aprovador distinto assina o fechamento
    Given uma unidade cujo aprovador é distinto de quem executou
    When o gate é fechado
    Then o registro identifica nominalmente executor e aprovador
    And o gate pode passar a aprovado

  Scenario: Nenhuma segunda instância disponível
    Given uma unidade cujo executor é também o único aprovador disponível
    When o fechamento é tentado
    Then o fechamento é recusado
    And o gate permanece pendente até instância distinta revisar
    And sinalizar a coincidência não substitui a revisão
```

#### AC-009 — Revisor não recebe a conclusão como verdade

**Cobre**: FR-003, FR-006, NFR-002

```gherkin
@FR-003 @FR-006 @NFR-002 @AC-009
Feature: Independência do parecer

  Scenario: Pacote entregue ao revisor
    Given um pacote de revisão contendo spec, plano, diff, testes e critérios
    When o revisor assume a unidade
    Then ele abre contexto novo e inicialmente somente leitura
    And a conclusão do implementador é tratada como alegação a verificar, não como fato
    And os achados são devolvidos por severidade, com evidência e correção proposta
```

#### AC-010 — Aprovação sem evidência não fecha gate

**Cobre**: FR-003, FR-011, NFR-002

```gherkin
@FR-003 @FR-011 @NFR-002 @AC-010
Feature: Evidência como condição de fechamento

  Scenario: Veredito favorável sem teste, diff ou evidência
    Given um veredito favorável que não apresenta teste, diff nem evidência
    When o gate é submetido a fechamento
    Then o gate não fecha
    And a evidência mínima é exigida antes de qualquer aprovação
```

#### AC-011 — Preflight precede toda operação sensível

**Cobre**: FR-004, US-004, NFR-003

```gherkin
@FR-004 @US-004 @NFR-003 @AC-011
Feature: Controle antes da ação

  Scenario: Operação sensível solicitada
    Given uma escrita em disco, troca ou criação de branch, commit, operação de remote ou publicação
    When a operação é solicitada
    Then o preflight somente leitura é executado antes da operação
    And enquanto não houver mecanismo versionado, a inspeção manual produz exatamente PROVISORIAMENTE SEGURO, PROVISORIAMENTE CONDICIONAL ou PROVISORIAMENTE BLOQUEADO
    And a classificação provisória não é registrada como veredito GG
    And ações destrutivas, publicação e deploy aguardam o gate humano aplicável
```

#### AC-012 — Veredito do Git Guardian é explícito e prefixado

**Cobre**: FR-004, NFR-002

```gherkin
@FR-004 @NFR-002 @AC-012
Feature: Vocabulário sem ambiguidade

  Scenario: Mecanismo executável produz evidência formal
    Given o mecanismo executável versionado do Git Guardian
    When sua saída é anexada ao relatório
    Then o veredito é exatamente um entre GG-SEGURO, GG-CONDICIONAL e GG-BLOQUEADO
    And o registro declara estado observado, operações permitidas e operações bloqueadas
    And o prefixo distingue o veredito do emitido pelo Session Guardian

  Scenario: Inspeção manual sem mecanismo executável
    Given uma inspeção manual somente leitura do repositório
    And nenhuma saída do mecanismo executável anexada ao relatório
    When o resultado é registrado
    Then o resultado é exatamente um entre PROVISORIAMENTE SEGURO, PROVISORIAMENTE CONDICIONAL e PROVISORIAMENTE BLOQUEADO
    And nenhum veredito GG é emitido por narrativa
    And a unidade não se autodeclara liberada

  Scenario: Condição reversível observada por inspeção manual
    Given trabalho conhecido que exige branch safety, tag, patch, backup ou outra proteção reversível e verificável
    And nenhuma contradição ou origem desconhecida que exija bloqueio
    When a inspeção manual é executada
    Then a classificação é PROVISORIAMENTE CONDICIONAL
    And a proteção especificada é aplicada
    And a inspeção manual é repetida
    And somente após PROVISORIAMENTE SEGURO a análise documental continua no escopo já autorizado

  Scenario: Condição reversível observada pelo mecanismo executável
    Given trabalho conhecido que exige branch safety, tag, patch, backup ou outra proteção reversível e verificável
    And nenhuma contradição ou origem desconhecida que exija bloqueio
    When o mecanismo executável produz o resultado
    Then o veredito formal é GG-CONDICIONAL
    And a proteção especificada é aplicada
    And o preflight executável é repetido
    And somente após GG-SEGURO as operações declaradas podem prosseguir
```

#### AC-013 — Worktree de origem desconhecida bloqueia

**Cobre**: FR-004, US-004, NFR-003

```gherkin
@FR-004 @US-004 @NFR-003 @AC-013
Feature: Não limpar o que não se sabe de onde veio

  Scenario: Sujeira de autoria não identificada
    Given uma worktree suja cuja origem não pôde ser atribuída
    When a inspeção manual é executada sem mecanismo versionado
    Then a classificação é PROVISORIAMENTE BLOQUEADO
    And nenhuma operação de descarte, redefinição ou troca de branch é executada para limpar o estado
    And a saída recomenda preservar o trabalho antes de qualquer alteração

  Scenario: Mecanismo formal encontra sujeira de origem desconhecida
    Given uma worktree suja cuja origem não pôde ser atribuída
    And o mecanismo executável versionado está disponível
    When sua saída é anexada ao relatório
    Then o veredito formal é GG-BLOQUEADO
    And nenhuma alteração ocorre até o risco ser explicado e reconciliado
```

#### AC-014 — Abertura localiza exatamente um contexto ativo

**Cobre**: FR-005, US-002, NFR-002, NFR-005

```gherkin
@FR-005 @US-002 @NFR-002 @NFR-005 @AC-014
Feature: Entrada de sessão verificada

  Scenario: Projeto com ponteiro consistente
    Given um projeto com roteador canônico e SESSION_CURRENT indicando o contexto ativo
    When a sessão é aberta
    Then exatamente um contexto ativo é localizado por SESSION_CURRENT
    And projeto, branch e HEAD declarados são comparados com o estado observado
    And os cinco campos obrigatórios estão presentes
    And o contexto não está superado e o escopo corresponde à unidade ativa
    And o veredito é SG-VÁLIDO
    And a verificação ocorre sem acesso a rede ou a serviço externo

  Scenario: Exatamente dois contextos marcados ATUAL
    Given exatamente dois contextos marcados ATUAL
    When a sessão é aberta
    Then o veredito é SG-BLOQUEADO
    And nenhum contexto é escolhido silenciosamente

  Scenario: Divergência entre contexto declarado e estado observado
    Given um contexto cujo projeto, branch ou HEAD diverge sem explicação do estado observado
    When a sessão é aberta
    Then o veredito é SG-BLOQUEADO
    And a continuidade é recusada até a divergência ser reconciliada
```

#### AC-015 — Transcript não é fonte canônica

**Cobre**: FR-005, US-002, NFR-004

```gherkin
@FR-005 @US-002 @NFR-004 @AC-015
Feature: Quem cura a memória

  Scenario: Retomada por histórico bruto ou resumo automático
    Given uma sessão retomada por transcript gravado ou por resumo automático da conversa
    When esse conteúdo é oferecido como contexto do projeto
    Then ele não é aceito como fonte canônica
    And se for a única fonte disponível o veredito é SG-BLOQUEADO
    And a retomada exige o arquivo curado indicado por SESSION_CURRENT
```

#### AC-016 — Mudança material durante a sessão exige registro novo

**Cobre**: FR-005, FR-008, US-002

```gherkin
@FR-005 @FR-008 @US-002 @AC-016
Feature: Unidade ativa correspondente ao trabalho

  Scenario: Escopo deixa de corresponder ao contexto ativo
    Given uma sessão em andamento sobre uma unidade declarada
    When uma decisão, o escopo incluído ou excluído ou a classe de risco muda
    Then a mudança é classificada como MUDANÇA MATERIAL
    And o veredito é SG-BLOQUEADO
    And nenhuma atualização reversível da rodada atual resolve o bloqueio
    And uma nova rodada de revisão precisa ser criada e indicada por CURRENT antes de prosseguir
    And o contexto anterior não é reescrito para acomodar o novo escopo

  Scenario: Correção não material e reversível
    Given um contexto íntegro e identificável
    And a correção completa metadado, evidência ou proveniência sem alterar decisão, escopo incluído ou excluído nem classe de risco
    When a sessão é verificada
    Then o veredito é SG-CONDICIONAL
    And o registro é corrigido de forma reversível
    And SESSION_CURRENT continua indicando o único contexto ativo inequívoco
    And a verificação é repetida
```

#### AC-017 — Fechamento valida os cinco campos e o ativo único

**Cobre**: FR-005, US-002, NFR-002

```gherkin
@FR-005 @US-002 @NFR-002 @AC-017
Feature: Saída de sessão verificada

  Scenario: Fechamento com handoff completo
    Given uma sessão com mudança relevante prestes a ser encerrada
    When o contexto de encerramento é gravado
    Then os cinco campos estão presentes, incluindo o porquê de cada decisão
    And exatamente um contexto permanece ativo
    And o anterior é marcado como superado com indicação de substituição, sem ter seu conteúdo reescrito
    And snapshot e SESSION_CURRENT são atualizados de forma conjunta
```

#### AC-018 — Fechamento com estado não verificado é impedido

**Cobre**: FR-005, FR-011, NFR-002

```gherkin
@FR-005 @FR-011 @NFR-002 @AC-018
Feature: Nada declarado sem observação

  Scenario: Encerramento declarando estado que não foi observado
    Given um contexto de encerramento que declara branch, HEAD, stage, worktree ou evidência sem observação registrada
    When o fechamento é submetido
    Then o veredito é SG-BLOQUEADO
    And o fechamento é impedido até o estado ser observado e registrado

  Scenario: Decisão registrada sem o porquê
    Given um contexto de encerramento cujas decisões registram apenas o que foi decidido
    When o fechamento é submetido
    Then o fechamento é recusado
    And o porquê é exigido como campo obrigatório

  Scenario: Perda de contexto impede reconstrução segura
    Given compressão ou perda de contexto que impede reconstruir com segurança a unidade ativa
    When a continuidade é verificada
    Then o veredito é SG-BLOQUEADO
    And nenhuma retomada automática substitui o handoff estruturado

  Scenario: Terceira compactação atinge o limiar documentado
    Given duas compactações anteriores registradas na mesma sessão
    When a terceira compactação é necessária
    Then o veredito é SG-CONDICIONAL
    And uma nova sessão com handoff estruturado é aberta antes de continuar
    And a verificação é repetida no novo contexto
```

#### AC-019 — Session Guardian, review-handoff e Git Guardian não se confundem

**Cobre**: FR-005, FR-004, NFR-004

```gherkin
@FR-005 @FR-004 @NFR-004 @AC-019
Feature: Três fronteiras complementares

  Scenario: Relatório com contexto, repasse e repositório
    Given uma sessão que executou preflight de repositório, verificação de contexto e repasse de revisão
    When os resultados são registrados no mesmo relatório
    Then os vereditos de contexto usam SG-VÁLIDO, SG-CONDICIONAL ou SG-BLOQUEADO
    And os vereditos de repositório usam o prefixo GG
    And review-handoff administra Review Request, Review Verdict, Correction Report e rodada
    And nenhum dos três substitui os demais como condição de prosseguir
```

#### AC-020 — A unidade de revisão é o pacote, não o prompt

**Cobre**: FR-006, FR-007, NFR-001

```gherkin
@FR-006 @FR-007 @NFR-001 @AC-020
Feature: Pacote consolidado

  Scenario: Vários prompts compondo uma unidade coerente
    Given três prompts consecutivos que produzem uma única unidade coerente
    When o pacote de repasse é preparado
    Then é gravado exatamente um pedido de revisão consolidado
    And não são exigidas três revisões, uma por prompt
```

#### AC-021 — Review Request declara estado e proveniência, sem transcript

**Cobre**: FR-007, FR-011, NFR-002

```gherkin
@FR-007 @FR-011 @NFR-002 @AC-021
Feature: Repasse por pacote delta

  Scenario: Pedido de revisão gravado
    Given uma unidade pronta para revisão
    When o Review Request é gravado
    Then ele declara unidade, risco e justificativa, branch e HEAD, base e escopo do diff, arquivos, testes, decisões, dúvidas, fontes e restrições
    And declara harness, modelo, effort e session ID do implementador
    And nenhum histórico de conversa é colado no pacote
```

#### AC-022 — Review Verdict é artefato separado e assinado

**Cobre**: FR-007, FR-003, NFR-002

```gherkin
@FR-007 @FR-003 @NFR-002 @AC-022
Feature: Parecer com identidade própria

  Scenario: Veredito gravado pelo revisor
    Given uma unidade em revisão
    When o Review Verdict é gravado
    Then ele é artefato separado do Review Request
    And declara harness, modelo, effort e session ID do revisor
    And apresenta evidências, achados classificados de P0 a P3, veredito, condições e gate resultante

  Scenario: Request e verdict com a mesma identidade
    Given um Review Request e um Review Verdict com o mesmo session ID
    When a aprovação é submetida
    Then a aprovação é bloqueada
```

#### AC-023 — Correção acontece em lote, dentro da rodada

**Cobre**: FR-007, FR-008, NFR-001

```gherkin
@FR-007 @FR-008 @NFR-001 @AC-023
Feature: Ciclo de correção sem revisão por item

  Scenario: Parecer com vários achados
    Given um veredito com achados classificados de P0 a P3
    When o implementador aplica as correções
    Then as correções são aplicadas em lote
    And um Correction Report é gravado na mesma rodada, com achados tratados, correções aplicadas e achados não aplicados com justificativa
    And o mesmo revisor reconfere o lote uma única vez
    And nenhuma revisão é disparada após cada correção isolada
```

#### AC-024 — Exatamente uma rodada ativa

**Cobre**: FR-008, FR-005, NFR-002

```gherkin
@FR-008 @FR-005 @NFR-002 @AC-024
Feature: Rodada única

  Scenario: Ponteiro indicando mais de uma rodada ativa
    Given CURRENT indicando mais de uma rodada ativa
    When a revisão é iniciada
    Then o estado é rejeitado
    And nenhuma rodada é escolhida silenciosamente
    And a ambiguidade é reportada antes de qualquer parecer
```

#### AC-025 — Rodada concluída é imutável

**Cobre**: FR-008, NFR-002, NFR-004

```gherkin
@FR-008 @NFR-002 @NFR-004 @AC-025
Feature: Histórico de revisão preservado

  Scenario: Tentativa de editar rodada encerrada
    Given uma rodada com veredito aprovado ou reprovado
    When uma alteração no seu conteúdo é tentada
    Then a alteração é recusada
    And qualquer revisão adicional ocorre em rodada nova
```

#### AC-026 — Mudança material abre nova rodada

**Cobre**: FR-005, FR-008, NFR-001

```gherkin
@FR-005 @FR-008 @NFR-001 @AC-026
Feature: Fronteira entre correção e escopo novo

  Scenario: Escopo alterado durante a rodada
    Given uma rodada aguardando correções
    When uma decisão, o escopo incluído ou excluído ou a classe de risco muda
    Then a alteração é MUDANÇA MATERIAL
    And uma nova rodada é criada
    And CURRENT passa a indicar a nova rodada
    And a rodada anterior é encerrada sem ser reescrita
```

#### AC-027 — Contrato incompleto não dispara

**Cobre**: FR-009, US-003, NFR-001

```gherkin
@FR-009 @US-003 @NFR-001 @AC-027
Feature: Contrato de Entrega como pré-condição

  Scenario: Trabalho iniciado sem contrato completo
    Given um Contrato de Entrega sem um dos treze campos obrigatórios
    When o trabalho é solicitado
    Then o trabalho não é iniciado
    And o campo ausente é apontado antes de qualquer execução
```

#### AC-028 — `PRONTO` não implica `ENTREGUE`

**Cobre**: FR-010, US-003, FR-009

```gherkin
@FR-010 @US-003 @FR-009 @AC-028
Feature: Concluir não é alcançar o destino

  Scenario: Artefato concluído na origem e ausente no destino
    Given um artefato concluído com verificações internas verdes e evidência produzida
    And nenhuma comprovação de presença ou alcance no destino declarado
    When o estado é registrado
    Then o estado é PRONTO
    And o estado ENTREGUE é recusado até a presença no destino ser comprovada
    And declarar a unidade concluída sem essa comprovação é violação do contrato
```

#### AC-029 — `ENTREGUE` não implica `ACEITO`

**Cobre**: FR-010, US-003, NFR-002

```gherkin
@FR-010 @US-003 @NFR-002 @AC-029
Feature: Chegar ao destino não é ser aceito

  Scenario: Entrega comprovada e aceite pendente
    Given um artefato cuja presença no destino foi comprovada
    And nenhum registro de conferência pelo aprovador designado
    When o estado é registrado
    Then o estado é ENTREGUE
    And o estado ACEITO é recusado até o aprovador registrar aceite explícito

  Scenario: Aceite humano não aplicável
    Given um contrato em que o aceite humano não se aplica
    When o contrato é escrito
    Then quem ou qual verificação ocupa o papel de aprovador é declarado no próprio contrato, antes da execução
    And esse papel não é inferido depois da entrega
```

#### AC-030 — Regressão após a entrega não é escondida

**Cobre**: FR-010, FR-011, US-003

```gherkin
@FR-010 @FR-011 @US-003 @AC-030
Feature: Honestidade do estado

  Scenario: Regressão antes da entrega
    Given um artefato no estado PRONTO
    When uma regressão é detectada antes de alcançar o destino
    Then o estado passa para CORREÇÃO NECESSÁRIA
    And após correção, verificações internas verdes e nova evidência o estado volta para PRONTO

  Scenario: Reprovação depois de entregue
    Given um artefato no estado ENTREGUE
    When o aprovador reprova um critério no destino declarado
    Then o estado passa para ENTREGUE COM CORREÇÕES
    And o motivo e a correção necessária são registrados
    And a correção volta para a origem
    And após verificações internas verdes o estado volta para PRONTO
    And uma nova entrega é obrigatória para retornar a ENTREGUE
    And nenhuma transição direta para ACEITO é permitida

  Scenario: Regressão depois do aceite
    Given um artefato no estado ACEITO
    When uma regressão é detectada
    Then o estado passa para ACEITE REVOGADO
    And a unidade reabre como CORREÇÃO NECESSÁRIA com motivo e nova evidência obrigatórios
    And precisa percorrer novamente PRONTO, ENTREGUE e ACEITO
    And nenhuma transição direta para ACEITO é permitida

  Scenario: Validação humana anterior à main
    Given uma validação humana concluída antes de o artefato chegar à main declarada como destino
    When o estado de entrega é calculado
    Then a validação conta como autorização para entrega ou evidência prévia
    And o estado ACEITO permanece recusado até a conferência do artefato no destino
```

#### AC-031 — Resíduos proibidos e rollback verificado

**Cobre**: FR-009, FR-011, NFR-003

```gherkin
@FR-009 @FR-011 @NFR-003 @AC-031
Feature: Encerrar sem deixar rastro indevido

  Scenario: Entrega com resíduo proibido
    Given uma entrega que deixa dado falso, artefato inerte, nome divergente entre código e documentação ou arquivo temporário não declarado
    When a entrega é verificada
    Then a entrega é recusada até o resíduo ser removido ou declarado

  Scenario: Rollback declarado mas não verificado
    Given um contrato cujo rollback nomeia destino e comando de desfazer
    And nenhuma verificação da integridade do ponto de retorno
    When a execução é autorizada
    Then a autorização é recusada até o ponto de retorno ser verificado
```

#### AC-032 — Revisão verde não escala sem gatilho

**Cobre**: FR-012, NFR-001, NFR-005

```gherkin
@FR-012 @NFR-001 @NFR-005 @AC-032
Feature: Escalonamento por gatilho, não por hábito

  Scenario: Revisão técnica aprovada sem gatilho material
    Given uma revisão técnica com veredito favorável
    And nenhum gatilho de decisão de negócio, arquitetura ou processo transversal, risco alto, divergência material ou falta de compreensão segura
    When a rodada é encerrada
    Then nenhuma consulta externa é aberta
    And os artefatos permanecem no repositório
    And o trabalho prossegue sem depender de serviço externo
```

#### AC-033 — Ação irreversível exige parada e gate humano

**Cobre**: FR-012, US-004, NFR-003

```gherkin
@FR-012 @US-004 @NFR-003 @AC-033
Feature: Fronteira de autonomia

  Scenario: Condição de parada obrigatória atingida
    Given uma ação que publica, altera histórico compartilhado, muda schema, migra dados, altera política de acesso, toca segredo ou remove dado
    When a ação é alcançada durante a execução autônoma
    Then a execução para antes de agir
    And um gate humano explícito é exigido
    And a aprovação por modelo não substitui esse gate

  Scenario: Falha repetida no mesmo critério
    Given três tentativas falhas consecutivas sobre o mesmo critério de aceite
    When a quarta tentativa é iniciada
    Then a execução para e devolve a decisão a quem orquestra
```

#### AC-034 — Governança funciona sem serviço externo

**Cobre**: FR-012, NFR-005, US-002

```gherkin
@FR-012 @NFR-005 @US-002 @AC-034
Feature: Autossuficiência da governança

  Scenario: Trabalho com serviço externo indisponível
    Given um projeto cujo serviço externo de contexto está indisponível
    When uma unidade de risco baixo ou médio é executada e revisada
    Then classificação, preflight, verificação de contexto, revisão e contrato de entrega ocorrem integralmente no repositório
    And apenas o escalonamento por gatilho material fica pendente, registrado como pendência
```

#### AC-035 — Risco alto exige pedidos distintos para plano e resultado

**Cobre**: FR-002, FR-007, FR-011, NFR-002

```gherkin
@FR-002 @FR-007 @FR-011 @NFR-002 @AC-035
Feature: Dois instantes de revisão no risco alto

  Scenario: Plano e resultado de uma unidade de risco alto
    Given uma unidade classificada como risco alto
    When a revisão obrigatória é preparada
    Then um Review Request do plano é gravado antes da escrita
    And outro Review Request do resultado é gravado depois da escrita
    And os dois pedidos são artefatos e instantes distintos da mesma unidade
```

#### AC-036 — Proveniência insuficiente impede o fechamento

**Cobre**: FR-002, FR-007, FR-011, NFR-002

```gherkin
@FR-002 @FR-007 @FR-011 @NFR-002 @AC-036
Feature: Proveniência nunca inferida

  Scenario: Identidade técnica ausente ou apenas inferida
    Given um Review Request ou Review Verdict sem harness, modelo, effort ou session ID observado
    When o fechamento da rodada é solicitado
    Then a rodada não fecha
    And cada valor não observado persiste exatamente como NÃO REGISTRADO
    And o relatório pode explicar a ausência sem substituir o token
    And nenhum valor é inferido de nome, contexto, transcript ou ferramenta
```

#### AC-037 — Review Request divergente da base observada bloqueia a revisão

**Cobre**: FR-007, FR-008, FR-011, NFR-002

```gherkin
@FR-007 @FR-008 @FR-011 @NFR-002 @AC-037
Feature: Parecer ancorado na base declarada

  Scenario: Branch ou HEAD observado difere do Review Request
    Given um Review Request que declara branch e HEAD
    And o revisor observa branch ou HEAD diferente
    When a revisão é iniciada
    Then a revisão não prossegue como se fosse sobre a mesma unidade
    And a rodada passa para CORREÇÕES SOLICITADAS
    And nenhum parecer de aprovação é emitido
    And o Review Request precisa ser corrigido
    And se a divergência for MUDANÇA MATERIAL a rodada é encerrada sem aprovação e uma nova rodada é aberta
    And nesse caso CURRENT passa a indicar a nova rodada
    And nenhum parecer é aprovado sobre base diferente da declarada
```

#### AC-038 — Evidência executável é obrigatória para veredito formal

**Cobre**: FR-004, FR-011, NFR-002

```gherkin
@FR-004 @FR-011 @NFR-002 @AC-038
Feature: Fechamento formal do Git Guardian

  Scenario: Relatório contém apenas inspeção manual
    Given um relatório com um dos três valores PROVISORIAMENTE permitidos
    And nenhuma saída do mecanismo executável versionado
    When um veredito formal do Git Guardian é exigido para fechar a unidade
    Then o fechamento é recusado
    And nenhum estado GG é atribuído por narrativa
```

### 7. Requisitos

#### Funcionais

- **FR-001**: **Classificação de risco.** Toda unidade de trabalho é classificada
  antes da execução em `BAIXO | MÉDIO | ALTO | CRÍTICO`, com justificativa
  registrada. **Baixo**: leitura, censo somente leitura, formatação, correção
  editorial, recálculo mecânico, execução de verificação existente e mudança
  pequena sem alteração de comportamento. **Médio**: comportamento novo de
  impacto limitado, alteração em múltiplos arquivos, contrato local ou mudança
  pronta para publicação interna. **Alto**: arquitetura, legado, mudança ampla,
  integração externa ou estado de repositório problemático. **Crítico**:
  produção, pagamento, autenticação, dado pessoal, migração de dados ou operação
  destrutiva de histórico. **Elevação automática** para alto ou crítico,
  independentemente do tamanho: segurança ou permissões; autenticação ou
  autorização; pagamentos ou faturamento; dado pessoal, segredo ou credencial;
  migração ou transformação de dados; arquitetura ou processo transversal;
  publicação em produção; operação destrutiva de histórico; decisão de negócio;
  promessa ou experiência de cliente; divergência material entre fontes ou entre
  famílias de modelo.
- **FR-002**: **Roteamento de modelo, effort e revisão.** Um roteador identifica
  o gate, aplica FR-001, seleciona a skill de gate, compõe os perfis aplicáveis,
  declara se a revisão exigida é **prévia, posterior ou ambas** e **rejeita o
  fechamento quando a proveniência for insuficiente**. Verificação por nível:
  baixo — autoverificação do executor, segunda família não obrigatória; médio —
  **uma** revisão do pacote consolidado antes do fechamento; alto — revisão do
  **plano antes** da escrita e do **resultado depois**; crítico — tudo do alto
  mais **gate humano antes da escrita** e **novo gate humano antes de ação
  externa ou irreversível**. Papéis são **lógicos** — planejamento forte,
  implementação, revisão e leitura barata — mapeados a harness, modelo, effort e
  data, nunca a fornecedor fixo. **Vedado** a modelo novo, barato ou não validado:
  aprovador final de segurança; autoridade para operação destrutiva de histórico;
  responsável único por publicação; revisor final de pagamento, autenticação ou
  dado pessoal. Promoção exige benchmark documentado e decisão explícita.
- **FR-003**: **Separação entre implementador e aprovador.** Instâncias distintas
  são **condição obrigatória** para fechar qualquer gate e para aceitar um
  parecer nos gatilhos obrigatórios. Ambas são identificadas nominalmente. **A
  coincidência não é sinalizada e liberada: ela bloqueia** — o gate permanece
  pendente até revisão por instância distinta, entendida como outro agente, outra
  sessão, outra família de modelo ou validação humana explícita. O revisor abre
  **contexto novo e inicialmente somente leitura**, recebe o pacote e **não recebe
  a conclusão do implementador como verdade**; devolve achados por severidade,
  com evidência e correção proposta. **Aprovação sem teste, diff ou evidência não
  fecha gate.** Bloquear o gate quando não existe segunda instância é aplicação
  da decisão aprovada de revisão independente, não ampliação silenciosa do
  Guardrail A.
- **FR-004**: **Git Guardian e preflight.** O preflight **precede** escrita em
  disco, troca ou criação de branch, commit, operação de remote e publicação.
  Opera **somente leitura** por padrão e inspeciona, de forma explícita: 1. pasta
  e raiz reais; 2. branch e HEAD; 3. working tree; 4. staged, modificados e não
  rastreados; 5. upstream e divergência ahead/behind; 6. remotes e identidade
  aplicável; 7. worktrees; 8. stashes; 9. tags e marcos; 10. operação pretendida
  e seus efeitos; 11. perfil específico do repositório e ambiente; 12.
  contradições entre documentação e estado observado; 13. proteção necessária;
  14. operações permitidas e bloqueadas; 15. próxima ação segura; 16. necessidade
  ou não de aprovação humana. O perfil específico prevalece sobre receita Git
  genérica. Worktree suja de origem desconhecida bloqueia. Detached HEAD bloqueia
  até preservação em branch. Trabalho em `main` ou `master` sem autorização exige
  criar branch antes de editar. É proibido executar `stash`, `reset`, `switch` ou
  `checkout` para “limpar” origem desconhecida. Ações destrutivas, publicação e
  deploy obedecem ao gate humano aplicável.

  O mecanismo executável versionado, quando existir, produz exatamente um
  veredito formal: **`GG-SEGURO`** — prosseguir somente nas operações declaradas;
  **`GG-CONDICIONAL`** — trabalho de origem conhecida pode prosseguir após branch
  safety, tag, patch, backup ou outra proteção reversível e verificável, desde
  que não exista contradição nem origem desconhecida; aplicar a proteção e
  repetir o preflight; **`GG-BLOQUEADO`** — nenhuma alteração até explicar e
  reconciliar o risco. O mecanismo **não está materializado** (`G-05`). Enquanto
  isso, a inspeção manual somente leitura produz exatamente um destes valores:
  **`PROVISORIAMENTE SEGURO`** — permite apenas continuar análise documental no
  escopo já autorizado; **`PROVISORIAMENTE CONDICIONAL`** — exige proteção ou
  correção reversível e nova inspeção; **`PROVISORIAMENTE BLOQUEADO`** — nenhuma
  escrita.
  Sem a saída do mecanismo executável anexada ao relatório, não existe veredito
  formal do Git Guardian e nenhuma unidade pode se autodeclarar liberada por
  narrativa. Este requisito define o contrato, não arquivo, script ou skill.
- **FR-005**: **Session Guardian.** Papel **verificador operacional** — não é
  produto, não é memória autônoma, não é terceira IA e **não substitui o Git
  Guardian nem `review-handoff`**. Verifica **continuidade entre sessões por
  contexto e handoff de sessão**, não estado de repositório nem pacote de revisão.
  **Na abertura**: localizar o roteador canônico; localizar **exatamente um**
  contexto ativo; verificar o identificador lógico `SESSION_CURRENT`; comparar projeto, branch e HEAD
  declarados com o estado observado; detectar contexto ausente, quebrado,
  ambíguo ou superado; **impedir que transcript bruto ou retomada automática seja
  tratado como fonte canônica**. **Durante a sessão**: classificar como
  `MUDANÇA MATERIAL` qualquer alteração de decisão, escopo incluído ou excluído
  ou classe de risco; retornar `SG-BLOQUEADO` até `review-handoff` criar nova
  rodada e atualizar `CURRENT`; sinalizar compressão ou perda de contexto que torne
  insegura a continuidade. **No fechamento**: validar os cinco campos do contrato
  de handoff em formato delta; garantir **exatamente um** ativo; marcar o anterior
  como superado **sem reescrever seu conteúdo**; validar a atualização conjunta de
  snapshot e `SESSION_CURRENT`; exigir branch, HEAD, stage, worktree, decisões, pendências
  e evidências **observadas**; **impedir fechamento que declare estado não
  verificado**. O contrato determinístico é:

  | Estado | Critérios | Conduta |
  | --- | --- | --- |
  | `SG-VÁLIDO` | exatamente um contexto ativo; `SESSION_CURRENT` presente e resolvendo para ele; projeto, branch e HEAD coerentes com o observado; cinco campos obrigatórios presentes; contexto não superado; escopo da sessão correspondente à unidade ativa | continuar no escopo declarado |
  | `SG-CONDICIONAL` | contexto identificável e íntegro, com correção não material e reversível: completar campo obrigatório sem alterar decisão, escopo ou risco; corrigir proveniência; atualizar `SESSION_CURRENT` desatualizado com alvo único; registrar a terceira compactação e preparar fechamento seguro | corrigir o registro e repetir a verificação |
  | `SG-BLOQUEADO` | `MUDANÇA MATERIAL`; contexto ausente; mais de um ativo; `SESSION_CURRENT` quebrado ou ambíguo; divergência não explicada de projeto, branch ou HEAD; contexto superado; perda que impeça reconstrução segura; transcript ou retomada automática como única fonte | nenhuma continuidade até reconstruir e reconciliar o contexto; mudança material exige nova rodada e `CURRENT` |

  A terceira compactação é o limiar documentado para abrir nova sessão com
  handoff estruturado. O prefixo `SG-` é obrigatório.
- **FR-006**: **Skills de revisão e perfis.** Cinco nomes lógicos canônicos:
  `review-router`, `review-definition`, `review-plan`, `review-delivery` e
  `review-handoff`. Quatro perfis lógicos: `security-auth-privacy` —
  segurança/autenticação/privacidade; `data-migration` — dados/migração;
  `git-deploy` — Git/deploy; `business-customer` — negócio/experiência do
  cliente. Os caminhos físicos serão definidos no Plan Gate. Perfis **complementam** a skill de gate: não a
  substituem, não fecham gate sozinhos e não geram skill por combinação.
- **FR-007**: **Contrato de repasse.** Três artefatos e um ponteiro.
  **Review Request**, gravado pelo implementador em formato delta: unidade
  revisada; risco e justificativa; branch e HEAD; base e escopo do diff;
  arquivos; testes; decisões; dúvidas; fontes; restrições; harness, modelo,
  effort e session ID do implementador. **Review Verdict**, gravado pelo revisor
  em artefato separado: harness, modelo, effort e session ID do revisor;
  evidências; achados de `P0` a `P3`; veredito; condições; gate resultante.
  **Correction Report**, gravado pelo implementador na mesma rodada: achados
  tratados; correções aplicadas; achados **não** aplicados com justificativa;
  novo diff e testes; estado Git; pedido de reconferência. **`CURRENT`** é o
  identificador lógico da rodada ativa e é validado por `review-handoff`. O
  implementador **não cola histórico de conversa**: a sessão nova recebe caminho
  e `CURRENT`. O pacote é **delta** e referencia fontes estáveis em vez de
  duplicá-las. `review-handoff` administra esse pacote entre implementador e
  revisor; não substitui o Session Guardian nem o Git Guardian. `CURRENT` e
  `SESSION_CURRENT` são identificadores lógicos distintos; nomes físicos e
  caminhos serão definidos somente no Plan Gate.
- **FR-008**: **Máquina de estados e regras de rodada.** Estados:
  `RASCUNHO → PRONTO PARA REVISÃO → EM REVISÃO → CORREÇÕES SOLICITADAS → PRONTO
  PARA RECONFERÊNCIA → APROVADO | REPROVADO`. **Exatamente uma rodada ativa.**
  Rodadas concluídas são **imutáveis**. **`MUDANÇA MATERIAL`** — qualquer alteração
  de decisão, escopo incluído ou excluído ou classe de risco — **sempre cria nova
  rodada**; não pode ser absorvida por atualização reversível da rodada atual.
  Correções não materiais de metadado ou evidência permanecem na
  rodada corrente, com **uma** reconferência consolidada. Parecer técnico comum
  permanece no repositório. Estes são estados da **revisão**, sempre qualificados
  por “para revisão” ou “para reconferência”; não se confundem com `PRONTO` da
  entrega.
- **FR-009**: **Contrato de Entrega.** Toda unidade de trabalho declara, **antes
  da execução**, treze campos; a ausência de qualquer um impede o início:
  1. **objetivo de uso**; 2. **artefato e destino**; 3. **estado final esperado**;
  4. **escopo incluído**, como lista fechada; 5. **escopo excluído**, explícito;
  6. **critérios de aceite verificáveis**, que declaram o que precisa ser
  verdadeiro; 7. **mecanismo de verificação**, que declara como provar cada
  critério por automação ou roteiro determinístico, nunca “deve ficar bom”;
  8. **evidência**, o registro produzido pela verificação; 9. **resíduos
  proibidos**; 10. **fronteira de autonomia e condições de parada**;
  11. **aprovador** designado; 12. **atualização documental** devida na mesma
  entrega; 13. **rollback**, com destino de retorno, ponto-base, comando e
  verificação da integridade do ponto de retorno. Critério, mecanismo e evidência
  são campos distintos e não podem ser colapsados.
- **FR-010**: **Estados `PRONTO`, `ENTREGUE` e `ACEITO`.** Não são sinônimos e não
  podem ser colapsados. **`PRONTO`**: artefato concluído na origem, verificações
  internas verdes e evidência produzida — **pode ainda não estar no destino**.
  **`ENTREGUE`**: artefato chegou ao destino declarado e sua presença e alcance
  foram **comprovados** — **não implica aceite**. **`ACEITO`**: o aprovador
  designado conferiu o artefato **já no destino declarado** e registrou aceite
  explícito. Antes da entrega, validação humana conta somente como **autorização
  para entrega** ou evidência prévia, nunca como `ACEITO`. As exceções mínimas
  são: regressão antes da entrega sai de `PRONTO` para `CORREÇÃO NECESSÁRIA`;
  falha de presença ou alcance não entra em `ENTREGUE`; reprovação após entrega
  vira `ENTREGUE COM CORREÇÕES`; regressão após aceite vira `ACEITE REVOGADO` e
  reabre a unidade como `CORREÇÃO NECESSÁRIA`, com motivo e nova evidência
  obrigatórios. `CORREÇÃO NECESSÁRIA` retorna a `PRONTO` somente após correção,
  verificações internas verdes e nova evidência. `ENTREGUE COM CORREÇÕES` volta à
  origem e, após verificações verdes, retorna a `PRONTO`, exigindo nova entrega.
  `ACEITE REVOGADO` percorre novamente `CORREÇÃO NECESSÁRIA → PRONTO → ENTREGUE →
  ACEITO`. Nenhum estado excepcional transita diretamente a `ACEITO`. Quando o aceite
  humano não for aplicável,
  o contrato **declara previamente** quem ou qual verificação ocupa esse papel;
  não se infere depois.
- **FR-011**: **Evidência, proveniência, rollback e resíduos.** Nenhum gate fecha
  sem: unidade revisada; classificação de risco e justificativa; branch e HEAD;
  harness, modelo, effort e session ID **do implementador e do revisor**; escopo
  ou diff; verificações executadas e seu resultado; achados; veredito; correções
  aplicadas; gate resultante. **Proveniência é declarada, nunca inferida**:
  todo valor não observado persiste exatamente como `NÃO REGISTRADO`; explicação
  não substitui o token, e campo obrigatório nesse estado bloqueia o fechamento.
  Falha é **reportada, nunca omitida**.
  Rollback e resíduos proibidos seguem FR-009.
- **FR-012**: **Escalonamento e limites de autonomia.** **Escalonamento externo**
  ocorre por gatilho, não por hábito: decisão de negócio; arquitetura ou processo
  transversal; risco alto ou crítico; divergência material entre fontes ou entre
  famílias; falta de compreensão segura por quem orquestra; marco de projeto.
  Fora desses casos, a revisão técnica permanece no repositório. **Parada
  obrigatória** antes de: publicar ou alterar histórico compartilhado; alterar
  schema, migrar dados, mudar política de acesso, tocar segredo ou autenticação;
  escrita destrutiva sem ponto de retorno verificado; **três falhas consecutivas
  no mesmo critério**; conclusão de que um critério exige decisão de produto ou
  de negócio. Ação **irreversível** exige gate humano explícito, e aprovação por
  modelo não o substitui. Validação por IA **não equivale** a revisão humana
  experiente em mudança crítica e irreversível (`G-07`).

#### Não funcionais

- **NFR-001**: **Proporcionalidade.** O custo de verificação acompanha o risco, e
  não o número de interações. **Verificação**: AC-001, AC-002, AC-005, AC-020,
  AC-023, AC-026, AC-027 e AC-032, mais as metas `M-2` e `M-7`.
- **NFR-002**: **Auditabilidade.** Toda decisão de gate é reconstituível a partir
  do registro, sem consultar transcript. **Verificação**: AC-007 a AC-010,
  AC-012, AC-014, AC-017, AC-018, AC-021, AC-022, AC-024, AC-025, AC-029 e a meta
  `M-3`, mais AC-035, AC-036, AC-037 e AC-038.
- **NFR-003**: **Segurança e irreversibilidade.** Nenhuma ação destrutiva ou
  externa ocorre sem preflight e sem gate humano declarado. **Verificação**:
  AC-003, AC-006, AC-011, AC-013, AC-031, AC-033 e a meta `M-6`.
- **NFR-004**: **Agnosticismo de harness e fornecedor.** Trocar de ferramenta ou
  de modelo não invalida a governança; papéis são lógicos e o contexto é arquivo
  portável. **Verificação**: AC-007, AC-015, AC-019 e AC-025.
- **NFR-005**: **Independência de serviço externo.** Classificação, preflight,
  verificação de contexto, revisão e contrato de entrega funcionam sem Notion,
  sem MCP e sem rede. **Verificação**: AC-014, AC-032 e AC-034.

#### Erros e casos-limite

- Unidade sem classificação de risco → recusar a execução antes de qualquer
  escrita.
- Classificação de risco contestada entre implementador e revisor → prevalece a
  mais alta até reconciliação explícita.
- Mecanismo executável indisponível → registrar exatamente um dos três valores
  `PROVISORIAMENTE SEGURO | PROVISORIAMENTE CONDICIONAL | PROVISORIAMENTE BLOQUEADO`;
  não emitir estado `GG-*` nem fechar unidade que exija evidência formal.
- Contexto ativo ausente, duplicado ou com `SESSION_CURRENT` quebrado → `SG-BLOQUEADO`;
  não escolher candidato por heurística.
- Handoff com os cinco campos presentes mas sem o porquê das decisões → recusar o
  fechamento; o porquê é obrigatório (`G-17`).
- Review Verdict sem proveniência → não fecha gate; não inferir o modelo.
- `CURRENT` indicando mais de uma rodada ativa → rejeitar e reportar.
- Contrato de Entrega sem aprovador declarado → não iniciar; não designar
  aprovador após a entrega.
- Artefato `PRONTO` que não alcança o destino na mesma rodada → registrar e
  explicar; não declarar concluído.
- Rollback declarado cujo ponto de retorno não pôde ser verificado → tratar a
  execução como não autorizada.

## Ato II — Projetar e provar

### 8. Plano técnico

#### Plano integrado do Plan Gate

Esta spec é a espinha transversal do plano conjunto com a SPEC-0001. A ordem
obrigatória é: Git Guardian; mecanismos transversais; mecanismos locais da
ponte; integração; validadores e fixtures; empacotamento da Camada Potestatem;
instalação em consumidor; piloto Tempus Mind Map; reconciliação; Delivery Gate.

A nomenclatura aprovada em 21/09/2026 é aplicada somente ao conteúdo novo:
**Potestatem SDD** é o método organizacional, **Specsfy** é a base upstream e
**Camada Potestatem** é a camada própria. `deco/`, `deco/v0.2` e o nome do repo
permanecem identificadores técnicos. Não há rename nem substituição global.

O censo atual não localizou mecanismo executável do Git Guardian. O Plan Gate
propõe resolver DEC-006 atribuindo à SPEC-0002 a primeira materialização futura,
antes dos demais mecanismos. Isso define dono e ordem, mas não afirma que o
mecanismo exista hoje e permanece sujeito à revisão independente.

Os quatro perfis de FR-006 continuam sendo **perfis de risco de revisão**. A
política organizacional de perfis técnicos por família de stack não cria um
catálogo universal nesta v0.2; esse catálogo fica para spec posterior. O piloto
pode declarar contrato Laravel/PostgreSQL local sem acoplar o Potestatem SDD a
essa stack.

**Decisão humana do Plan Gate (21/09/2026):** o runner TDD canônico da v0.2
é `python3 -B -m unittest`, integrado à descoberta da raiz em
`tests/test_deco_*.py`; os cenários BDD da camada ficam em
`tests/features/deco_*.feature` e são executados também pela regressão da
raiz. A validação de entrega deve provar execução real das suítes da camada,
com teste negativo para ausência, exclusão ou não execução. Nenhum
`deco/tests/**/*.test.mjs` é adotado por este plano.

#### Contexto existente

A organização já possui as decisões de método (`G-01` a `G-17`), a peça 1 do
contrato de handoff em `deco/rules/canonical.md:15-43`, os templates de ponteiro e
snapshot em `deco/templates/` e três fixtures documentais em
`deco/fixtures/handoff/` — `valid/`, `missing-field/` e `broken-pointer/` — que
cobrem somente contexto válido, campo ausente e ponteiro quebrado. Não cobrem
dois contextos `ATUAL`, divergência declarado × observado, compactação ou perda
de contexto; a fixture de dois `ATUAL` é lacuna futura e não é criada nesta
rodada. **Nenhum verificador executável existe.** A SPEC-0001 especifica a ponte
Notion ↔ repositório já recomposta; a governança transversal foi removida dela e
passou a ter esta spec como fonte normativa.

#### Arquitetura e módulos

Três planos, deliberadamente separados:

1. **Plano de governança** (esta spec) — regras que valem para qualquer fatia,
   independentemente de produto, stack, harness ou fornecedor.
2. **Plano de fatia** — cada spec de produto, incluindo a SPEC-0001, que consome
   a governança e fornece suas próprias superfícies e contratos.
3. **Plano de implementação** — skills, verificadores e scripts que materializam
   a governança. **Não existe**; é matéria do Plan Gate.

#### Artefatos previstos por esta spec

O Definition Gate decide **quais artefatos precisam existir e o que cada um deve
conter**; onde ficam, em que formato e como são executados é matéria do Plan Gate.

| Artefato | Natureza | Conteúdo obrigatório |
| --- | --- | --- |
| Matriz de risco e gatilhos de elevação | norma | quatro níveis, exemplos e onze gatilhos automáticos (FR-001) |
| Contrato do roteador de revisão | norma | responsabilidades, composição gate + perfil, rejeição por proveniência (FR-002) |
| Regra de separação implementador/aprovador | norma | condição obrigatória e bloqueio na coincidência (FR-003) |
| Contrato do Git Guardian | norma herdada | dezesseis dimensões, classificação manual provisória, vereditos formais `GG-*` e condutas (FR-004) |
| Contrato do Session Guardian | norma | verificações de abertura, sessão e fechamento; vereditos `SG-*` (FR-005) |
| Catálogo de skills e perfis | norma | cinco skills, quatro perfis, regra de composição (FR-006) |
| Contrato de repasse | norma | campos dos três artefatos e de `CURRENT` (FR-007) |
| Máquina de estados da revisão | norma | sete estados, rodada única, imutabilidade (FR-008) |
| Modelo de Contrato de Entrega | norma | treze campos obrigatórios (FR-009) |
| Regra dos três estados de entrega | norma | definições não colapsáveis e regressão explícita (FR-010) |
| Registro de evidência de gate | evidência | doze itens de FR-011, por gate fechado |

#### Migrations, models, controllers, queries e jobs

Não aplicável em todos os casos: a governança não possui banco de dados, schema,
persistência versionada, aplicação, camada de serviço, rota, repositório de dados
nem processamento assíncrono. As entidades da seção 9 são documentos e papéis,
não registros persistidos. Trigger, worker e agente autônomo permanecem fora de
escopo, em consonância com o limite de automação da SPEC-0001.

#### Estrutura de arquivos

Existente e aprovado nesta fase:

```text
deco/specs/0002-governanca-sdd/
  spec.md
  research/notion/fontes-notion.md
```

A estrutura que receberá contratos, skills e verificadores é **proposta** e será
fixada no Plan Gate. Esta seção não a antecipa.

#### Decisão deliberada de não implementar agora

Nenhuma skill, verificador, script, ponteiro, diretório de rodada ou contrato
materializado é criado por esta spec. A implementação é avaliada no Plan Gate,
depois que o conteúdo aqui for revisado por instância distinta.

### 9. Modelo de dados

#### Entidades

| Entidade | Identidade | Atributos e regras | Relações |
| --- | --- | --- | --- |
| Unidade de trabalho | identificador da fatia mais gate | classificação de risco obrigatória antes da execução; contrato de entrega associado | 1 unidade → 1..N rodadas |
| Contrato de Entrega | identificador da unidade | treze campos obrigatórios; aprovador declarado antes da execução | 1 contrato → 1 unidade |
| Rodada de revisão | sequencial por unidade | exatamente uma ativa; imutável após conclusão; indicada logicamente por `CURRENT`, validado por `review-handoff` | 1 rodada → 1 Request → 0..1 Verdict → 0..N Correction Reports |
| Review Request | rodada mais identidade do implementador | formato delta; declara branch e HEAD; sem histórico de conversa | N requests → 1 unidade |
| Review Verdict | rodada mais identidade do revisor | artefato separado; achados `P0`–`P3`; proveniência completa | 1 verdict → 1 rodada |
| Correction Report | rodada mais ordem de emissão | achados tratados e não tratados com justificativa | N reports → 1 rodada |
| Contexto de sessão | projeto mais data | cinco campos em formato delta; exatamente um ativo indicado logicamente por `SESSION_CURRENT`; anterior superado sem reescrita | 1 ativo → N superados |
| Classificação manual de preflight | inspeção somente leitura | `PROVISORIAMENTE SEGURO`, `PROVISORIAMENTE CONDICIONAL` ou `PROVISORIAMENTE BLOQUEADO`; nunca emite `GG-*` | N classificações → 1 unidade |
| Veredito formal de preflight | execução do mecanismo versionado | `GG-SEGURO`, `GG-CONDICIONAL` ou `GG-BLOQUEADO`, saída anexada e estado observado | N vereditos → 1 unidade |
| Veredito de contexto | execução do Session Guardian | `SG-VÁLIDO`, `SG-CONDICIONAL` ou `SG-BLOQUEADO` | N vereditos → 1 sessão |

#### Estados e transições

| Entidade | Estado atual | Evento | Próximo estado | Invariantes |
| --- | --- | --- | --- | --- |
| Rodada | `RASCUNHO` | Review Request gravado | `PRONTO PARA REVISÃO` | branch e HEAD declarados; pacote delta |
| Rodada | `PRONTO PARA REVISÃO` | revisor assume em contexto novo | `EM REVISÃO` | revisor distinto; estado observado confere com o declarado |
| Rodada | `EM REVISÃO` | Verdict com achados | `CORREÇÕES SOLICITADAS` | achados de `P0` a `P3` |
| Rodada | `CORREÇÕES SOLICITADAS` | Correction Report gravado | `PRONTO PARA RECONFERÊNCIA` | correções em lote, mesma rodada |
| Rodada | `PRONTO PARA RECONFERÊNCIA` | reconferência do mesmo revisor | `APROVADO` \| `REPROVADO` | uma reconferência por rodada; proveniência completa |
| Rodada | `EM REVISÃO` | Verdict sem achado bloqueante | `APROVADO` | aprovador distinto do executor |
| Rodada | qualquer estado ativo | `MUDANÇA MATERIAL` de decisão, escopo incluído/excluído ou classe de risco | rodada encerrada sem aprovação; nova em `RASCUNHO` | anterior não reescrita; `CURRENT` passa à nova |
| Rodada | `APROVADO` \| `REPROVADO` | tentativa de edição | inalterado | rodada concluída é imutável |
| Entrega | — | verificações internas verdes e evidência produzida | `PRONTO` | destino ainda não comprovado |
| Entrega | `PRONTO` | regressão antes da entrega | `CORREÇÃO NECESSÁRIA` | sem transição direta a `ACEITO` |
| Entrega | `CORREÇÃO NECESSÁRIA` | correção concluída, verificações internas verdes e nova evidência | `PRONTO` | evidência registrada |
| Entrega | `PRONTO` | presença e alcance comprovados no destino | `ENTREGUE` | comprovação registrada, não presumida |
| Entrega | `ENTREGUE` | aprovador registra aceite explícito | `ACEITO` | aprovador é o declarado no contrato |
| Entrega | `ENTREGUE` | reprovação no destino | `ENTREGUE COM CORREÇÕES` | motivo e correção registrados |
| Entrega | `ENTREGUE COM CORREÇÕES` | correção retorna à origem | `CORREÇÃO NECESSÁRIA` | sem transição direta a `ACEITO` |
| Entrega | `CORREÇÃO NECESSÁRIA` | correção pós-entrega validada internamente | `PRONTO` | nova entrega obrigatória para voltar a `ENTREGUE` |
| Entrega | `ACEITO` | regressão detectada | `ACEITE REVOGADO` | motivo e nova evidência obrigatórios |
| Entrega | `ACEITE REVOGADO` | unidade reaberta | `CORREÇÃO NECESSÁRIA` | percorre novamente `PRONTO → ENTREGUE → ACEITO`; sem atalho |
| Contexto de sessão | ativo | novo contexto gravado | superado | `SESSION_CURRENT` passa ao novo; marcação sem reescrita |

#### Migração e retenção

- Rodadas, pareceres e contextos **nunca são apagados nem reescritos**; o
  histórico é a própria prova de que a governança foi aplicada.
- Contexto superado permanece como rastreabilidade e **não é lido em sequência**
  na abertura de sessão.
- Nenhuma migração de schema: não há schema.

### 10. Interfaces e contratos

#### Interface para pessoas

- **Há interface para pessoas**: **Não.** A governança é processo e não cria
  superfície própria — nem tela, nem componente, nem rota. As duas superfícies
  humanas do fluxo, o cockpit e a `Consulta SDD`, pertencem à SPEC-0001 e são
  consumidas por referência, nunca redefinidas aqui. A leitura humana dos
  artefatos desta spec acontece em Markdown versionado no repositório, com a
  obrigação de redação da peça 4 (`deco/rules/canonical.md:77-87`): quem
  orquestra precisa conseguir julgar sem ler diff.

#### O que a SPEC-0002 consome da SPEC-0001

| Interface | Fornecida por | Uso na governança |
| --- | --- | --- |
| Cockpit do projeto | SPEC-0001 — contrato “Cockpit do projeto” | superfície onde o gate fechado e o par executor/aprovador ficam visíveis |
| Consulta SDD | SPEC-0001 — contrato “Consulta SDD” | canal de escalonamento quando um gatilho local de escalonamento ocorre |
| Relatório Modo B | SPEC-0001 — contrato “Relatório Modo B” | parecer externo nos gatilhos obrigatórios |
| Limite de interação | SPEC-0001 — contrato “Limite de interação” | regra local que impede inferência de identidade, estado ou proveniência |
| Precedência e reconciliação entre repositório e Notion | SPEC-0001 — contrato “Precedência e reconciliação entre repositório e Notion” | resolução de conflito material que mantém o gate bloqueado |
| Permissões MCP e vedações | SPEC-0001 — contrato “Permissões MCP e vedações” | condição para qualquer escrita externa feita sob esta governança |

#### O que a SPEC-0002 fornece à SPEC-0001 e a specs de produto

| Interface | Definida em | Consumida como |
| --- | --- | --- |
| Matriz de risco e gatilhos de elevação | FR-001 | vocabulário de risco usado pelas fatias |
| Roteamento e papéis vedados | FR-002 | escolha de revisão por gate |
| Separação implementador/aprovador | FR-003 | condição de fechamento de qualquer gate |
| Git Guardian e preflight | FR-004 | controle que precede escrita |
| Session Guardian | FR-005 | verificação de contexto de sessão |
| Skills e contrato de repasse | FR-006, FR-007, FR-008 | mecanismo de revisão |
| Contrato de Entrega | FR-009 | pré-condição de execução de unidade |
| Estados `PRONTO`, `ENTREGUE`, `ACEITO` | FR-010 | vocabulário de conclusão |
| Evidência mínima de gate | FR-011 | condição de fechamento |

**Enquanto a SPEC-0001 estiver em `Defined`**, cada interface acima é **dependência
versionada, não comportamento entregue**: a governança referencia o requisito
pelo identificador e pela versão da spec, e nenhum gate desta spec pode ser
fechado sob a alegação de que a ponte "já funciona".

#### Contratos com specs de produto

Uma spec de produto consome a governança declarando, no seu próprio corpo: o
nível de risco de cada unidade; o aprovador designado; o Contrato de Entrega da
unidade; e a evidência que pretende produzir. A governança **não** define
comportamento de produto e **não** substitui requisitos de fatia.

#### APIs, eventos e outros contratos

Não aplicável. Esta spec não expõe rota, endpoint, evento nem schema, e não
consome API externa: todos os seus controles operam sobre arquivos do
repositório e sobre o estado observado do próprio repositório.

### 11. Estratégia TDD

Estratégia de verificação em nível de intenção. O runner e os caminhos dos
artefatos executáveis foram confirmados pela decisão humana deste Plan Gate
(DEC-009); os testes ainda não foram implementados.

- **Unidade**: leitura de cada contrato materializado — presença das cláusulas
  obrigatórias, dos estados admitidos, dos vereditos prefixados e das vedações.
- **Integração/contrato**: coerência entre os contratos e esta spec — cada
  estado, gatilho e vedação citado em um cenário existe no contrato
  correspondente; nenhum contrato contradiz `deco/rules/canonical.md`; nenhum
  redefine interface fornecida pela SPEC-0001.
- **BDD/aceite**: a seção 6 contém **trinta e oito identificadores AC** e
  **cinquenta e seis blocos `Scenario`**. Antes da C1 eram trinta e quatro IDs AC
  e quarenta e um blocos; ao fim da C1 eram trinta e oito IDs e cinquenta e quatro blocos;
  as duas contagens nunca são tratadas como equivalentes. O Gherkin desta spec
  permanece fonte normativa; a projeção executável planejada vive em
  `tests/features/deco_*.feature` e participa da regressão da raiz.
- **Runner TDD confirmado**: `python3 -B -m unittest`, com casos
  `tests/test_deco_*.py` descobertos na raiz. O Delivery Gate exige prova de
  execução de todos os casos da camada, não só saída global verde.
- **E2E**: não aplicável — não há aplicação a percorrer.
- **Verificação manual**: inevitável para o que só se observa em uso real — a
  qualidade de um parecer, a adequação de uma classificação de risco e o aceite
  humano. As fixtures em `deco/fixtures/handoff/` apoiam somente os casos de
  contexto válido, campo ausente e ponteiro quebrado; os demais permanecem RED
  documental até materialização no Plan Gate.

#### Evidência RED-GREEN-REFACTOR

| IDs | BDD de referência | Teste informado pelo BDD | RED observado | GREEN observado | Refactor/regressão |
| --- | --- | --- | --- | --- | --- |
| FR-001, US-001, NFR-001, AC-001 | AC-001 na seção 6 | caso derivado do AC-001 | Pending | Pending | Pending |
| FR-001, FR-002, NFR-001, AC-002 | AC-002 na seção 6 | caso derivado do AC-002 | Pending | Pending | Pending |
| FR-001, NFR-003, US-004, AC-003 | AC-003 na seção 6 | caso derivado do AC-003 | Pending | Pending | Pending |
| FR-002, FR-006, US-001, AC-004 | AC-004 na seção 6 | caso derivado do AC-004 | Pending | Pending | Pending |
| FR-002, FR-006, NFR-001, AC-005 | AC-005 na seção 6 | caso derivado do AC-005 | Pending | Pending | Pending |
| FR-002, FR-003, NFR-003, AC-006 | AC-006 na seção 6 | caso derivado do AC-006 | Pending | Pending | Pending |
| FR-002, NFR-002, NFR-004, AC-007 | AC-007 na seção 6 | caso derivado do AC-007 | Pending | Pending | Pending |
| FR-003, US-001, NFR-002, AC-008 | AC-008 na seção 6 | caso derivado do AC-008 | Pending | Pending | Pending |
| FR-003, FR-006, NFR-002, AC-009 | AC-009 na seção 6 | caso derivado do AC-009 | Pending | Pending | Pending |
| FR-003, FR-011, NFR-002, AC-010 | AC-010 na seção 6 | caso derivado do AC-010 | Pending | Pending | Pending |
| FR-004, US-004, NFR-003, AC-011 | AC-011 na seção 6 | caso derivado do AC-011 | Pending | Pending | Pending |
| FR-004, NFR-002, AC-012 | AC-012 na seção 6 | vocabulário formal/provisório e caminho condicional manual/formal | Pending | Pending | Pending |
| FR-004, US-004, NFR-003, AC-013 | AC-013 na seção 6 | caso derivado do AC-013 | Pending | Pending | Pending |
| FR-005, US-002, NFR-002, NFR-005, AC-014 | AC-014 na seção 6 | somente contexto válido e ponteiro quebrado têm fixture; dois `ATUAL` e divergência permanecem Pending | Pending | Pending | Pending |
| FR-005, US-002, NFR-004, AC-015 | AC-015 na seção 6 | caso derivado do AC-015 | Pending | Pending | Pending |
| FR-005, FR-008, US-002, AC-016 | AC-016 na seção 6 | caso derivado do AC-016 | Pending | Pending | Pending |
| FR-005, US-002, NFR-002, AC-017 | AC-017 na seção 6 | caso derivado do AC-017, apoiado na fixture de campo ausente | Pending | Pending | Pending |
| FR-005, FR-011, NFR-002, AC-018 | AC-018 na seção 6 | caso derivado do AC-018 | Pending | Pending | Pending |
| FR-005, FR-004, NFR-004, AC-019 | AC-019 na seção 6 | caso derivado do AC-019 | Pending | Pending | Pending |
| FR-006, FR-007, NFR-001, AC-020 | AC-020 na seção 6 | caso derivado do AC-020 | Pending | Pending | Pending |
| FR-007, FR-011, NFR-002, AC-021 | AC-021 na seção 6 | caso derivado do AC-021 | Pending | Pending | Pending |
| FR-007, FR-003, NFR-002, AC-022 | AC-022 na seção 6 | caso derivado do AC-022 | Pending | Pending | Pending |
| FR-007, FR-008, NFR-001, AC-023 | AC-023 na seção 6 | caso derivado do AC-023 | Pending | Pending | Pending |
| FR-008, FR-005, NFR-002, AC-024 | AC-024 na seção 6 | caso derivado do AC-024 | Pending | Pending | Pending |
| FR-008, NFR-002, NFR-004, AC-025 | AC-025 na seção 6 | caso derivado do AC-025 | Pending | Pending | Pending |
| FR-005, FR-008, NFR-001, AC-026 | AC-026 na seção 6 | caso derivado do AC-026 | Pending | Pending | Pending |
| FR-009, US-003, NFR-001, AC-027 | AC-027 na seção 6 | caso derivado do AC-027 | Pending | Pending | Pending |
| FR-010, US-003, FR-009, AC-028 | AC-028 na seção 6 | caso derivado do AC-028 | Pending | Pending | Pending |
| FR-010, US-003, NFR-002, AC-029 | AC-029 na seção 6 | caso derivado do AC-029 | Pending | Pending | Pending |
| FR-010, FR-011, US-003, AC-030 | AC-030 na seção 6 | caso derivado do AC-030 | Pending | Pending | Pending |
| FR-009, FR-011, NFR-003, AC-031 | AC-031 na seção 6 | caso derivado do AC-031 | Pending | Pending | Pending |
| FR-012, NFR-001, NFR-005, AC-032 | AC-032 na seção 6 | caso derivado do AC-032 | Pending | Pending | Pending |
| FR-012, US-004, NFR-003, AC-033 | AC-033 na seção 6 | caso derivado do AC-033 | Pending | Pending | Pending |
| FR-012, NFR-005, US-002, AC-034 | AC-034 na seção 6 | caso derivado do AC-034 | Pending | Pending | Pending |
| FR-002, FR-007, FR-011, NFR-002, AC-035 | AC-035 na seção 6 | pedidos distintos de plano e resultado | Pending | Pending | Pending |
| FR-002, FR-007, FR-011, NFR-002, AC-036 | AC-036 na seção 6 | proveniência incompleta submetida a fechamento | Pending | Pending | Pending |
| FR-007, FR-008, FR-011, NFR-002, AC-037 | AC-037 na seção 6 | branch ou HEAD divergente do Review Request | Pending | Pending | Pending |
| FR-004, FR-011, NFR-002, AC-038 | AC-038 na seção 6 | relatório manual sem saída executável | Pending | Pending | Pending |

### 12. Plano de testes e rastreabilidade

A coluna de instrumento descreve **o que verifica**, não o arquivo que executa: o
caminho e o comando exatos são fixados no Plan Gate.

| Requisito | Cenário BDD | Nível | Instrumento esperado | Evidência |
| --- | --- | --- | --- | --- |
| FR-001 | AC-001, AC-002, AC-003 | Contrato | leitura da matriz de risco e aplicação a casos-teste | Pending |
| FR-002 | AC-002, AC-004, AC-005, AC-006, AC-007, AC-035, AC-036 | Contrato + aceite | roteamento simulado de unidades em gates distintos | Pending |
| FR-003 | AC-006, AC-008, AC-009, AC-010, AC-022 | Contrato + aceite | tentativa de fechamento com identidade coincidente | Pending |
| FR-004 | AC-011, AC-012, AC-013, AC-019, AC-038 | Contrato | classificação provisória e veredito formal com saída executável | Pending |
| FR-005 | AC-014 a AC-019, AC-024, AC-026 | Contrato + integração | fixtures existentes só para válido, campo ausente e ponteiro quebrado; fixture de dois `ATUAL` diferida | Pending |
| FR-006 | AC-004, AC-005, AC-009, AC-020 | Contrato | leitura do catálogo e composição gate mais perfil | Pending |
| FR-007 | AC-020, AC-021, AC-022, AC-023, AC-035, AC-036, AC-037 | Contrato | leitura do contrato de repasse e dos três artefatos | Pending |
| FR-008 | AC-016, AC-023, AC-024, AC-025, AC-026, AC-037 | Contrato | rodada simulada com `CURRENT` e transições | Pending |
| FR-009 | AC-027, AC-028, AC-031 | Contrato | contrato incompleto submetido à execução | Pending |
| FR-010 | AC-028, AC-029, AC-030 | Contrato + aceite | percurso `PRONTO` → `ENTREGUE` → `ACEITO` com regressão provocada | Pending |
| FR-011 | AC-010, AC-018, AC-021, AC-030, AC-031, AC-035 a AC-038 | Contrato | fechamento tentado sem a evidência mínima | Pending |
| FR-012 | AC-032, AC-033, AC-034 | Aceite | condição de parada provocada e trabalho com serviço externo desligado | Pending |
| NFR-001 | AC-001, AC-002, AC-005, AC-020, AC-023, AC-026, AC-027, AC-032 | Manual medido | metas `M-2` e `M-7` no piloto | Pending |
| NFR-002 | AC-007 a AC-010, AC-012, AC-014, AC-017, AC-018, AC-021, AC-022, AC-024, AC-025, AC-029, AC-035 a AC-038 | Contrato | reconstituição de um gate só pelo registro | Pending |
| NFR-003 | AC-003, AC-006, AC-011, AC-013, AC-031, AC-033 | Contrato + empírico | meta `M-6` e tentativa de ação irreversível | Pending |
| NFR-004 | AC-007, AC-015, AC-019, AC-025 | Integração | leitura do contexto sem harness específico | Pending |
| NFR-005 | AC-014, AC-032, AC-034 | Integração | execução completa com rede desligada | Pending |
| US-001 | AC-001, AC-004, AC-008 | Aceite | duas unidades de risco distinto submetidas ao roteador | Pending |
| US-002 | AC-014 a AC-017, AC-034 | Aceite | abertura de sessão sem transcript | Pending |
| US-003 | AC-027 a AC-030 | Aceite | contrato percorrido até aceite explícito | Pending |
| US-004 | AC-003, AC-011, AC-013, AC-033 | Aceite | operação destrutiva solicitada com worktree suspeita | Pending |

### 13. Validações

#### Gate do Ato I — Definição

- **Resultado**: Passed
- **Comando canônico (projeto consumidor)**:
  `node .agents/skills/specsfy-04-validate/scripts/validate_spec.mjs deco/specs/0002-governanca-sdd/spec.md --allow-draft`
- **Comando equivalente neste monorepo**:
  `node skills/specsfy-04-validate/scripts/validate_spec.mjs deco/specs/0002-governanca-sdd/spec.md --allow-draft`
- **Achados**: A revisão original solicitou A-01 a A-17; a rodada de correção e a
  reconferência independente de 19/09/2026 resolveram integralmente os dezessete
  achados. O-01 foi encerrado neste ato, e Deco Ribeyro aprovou explicitamente o
  Definition Gate em 19/09/2026.

##### Evidência FR-011 — fechamento documental de 19/09/2026

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

- **Resultado**: Passed em 21/09/2026, por decisão humana de Deco: aprovado com as condições registradas.
- **Comando equivalente neste monorepo**:
  `node skills/specsfy-05-tasks/scripts/validate_tasks.mjs deco/specs/0002-governanca-sdd/spec.md --allow-draft`
- **Achados**: a reconferência independente recomendou aprovação após conferir
  32/32 tarefas, tabela, grafo, cortes e correções. O validador de tarefas ainda
  retorna o erro de caminho `verify_evidence.mjs` próprio desta raiz do monorepo;
  não é evidência verde nem condição declarada resolvida. O diagnóstico anterior
  à geração das tarefas fica preservado no histórico Git.
- **Evidência FR-011 e condições**:
  [ato de aprovação do Plan Gate](reviews/plan-gate-2026-09-21/plan-gate-approval.md).
  `Delivery Gate` permanece `Pending`; nenhuma tarefa foi implementada.

#### Gate do Ato III — Entrega

- **Resultado**: Pending
- **Comando equivalente neste monorepo**:
  `node skills/specsfy-06-tdd-bdd/scripts/check_traceability.mjs deco/specs/0002-governanca-sdd/spec.md deco/specs/0002-governanca-sdd`
- **Achados**: Pending. Enquanto nenhum verificador existir, o resultado esperado
  é `GAPS` com todos os identificadores sem teste. A raiz passada ao script deve
  ser a pasta desta spec.

#### Limitação conhecida do tooling

A validação (`validate_spec.mjs`, com ou sem `--allow-draft`) acusa `Marcadores
não resolvidos` por um falso positivo upstream. O check atual, representado aqui
com tokens interrompidos como `/\b(?:TO·DO|TB·D|FIX·ME)\b/i`, é case-insensitive
e usa fronteiras ASCII. Por isso, alcança tanto a palavra portuguesa `todo`
quanto a terminação de **"método"**. A autorreferência local anterior foi
eliminada, e não existe marcador real pendente nesta spec. `skills/` não é
alterado.

**CORREÇÃO FACTUAL PÓS-GATE — NÃO MATERIAL.** A simulação da auditoria
pré-commit de 19/09/2026 comprovou que a alternativa somente case-sensitive é
suficiente para os tokens canônicos em maiúsculas: não alcança `todo` nem
"método". Fronteiras Unicode isoladas eliminam o casamento interno em "método",
mas continuam alcançando a palavra inteira `todo` se a flag case-insensitive for
mantida; portanto, não são solução suficiente isoladamente. A recomendação
robusta combina tokens canônicos em maiúsculas, correspondência case-sensitive
e fronteiras Unicode. Em forma conceitual, com os tokens interrompidos apenas
para evitar autorreferência documental:
`(?<![\p{L}\p{N}_])(?:TO·DO|TB·D|FIX·ME)(?![\p{L}\p{N}_])`, com flag Unicode e
sem flag case-insensitive; a expressão executável remove os pontos medianos.

O validador upstream não é alterado nesta rodada. Por isso, tanto
`validate_spec.mjs --allow-draft` quanto o modo estrito permanecem com exit 1
residual até a correção upstream, sem invalidar o Definition Gate já aprovado.
Esta correção documental não altera decisão, escopo, classe de risco nem
comportamento exigido do produto.

### 14. Tarefas

Todas as tarefas permanecem abertas. `GREEN` abaixo é evidência futura esperada,
não resultado observado nesta missão.

- [ ] T001 [TEST] [TDD] Criar testes de contratos transversais em tests/test_deco_governance_contracts.py — Refs: US-001, US-002, US-003, US-004, FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013 — Depends: none
  - [ ] **PREP**: derivar matriz, roteador, separação de papéis e Git Guardian do BDD aprovado; projetar BDD executável em `tests/features/deco_governance_contracts.feature`.
  - [ ] **EXECUTE**: materializar somente os testes; observar RED por contratos ausentes.
  - [ ] **VERIFY**: executar o runner focal e confirmar falha comportamental, não ambiental.
  - [ ] **VISUAL**: não aplicável; artefato sem interface visual.
  - [ ] **EVIDENCE**: registrar comando, exit e casos RED na seção 11.
  - [ ] **IMPROVE**: reduzir duplicação das fixtures sem enfraquecer oráculos.
- [ ] T002 [P] [TEST] [TDD] Criar testes de sessão, rodada e ponteiros em tests/test_deco_governance_rounds.py — Refs: US-001, US-002, US-003, US-004, FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019, AC-020, AC-021, AC-022, AC-023, AC-024, AC-025, AC-026 — Depends: none
  - [ ] **PREP**: derivar estados, CURRENT, SESSION_CURRENT e imutabilidade do BDD; projetar BDD executável em `tests/features/deco_governance_rounds.feature`.
  - [ ] **EXECUTE**: materializar somente os testes; observar RED pelos mecanismos ausentes.
  - [ ] **VERIFY**: executar casos de ambiguidade, mudança material e rodada histórica.
  - [ ] **VISUAL**: não aplicável; artefato sem interface visual.
  - [ ] **EVIDENCE**: registrar comandos e falhas RED rastreáveis.
  - [ ] **IMPROVE**: consolidar builders de rodada sem ocultar estados.
- [ ] T003 [P] [TEST] [TDD] Criar testes de entrega, evidência e escalonamento em tests/test_deco_governance_delivery.py — Refs: US-001, US-002, US-003, US-004, FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, AC-027, AC-028, AC-029, AC-030, AC-031, AC-032, AC-033, AC-034, AC-035, AC-036, AC-037, AC-038 — Depends: none
  - [ ] **PREP**: derivar Contrato de Entrega, três estados e gates do BDD; projetar BDD executável em `tests/features/deco_governance_delivery.feature`.
  - [ ] **EXECUTE**: materializar somente os testes; observar RED por contratos ausentes.
  - [ ] **VERIFY**: executar regressões, escalonamento e proveniência negativa.
  - [ ] **VISUAL**: não aplicável; artefato sem interface visual.
  - [ ] **EVIDENCE**: registrar comandos e casos RED na matriz.
  - [ ] **IMPROVE**: separar oráculos de entrega dos oráculos de revisão.
- [ ] T004 [CODE] Materializar Git Guardian em deco/skills/git-guardian/SKILL.md — Refs: FR-004, AC-011, AC-012, AC-013, AC-038 — Depends: T001, T002, T003
  - [ ] **PREP**: confirmar as dezesseis dimensões e a regra fail-closed.
  - [ ] **EXECUTE**: implementar três vereditos GG sem operação destrutiva automática.
  - [ ] **VERIFY**: obter GREEN nos casos de branch, HEAD, remote, stage e origem desconhecida.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar saída estruturada e testes negativos.
  - [ ] **IMPROVE**: remover duplicação sem fundir Git e Session Guardian.
- [ ] T005 [P] [CODE] Materializar Session Guardian em deco/skills/session-guardian/SKILL.md — Refs: FR-005, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019 — Depends: T001, T002, T003
  - [ ] **PREP**: fixar abertura, continuidade e fechamento sem transcript como fonte.
  - [ ] **EXECUTE**: implementar SG e validação lógica de SESSION_CURRENT.
  - [ ] **VERIFY**: obter GREEN em ausência, ambiguidade, compressão e mudança material.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar vereditos SG e fixtures correspondentes.
  - [ ] **IMPROVE**: manter fronteira explícita com review-handoff.
- [ ] T006 [P] [CODE] Materializar contratos de repasse em deco/templates/review-request.md — Refs: FR-007, FR-008, AC-020, AC-021, AC-022, AC-023, AC-024, AC-025, AC-026 — Depends: T001, T002, T003
  - [ ] **PREP**: fixar campos de Review Request, Verdict, Correction Report e CURRENT.
  - [ ] **EXECUTE**: criar templates e regras de rodada imutável.
  - [ ] **VERIFY**: obter GREEN em campos ausentes, HEAD divergente e nova rodada.
  - [ ] **VISUAL**: não aplicável; templates Markdown sem interface gráfica.
  - [ ] **EVIDENCE**: registrar schemas e fixtures válidas/inválidas.
  - [ ] **IMPROVE**: eliminar campos duplicados entre os três contratos.
- [ ] T007 [CODE] Implementar review-router em deco/skills/review-router/SKILL.md — Refs: FR-001, FR-002, FR-003, FR-006, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010 — Depends: T004, T005, T006
  - [ ] **PREP**: mapear quatro riscos, onze gatilhos e quatro perfis de risco.
  - [ ] **EXECUTE**: compor gate e perfis sem criar combinações de skills.
  - [ ] **VERIFY**: obter GREEN em roteamento, bloqueio e proveniência ausente.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar matriz de decisão e casos limítrofes.
  - [ ] **IMPROVE**: simplificar regras mantendo exemplos auditáveis.
- [ ] T008 [P] [CODE] Implementar review-definition em deco/skills/review-definition/SKILL.md — Refs: FR-006, AC-004, AC-005, AC-020 — Depends: T007
  - [ ] **PREP**: fixar unidade coerente e critérios do Definition Gate.
  - [ ] **EXECUTE**: implementar revisão de problema, requisitos, escopo e decisões.
  - [ ] **VERIFY**: obter GREEN em achados priorizados e não autoaprovação.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar Review Verdict de fixture.
  - [ ] **IMPROVE**: reduzir repetição com o roteador.
- [ ] T009 [P] [CODE] Implementar review-plan em deco/skills/review-plan/SKILL.md — Refs: FR-006, AC-004, AC-005, AC-020 — Depends: T007
  - [ ] **PREP**: fixar arquitetura, tarefas, ordem, riscos, rollback e testes previstos.
  - [ ] **EXECUTE**: implementar revisão do Plan Gate sem promovê-lo automaticamente.
  - [ ] **VERIFY**: obter GREEN em dependências cíclicas, gaps e escopo adiado.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar verdicts aprovando e solicitando correções.
  - [ ] **IMPROVE**: compartilhar somente contratos comuns com outras reviews.
- [ ] T010 [P] [CODE] Implementar review-delivery em deco/skills/review-delivery/SKILL.md — Refs: FR-006, FR-009, FR-010, FR-011, AC-027, AC-028, AC-029, AC-030, AC-031 — Depends: T007
  - [ ] **PREP**: fixar diff, testes, evidências, regressões e aderência.
  - [ ] **EXECUTE**: implementar revisão dos três estados de entrega.
  - [ ] **VERIFY**: obter GREEN em regressão e evidência material ausente.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar verdicts e regressões de fixture.
  - [ ] **IMPROVE**: manter PRONTO, ENTREGUE e ACEITO não colapsáveis.
- [ ] T011 [CODE] Implementar review-handoff em deco/skills/review-handoff/SKILL.md — Refs: FR-007, FR-008, FR-011, AC-020, AC-021, AC-022, AC-023, AC-024, AC-025, AC-026, AC-035, AC-036, AC-037 — Depends: T006, T008, T009, T010
  - [ ] **PREP**: definir criação, validação, correção e encerramento de rodada.
  - [ ] **EXECUTE**: implementar ponteiros e pacotes sem reescrever histórico.
  - [ ] **VERIFY**: obter GREEN em CURRENT quebrado, HEAD divergente e nova rodada.
  - [ ] **VISUAL**: não aplicável; skill sem interface visual.
  - [ ] **EVIDENCE**: registrar fixtures e provenance tokens.
  - [ ] **IMPROVE**: separar CURRENT de SESSION_CURRENT em código e mensagens.
- [ ] T012 [CODE] Materializar Contrato de Entrega em deco/rules/delivery-contract.md — Refs: FR-009, FR-010, FR-011, AC-027, AC-028, AC-029, AC-030, AC-031 — Depends: T003, T011
  - [ ] **PREP**: fixar treze campos, estados e regressões permitidas.
  - [ ] **EXECUTE**: criar regra e template em deco/templates/delivery-contract.md.
  - [ ] **VERIFY**: obter GREEN em alcance, aceite, revogação e rollback.
  - [ ] **VISUAL**: não aplicável; contrato Markdown sem interface gráfica.
  - [ ] **EVIDENCE**: registrar exemplos válidos e inválidos.
  - [ ] **IMPROVE**: generalizar precedente sem transportar domínio alheio.
- [ ] T013 [CODE] Integrar validador, fixtures e regressão da raiz em deco/scripts/validate-governance.mjs e tests/test_deco_regression_contract.py — Refs: FR-001, FR-003, FR-004, FR-005, FR-007, FR-008, FR-011, FR-012, AC-032, AC-033, AC-034, AC-035, AC-036, AC-037, AC-038 — Depends: T004, T005, T006, T007, T008, T009, T010, T011, T012
  - [ ] **PREP**: enumerar fixtures positivas/negativas em deco/fixtures/governance/; definir inventário esperado dos testes `test_deco_*.py` e `deco_*.feature`; reconciliar `tests/test_references.py` com fixtures negativas sem ocultar links reais quebrados; guardar o contexto desta rodada em `deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/session-context.md`, nunca em `docs/sessoes/` na raiz do monorepo.
  - [ ] **EXECUTE**: implementar códigos de saída determinísticos e contrato de regressão da raiz que verifica presença, descoberta e execução de todos os testes da Camada Potestatem.
  - [ ] **VERIFY**: obter GREEN em fixtures e na regressão da raiz; simular ausência, exclusão e não execução de qualquer suíte da camada e exigir falha não zero em cada caso; exigir verdes `test_docs_has_exactly_the_user_and_develop_trees` e `test_all_documents_are_reachable_from_portal`.
  - [ ] **VISUAL**: não aplicável; validador sem interface visual.
  - [ ] **EVIDENCE**: registrar matriz fixture → requisito → resultado, IDs descobertos/executados e os três exits negativos; nenhuma suíte ignorada pode gerar verde.
  - [ ] **IMPROVE**: reduzir acoplamento entre validadores focais.
- [ ] T014 [CODE] Empacotar e instalar a Camada Potestatem por deco/scripts/install.mjs — Refs: FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005 — Depends: T013
  - [ ] **PREP**: atualizar deco/manifest.json e definir lock, dry-run, conflito e backup.
  - [ ] **EXECUTE**: implementar install.mjs e deco/scripts/verify.mjs.
  - [ ] **VERIFY**: obter GREEN em instalação limpa, idempotência, conflito e rollback.
  - [ ] **VISUAL**: não aplicável; CLI sem interface visual nesta fatia.
  - [ ] **EVIDENCE**: registrar árvore instalada, hashes e restauração verificada.
  - [ ] **IMPROVE**: minimizar superfície instalada sem incluir deco/specs/.
- [ ] T015 [OPS] Validar instalação isolada em deco/fixtures/consumer/valid/AGENTS.md — Refs: FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, NFR-001, NFR-003, NFR-005 — Depends: T014
  - [ ] **PREP**: criar consumidor sintético sem dados reais; esta execução é baseline transversal anterior à ponte, não evidência final de instalação.
  - [ ] **EXECUTE**: executar dry-run, instalação, verificação e rollback.
  - [ ] **VERIFY**: confirmar zero arquivo fora do manifest e runtime offline; a prova final depende da revalidação pós-integração em SPEC-0001/T110.
  - [ ] **VISUAL**: não aplicável; validação operacional sem interface visual.
  - [ ] **EVIDENCE**: registrar comandos, exits, hashes e diff da fixture.
  - [ ] **IMPROVE**: reduzir passos manuais sem automatizar decisão humana.
- [ ] T016 [DOC] Registrar contrato transversal do piloto em deco/pilots/tempus-mind-map/governance-acceptance.md — Refs: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012 — Depends: T015
  - [ ] **PREP**: executar censo Git read-only do consumidor antes de fixar caminhos reais.
  - [ ] **EXECUTE**: registrar stack local, branch própria, escopo máximo, exclusões e protocolo de cinco Consultas SDD completas ou sete dias, o que ocorrer depois.
  - [ ] **VERIFY**: confirmar baseline LionCode preservada, projeto não crítico e nunca legado nem com cliente ativo; manter piloto aberto até sete dias e exatamente cinco consultas completas, sem usar atualização de cockpit como substituto.
  - [ ] **VISUAL**: não aplicável; contrato documental sem interface gráfica.
  - [ ] **EVIDENCE**: registrar branch, HEAD, footprint e critérios de aceite.
  - [ ] **IMPROVE**: cortar acabamento antes de testes, isolamento, auditoria ou revisão.
- [ ] T017 [DOC] Reconciliar piloto e preparar Delivery Gate em deco/pilots/tempus-mind-map/governance-evidence.md — Refs: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005 — Depends: T016
  - [ ] **PREP**: coletar métricas, desvios, revisão, handoff e atualizações de cockpit por marco; exigir evidência local da SPEC-0001/T115.
  - [ ] **EXECUTE**: classificar correções não materiais ou abrir nova rodada quando material.
  - [ ] **VERIFY**: executar focais, `python3 -B -m unittest discover -s tests -p 'test_*.py'`, BDD da raiz e verificação do pacote após SPEC-0001/T110; conferir IDs esperados e executados da camada, negativa de ausência/exclusão/não execução e nenhuma falha mascarada antes de qualquer Delivery Gate verde.
  - [ ] **VISUAL**: não aplicável; evidência documental sem interface própria.
  - [ ] **EVIDENCE**: anexar comandos, exits, contagens, Contrato de Entrega, cinco consultas completas, janela mínima de sete dias e Review Verdict independente.
  - [ ] **IMPROVE**: registrar somente problemas observados no piloto.

### 15. Ordem de execução

1. `T001 || T002 || T003`: predecessores RED no `unittest` da raiz e BDD da
   raiz; `T004` materializa Git Guardian depois deles, não antes.
2. `T005 || T006`, `T007`, `T008 || T009 || T010`, `T011` e `T012`
   materializam a governança transversal; `T013` integra seus testes à
   regressão da raiz e prova os três casos de falso verde.
3. `T014` empacota a base transversal; `T015` valida instalação sintética
   inicial. Essa validação **não** é evidência final do pacote com a ponte.
4. A SPEC-0001 executa `T101`–`T109`, integra a ponte em `T110` e
   **revalida instalação, idempotência, conflitos e runtime offline após a
   integração**. Sem esse GREEN posterior, nem piloto nem Delivery Gate.
5. Após o censo read-only da SPEC-0001/T111, `T016` registra o contrato
   transversal do piloto em `governance-acceptance.md`; SPEC-0001/T112–T113
   possui `acceptance.md` local. A SPEC-0001/T114 mantém o piloto aberto
   até **cinco consultas completas ou sete dias, o que ocorrer depois**.
6. SPEC-0001/T115 reconcilia `evidence.md` local; `T017` possui
   `governance-evidence.md` e só prepara o Delivery Gate após essa evidência,
   regressão integral e revisão independente. O Plan Gate foi fechado por
   decisão humana externa de Deco em 21/09/2026, não por esta autoria.

**Caminho crítico:** `T001–T003 → T004 → T007 → T011 → T013 → T014 → T015 →
SPEC-0001/T101–T109 → T110 [revalidação pós-ponte] → T111 → T016 →
T112–T114 [≥7 dias e 5 consultas] → T115 → T017 → Delivery Gate`.

**Cortes disjuntos:** mínimo pilotável = `T001`–`T016` (inclui
`T013` e `T015`); necessário para Delivery Gate = `T017`; pós-piloto
= nenhuma tarefa desta spec. Catálogo técnico universal, rename e automação
Notion exigem trabalho posterior separado. Uma tarefa aparece em um único
corte; nenhuma evidência anterior a `T110` valida a instalação final.

## Ato III — Entregar e validar

### 16. Dependências, riscos e suposições

#### Dependências

- **Git Guardian — dependência externa não satisfeita** (FR-004). Os princípios
  são normativos e vigentes (`G-04`), mas o mecanismo executável e versionado não
  foi localizado (`G-05`). **Antes do Plan Gate** é obrigatório localizar e
  referenciar a fonte canônica versionada, ou abrir spec própria para
  materializá-la. Até lá, inspeção manual somente leitura obrigatória, sempre
  limitada aos três valores definidos em FR-004, sem estado `GG-*`. Esta spec
  **não redefine nem substitui** o mecanismo.
- **SPEC-0001 em `Draft`** — as seis interfaces da seção 10 são dependência
  versionada, não comportamento entregue.
- **Instância revisora distinta**, com harness, modelo, effort e session ID
  identificáveis, disponível nos gates de risco médio ou superior (FR-003).
- **Aprovador humano designado** para aceite nos contratos em que o aceite humano
  se aplica (FR-010).
- Decisões aprovadas em `89aafb8557414ba8b2c77ef42a41bff0`,
  `698186dcacc94713b91d5d152c0d7f0b` e `4ff22dd2037a4f76a517b065fcdfc652` como
  origem normativa, com cópia derivada em `research/notion/fontes-notion.md`.

#### Riscos

- **RISK-001 — RESOLVIDO NESTA RODADA DOCUMENTAL**: a duplicação transitória foi
  encerrada pela remoção da governança residual da SPEC-0001. Evidência: busca de
  ausência de governança residual, validações `VALID DRAFT` das duas specs e
  registro executado no research. Risco residual separado: divergência futura
  entre as interfaces semânticas das duas specs; o Plan Gate deve verificá-las.
- **RISK-002**: explosão de skills — uma skill por combinação de gate e perfil.
  Mitigação: FR-006 fixa cinco skills e quatro perfis compostos em tempo de
  execução; AC-005 e AC-026 verificam.
- **RISK-003**: `CURRENT` de rodada ou `SESSION_CURRENT` de contexto quebrado ou
  ambíguo. Mitigação: namespaces lógicos distintos, `review-handoff` validando o
  primeiro e Session Guardian validando o segundo; AC-014 e AC-024 rejeitam
  ambiguidade.
- **RISK-004**: parecer aplicado sobre HEAD diferente do declarado. Mitigação: o
  Review Request declara branch e HEAD; FR-007 e AC-037 impedem parecer sobre
  base observada diferente e exigem corrigir o Request ou abrir nova rodada.
- **RISK-005**: rodada histórica reescrita ou mudança material absorvida como
  correção reversível, apagando a base real da aprovação. Mitigação: imutabilidade
  e nova rodada obrigatória em FR-005 e FR-008, verificadas por AC-016, AC-025 e
  AC-026.
- **RISK-006**: pacote de repasse crescendo até virar cópia do repositório.
  Mitigação: formato delta e referência a fontes estáveis em FR-007; AC-020 e
  AC-021 verificam.
- **RISK-007**: revisor ancorado pelo raciocínio do implementador. Mitigação:
  contexto novo, artefatos separados e a regra de `G-03`; AC-009 e AC-022.
- **RISK-008**: classificação de risco rebaixada por conveniência, esvaziando
  toda a governança a partir do primeiro passo. Mitigação: gatilhos de elevação
  automática em FR-001, verificados por AC-003; em contestação prevalece a
  classificação mais alta.
- **RISK-009**: a palavra "pronto" continuar encobrindo o que não foi entregue
  nem aceito, por hábito de linguagem. Mitigação: FR-010 e AC-028 a AC-030; a
  regressão é explícita e registrada.
- **RISK-010**: Session Guardian confundido com Git Guardian, ou tratado como
  memória autônoma. Mitigação: definição negativa em FR-005, vereditos
  prefixados e AC-019.
- **RISK-011**: a governança virar burocracia que ninguém aplica, por exigir mais
  registro do que o trabalho comporta. Mitigação: PR-001 e a faixa de risco
  baixo, que exige apenas autoverificação; a meta `M-7` mede o excesso de
  rodadas. **Este risco não está plenamente mitigado** e o piloto existe para
  medi-lo.
- **RISK-012**: o Git Guardian nunca ser materializado, bloqueando indefinidamente
  o Plan Gate. Mitigação parcial: DEC-006 admite duas saídas — localizar a fonte
  ou abrir spec própria. **Sem dono nem prazo definidos** (`G-28`).

#### Suposições

- Haverá uma segunda instância — outro agente, outra sessão, outra família ou uma
  pessoa — disponível para atuar como aprovador nos gates de risco médio ou
  superior.
- O custo de registro exigido por FR-011 é aceitável no volume de trabalho real;
  o piloto pode refutar essa suposição.
- As fixtures existentes representam somente contexto válido, campo ausente e
  ponteiro quebrado. A fixture de exatamente dois contextos `ATUAL` é lacuna
  futura e não é criada nesta rodada.

### 17. Decisões

- **DEC-001**: separar a governança transversal da spec da ponte, criando a
  SPEC-0002 com IDs próprios em vez de manter tudo na SPEC-0001.
  **Razão**: metade dos cenários e dois requisitos inteiros da SPEC-0001 não
  mencionavam Notion, MCP, cockpit nem Consulta SDD, e governavam qualquer
  trabalho assistido por IA; a spec da ponte havia dobrado de tamanho com
  material que nenhuma revisão lhe pediu.
  **Alternativa descartada**: manter tudo na SPEC-0001, rejeitada porque a
  dependência do Git Guardian bloqueava o Plan Gate da ponte por um motivo que
  não era da ponte.
  **Trade-off**: ganha-se escopo legível e reaproveitável por outras fatias;
  a transição documental exigiu recomposição e migração coordenadas, já
  executadas, e deixa como risco residual apenas a evolução das interfaces
  semânticas (RISK-001 encerrado).
- **DEC-002**: revisar unidades coerentes, nunca prompts isolados.
  **Razão**: revisar turno a turno multiplica custo sem aumentar garantia, e a
  unidade preferencial já estava aprovada em `G-09`.
  **Alternativa descartada**: revisão a cada interação, rejeitada por tornar o
  custo proporcional à conversa em vez de ao risco.
  **Trade-off**: ganha-se custo proporcional; perde-se detecção precoce — um erro
  introduzido no primeiro prompt só aparece na revisão do pacote.
- **DEC-003**: compor skill de gate com perfil de risco, em vez de criar uma
  skill por combinação.
  **Razão**: quatro gates por quatro perfis produziriam dezesseis artefatos quase
  idênticos, que divergiriam na primeira manutenção (`G-10`).
  **Alternativa descartada**: uma skill genérica parametrizada, rejeitada por
  concentrar critérios heterogêneos num só artefato e impedir revisar a política
  por partes.
  **Trade-off**: ganha-se manutenção barata; perde-se especialização — a
  composição precisa ser resolvida em tempo de execução pelo roteador, que passa
  a ser ponto único de falha.
- **DEC-004**: repassar contexto por artefato versionado, nunca por transcript.
  **Razão**: `G-11` e `G-15` — nada sobrevive dentro da LLM entre sessões, e
  colar histórico traz becos sem saída e decisões superadas, além de ancorar o
  revisor no raciocínio do implementador.
  **Alternativa descartada**: repasse por retomada automática de sessão,
  rejeitada porque o conteúdo passa a ser curado pela máquina, não por quem
  conduz.
  **Trade-off**: ganha-se contexto de alto sinal e auditável; perde-se
  conveniência — alguém precisa escrever o pacote a cada rodada. `review-handoff`
  valida `CURRENT`, identificador lógico da rodada ativa.
- **DEC-005**: definir o Session Guardian como papel verificador com vocabulário
  próprio, delimitado pela convenção de handoff já aprovada.
  **Razão**: o termo aparecia nominalmente apenas no handoff, sem definição
  (`G-24`). Em vez de inventar responsabilidades, atribuí a ele exatamente as
  verificações que `G-13` a `G-17` já exigem e que hoje ninguém garante.
  **Alternativa descartada**: ampliar o Git Guardian para cobrir contexto de
  sessão, rejeitada porque os objetos são distintos — um observa o repositório,
  o outro observa a continuidade do trabalho — e fundi-los tornaria ambíguo qual
  controle barrou o quê.
  **Trade-off**: ganha-se um verificador com escopo nítido; perde-se economia —
  são dois papéis a materializar em vez de um, e o risco de confusão entre eles
  passa a existir (RISK-010). O papel valida `SESSION_CURRENT`, identificador
  lógico do contexto ativo; caminho e nome físico ficam para o Plan Gate.
- **DEC-006**: manter o Git Guardian como **dependência externa não satisfeita**,
  também nesta spec.
  **Razão**: `G-05` — a materialização não foi executada e a busca no repositório
  não encontrou artefato. Afirmar que existe seria declarar satisfeita uma
  proteção que ninguém pode executar.
  **Alternativa descartada**: especificar a implementação do Git Guardian aqui,
  rejeitada porque a governança define o contrato, e fixar arquivo, script e
  formato de saída no Definition Gate antecipa decisões do plano.
  **Trade-off**: ganha-se honestidade sobre o estado real; perde-se autonomia —
  o Plan Gate depende de trabalho que ainda não tem dono nem prazo (RISK-012).
- **DEC-007**: separar `PRONTO`, `ENTREGUE` e `ACEITO` em três estados distintos e
  não colapsáveis.
  **Razão**: há prova empírica dos dois colapsos — três funcionalidades prontas e
  inalcançáveis (`G-19`), e um contrato verde por automação que ainda assim
  registrou pendência de validação humana (`G-20`).
  **Alternativa descartada**: manter um único estado "concluído" com critérios de
  aceite mais rigorosos, rejeitada porque critério rigoroso não impede a
  linguagem de encobrir: "pronto" continuaria sendo dito antes de o artefato
  chegar ao destino.
  **Trade-off**: ganha-se honestidade de estado; perde-se fluidez — cada entrega
  passa a exigir duas comprovações adicionais, e há custo real em provar alcance
  no destino.
- **DEC-008**: tratar o modelo de Contrato de Entrega do MusicFlow como
  **precedente**, não como norma transversal.
  **Razão**: é contrato de um projeto, com regras de interface gráfica, domínio
  musical e stack específicos (`G-25`). Generalizar tudo importaria vocabulário
  que não se aplica; descartar tudo perderia um modelo já validado em uso real.
  O precedente continha sete campos gerais. A versão anterior desta SPEC-0002
  omitiu dois deles — objetivo de uso e critérios de aceite — e a C1 os restitui.
  **Alternativa descartada**: importar também regras específicas de interface,
  música, cliques, banco e ferramenta de teste do projeto de origem.
  **Trade-off**: ganha-se um contrato transversal de treze campos aplicável a
  qualquer artefato; perde-se a concretude do original — o contrato genérico é
  mais abstrato e exige mais julgamento de quem o escreve.
- **DEC-009 — runner TDD da v0.2 (decisão humana, 21/09/2026)**:
  confirmar `python3 -B -m unittest` na raiz para todos os testes
  `tests/test_deco_*.py`; cenários `tests/features/deco_*.feature` participam
  da regressão BDD. O Delivery Gate requer prova de presença, descoberta e
  execução de todas as suítes da Camada Potestatem, além de negativas para
  ausência, exclusão e não execução. Não adotar `deco/tests/**/*.test.mjs`.
  **Razão**: reutilizar o runner existente e impedir que a regressão da raiz
  fique verde sem testar a camada (FR-012, AC-032–AC-038).
  **Alternativa descartada**: harness Node paralelo sem integração à descoberta
  da raiz, que produziria falso verde.
  **Trade-off**: mantém um runner canônico e exige guarda adicional da matriz
  de descoberta/execução antes do Delivery Gate.

### 18. Definition of Done

- [ ] `Definition Gate` está `Passed`, aprovado por instância distinta de quem
      escreveu a spec (FR-003), com atenção explícita ao que o research marca
      como `INFERÊNCIA DE ARQUITETURA`.
- [ ] `Plan Gate` está `Passed`.
- [ ] `Delivery Gate` está `Passed`.
- [ ] Todos os cenários `AC` aplicáveis passam.
- [ ] Todos os requisitos possuem evidência de verificação.
- [ ] Todas as tarefas geradas no Plan Gate estão concluídas.
- [ ] Verificações e checks estáticos disponíveis passam.
- [x] Rodada de migração concluída: conteúdo duplicado removido da SPEC-0001, sem
      referência cruzada quebrada, encerrando RISK-001 nesta rodada documental.
- [ ] Dependência do Git Guardian resolvida: fonte canônica versionada localizada
      e referenciada, **ou** spec própria aberta, **ou** primeira materialização
      executada e validada pela `T004` desta SPEC-0002 (FR-004, DEC-006).
- [ ] Regressão da raiz executou todas as suítes `test_deco_*.py` e
      `deco_*.feature`; ausência, exclusão ou não execução de qualquer uma
      causou falha demonstrada, sem falso verde (DEC-009, FR-012).
- [ ] Contratos materializados no destino fixado pelo Plan Gate.
- [ ] Piloto concluído e medido contra `M-1` a `M-7`, com desvios registrados,
      incluindo avaliação explícita de RISK-011.
- [ ] Cada gate fechado nesta spec registra a evidência mínima de FR-011.
- [ ] Nenhum item fora de escopo introduzido.

## Proveniência

Origens normativas: Notion — "Decisão — Fluxo repo-first, dupla validação e Git
Guardian" (`APROVADA · 28/08/2026`), `89aafb8557414ba8b2c77ef42a41bff0`;
"Decisão — Fluxo SDD repo-first com ponte Notion MCP" (`APROVADA · 16/09/2026`,
com adendo de skills e repasse), `698186dcacc94713b91d5d152c0d7f0b`; "Convenção
handoff × SDD" (`APROVADA · 18/08/2026`), `4ff22dd2037a4f76a517b065fcdfc652`.
Estado de entrada: "Handoff — 16/09/2026 · Deco v0.2",
`e094d66f42c14e1fbb98150d9a2d6518`. Precedente, não norma: "Modelo de Contrato de
Entrega — MusicFlow", `e9555dfab1ce43fab2a4b74110c4617f`. A evidência derivada
das cinco está em `research/notion/fontes-notion.md`. As referências são
proveniência, não dependência de runtime.

Autoria da SPEC-0002: **Codex/Sol**, em **16/09/2026**. Effort solicitado ao
autor: **alto**; effort efetivo observado: `NÃO REGISTRADO`; session ID do autor:
`NÃO REGISTRADO`. Revisão independente original: **Claude Code/Opus**, em
**19/09/2026**; rodada de correção: **Codex/Sol**, em **19/09/2026**;
reconferência aceita: **Claude Code/Opus**, em **19/09/2026**. Effort e session ID
do corretor e do revisor: `NÃO REGISTRADO`. Estado terminal da rodada:
**APROVADO**. A aprovação dos Definition Gates foi decisão humana explícita de
**Deco Ribeyro**, não ato do revisor. Revisão original:
<https://app.notion.com/p/3e0c76b764a4811fbafccd88e379b016>. Reconferência:
<https://app.notion.com/p/3e1c76b764a481ccaac2fe756352cc39>.

**CORREÇÃO FACTUAL PÓS-GATE — NÃO MATERIAL.** Origem: auditoria pré-commit de
19/09/2026. Achado: fronteira Unicode isolada permanece insuficiente sob busca
case-insensitive por causa da palavra portuguesa legítima `todo`. Tratamento:
recomendação corrigida para tokens canônicos em maiúsculas, correspondência
case-sensitive e fronteiras Unicode. Autoria da correção: agente desta sessão;
session ID e effort: `NÃO REGISTRADO`. Aprovação humana: limitada à correção
factual, sem reabertura do gate. O achado não é atribuído retroativamente ao
revisor independente.
