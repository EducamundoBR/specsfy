STATUS: CANDIDATAS — NÃO APROVADAS.
Este arquivo não é instalado como norma, não é roteado aos agentes e não
participa de gates. Existe apenas para avaliação futura.

# Camada Deco — candidatas

Heurísticas observadas em uso real que ainda **não** foram promovidas a peça
canônica. Nada aqui tem força normativa: não vale como regra, não é lido pelos
agentes no fluxo de trabalho e não bloqueia nenhuma entrega.

## Candidata 1 — Timing de operações Git/GitHub

Antes de sugerir ou executar commit, push, merge, rebase ou abertura de PR,
avaliar se aquele é o **momento** adequado — trabalho concluído, testes
passando, nada pela metade — e não apenas se a operação em si é segura.

**Origem:** observação de uso, 20/08/2026. Operações corretas executadas no
momento errado geraram retrabalho de correção depois.

**O que falta para virar peça:** definir onde a avaliação entra sem duplicar os
gates que o Specsfy já aplica, e decidir se é regra de comportamento ou
critério dentro de uma skill dedicada a Git.

## Candidata 2 — Endereço sugerido em toda proposta de acréscimo

Ao propor acrescentar algo — regra, skill, conteúdo — indicar junto o destino
sugerido: camada Deco neste fork, contribuição ao upstream, ou projeto
consumidor.

**Origem:** observação de uso, 20/08/2026. Sem o endereço explícito, preferência
organizacional tende a cair em diretório gerenciado pelo CLI (perdida na
próxima atualização) e melhoria genérica tende a ficar presa neste fork, sem
chegar ao upstream.

**O que falta para virar peça:** critério objetivo de fronteira entre "genérico
o bastante para o upstream" e "específico desta organização", para não
transformar cada sugestão em uma decisão de arquitetura.
