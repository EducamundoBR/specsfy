# Handoff ativo

Handoff ATUAL: [`docs/sessoes/2026-09-15-handoff.md`](sessoes/2026-09-15-handoff.md)

Ao abrir uma sessão neste projeto, leia **somente** o arquivo apontado acima.
Handoffs anteriores ficam em `docs/sessoes/` marcados como `SUPERADO` e servem
apenas como rastreabilidade — não devem ser lidos em sequência.

Ao fechar uma sessão com mudança relevante: grave o próximo snapshot em
`docs/sessoes/<AAAA-MM-DD>-handoff.md`, marque o anterior como `SUPERADO` com a
indicação "substituído por", e atualize o ponteiro acima. Exatamente um arquivo
pode ter status `ATUAL`.

Formato do snapshot: cinco campos fixos, delta apenas, releitura em até 30
segundos. Contrato completo em `.deco/RULES.md` (peça 1).
