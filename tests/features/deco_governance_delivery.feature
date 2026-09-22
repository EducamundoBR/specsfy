@spec0002 @t003 @governance @red
Feature: Entrega, evidência e escalonamento da governança transversal
  Os contratos são testados antes da implementação dos mecanismos donos.

  @AC-027
  Scenario: Contrato incompleto não inicia trabalho
    Given um Contrato de Entrega omite um campo obrigatório
    When o trabalho é solicitado
    Then a execução é recusada e o campo é apontado

  @AC-028
  Scenario: PRONTO não prova alcance no destino
    Given verificações internas e evidência estão verdes
    When não há comprovação no destino
    Then ENTREGUE é recusado e o estado permanece PRONTO

  @AC-029
  Scenario: ENTREGUE não prova aceite
    Given a presença do artefato no destino foi comprovada
    When nenhum aprovador registrou aceite explícito
    Then ACEITO é recusado e o estado permanece ENTREGUE

  @AC-029
  Scenario: Papel de aceite não humano é pré-declarado
    Given aceite humano não se aplica ao contrato
    When o contrato é escrito antes da execução
    Then a verificação aprovadora é declarada sem inferência posterior

  @AC-030
  Scenario: Regressão em PRONTO exige nova evidência
    Given um artefato está PRONTO
    When uma regressão é detectada antes do destino
    Then CORREÇÃO NECESSÁRIA exige verde e nova evidência

  @AC-030
  Scenario: Reprovação em ENTREGUE retorna à origem
    Given um artefato está ENTREGUE
    When o aprovador reprova um critério no destino
    Then ENTREGUE COM CORREÇÕES exige nova entrega

  @AC-030
  Scenario: Regressão em ACEITO revoga o aceite
    Given um artefato está ACEITO
    When uma regressão é detectada
    Then ACEITE REVOGADO reabre o percurso completo

  @AC-030
  Scenario: Validação anterior ao destino não é aceite
    Given validação humana ocorreu antes da main declarada
    When o estado da entrega é calculado
    Then ACEITO aguarda conferência no destino

  @AC-031
  Scenario: Resíduo proibido recusa entrega
    Given a entrega contém resíduo falso inerte divergente ou temporário
    When a entrega é verificada
    Then o resíduo deve ser removido ou declarado

  @AC-031
  Scenario: Rollback exige ponto de retorno verificado
    Given rollback nomeia destino e comando sem provar integridade
    When a execução é autorizada
    Then a autorização é recusada até a verificação

  @AC-032
  Scenario: Revisão verde não escala sem gatilho
    Given a revisão favorável não possui gatilho material
    When a rodada é encerrada
    Then o trabalho prossegue localmente sem consulta externa

  @AC-033
  Scenario: Ação irreversível exige gate humano
    Given uma ação irreversível é alcançada
    When a execução autônoma chega antes da ação
    Then a execução para e exige gate humano

  @AC-033
  Scenario: Quarta tentativa falha é recusada
    Given três tentativas falharam no mesmo critério
    When uma quarta tentativa seria iniciada
    Then a decisão retorna ao orquestrador

  @AC-034
  Scenario: Governança funciona com serviço externo desligado
    Given o serviço externo de contexto está indisponível
    When uma unidade de risco baixo ou médio é revisada
    Then o fluxo local completa e somente o escalonamento fica pendente

  @AC-035
  Scenario: Risco alto separa revisão de plano e resultado
    Given uma unidade possui risco alto
    When a revisão obrigatória é preparada
    Then dois Review Requests distintos cercam a escrita

  @AC-036
  Scenario: Proveniência ausente impede fechamento
    Given Request ou Verdict omite proveniência observada
    When o fechamento é solicitado
    Then a rodada permanece aberta com NÃO REGISTRADO

  @AC-037
  Scenario: Base observada divergente bloqueia revisão
    Given branch ou HEAD observado difere do Review Request
    When a revisão de entrega é iniciada
    Then CORREÇÕES SOLICITADAS impede parecer de aprovação

  @AC-038
  Scenario: Veredito Git formal exige evidência executável
    Given o relatório possui somente valor PROVISORIAMENTE
    When um veredito formal do Git Guardian é exigido
    Then o fechamento é recusado sem atribuir estado GG
