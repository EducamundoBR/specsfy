# Contratos de repasse da rodada de revisão

Este arquivo define os campos e decisões para três artefatos distintos de uma
única rodada. Ao usar, criar arquivos separados para Review Request, Review
Verdict e Correction Report; cada bloco abaixo é um modelo, não um parecer
preenchido. O implementador redige pedido e correções; o revisor redige o
veredito; o decisor humano registra o gate. Nenhum autor se autoaprova.
Copiar apenas o modelo preenchível deste arquivo para o pedido da rodada. O
revisor usa `review-verdict.md`; o implementador usa `correction-report.md`
quando houver achados. Os três arquivos da rodada são distintos e não se
sobrescrevem.

## Estados e pré-condições

`RASCUNHO → PRONTO PARA REVISÃO → EM REVISÃO → CORREÇÕES SOLICITADAS → PRONTO
PARA RECONFERÊNCIA → APROVADO | REPROVADO`. Os termos “para revisão” e “para
reconferência” são estados deste pacote, distintos do `PRONTO` da entrega.
Exatamente uma rodada fica ativa. `CURRENT` identifica logicamente essa rodada;
`SESSION_CURRENT` identifica a sessão e é controlado pelo Session Guardian.
O `review-handoff` valida `CURRENT`, transições e unicidade. A revisão começa
somente após diff, teste e evidência verificáveis. Nenhum gate se fecha por
parecer sem essas evidências.

| Entrada | Decisão | Saída |
| --- | --- | --- |
| Pedido incompleto, base não comprovada ou autor sem identidade | Não iniciar revisão. | `RASCUNHO`, lacunas registradas. |
| Pedido completo e um `CURRENT` inequívoco | Encaminhar pacote ao revisor distinto, inicialmente em leitura. | `PRONTO PARA REVISÃO`, depois `EM REVISÃO`. |
| Achados com correção possível | Implementador trata em lote; revisor recebe uma reconferência consolidada. | `CORREÇÕES SOLICITADAS`, depois `PRONTO PARA RECONFERÊNCIA`. |
| Parecer independente e decisão humana com teste, diff e evidência | Registrar resultado sem alterar rodada encerrada. | `APROVADO` ou `REPROVADO`. |

### AC-020 — Unidade consolidada

Três prompts de revisão referentes ao mesmo gate compõem uma única unidade de
trabalho e exatamente um Review Request consolidado. Não abrir três revisões
separadas por prompt; perfis complementares são anexos ao mesmo pedido. Uma
unidade traz escopo, base, risco, evidência e decisor identificados.

| Condição | Resultado |
| --- | --- |
| Vários prompts do mesmo gate e mesma base | Consolidar em um pedido, preservar perfis e evitar pareceres incompatíveis. |
| Gates ou bases diferentes | Abrir rodada própria para cada unidade, com `CURRENT` inequívoco. |

### AC-021 — Review Request (implementador)

Preencher o artefato de pedido em formato delta, referenciando fontes canônicas.
Campo desconhecido recebe `NÃO REGISTRADO`, com impacto e ação para completar;
campo obrigatório ausente mantém `RASCUNHO`. Sem histórico de conversa ou
transcript no pedido: referenciar apenas fontes estáveis.

**Modelo preenchível do pedido**

Responsável: implementador

- **Unidade**: <preencher>
- **Risco**: <preencher>
- **Justificativa**: <preencher>
- **Gate**: <preencher>
- **Perfil**: <preencher>
- **Branch**: <preencher>
- **HEAD**: <preencher>
- **Base**: <preencher>
- **Escopo do diff**: <preencher>
- **Arquivos**: <preencher>
- **Testes**: <preencher>
- **Decisões**: <preencher>
- **Dúvidas**: <preencher>
- **Fontes**: <preencher>
- **Restrições**: <preencher>
- **Harness**: <preencher>
- **Modelo**: <preencher>
- **Effort**: <preencher>
- **Session ID**: <preencher>
- **Implementador**: <preencher>
- **Revisor designado**: <preencher>
- **Decisor designado**: <preencher>

Exemplo válido: base e HEAD observados, diff delimitado, testes com resultados
e proveniência completa. Exemplo inválido: `HEAD` apenas presumido ou `Session ID`
ausente; manter `RASCUNHO`, sem enviar ao revisor.

| Condição | Resultado |
| --- | --- |
| Base, HEAD, testes ou identidade do implementador ausentes | Manter `RASCUNHO` e completar o campo com evidência antes do envio. |
| Campos completos e escopo verificável | Encaminhar um Review Request consolidado. |

| Campo obrigatório | Valor a registrar |
| --- | --- |
| Unidade, risco e justificativa, branch, HEAD, base e escopo do diff | Identidade, classificação, SHA observado e intervalo revisável. |
| Arquivos, testes, decisões, dúvidas, fontes e restrições | Paths, comandos e resultados, decisões com motivos, links estáveis e limites. |
| Harness, modelo, effort, session ID e implementador | Proveniência nominal e verificável da autoria. |
| Gate, perfil e decisor | Gate solicitado, perfil de revisão e pessoa responsável pela decisão. |

Checklist antes de envio: [ ] base e HEAD conferidos; [ ] diff no escopo; [ ]
testes e falhas classificados; [ ] evidências acessíveis; [ ] restrições e
rollback registrados; [ ] revisor diferente do implementador.

### AC-022 — Review Verdict (revisor)

Review Verdict é artefato separado e distinto do Review Request. O revisor
registra harness, modelo, effort, session ID e revisor nominal, com evidências,
achados `P0`, `P1`, `P2` e `P3`, veredito, condições e gate resultante recomendado.
Cada achado contém arquivo ou fonte, trecho verificável, impacto, severidade e
correção proposta. P0 bloqueia imediatamente; P1 bloqueia o gate; P2 exige
correção ou justificativa aceita; P3 registra melhoria sem aprovação tácita.
O decisor registra decisão separada do parecer técnico. Se implementador e
revisor têm o mesmo session ID, aprovação bloqueada até revisão independente
por instância distinta. Identidade nominal coincidente também bloqueia.

| Condição | Resultado |
| --- | --- |
| Evidências ou escopo insuficientes | Devolver pedido ao implementador; gate pendente. |
| Revisor igual ao implementador ou mesmo session ID | Recusar aprovação; obter outra instância. |
| Parecer completo | Registrar achados por severidade e recomendação, sem autoaprovar gate. |

### AC-023 — Correction Report (implementador)

Correções em lote preservam uma reconferência por rodada. Correction Report fica
na mesma rodada. Enviar ao mesmo revisor uma única vez, com pacote consolidado;
nenhuma revisão isolada para cada correção. Revisor confere cada achado e a
regressão; correção não material permanece no mesmo `CURRENT`.
Registrar achados tratados, correções aplicadas e achados não aplicados com justificativa,
novo diff, testes, estado Git e pedido de reconferência.

| Condição | Resultado |
| --- | --- |
| Correção altera somente metadado ou evidência | Atualizar Correction Report nesta rodada, preservar base e pedir reconferência. |
| Achado não aplicado | Registrar justificativa e risco residual para revisor e decisor. |

### AC-024 — Ponteiro único

| Condição | Resultado |
| --- | --- |
| `CURRENT` resolve exatamente uma rodada ativa | Prosseguir, após conferir base e HEAD. |
| `CURRENT` indica mais de uma rodada ativa | Revisão rejeitada; nenhuma rodada é escolhida silenciosamente. Resolver ambiguidade antes de emitir parecer. |
| `CURRENT` ausente, quebrado ou alvo encerrado | Bloquear revisão e reconciliar o ponteiro. |

### AC-025 — Rodada concluída

| Condição | Resultado |
| --- | --- |
| Veredito final aprovado ou reprovado, com gate registrado | Encerrar rodada e preservar seus artefatos imutáveis. |
| Alteração solicitada em rodada encerrada | Alteração recusada; revisão adicional exige rodada nova. |

### AC-026 — Mudança material

Qualquer mudança de decisão, escopo incluído ou excluído ou classe de risco é
`MUDANÇA MATERIAL`: criar nova rodada e atualizar `CURRENT` antes de nova
revisão. A rodada anterior é encerrada sem reescrita de seu conteúdo. Registrar
o motivo, a base anterior e a nova base; não absorver a mudança no Correction
Report da rodada atual.

| Condição | Resultado |
| --- | --- |
| Mudança material detectada em qualquer estado | Bloquear avanço da rodada atual; abrir nova rodada com pedido delta e ponteiro único. |
| Nenhuma mudança material e correções consolidadas | Preservar rodada atual e solicitar uma reconferência. |
