@SPEC-0002 @T002 @governance @red
Feature: Sessão, rodada e ponteiros da governança transversal
  Os testes descrevem o contrato aprovado antes de os mecanismos existirem.

  @AC-014 @FR-005 @US-002 @NFR-002 @NFR-005
  Scenario: Abertura encontra um único contexto ativo
    Given SESSION_CURRENT indica um único contexto íntegro
    When a sessão é aberta sem serviço externo
    Then o contexto e a identidade Git são validados com SG-VÁLIDO

  @AC-014 @FR-005 @US-002 @NFR-002 @NFR-005
  Scenario: Dois contextos ativos bloqueiam a abertura
    Given dois contextos estão marcados como ATUAL
    When a sessão é aberta
    Then nenhum contexto é escolhido e o veredito é SG-BLOQUEADO

  @AC-014 @FR-005 @US-002 @NFR-002 @NFR-005
  Scenario: Identidade divergente bloqueia continuidade
    Given projeto branch ou HEAD diverge sem explicação
    When a sessão é aberta
    Then a continuidade é recusada até reconciliação

  @AC-015 @FR-005 @US-002 @NFR-004
  Scenario: Transcript não substitui contexto curado
    Given transcript ou resumo automático é a única memória disponível
    When o conteúdo é oferecido como contexto canônico
    Then a retomada exige o arquivo curado de SESSION_CURRENT

  @AC-016 @FR-005 @FR-008 @US-002
  Scenario: Mudança material abre nova rodada
    Given decisão escopo ou risco muda durante a sessão
    When a continuidade é verificada
    Then SG-BLOQUEADO exige nova rodada indicada por CURRENT

  @AC-016 @FR-005 @FR-008 @US-002
  Scenario: Correção reversível preserva SESSION_CURRENT
    Given metadado evidência ou proveniência é corrigido sem mudança material
    When a sessão é verificada novamente
    Then SG-CONDICIONAL preserva o único contexto ativo

  @AC-017 @FR-005 @US-002 @NFR-002
  Scenario: Fechamento preserva contexto superado
    Given uma sessão com mudança relevante será encerrada
    When o contexto de encerramento é gravado
    Then os cinco campos e o contexto anterior imutável são validados

  @AC-018 @FR-005 @FR-011 @NFR-002
  Scenario: Estado não observado bloqueia fechamento
    Given o encerramento declara estado Git sem observação
    When o fechamento é submetido
    Then SG-BLOQUEADO exige observação registrada

  @AC-018 @FR-005 @FR-011 @NFR-002
  Scenario: Decisão sem motivo é recusada
    Given o encerramento registra somente o que foi decidido
    When o fechamento é submetido
    Then o porquê obrigatório é exigido

  @AC-018 @FR-005 @FR-011 @NFR-002
  Scenario: Perda de contexto não permite retomada automática
    Given compressão impede reconstruir a unidade ativa
    When a continuidade é verificada
    Then SG-BLOQUEADO exige handoff estruturado

  @AC-018 @FR-005 @FR-011 @NFR-002
  Scenario: Terceira compactação inicia nova sessão
    Given duas compactações anteriores já foram registradas
    When uma terceira compactação é necessária
    Then SG-CONDICIONAL abre nova sessão e repete a verificação

  @AC-019 @FR-005 @FR-004 @NFR-004
  Scenario: Session Guardian Git Guardian e handoff não se substituem
    Given as três verificações foram executadas
    When os resultados são reunidos no relatório
    Then cada mecanismo mantém seus vereditos e responsabilidade

  @AC-020 @FR-006 @FR-007 @NFR-001
  Scenario: Unidade de revisão é um pacote consolidado
    Given três prompts formam uma unidade coerente
    When o pacote de repasse é preparado
    Then exatamente um pedido consolidado é gravado

  @AC-021 @FR-007 @FR-011 @NFR-002
  Scenario: Review Request registra estado e proveniência
    Given uma unidade está pronta para revisão
    When o Review Request é gravado
    Then os campos obrigatórios aparecem sem transcript

  @AC-022 @FR-007 @FR-003 @NFR-002
  Scenario: Review Verdict é separado e assinado
    Given uma unidade está em revisão
    When o Review Verdict é gravado
    Then proveniência achados veredito condições e gate são registrados

  @AC-022 @FR-007 @FR-003 @NFR-002
  Scenario: Mesma sessão não pode aprovar
    Given Request e Verdict declaram o mesmo session ID
    When a aprovação é submetida
    Then a aprovação é bloqueada

  @AC-023 @FR-007 @FR-008 @NFR-001
  Scenario: Correções ocorrem em lote na mesma rodada
    Given o veredito contém achados P0 a P3
    When o implementador corrige a unidade
    Then um Correction Report consolidado recebe uma reconferência

  @AC-024 @FR-008 @FR-005 @NFR-002
  Scenario: CURRENT ambíguo é rejeitado
    Given CURRENT indica mais de uma rodada ativa
    When a revisão é iniciada
    Then nenhuma rodada é escolhida silenciosamente

  @AC-025 @FR-008 @NFR-002 @NFR-004
  Scenario: Rodada concluída é imutável
    Given uma rodada possui veredito aprovado ou reprovado
    When uma alteração histórica é tentada
    Then a alteração é recusada e nova rodada é exigida

  @AC-026 @FR-005 @FR-008 @NFR-001
  Scenario: Mudança material reposiciona CURRENT
    Given uma rodada aguarda correções
    When decisão escopo ou risco muda
    Then nova rodada é criada sem reescrever a anterior
