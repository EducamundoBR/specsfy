---
name: review-router
description: Classificar o risco de uma unidade de trabalho antes da execução, selecionar a skill do gate corrente, compor perfis de risco e definir revisão, papéis e bloqueios por proveniência, sem aprovar gate.
---

# Review Router

## Escopo e autoridade

Esta skill é o roteador de revisão da Camada Potestatem (SPEC-0002/T007). Ela
classifica o risco, identifica o gate, seleciona uma das quatro skills de gate,
compõe perfis de risco, declara o momento da revisão e registra papéis lógicos.
Ela **não** revisa conteúdo, **não** aprova gate e **não** substitui o Git
Guardian (estado Git), o Session Guardian (continuidade de sessão) nem o
`review-handoff` (pacote e rodada). A decisão de gate continua sendo humana ou
de instância distinta conforme a tabela de níveis.

Precedência em contestação: vale a classificação **mais alta** proposta por
qualquer participante. Nenhuma justificativa rebaixa um gatilho de elevação.

## Entradas

- Unidade de trabalho: identificação, objetivo e escopo declarado.
- Gate corrente: definição, plano ou entrega; ou administração de rodada.
- Superfície tocada: arquivos, sistemas, dados e ações externas previstas.
- Executor, revisor e aprovador previstos, com harness, modelo, effort, data e
  session ID quando observados.

Entrada ausente não é inferida: registra-se `NÃO REGISTRADO` e aplica-se a regra
de bloqueio correspondente.

## Matriz de risco

| Nível | Exemplos | Verificação exigida |
| --- | --- | --- |
| `BAIXO` | leitura, censo somente leitura, formatação, correção editorial, recálculo mecânico, execução de verificação existente, mudança pequena sem alteração de comportamento | autoverificação do executor; segunda família não obrigatória |
| `MÉDIO` | comportamento novo de impacto limitado, alteração em múltiplos arquivos, contrato local, mudança pronta para publicação interna | uma revisão do pacote consolidado antes do fechamento |
| `ALTO` | arquitetura, legado, mudança ampla, integração externa, estado de repositório problemático | revisão do plano antes da escrita e do resultado depois |
| `CRÍTICO` | produção, pagamento, autenticação, dado pessoal, migração de dados, operação destrutiva de histórico | tudo do alto, mais gate humano antes da escrita e novo gate humano antes de ação externa ou irreversível |

Onze gatilhos elevam automaticamente para `ALTO` ou `CRÍTICO`,
independentemente do tamanho:

1. segurança ou permissões;
2. autenticação ou autorização;
3. pagamentos ou faturamento;
4. dado pessoal, segredo ou credencial;
5. migração ou transformação de dados;
6. arquitetura ou processo transversal;
7. publicação em produção;
8. operação destrutiva de histórico;
9. decisão de negócio;
10. promessa ou experiência de cliente;
11. divergência material entre fontes ou entre famílias de modelo.

Os gatilhos 2, 3, 4, 5, 7 e 8 levam a `CRÍTICO`; os demais levam, no mínimo, a
`ALTO`. Mais de um gatilho mantém o nível mais alto entre eles.

## Catálogo de skills e perfis

| Gate ou função | Skill selecionada |
| --- | --- |
| Definição | `review-definition` |
| Plano | `review-plan` |
| Entrega | `review-delivery` |
| Pacote, rodada, `CURRENT` e reconferência | `review-handoff` |

| Perfil de risco | Aplica-se quando a unidade toca |
| --- | --- |
| `security-auth-privacy` | segurança, permissões, autenticação, autorização, privacidade, dado pessoal, segredo ou credencial |
| `data-migration` | schema, migração ou transformação de dados, retenção ou remoção de dado |
| `git-deploy` | histórico Git compartilhado, remote, publicação, deploy ou produção |
| `business-customer` | decisão de negócio, pagamento, faturamento, promessa ou experiência de cliente |

A composição é sempre **uma skill de gate + zero ou mais perfis**. Nunca existe
skill por combinação, e perfil não substitui a skill de gate.

### AC-001 — Classificação precede a execução

O risco é classificado antes da execução de qualquer unidade de trabalho. Sem
classificação registrada, o roteador recusa o início e bloqueia a execução. A
justificativa da classificação é registrada junto da unidade, no mesmo registro
de roteamento.

| Condição | Resultado |
| --- | --- |
| Unidade sem classificação de risco registrada | Recusar a execução até classificar e justificar. |
| Classificação sem justificativa | Recusar; justificativa é campo obrigatório. |
| Classificação e justificativa registradas | Prosseguir para gate, skill, perfis e momento da revisão. |

### AC-002 — Risco baixo exige apenas autoverificação

Correção editorial, formatação, leitura ou recálculo mecânico sem alteração de
comportamento e sem gatilho de elevação é risco baixo. A autoverificação do
executor basta, com as verificações existentes executadas e registradas; não há
exigência de segunda família de modelo nesse nível.

| Condição | Resultado |
| --- | --- |
| Risco baixo, nenhum gatilho, verificações existentes verdes | Autoverificação suficiente; fechar sem segunda família. |
| Qualquer gatilho de elevação presente | Não é risco baixo; reclassificar pela matriz. |

### AC-003 — Elevação automática por natureza do assunto

Elevação automática: uma mudança que toca permissão, autenticação, segredo,
dado pessoal, migração de dados, produção ou histórico de Git é classificada
como alto ou crítico conforme a matriz. O tamanho da mudança não rebaixa a classificação:
uma única linha que altera autenticação continua crítica.

| Condição | Resultado |
| --- | --- |
| Mudança pequena que aciona um dos onze gatilhos | Elevar para alto ou crítico; registrar o gatilho. |
| Pedido para rebaixar por tamanho, pressa ou conveniência | Recusar; prevalece a classificação mais alta. |

### AC-004 — Seleção da skill do gate corrente

No gate de definição, o roteador seleciona `review-definition`; no gate de plano,
`review-plan`; no gate de entrega, `review-delivery`. A administração do pacote
e da rodada cabe a `review-handoff`. O roteador declara o momento da revisão:
prévia (antes da escrita), posterior (depois do resultado) ou ambas.

| Condição | Resultado |
| --- | --- |
| Spec submetida no gate de definição | `review-definition`; momento conforme o nível: médio posterior, alto e crítico ambas. |
| Plano submetido no gate de plano | `review-plan`, com o mesmo critério de momento. |
| Resultado submetido no gate de entrega | `review-delivery`; alto e crítico exigem também a revisão prévia do plano. |
| Gate não identificado | Recusar o roteamento até o gate ser declarado. |

### AC-005 — Perfil compõe com o gate

Uma entrega que altera autenticação compõe `review-delivery` com o perfil
`security-auth-privacy` (segurança, autenticação e privacidade). Não se cria
nova skill para essa combinação: o perfil complementa a skill de gate e acrescenta
critérios à mesma revisão. O perfil não fecha o gate sozinho; o fechamento segue
a skill de gate e a regra de separação.

| Condição | Resultado |
| --- | --- |
| Gate de entrega e superfície de autenticação | `review-delivery` + `security-auth-privacy`, no mesmo pedido de revisão. |
| Pedido de skill dedicada à combinação gate + perfil | Recusar; compor em tempo de execução. |
| Parecer apenas do perfil, sem a skill de gate | Não fecha gate. |

### AC-006 — Papéis vedados a modelo não validado

Modelo novo, barato ou não validado tem a indicação recusada nos papéis
críticos, vedados a ele: aprovador final de segurança; autoridade para operação
destrutiva de histórico; responsável único por publicação; revisor final de
pagamento, autenticação ou dado pessoal. Ele continua autorizado para leitura,
exploração, classificação, documentação mecânica, busca e terceira opinião não
vinculante. A promoção exige benchmark documentado e decisão explícita de quem
orquestra, registrados antes do novo papel.

| Condição | Resultado |
| --- | --- |
| Modelo não validado indicado para papel crítico | Recusar a indicação e manter o papel vago até instância validada. |
| Modelo não validado em tarefa não vinculante | Permitir e registrar o papel lógico. |
| Pedido de promoção sem benchmark ou sem decisão explícita | Recusar a promoção. |

### AC-007 — Papel lógico mapeado a execução concreta

Cada papel lógico — planejamento forte, implementação, revisão e leitura barata —
é registrado mapeado a harness, modelo, effort e data da execução concreta, além
do session ID quando observado. A troca de nome ou versão do modelo não invalida
o processo: atualiza-se o mapeamento, e o fornecedor nunca é fixo. Valor não
observado persiste como `NÃO REGISTRADO`, nunca inferido nem completado depois.

| Condição | Resultado |
| --- | --- |
| Papel executado com harness, modelo, effort e data observados | Registrar o mapeamento completo. |
| Algum valor não observado | Registrar `NÃO REGISTRADO`; se o campo for obrigatório para fechar, bloquear o fechamento. |
| Modelo renomeado ou atualizado | Atualizar o mapeamento; o processo continua válido. |

### AC-008 — Separação entre executor e aprovador

O registro identifica nominalmente o executor (implementador) e o aprovador,
pelo nome ou pela identificação da instância. Quando o aprovador é distinto do
executor, o fechamento do gate pode passar a aprovado, se as demais condições
forem atendidas. Quando executor e aprovador são a mesma instância —
coincidência de agente, sessão ou identidade nominal —, o fechamento é recusado e
bloqueado. O gate permanece pendente até que uma instância distinta ou
independente revise: outro agente, outra sessão, outra família de modelo ou
validação humana explícita. Sinalizar a coincidência não substitui a revisão.

| Condição | Resultado |
| --- | --- |
| Executor e aprovador distintos e nomeados | Fechamento pode seguir para aprovado. |
| Executor é o único aprovador disponível | Recusar o fechamento; gate pendente até instância distinta. |
| Coincidência apenas sinalizada no registro | Continua bloqueado; a sinalização não é revisão. |

### AC-009 — Revisor verifica em vez de herdar a conclusão

O revisor abre contexto novo, inicialmente somente leitura, e recebe o pacote
(spec, plano, diff, testes e critérios). A conclusão do implementador é tratada
como alegação a verificar por teste e evidência, não como fato. Os achados
voltam por severidade (`P0` a `P3`), cada um com evidência e correção proposta.

| Condição | Resultado |
| --- | --- |
| Revisão iniciada no mesmo contexto do implementador | Recusar; abrir contexto novo. |
| Revisor com escrita habilitada no início | Recusar até restringir a somente leitura. |
| Achado sem severidade, evidência ou correção proposta | Devolver ao revisor para completar. |

### AC-010 — Evidência como condição de fechamento

Veredito favorável sem teste, diff e evidência não fecha gate. Na ausência de
evidência mínima, o fechamento é recusado e a aprovação fica bloqueada até que a
evidência seja anexada e conferida.

| Condição | Resultado |
| --- | --- |
| Veredito favorável sem teste, diff ou evidência | Não fecha; exigir a evidência mínima. |
| Veredito com teste, diff e evidência e instância distinta | Encaminhar ao decisor do gate. |

## Registro de roteamento

Saída obrigatória, gravada junto da unidade antes da execução:

- **Unidade**: identificação e objetivo.
- **Risco**: `BAIXO`, `MÉDIO`, `ALTO` ou `CRÍTICO`.
- **Justificativa**: fatos que sustentam o nível.
- **Gatilhos**: números da lista de onze, ou `nenhum`.
- **Gate e skill**: gate corrente e skill selecionada.
- **Perfis**: perfis compostos, ou `nenhum`.
- **Momento da revisão**: `prévia`, `posterior` ou `ambas`.
- **Gates humanos**: exigidos antes da escrita e antes de ação externa, quando crítico.
- **Papéis lógicos**: papel → harness, modelo, effort, data e session ID, com `NÃO REGISTRADO` onde não observado.
- **Executor e aprovador previstos**: nomeados; coincidência bloqueia.

## Casos limítrofes

| Caso | Roteamento |
| --- | --- |
| Correção de ortografia em spec | `BAIXO`; autoverificação. |
| Correção de ortografia em texto de consentimento de dados | Gatilho 4 ou 10: no mínimo `ALTO`. |
| Uma linha em middleware de autenticação | `CRÍTICO`; `security-auth-privacy`; gates humanos antes da escrita e da publicação. |
| Novo teste para comportamento existente | `MÉDIO`; uma revisão consolidada. |
| Refatoração transversal sem mudança de comportamento | Gatilho 6: `ALTO`; plano e resultado revisados. |
| Push de branch local já aprovada | Gatilho 7 ou 8 conforme o alvo; `git-deploy`; gate humano antes da ação. |
| Pareceres divergentes de famílias diferentes | Gatilho 11: `ALTO`; escalar a quem orquestra. |
| Modelo recém-lançado como revisor final de pagamento | Recusar pelo AC-006. |
