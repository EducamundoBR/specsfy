# Correction Report — modelo da mesma rodada

Responsável: implementador

Produzir um único relatório delta depois de tratar os achados em lote. Preservar
o Review Request e o Review Verdict originais. Enviar ao mesmo revisor uma
reconferência consolidada na mesma rodada quando a correção não alterar decisão,
escopo ou classe de risco. `MUDANÇA MATERIAL` exige rodada nova e novo `CURRENT`;
não reescrever rodada encerrada.

## Identificação e proveniência

- **Unidade**: <preencher>
- **CURRENT**: <preencher>
- **Review Request**: <preencher>
- **Review Verdict**: <preencher>
- **Implementador**: <preencher>
- **Revisor da reconferência**: <preencher>
- **Base original**: <preencher>
- **HEAD observado**: <preencher>

## Tratamento dos achados

- **Achados tratados**: <preencher>
- **Correções aplicadas**: <preencher>
- **Não aplicados e justificativa**: <preencher>

| Achado | Correção e arquivo | Evidência | Não aplicado: motivo e risco residual |
| --- | --- | --- | --- |
| <preencher> | <preencher> | <preencher> | <preencher> |

Usar `Nenhum` nos campos de não aplicados somente após conferir todos os achados.
Não abrir revisão isolada por correção. O revisor confere o lote e a regressão.

## Novo estado e reconferência

- **Novo diff**: <preencher>
- **Testes**: <preencher>
- **Estado Git**: <preencher>
- **Pedido de reconferência**: <preencher>

O estado Git inclui raiz, branch, HEAD, upstream, divergência, stage, working
tree e operação em andamento observados. Declarar falhas e testes não executados;
não inferir resultado. O pedido de reconferência identifica o mesmo revisor,
salvo impossibilidade documentada, e referencia o pacote consolidado.

| Condição | Resultado |
| --- | --- |
| Correção não material, diff e testes completos | Manter `CURRENT` e pedir uma reconferência consolidada. |
| Decisão, escopo incluído ou excluído, ou classe de risco alterados | Encerrar a rodada anterior sem reescrita; abrir nova rodada e atualizar `CURRENT`. |
| Achado sem tratamento nem justificativa | Não declarar pronto para reconferência. |

Exemplo válido: todos os achados mapeados ao novo diff e testes, com não aplicados
justificados. Exemplo inválido: correção registrada sem novo HEAD ou sem resultado
dos testes; a reconferência não começa.
