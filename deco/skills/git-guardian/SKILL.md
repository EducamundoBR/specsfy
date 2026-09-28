---
name: git-guardian
description: Verificar estado Git e autorizações antes de qualquer escrita ou operação sensível, emitindo um único veredito GG com evidência observada.
---

# Git Guardian

## Escopo e autoridade

Esta skill contém o procedimento e o bloco Python versionado que executa o
preflight somente leitura. O operador informa expectativas de fonte identificada,
executa o bloco, anexa a saída JSON e aplica a decisão; a pessoa
responsável aprova separadamente publicação, deploy ou operação destrutiva. O
preflight precede a escrita em disco, criação ou troca de branch, commit, operação
de remote e publicação ou push. Nenhum resultado autoriza force push. O perfil
específico do repositório e suas instruções prevalecem sobre receita Git genérica.

## Entradas obrigatórias

- Caminho pretendido, projeto, perfil do repositório e operação pretendida com
  efeitos, alvo, aprovador e limite de autorização.
- Branch, HEAD, upstream e remote esperados, provenientes de fonte identificada.
  O valor literal `AUSENTE` é válido para upstream ou remote quando a ausência
  foi conferida e a operação é apenas local; não é um fallback para publicação.
- Origem de cada alteração já existente e proteção reversível disponível.
- Documentação, marco ou tag que fixe a base declarada.

Ausência de entrada ou origem não identificada bloqueia alteração. Não inferir
autorização a partir de um status limpo.

## Coleta somente leitura

Capturar `pwd -P` antes de mudar de pasta; então rodar na raiz Git real do
workspace pretendido. Saída esperada: valores observados
para cada item abaixo, com data, comando, exit code e evidência resumida. Se um
comando essencial falhar sem uma ausência esperada declarada, registrar
`NÃO VERIFICADO` e bloquear. Rollback: nenhum, pois os comandos são somente leitura.

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

Falha de `@{upstream}` é esperada somente quando a fonte declara `AUSENTE`;
registrar divergência como `NÃO APLICÁVEL` para operação local. Verificar também operações em andamento por `git status` e pelos estados de
merge, rebase, cherry-pick e revert. Consultar o SHA remoto com `git ls-remote`
para operação de remote ou publicação; falha de rede bloqueia essas operações,
mas não altera a autorização de uma operação estritamente local. Não executar
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

Os tokens permitidos são `GG-SEGURO`, `GG-CONDICIONAL` e `GG-BLOQUEADO`.
Avaliar bloqueio primeiro, condição depois e segurança por último: a prioridade
fail-closed é `GG-BLOQUEADO` > `GG-CONDICIONAL` > `GG-SEGURO`. A saída registra **estado observado**, **operações permitidas**
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

## Execução versionada e saída verificável

Esta skill é o mecanismo versionado de T004: o bloco abaixo coleta Git real e
emite uma saída JSON. Um checklist preenchido sem executar o bloco permanece
provisório. Para emitir `GG-*`, informar as variáveis `GG_EXPECTED_ROOT`,
`GG_EXPECTED_BRANCH`, `GG_EXPECTED_HEAD`, `GG_EXPECTED_UPSTREAM`,
`GG_EXPECTED_REMOTE`, `GG_OPERATION`, `GG_DIRTY_ORIGIN`, `GG_PROTECTION`,
`GG_WORKTREES_KNOWN`, `GG_CONTRADICTION`, `GG_HUMAN_APPROVAL` e `GG_PROFILE`,
além de `GG_COMMAND` e `GG_TARGET` para o comando pretendido e seu alvo,
sem segredos, com valores e proveniência no relatório. Para upstream presente, informar
`GG_EXPECTED_AHEAD` e `GG_EXPECTED_BEHIND`. Para operação de remote ou
publicação, informar `GG_REMOTE_NAME` e `GG_EXPECTED_REMOTE_SHA`. O operador
executa o bloco Python na raiz observada; saída esperada: um objeto JSON com
exatamente um `veredito`, dezesseis dimensões, evidência dos comandos e motivos.
Rollback: nenhum; o bloco só lê Git e arquivos de perfil. Anexar a saída
integral ao relatório, sem segredos. A falta dela impede veredito formal.

Na raiz Git, após definir as entradas `GG_*`, executar o bloco versionado pelo
comando abaixo. Saída esperada: exatamente um objeto JSON. Rollback: nenhum.

```sh
python3 -B -c 'import pathlib, re; p = pathlib.Path("deco/skills/git-guardian/SKILL.md"); s = p.read_text(encoding="utf-8"); m = re.search(r"<!-- GG_EXECUTABLE_BEGIN -->\s*```python\n(.*?)\n```\s*<!-- GG_EXECUTABLE_END -->", s, re.S); assert m, "bloco executável ausente"; exec(compile(m.group(1), str(p), "exec"))'
```

<!-- GG_EXECUTABLE_BEGIN -->
```python
import datetime
import hashlib
import json
import os
import pathlib
import shlex
import subprocess


e = os.environ
evidence = []
block = []
conditional = []
cwd = pathlib.Path.cwd().resolve()


def git(*args, timeout=12):
    try:
        result = subprocess.run(
            ["git", *args], cwd=cwd, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
        out = result.stdout.strip()
        code = result.returncode
    except (OSError, subprocess.TimeoutExpired):
        out, code = "", 124
    evidence.append({
        "comando": "git " + " ".join(args), "exit_code": code,
        "sha256_saida": hashlib.sha256(out.encode()).hexdigest(),
    })
    return code, out


def need(name, allowed=None):
    value = e.get(name, "").strip()
    if not value or (allowed and value not in allowed):
        block.append("entrada inválida: " + name)
    return value


expected_root = need("GG_EXPECTED_ROOT")
expected_branch = need("GG_EXPECTED_BRANCH")
expected_head = need("GG_EXPECTED_HEAD")
expected_upstream = need("GG_EXPECTED_UPSTREAM")
expected_remote = need("GG_EXPECTED_REMOTE")
operation = need("GG_OPERATION", {"read", "edit", "commit", "branch", "remote", "publish", "deploy", "destructive"})
command = need("GG_COMMAND")
target = need("GG_TARGET")
try:
    command_parts = shlex.split(command)
except ValueError:
    command_parts = []
    block.append("comando pretendido inválido")
dirty_origin = need("GG_DIRTY_ORIGIN", {"clean", "known", "unknown"})
protection = need("GG_PROTECTION", {"none", "required", "verified"})
worktrees_known = need("GG_WORKTREES_KNOWN", {"yes", "no"})
contradiction = need("GG_CONTRADICTION", {"yes", "no"})
approval = need("GG_HUMAN_APPROVAL", {"yes", "no"})
profile = need("GG_PROFILE")

root_code, root_raw = git("rev-parse", "--show-toplevel")
root = pathlib.Path(root_raw).resolve() if root_code == 0 else None
branch_code, branch = git("branch", "--show-current")
head_code, head = git("rev-parse", "HEAD")
status_code, status = git("status", "--porcelain=v1", "-uall")
stage_code, stage = git("diff", "--cached", "--name-status")
up_code, upstream_raw = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
remote_code, remotes = git("remote", "-v")
worktree_code, worktrees = git("worktree", "list", "--porcelain")
stash_code, stashes = git("stash", "list")
tag_code, tags = git("tag", "--points-at", "HEAD")
git("status", "--branch", "--short")

for name, code in (("raiz", root_code), ("branch", branch_code),
                   ("HEAD", head_code), ("working tree", status_code),
                   ("stage", stage_code), ("remotes", remote_code),
                   ("worktrees", worktree_code), ("stashes", stash_code),
                   ("tags", tag_code)):
    if code != 0:
        block.append("coleta falhou: " + name)
if root is None or str(root) != str(pathlib.Path(expected_root).resolve()):
    block.append("raiz divergente")
if branch_code != 0 or not branch or branch != expected_branch:
    block.append("branch divergente ou detached HEAD")
if head_code != 0 or head != expected_head:
    block.append("HEAD divergente")
if branch in {"main", "master"} and e.get("GG_MAIN_AUTH") != "yes":
    block.append("branch principal sem autorização")
if not pathlib.Path(profile).is_file() or root is None or not pathlib.Path(profile).resolve().is_relative_to(root):
    block.append("perfil do repositório ausente")
if contradiction == "yes":
    block.append("contradição declarada")

upstream = upstream_raw if up_code == 0 else "AUSENTE"
ahead = behind = "NÃO APLICÁVEL"
if upstream != expected_upstream:
    block.append("upstream divergente")
if upstream != "AUSENTE":
    div_code, divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    if div_code != 0:
        block.append("divergência não verificada")
    else:
        parts = divergence.split()
        if len(parts) != 2:
            block.append("divergência inválida")
        else:
            ahead, behind = parts
            if ahead != e.get("GG_EXPECTED_AHEAD") or behind != e.get("GG_EXPECTED_BEHIND"):
                block.append("ahead/behind divergente")
elif operation in {"remote", "publish"}:
    block.append("upstream ausente para operação remota")

remote_present = bool(remotes)
if expected_remote == "AUSENTE":
    if remote_present:
        block.append("remote inesperado")
elif expected_remote not in remotes:
    block.append("remote divergente")
if operation in {"remote", "publish"}:
    remote_name = need("GG_REMOTE_NAME")
    remote_sha = need("GG_EXPECTED_REMOTE_SHA")
    ref = "refs/heads/" + expected_branch
    remote_sha_code, observed_remote = git("ls-remote", remote_name, ref, timeout=12)
    if remote_sha_code != 0 or not observed_remote or not observed_remote.startswith(remote_sha + "\t"):
        block.append("SHA remoto ausente ou divergente")

state_paths = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD",
               "rebase-merge", "rebase-apply")
ongoing = []
for name in state_paths:
    code, path = git("rev-parse", "--git-path", name)
    if code != 0 or not path:
        block.append("operação Git não verificável: " + name)
    elif pathlib.Path(path).exists():
        ongoing.append(name)
if ongoing:
    block.append("operação Git em andamento")
worktree_count = worktrees.count("worktree ")
if worktree_count > 1 and worktrees_known != "yes":
    block.append("worktree auxiliar sem origem conhecida")
dirty = bool(status)
if dirty and dirty_origin == "unknown":
    block.append("worktree suja de origem desconhecida")
if dirty and dirty_origin == "clean":
    block.append("origem declarada limpa contradiz status")
if dirty and dirty_origin == "known" and protection != "verified":
    conditional.append("proteger trabalho conhecido e repetir preflight")
if protection == "required":
    conditional.append("proteção reversível pendente")
if operation in {"publish", "deploy", "destructive"} and approval != "yes":
    block.append("aprovação humana obrigatória")
if operation == "destructive":
    block.append("operação destrutiva requer gate próprio; sem autorização implícita")
if e.get("GG_FORCE_PUSH") == "yes":
    block.append("force push nunca autorizado implicitamente")
if any(part in {"-f", "--force", "--force-with-lease"}
       or part.startswith(("--force=", "--force-with-lease="))
       for part in command_parts) or (len(command_parts) > 2 and command_parts[0:2] == ["git", "push"]
                                    and any(part.startswith("+") for part in command_parts[2:])):
    block.append("comando com force bloqueado")
if command_parts[0:2] == ["git", "push"] and operation != "publish":
    block.append("push declarado como outra operação")
if operation == "publish" and command_parts[0:2] != ["git", "push"]:
    block.append("operação declarada não corresponde ao comando")

verdict = "GG-BLOQUEADO" if block else "GG-CONDICIONAL" if conditional else "GG-SEGURO"
dimensions = {
    "1": {"pasta": str(cwd), "raiz": str(root) if root else "NÃO VERIFICADO"},
    "2": {"branch": branch, "HEAD": head},
    "3": {"working_tree_suja": dirty},
    "4": {"stage_sujo": bool(stage), "modificados_ou_nao_rastreados": dirty},
    "5": {"upstream": upstream, "ahead": ahead, "behind": behind},
    "6": {"remote_corresponde": expected_remote == "AUSENTE" and not remote_present or expected_remote in remotes},
    "7": {"worktrees": worktree_count, "origem_conhecida": worktrees_known == "yes"},
    "8": {"stashes": len(stashes.splitlines()) if stashes else 0},
    "9": {"tags_no_HEAD": len(tags.splitlines()) if tags else 0},
    "10": {"operacao": operation, "comando": command, "alvo": target},
    "11": {"perfil_presente": pathlib.Path(profile).is_file()},
    "12": {"contradicao": contradiction},
    "13": {"protecao": protection},
    "14": {"permitidas": [operation] if verdict == "GG-SEGURO" else [],
           "bloqueadas": [operation] if verdict != "GG-SEGURO" else []},
    "15": {"proxima_acao": "reconciliar" if block else "proteger e repetir" if conditional else operation},
    "16": {"aprovacao_humana": approval},
}
print(json.dumps({
    "veredito": verdict, "dimensoes": dimensions, "motivos": block + conditional,
    "evidencias": evidence, "operacoes_permitidas": dimensions["14"]["permitidas"],
    "operacoes_bloqueadas": dimensions["14"]["bloqueadas"],
    "momento_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
}, ensure_ascii=False, sort_keys=True))
```
<!-- GG_EXECUTABLE_END -->

## Saída obrigatória

Registrar uma linha `Veredito: GG-...` com apenas um token, seguida de projeto,
raiz, branch/HEAD, upstream, remotes, divergência, worktrees, stashes, tags,
operação pretendida, dezesseis dimensões, evidência de execução, operações
permitidas, operações bloqueadas, proteção, próxima ação, autorização e momento
da coleta. `GG-CONDICIONAL` exige nova coleta após proteção. `GG-BLOQUEADO`
encerra a unidade até reconciliação, sem autoaprovação.
