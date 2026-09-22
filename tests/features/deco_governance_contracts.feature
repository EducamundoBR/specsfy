@SPEC-0002 @T001
Feature: Contratos transversais da Camada Potestatem
  Os mecanismos de revisão e Git devem observar AC-001 a AC-013.

  @AC-001 @FR-001 @US-001 @NFR-001
  Scenario: Unidade iniciada sem classificação de risco
    Given uma unidade de trabalho prestes a ser executada sem classificação registrada
    When a execução é iniciada
    Then a execução é recusada até o risco ser classificado e justificado
    And a classificação fica registrada junto da unidade

  @AC-002 @FR-001 @FR-002 @NFR-001
  Scenario: Correção editorial de risco baixo
    Given uma correção editorial sem alteração de comportamento nem gatilho de elevação
    When o executor conclui e roda as verificações existentes
    Then a autoverificação do executor basta
    And nenhuma revisão por segunda família é exigida

  @AC-003 @FR-001 @US-004 @NFR-003
  Scenario: Mudança pequena que toca assunto sensível
    Given uma mudança pequena em permissão, autenticação, segredo, dado pessoal, migração, produção ou histórico de Git
    When o risco é classificado
    Then a classificação sobe automaticamente para alto ou crítico
    And o tamanho reduzido não rebaixa essa classificação

  @AC-004 @FR-002 @FR-006 @US-001
  Scenario: Gate de definição seleciona a revisão correspondente
    Given uma spec submetida ao gate de definição
    When o roteador classifica a unidade
    Then a skill selecionada é review-definition
    And o roteador declara revisão prévia, posterior ou ambas

  @AC-005 @FR-002 @FR-006 @NFR-001
  Scenario: Entrega de autenticação compõe gate e perfil
    Given uma entrega que altera autenticação
    When o roteador classifica a unidade
    Then seleciona review-delivery e o perfil de segurança, autenticação e privacidade
    And não cria skill nova para a combinação
    And o perfil não fecha o gate sozinho

  @AC-006 @FR-002 @FR-003 @NFR-003
  Scenario: Modelo não validado indicado a papel crítico
    Given um modelo novo, barato ou ainda não validado
    When é indicado para aprovação final de segurança, histórico destrutivo, publicação única, pagamento, autenticação ou dado pessoal
    Then a indicação é recusada
    And leitura, exploração, classificação, documentação, busca e terceira opinião não vinculante continuam permitidas
    And promoção exige benchmark documentado e decisão explícita

  @AC-007 @FR-002 @NFR-002 @NFR-004
  Scenario: Papel lógico usa execução concreta rastreável
    Given um papel lógico atribuído a uma instância
    When a execução é registrada
    Then constam harness, modelo, effort e data reais
    And mudança de versão do modelo não invalida o processo
    And dado desconhecido permanece literalmente NÃO REGISTRADO

  @AC-008 @FR-003 @US-001 @NFR-002
  Scenario: Aprovador distinto assina o fechamento
    Given o aprovador é distinto de quem executou
    When o gate é fechado
    Then o registro identifica nominalmente executor e aprovador
    And o gate pode passar a aprovado

  @AC-008 @FR-003 @US-001 @NFR-002
  Scenario: Executor é o único aprovador disponível
    Given o executor é também o único aprovador disponível
    When o fechamento é tentado
    Then o fechamento é recusado e o gate permanece pendente
    And sinalizar a coincidência não substitui revisão por instância distinta

  @AC-009 @FR-003 @FR-006 @NFR-002
  Scenario: Revisor verifica a conclusão em vez de herdá-la
    Given um pacote com spec, plano, diff, testes e critérios
    When o revisor assume a unidade
    Then abre contexto novo e inicialmente somente leitura
    And trata a conclusão do implementador como alegação a verificar
    And devolve achados por severidade com evidência e correção proposta

  @AC-010 @FR-003 @FR-011 @NFR-002
  Scenario: Veredito favorável sem evidência não fecha o gate
    Given um veredito favorável sem teste, diff nem evidência
    When o gate é submetido a fechamento
    Then o gate não fecha
    And exige-se evidência mínima antes de aprovação

  @AC-011 @FR-004 @US-004 @NFR-003
  Scenario: Preflight precede escrita e operação sensível
    Given uma escrita, troca de branch, commit, alteração de remote ou publicação proposta
    When a operação é considerada
    Then o preflight Git read-only é realizado antes dela
    And sem mecanismo versionado o parecer permanece provisório
    And operação destrutiva, publicação ou deploy espera decisão humana

  @AC-012 @FR-004 @NFR-002
  Scenario: Mecanismo formal emite veredito prefixado
    Given o Git Guardian executável versionado
    When sua saída é anexada ao relatório
    Then o veredito é exatamente um entre GG-SEGURO, GG-CONDICIONAL e GG-BLOQUEADO
    And declara estado observado, operações permitidas e bloqueadas
    And o prefixo o distingue do Session Guardian

  @AC-012 @FR-004 @NFR-002
  Scenario: Inspeção manual não inventa veredito formal
    Given inspeção manual somente leitura sem saída executável anexada
    When o resultado é registrado
    Then é exatamente um entre PROVISORIAMENTE SEGURO, PROVISORIAMENTE CONDICIONAL e PROVISORIAMENTE BLOQUEADO
    And nenhum veredito GG é emitido por narrativa
    And a unidade não se autodeclara liberada

  @AC-012 @FR-004 @NFR-002
  Scenario: Condição manual exige proteção e nova inspeção
    Given trabalho conhecido com proteção reversível verificável e sem origem desconhecida
    When a inspeção manual retorna PROVISORIAMENTE CONDICIONAL
    Then a proteção especificada é aplicada e a inspeção é repetida
    And somente após PROVISORIAMENTE SEGURO a análise autorizada continua

  @AC-012 @FR-004 @NFR-002
  Scenario: Condição formal exige proteção e novo preflight
    Given trabalho conhecido com proteção reversível verificável e sem origem desconhecida
    When o Git Guardian retorna GG-CONDICIONAL
    Then a proteção especificada é aplicada e o preflight executável é repetido
    And somente após GG-SEGURO as operações declaradas prosseguem

  @AC-013 @FR-004 @US-004 @NFR-003
  Scenario: Origem desconhecida bloqueia inspeção manual
    Given uma worktree suja de autoria desconhecida
    When a inspeção manual ocorre sem mecanismo versionado
    Then o resultado é PROVISORIAMENTE BLOQUEADO
    And não ocorre descarte, redefinição nem troca de branch para limpar o estado
    And recomenda-se preservar o trabalho antes de alterar

  @AC-013 @FR-004 @US-004 @NFR-003
  Scenario: Origem desconhecida bloqueia mecanismo formal
    Given uma worktree suja de autoria desconhecida
    When a saída do mecanismo versionado é anexada
    Then o veredito é GG-BLOQUEADO
    And nenhuma alteração ocorre até o risco ser explicado e reconciliado
