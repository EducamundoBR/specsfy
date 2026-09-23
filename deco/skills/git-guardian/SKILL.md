---
name: git-guardian
description: Verificar estado Git e autorizações antes de qualquer escrita ou operação sensível, emitindo um único veredito GG com evidência observada.
---

# Git Guardian

## Escopo e autoridade

Esta skill é um procedimento operacional de preflight somente leitura. O operador
executa os comandos, registra a saída e aplica a tabela de decisão; a pessoa
responsável aprova separadamente publicação, deploy ou operação destrutiva. O
preflight precede a escrita em disco, criação ou troca de branch, commit, operação
de remote e publicação ou push. Nenhum resultado autoriza force push. O perfil
específico do repositório e suas instruções prevalecem sobre receita Git genérica.

## Entradas obrigatórias

- Caminho pretendido, projeto, perfil do repositório e operação pretendida com
  efeitos, alvo, aprovador e limite de autorização.
- Branch, HEAD, upstream e remote esperados, provenientes de fonte identificada.
- Origem de cada alteração já existente e proteção reversível disponível.
- Documentação, marco ou tag que fixe a base declarada.

Ausência de entrada ou origem não identificada bloqueia alteração. Não inferir
autorização a partir de um status limpo.

## Coleta somente leitura

Rodar na raiz Git real do workspace pretendido. Saída esperada: valores observados
para cada item abaixo, com data, comando, exit code e evidência resumida. Se um
comando falhar, registrar `NÃO VERIFICADO` e bloquear; rollback: nenhum, pois os
comandos são somente leitura.

```sh
pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1 -uall
git diff --cached --name-status
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git rev-list --left-right --count 'HEAD...@{upstream}'
git remote -v
git worktree list --porcelain
git stash list
git tag --points-at HEAD
git status --branch --short
```

Verificar também operações em andamento por `git status` e pelos estados de
merge, rebase, cherry-pick e revert. Consultar o SHA remoto com `git ls-remote`
quando houver acesso; falha de rede não vira igualdade presumida. Não executar
`stash`, `reset`, `switch` ou `checkout` para limpar origem desconhecida.

## Registro das dezesseis dimensões

Preencher cada linha com observado, esperado, origem da evidência e conclusão.

| Nº | Dimensão | Evidência mínima |
| --- | --- | --- |
| 1 | Pasta e raiz reais | `pwd`, raiz Git |
| 2 | Branch e HEAD | branch simbólica, SHA, detached HEAD |
| 3 | Working tree | status completo |
| 4 | Staged, modificados e não rastreados | paths e origem de cada delta |
| 5 | Upstream e divergência | upstream, ahead/behind |
| 6 | Remotes e identidade aplicável | URLs e SHA do alvo, quando verificável |
| 7 | Worktrees | lista, branches e possíveis conflitos |
| 8 | Stashes | lista e origem relevante |
| 9 | Tags e marcos | tags no HEAD e base declarada |
| 10 | Operação pretendida e efeitos | comando/alvo/efeito declarados |
| 11 | Perfil do repositório e ambiente | AGENTS e regras locais aplicáveis |
| 12 | Contradições | documentação versus estado observado |
| 13 | Proteção necessária | branch safety, tag, patch ou backup verificável |
| 14 | Permissões | operações permitidas e operações bloqueadas |
| 15 | Próxima ação segura | uma ação concreta dentro da autorização |
| 16 | Aprovação humana | sim/não, pessoa e gate aplicável |

Uma worktree auxiliar conhecida deve ser registrada; a existência dela não é
automaticamente sujeira na worktree ativa. Operação Git em andamento, origem
desconhecida, conflito, divergência não explicada ou detached HEAD são bloqueios.
Em `main` ou `master` sem autorização específica, criar branch segura antes de
editar, após novo preflight e conforme autorização local.

## Decisão formal

Produzir exatamente um dos tokens nesta ordem de precedência:
`GG-SEGURO`, `GG-CONDICIONAL`, `GG-BLOQUEADO`. O prefixo GG é distinto do
Session Guardian. A saída registra **estado observado**, **operações permitidas**
e **operações bloqueadas**, evidências, proteção, próxima ação e aprovação humana.

### AC-011 — Precedência

| Condição | Resultado |
| --- | --- |
| Preflight completo antes de qualquer escrita e de branch, commit, remote e publicação | Classificar pela tabela abaixo. |
| Ação destrutiva, publicação ou deploy sem aprovação humana aplicável | `GG-BLOQUEADO`; obter decisão humana antes da ação. |

### AC-012 — Veredito e proteção

Os vereditos formais possíveis são GG-SEGURO, GG-CONDICIONAL e GG-BLOQUEADO.
O prefixo GG é distinto do Session Guardian e impede confundir estado Git com
continuidade da sessão. A saída inclui estado observado, operações permitidas e
operações bloqueadas.

| Condição | Resultado |
| --- | --- |
| Todas as dimensões verificadas, identidade coerente, operação autorizada e sem risco pendente | `GG-SEGURO` somente para as operações declaradas. |
| Trabalho de origem conhecida, proteção reversível necessária, sem contradição | `GG-CONDICIONAL`: aplicar proteção verificável, fazer preflight executável repetido; avançar somente após GG-SEGURO. |
| Origem, identidade ou autorização desconhecida; contradição; operação em andamento; risco não reconciliado | `GG-BLOQUEADO`: nenhuma alteração. |

Antes da materialização versionada, a inspeção manual só admite
`PROVISORIAMENTE SEGURO`, `PROVISORIAMENTE CONDICIONAL` e
`PROVISORIAMENTE BLOQUEADO`. `PROVISORIAMENTE CONDICIONAL` exige proteção
reversível verificável; a inspeção manual deve ser repetida e a análise avança
somente após PROVISORIAMENTE SEGURO, restrita ao escopo já autorizado. Sem saída
do mecanismo executável, não há veredito GG por narrativa. O operador não pode
autodeclarar a unidade liberada por mera explicação.

### AC-013 — Origem desconhecida

| Condição | Resultado |
| --- | --- |
| Worktree suja de origem desconhecida na inspeção manual | `PROVISORIAMENTE BLOQUEADO`; nenhuma limpeza ou reset para abrir branch. |
| Worktree suja de origem desconhecida no mecanismo formal | `GG-BLOQUEADO`; nenhuma alteração até a origem ser explicada e reconciliada. |

Preservar o estado antes de qualquer alteração. Não descartar, redefinir, mover
ou ocultar o trabalho desconhecido.

### AC-038 — Evidência executável

| Condição | Resultado |
| --- | --- |
| Relatório apenas PROVISORIAMENTE classificado, sem saída ou evidência do mecanismo executável | Nenhum estado GG pode ser atribuído por narrativa. |
| Sem saída verificável do mecanismo versionado | Veredito formal ausente; fechamento recusado. |

## Saída obrigatória

Registrar uma linha `Veredito: GG-...` com apenas um token, seguida de projeto,
raiz, branch/HEAD, upstream, remotes, divergência, worktrees, stashes, tags,
operação pretendida, dezesseis dimensões, evidência de execução, operações
permitidas, operações bloqueadas, proteção, próxima ação, autorização e momento
da coleta. `GG-CONDICIONAL` exige nova coleta após proteção. `GG-BLOQUEADO`
encerra a unidade até reconciliação, sem autoaprovação.
