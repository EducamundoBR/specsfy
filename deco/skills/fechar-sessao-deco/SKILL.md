---
name: fechar-sessao-deco
description: Fechar a sessão gravando o handoff de cinco campos, marcar o anterior como SUPERADO e atualizar o ponteiro docs/HANDOFF.md. Use ao encerrar trabalho com mudança relevante.
---

# Fechar sessão (camada Deco)

> **CONTRATO DOCUMENTAL DA V0.1 — execução automática pendente do instalador e
> do verifier.** Nesta versão a skill descreve o procedimento e os critérios de
> aceite; a aplicação é manual e a atomicidade ainda não está implementada.

## Quando usar

Ao encerrar uma sessão que produziu mudança relevante: troca de thread, troca de
dia ou pedido explícito de fechamento. Continuação imediata do mesmo assunto no
mesmo dia não gera handoff — não há delta a registrar.

## Procedimento

1. **Confirmar o projeto e o estado verificável.** Ler o diretório de trabalho,
   a branch corrente, o HEAD e o status do repositório. Sem esses quatro dados o
   campo 2 do handoff não pode ser preenchido.
2. **Localizar `docs/HANDOFF.md`.** Ele é a porta de entrada e aponta para
   exatamente um snapshot ativo.
3. **Ler somente o snapshot ativo** indicado pelo ponteiro. Não ler handoffs
   anteriores em sequência: eles são rastreabilidade, não contexto.
4. **Produzir o novo handoff** com os cinco campos fixos. A fonte normativa
   desses campos e das regras abaixo é `.deco/RULES.md` (peça 1) no projeto
   consumidor, derivada de `deco/rules/canonical.md` nesta distribuição — esta
   skill apenas operacionaliza essa peça e não constitui uma segunda norma. Em
   divergência, vale `.deco/RULES.md`. A enumeração a seguir é reproduzida para
   a skill ser executável sem consulta externa, nesta ordem e com estes nomes:
   1. Projeto e data
   2. Estado verificável
   3. Decisões da sessão + porquê
   4. Pendências e próximo passo
   5. Evidências e links canônicos
5. **Aplicar formato delta e a regra dos 30 segundos.** Registrar só o que mudou
   nesta sessão; linkar contexto estável em vez de duplicá-lo; cortar o que não
   couber em meio minuto de releitura. O porquê das decisões é obrigatório.
6. **Marcar o anterior como `SUPERADO`**, alterando seu campo de status.
7. **Acrescentar "substituído por"** no anterior, apontando para o caminho do
   novo snapshot.
8. **Criar o novo snapshot datado** em `docs/sessoes/<AAAA-MM-DD>-handoff.md`.
9. **Atualizar `docs/HANDOFF.md`** para apontar para o novo snapshot.
10. **Validar que existe exatamente um `ATUAL`**: o arquivo apontado pelo
    ponteiro tem status `ATUAL` e nenhum outro snapshot em `docs/sessoes/`
    mantém esse status.
11. **Falhar sem alterar parcialmente os arquivos** se qualquer validação
    anterior falhar. Um handoff pela metade é pior que nenhum: deixa o ponteiro
    e o snapshot em desacordo.

## Critérios de aceite

- `docs/HANDOFF.md` aponta para um arquivo que existe.
- O arquivo apontado tem os cinco campos, com os nomes exatos acima.
- Exatamente um snapshot tem status `ATUAL`.
- O snapshot anterior tem status `SUPERADO` e a indicação "substituído por".
- Nenhum campo "Decisões da sessão + porquê" registra apenas o quê.

## Limites

- A skill não escreve no Notion. Quando o projeto tiver espelho canônico lá,
  sinalizar que ele também precisa ser atualizado e deixar a ação com a pessoa.
- A skill não substitui o fluxo de fechamento do método base nem desliga
  qualquer regra dele.
- Enquanto a atomicidade do passo 11 não estiver implementada, conferir
  manualmente o par ponteiro/snapshot antes de encerrar.
