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
sem segredos, com valores e proveniência no relatório. `GG_EXPECTED_REMOTE` é
`AUSENTE` ou `<nome> <URL>`, comparado exatamente com as linhas fetch e push de
`git remote -v`, nunca por substring. Para upstream presente, informar
`GG_EXPECTED_AHEAD` e `GG_EXPECTED_BEHIND`. Para operação de remote ou
publicação, informar `GG_REMOTE_NAME`, igual ao nome do remote esperado, e
`GG_EXPECTED_REMOTE_SHA`. Em `main` ou `master`, `GG_MAIN_AUTH=yes` registra a
autorização específica; sem ela, bloqueio. O operador
executa o bloco Python na raiz observada; saída esperada: um objeto JSON com
exatamente um `veredito`, dezesseis dimensões, evidência dos comandos e motivos.
Rollback: nenhum; o bloco só lê Git e arquivos de perfil. Anexar a saída
integral ao relatório, sem segredos. A falta dela impede veredito formal.

### Comando efetivo, não rótulo declarado

O bloco tokeniza `GG_COMMAND` e deriva a operação efetiva sem executá-lo. O
rótulo `GG_OPERATION` precisa coincidir com ela; explicação, comentário ou
justificativa textual nunca substitui o token nem as entradas enumeradas.

| Condição | Resultado |
| --- | --- |
| Opções globais `-C`, `-c`, `--git-dir`, `--work-tree` e flags neutras antes do subcomando | Normalizadas; o subcomando real é classificado. |
| `-C`, `--git-dir` ou `--work-tree` apontam para fora da raiz verificada | `GG-BLOQUEADO`. |
| `-c` fora da lista neutra (`user.name`, `user.email`, `color.*`, `core.quotepath`, `advice.*`), inclusive `alias.*` | `GG-BLOQUEADO`. |
| Wrappers `env`, `command`, `nohup`, `time` e `exec` sem opções; variáveis `LANG`, `LC_*`, `TZ`, `NO_COLOR` e `TERM` | Descartados antes da classificação; outras variáveis ou opções bloqueiam. |
| Operador de shell, redirecionamento, expansão `$` ou crase; executável desconhecido; subcomando desconhecido ou alias; opção não suportada | `GG-BLOQUEADO`: parsing ambíguo nunca é tratado como leitura. |
| Abreviação de opção longa sensível, como `--amen` ou `--forc` | Tratada como a opção completa. |
| `push` rotulado como outra operação; `reset --hard`, `branch -D` ou `-d`, `checkout -- .`, `stash drop` ou `pop`, `remote prune`, `fetch`/`pull`/`remote update` com `--prune` ou `--prune-tags`, `clean -f`, `commit --amend` ou `rebase` rotulados como edição | Remoção ou reescrita tem operação efetiva `destructive`, divergente do rótulo; `GG-BLOQUEADO`. |
| `remote add`, `rename`, `set-url`, `set-head` ou `set-branches` | Mutação de remote: exige `GG_HUMAN_APPROVAL=yes` e nomes de remote presentes em `GG_TARGET`; `fetch` não exige aprovação; `remote prune --dry-run` é leitura. |
| Paths efetivos de `add`, `rm`, `mv`, `commit`, `restore --staged`, `reset -- <path>` e `edit <alvo>`; em `commit` sem pathspec, todos os paths já staged | Precisam ficar dentro de `GG_TARGET`, que aceita vários alvos separados por espaço. |
| Escopo amplo (`add -A`, `add -u`, `add .`, `add -p` sem path, `--pathspec-from-file`, `commit -a`, `commit -p`, `merge`, `apply`, `stash`, `reset` sem path) | Exige `GG_TARGET=.`; caso contrário, `GG-BLOQUEADO`. |
| Nome de branch ou tag criado, trocado ou renomeado; branch atual quando upstream, descrição, rename ou cópia não nomeiam outra | Precisa coincidir literalmente com um item de `GG_TARGET`. |
| `worktree add` | Caminho dentro da raiz e de `GG_TARGET`; branch criada (por `-b` ou pelo nome do diretório) em `GG_TARGET`; `-f` ou `-B` é destrutivo. |
| `pull` | Integra mudanças na árvore: exige `GG_TARGET=.` além das regras de remote. |
| `push` sem remote explícito | Destino resolvido por `branch.<b>.pushRemote`, `remote.pushDefault` e `branch.<b>.remote`; precisa ser o remote verificado. `push.default` fora de `simple`, `current` ou `upstream` e `remote.<nome>.push` configurado bloqueiam. |
| `main` ou `master` sem `GG_MAIN_AUTH=yes` | Somente leitura real e `git switch -c <branch>` ou `git checkout -b <branch>` a partir do HEAD observado, declarados como `branch`, podem prosseguir; qualquer outra operação ou ponto de partida bloqueia. |
| Push com force, `+refspec` ou lease; push fora do remote e da branch verificados; `--all`, `--mirror` ou `--tags` | `GG-BLOQUEADO`; force push nunca é autorizado implicitamente. |
| Leitura real (`status`, `log`, `diff`, `show`, listagens de branch/tag/remote/stash/worktree, `config --get`, `clean -n`) | Operação efetiva `read`; segue a classificação das demais dimensões. |

Formas declarativas sem Git (`edit <alvo>`, `write <alvo>`, `read <alvo>` e
`deploy <alvo>`) mapeiam para a operação homônima. A dimensão 10 registra a
operação efetiva, o executável, o subcomando e o diretório-alvo.

### Perfil fechado `miguel-day1`

`GG_MODE=miguel-day1` troca a análise geral por uma allowlist fechada,
comparada pelo argv completo do texto bruto de `GG_COMMAND` (sem espaço nas
bordas, quebra de linha ou tabulação). Não há prefixo, substring nem abreviação; o que
não coincidir exatamente com uma forma abaixo é `GG-BLOQUEADO`. As demais
dimensões continuam valendo. `GG_TARGET` precisa ser a raiz (`.` ou o caminho
absoluto dela); `GG_MAIN_AUTH` é ignorado; outro valor de `GG_MODE` bloqueia.

| Condição | Resultado |
| --- | --- |
| `git status`, `git status --short`, `git diff`, `git diff --cached`, `git rev-parse HEAD`, `git rev-parse --show-toplevel`, `git rev-parse --abbrev-ref HEAD`, `git branch --show-current`, `git worktree list`, `git ls-files` | Leitura; `GG-SEGURO` se as dimensões passarem. |
| `git log` com somente `--oneline`, `--stat`, `--graph`, `--decorate` e `-n <1-999>`, sem repetição | Leitura. |
| `git show <ref>` ou `git show --stat <ref>`, com `HEAD`, `HEAD~N` ou SHA hexadecimal que resolva para commit | Leitura. |
| `git switch -c piloto/<slug>` (minúsculas, dígitos e hífens; branch inexistente; sem ponto de partida) | Branch local; única escrita liberada em `main`/`master`. |
| `git add -- <path>...` com paths existentes ou rastreados, dentro da raiz após resolver symlinks, fora de `.git`, sem `.`, glob, `:` mágico, `@`, hífen inicial ou path vazio | Edição local. |
| `git commit -m <mensagem não vazia>` com stage não vazio, `git diff --cached --check` verde e `GG_STAGE_SHA256` igual ao SHA-256 dos bytes crus de `git diff --cached --binary` | Nunca `GG-SEGURO`: no máximo `GG-CONDICIONAL`, que exige aprovação de Deco. A saída traz `stage_evidencia` (arquivos, numstat, check e hash). |
| `git push` em qualquer forma, mesmo com aprovação declarada | `GG-BLOQUEADO`; a publicação é um procedimento separado com autorização humana, novo GG, destino e SHA. |
| Qualquer outro comando, opção, wrapper, executável absoluto, opção global, composição, redirecionamento, subshell, substituição, comentário ou quebra de linha | `GG-BLOQUEADO`. |

Para o commit, inspecionar `git diff --cached` e registrar o `sha256_diff` de
`stage_evidencia`; repetir o GG com `GG_STAGE_SHA256` imediatamente antes do
commit. Se algo entrar no stage depois da inspeção, o hash diverge e bloqueia.

Na raiz Git, após definir as entradas `GG_*`, executar o bloco versionado pelo
comando abaixo. Em projeto consumidor sem a camada instalada, `GG_SKILL` aponta
o caminho absoluto deste arquivo; o bloco continua lendo o Git do diretório
atual. Saída esperada: exatamente um objeto JSON. Rollback: nenhum.

```sh
python3 -B -c 'import os, pathlib, re; p = pathlib.Path(os.environ.get("GG_SKILL", "deco/skills/git-guardian/SKILL.md")); s = p.read_text(encoding="utf-8"); m = re.search(r"<!-- GG_EXECUTABLE_BEGIN -->\s*```python\n(.*?)\n```\s*<!-- GG_EXECUTABLE_END -->", s, re.S); assert m, "bloco executável ausente"; exec(compile(m.group(1), str(p), "exec"))'
```

<!-- GG_EXECUTABLE_BEGIN -->
```python
import datetime
import hashlib
import json
import os
import pathlib
import re
import shlex
import subprocess


e = os.environ
evidence = []
block = []
conditional = []
cwd = pathlib.Path.cwd().resolve()


def git(*args, timeout=12, where=None):
    where = where or cwd
    try:
        result = subprocess.run(
            ["git", *args], cwd=where, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
        out = result.stdout.strip()
        code = result.returncode
    except (OSError, subprocess.TimeoutExpired):
        out, code = "", 124
    prefix = "git " if where == cwd else "git -C " + shlex.quote(str(where)) + " "
    evidence.append({
        "comando": prefix + " ".join(args), "exit_code": code,
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
dirty_origin = need("GG_DIRTY_ORIGIN", {"clean", "known", "unknown"})
protection = need("GG_PROTECTION", {"none", "required", "verified"})
worktrees_known = need("GG_WORKTREES_KNOWN", {"yes", "no"})
contradiction = need("GG_CONTRADICTION", {"yes", "no"})
approval = need("GG_HUMAN_APPROVAL", {"yes", "no"})
profile = need("GG_PROFILE")
expected_remote_name = "" if expected_remote == "AUSENTE" else expected_remote.partition(" ")[0]

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
# Paths já staged: um commit sem pathspec inclui todos eles.
staged_paths = [part for line in stage.splitlines() for part in line.split("\t")[1:]]

# Análise do comando pretendido. O comando nunca é executado: apenas tokenizado
# e classificado. Rótulo declarado não substitui a operação efetiva; parsing
# desconhecido ou ambíguo devolve operação None e bloqueia.
SHELL_META = re.compile(r"[;&|<>`$\n\r]")
ENV_ALLOWED = re.compile(r"(?:LANG|LC_[A-Z]+|TZ|NO_COLOR|TERM)=")
CONFIG_ALLOWED = re.compile(r"(?:user\.name|user\.email|color\.[a-z.]+|core\.quotepath|advice\.[a-z]+)=", re.I)
WRAPPERS = {"env", "command", "nohup", "time", "exec"}
DECLARATIVE = {"read": "read", "edit": "edit", "write": "edit", "deploy": "deploy"}
GLOBAL_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree"}
GLOBAL_FLAGS = {"--no-pager", "-p", "--paginate", "-P", "--no-replace-objects",
                "--literal-pathspecs", "--glob-pathspecs", "--noglob-pathspecs",
                "--icase-pathspecs", "--no-optional-locks", "--no-advice"}
READ_ONLY = {"status", "log", "diff", "show", "rev-parse", "rev-list", "ls-files", "ls-tree",
             "cat-file", "blame", "annotate", "describe", "shortlog", "grep", "merge-base",
             "name-rev", "for-each-ref", "show-ref", "show-branch", "count-objects",
             "check-ignore", "check-attr", "check-ref-format", "cherry", "range-diff",
             "whatchanged", "verify-commit", "verify-tag", "ls-remote", "diff-tree",
             "diff-index", "diff-files", "var", "version", "help"}
ALWAYS_DESTRUCTIVE = {"rebase", "filter-branch", "filter-repo", "update-ref", "gc", "prune", "replace"}
b = expected_branch
PUSH_REFSPECS = {b, "HEAD", "HEAD:" + b, b + ":" + b, "refs/heads/" + b, "HEAD:refs/heads/" + b,
                 b + ":refs/heads/" + b, "refs/heads/" + b + ":refs/heads/" + b}


# O Git aceita abreviações de opções longas (--amen = --amend). Todo prefixo de
# uma opção sensível é tratado como a própria opção sensível.
SENSITIVE_LONG = {"--hard", "--merge", "--keep", "--force", "--force-with-lease",
                  "--force-if-includes", "--force-create", "--amend", "--delete", "--prune",
                  "--mirror", "--all", "--branches", "--tags", "--follow-tags",
                  "--discard-changes", "--patch", "--rebase", "--abort", "--no-verify",
                  "--output", "--ext-diff", "--open-files-in-pager", "--upload-pack",
                  "--receive-pack", "--exec", "--worktree", "--overlay", "--no-overlay",
                  "--ours", "--theirs", "--pathspec-from-file", "--interactive", "--refmap",
                  "--prune-tags"}


def shorts(args):
    """Normaliza flags: -fdx vira -f, -d, -x; -n5 vira -n; --opt=v vira --opt."""
    flags = set()
    for arg in args:
        if re.fullmatch(r"-[A-Za-z]+", arg):
            flags.update("-" + char for char in arg[1:])
        elif re.fullmatch(r"-[A-Za-z]\d+", arg):
            flags.add(arg[:2])
        elif arg.startswith("-") and arg != "--":
            option = arg.split("=", 1)[0]
            flags.add(option)
            if option.startswith("--") and len(option) > 3:
                flags.update(name for name in SENSITIVE_LONG if name.startswith(option))
    return flags


def positionals(args, valued=()):
    found, skip = [], False
    for arg in args:
        if arg == "--":
            break
        if skip:
            skip = False
        elif arg in valued or (re.fullmatch(r"-[A-Za-z]+", arg) and "-" + arg[-1] in valued):
            skip = True
        elif not arg.startswith("-"):
            found.append(arg)
    return found


# Alvos efetivos do comando, confrontados depois com GG_TARGET.
scope = {"caminhos": [], "nomes": [], "amplo": None, "cria_branch": False, "altera_remote": False,
         "integra": False}


def pathspecs(args, valued=()):
    found = positionals(args, valued)
    if "--" in args:
        found += args[args.index("--") + 1:]
    return found


def bind(paths=(), names=(), broad=None):
    if broad and not scope["amplo"]:
        scope["amplo"] = broad
    for path in paths:
        if path in {".", ":", ":/", "*"} or path.startswith(":("):
            scope["amplo"] = scope["amplo"] or path
        else:
            scope["caminhos"].append(path)
    scope["nomes"].extend(names)


def unsupported(sub, option):
    return None, ["opção não suportada em git " + sub + ": " + option]


def remote_problem(sub, name):
    if name is not None and name != expected_remote_name:
        return ["remote do " + sub + " diverge do remote verificado: " + name]
    return []


def classify_push(rest):
    problems, force, delete, found = [], False, False, []
    k = 0
    while k < len(rest):
        arg = rest[k]
        if arg == "--":
            found += rest[k + 1:]
            break
        if not arg.startswith("-"):
            found.append(arg)
        elif arg in {"-o", "--push-option"}:
            k += 1
        elif arg.startswith("--push-option="):
            pass
        else:
            given = shorts([arg])
            forced = given & {"-f", "--force", "--force-with-lease", "--force-if-includes"}
            deleted = given & {"-d", "--delete", "--prune"}
            scoped = given & {"--all", "--branches", "--mirror", "--tags", "--follow-tags"}
            force, delete = force or bool(forced), delete or bool(deleted)
            if scoped:
                problems.append("escopo de push além do alvo verificado: " + arg)
            known = {"-u", "--set-upstream", "-v", "--verbose", "-q", "--quiet", "--porcelain",
                     "--progress", "--no-progress", "--atomic", "--no-atomic", "-n", "--dry-run"}
            if not (forced or deleted or scoped) and given - known:
                return unsupported("push", arg)
        k += 1
    for spec in found[1:]:
        if spec.startswith("+"):
            force, spec = True, spec[1:]
        if spec.startswith(":"):
            delete = True
        elif spec not in PUSH_REFSPECS:
            problems.append("refspec de push fora do alvo verificado: " + spec)
    # Sem remote explícito, o destino vem da configuração, não do rótulo.
    remote = found[0] if found else None
    for key in ("branch." + branch + ".pushRemote", "remote.pushDefault", "branch." + branch + ".remote"):
        if remote is None:
            code, value = git("config", "--get", key)
            remote = value if code == 0 and value else None
    remote = remote or "origin"
    problems += remote_problem("push", remote)
    if len(found) < 2:
        code, mode = git("config", "--get", "push.default")
        if code == 0 and mode not in {"simple", "current", "upstream"}:
            problems.append("push.default não suportado: " + mode)
    code, configured = git("config", "--get-all", "remote." + remote + ".push")
    if code == 0 and configured:
        problems.append("refspec de push configurado no remote: " + remote)
    if delete:
        return "destructive", problems
    if force:
        problems.insert(0, "comando com force bloqueado")
    return "publish", problems


def safe_start(start):
    """Ponto de partida de branch nova: ausente ou o próprio HEAD observado."""
    return start is None or start in {"HEAD", head, branch}


def classify(sub, rest, where):
    flags = shorts(rest)
    dashdash = "--" in rest
    pos = positionals(rest)
    if "--pathspec-from-file" in flags:
        bind(broad="--pathspec-from-file")
    if sub in READ_ONLY:
        for arg in rest:
            if arg == "--":
                break
            if (shorts([arg]) & {"--ext-diff", "--output", "--open-files-in-pager", "--upload-pack"}
                    or (sub == "grep" and arg.startswith("-O"))):
                return unsupported(sub, arg)
        return "read", []
    if sub == "push":
        return classify_push(rest)
    if sub in ALWAYS_DESTRUCTIVE:
        return "destructive", []
    if sub in {"add", "mv", "rm"}:
        if sub == "rm" and flags & {"-f", "--force"}:
            return "destructive", []
        paths = pathspecs(rest, {"--chmod", "--pathspec-from-file"})
        broad = sorted(flags & {"-A", "--all", "-u", "--update"}) if sub == "add" else []
        if sub == "add" and not paths and flags & {"-p", "--patch", "-i", "--interactive", "-e", "--edit"}:
            broad = broad or ["--patch"]
        bind(paths, broad=broad[0] if broad else None)
        return "edit", []
    if sub in {"apply", "format-patch"}:
        bind(broad=sub)
        return "edit", []
    if sub == "commit":
        if "--amend" in flags:
            return "destructive", []
        if flags & {"-n", "--no-verify"}:
            return unsupported(sub, "--no-verify")
        valued = {"-m", "--message", "-F", "--file", "-C", "--reuse-message", "-c", "--reedit-message",
                  "--author", "--date", "--fixup", "--squash", "-t", "--template", "--trailer", "--cleanup"}
        broad = sorted(flags & {"-a", "--all", "-p", "--patch", "--interactive"})
        paths = pathspecs(rest, valued | {"--pathspec-from-file"})
        bind(paths, broad=broad[0] if broad else None)
        if not paths or flags & {"-i", "--include"}:
            bind(staged_paths)
        return "commit", []
    if sub in {"merge", "cherry-pick", "revert", "am"}:
        bind(broad=sub)
        return ("destructive" if "--abort" in flags else "commit"), []
    if sub == "reset":
        if flags & {"--hard", "--merge", "--keep"}:
            return "destructive", []
        if flags & {"-p", "--patch"} or dashdash:
            paths = pathspecs(rest)
            paths = paths[1:] if paths[:1] == ["HEAD"] else paths
            bind(paths, broad=None if paths else "reset")
            return "edit", []
        extra = flags - {"-q", "--quiet", "--mixed", "--soft", "-N"}
        if extra:
            return unsupported(sub, sorted(extra)[0])
        if pos in ([], ["HEAD"]):
            bind(broad="reset")
            return "edit", []
        return "destructive", []
    if sub == "restore":
        staged_only = flags & {"-S", "--staged"} and not flags & {"-W", "--worktree"}
        if staged_only:
            bind(pathspecs(rest, {"-s", "--source", "--pathspec-from-file"}))
            return "edit", []
        return "destructive", []
    if sub == "clean":
        dry = flags & {"-n", "--dry-run"} and not flags & {"-f", "--force", "-i", "--interactive"}
        return ("read" if dry else "destructive"), []
    if sub == "checkout":
        if (flags & {"-f", "--force", "-B", "-p", "--patch", "-m", "--merge", "--ours", "--theirs",
                     "--overlay", "--no-overlay", "--pathspec-from-file"} or dashdash):
            return "destructive", []
        extra = flags - {"-q", "--quiet", "-b", "--orphan", "--detach", "-t", "--track",
                         "--no-track", "--progress", "--no-progress", "--guess", "--no-guess"}
        if extra:
            return unsupported(sub, sorted(extra)[0])
        if flags & {"-b", "--orphan"}:
            if len(pos) > 2:
                return "destructive", []
            bind(names=pos[:1])
            scope["cria_branch"] = "-b" in flags and safe_start(pos[1] if len(pos) > 1 else None)
            return "branch", []
        if not pos:
            return ("branch" if "--detach" in flags else "read"), []
        if len(pos) == 1 and pos[0] != "." and not (where / pos[0]).exists():
            code, _ = git("rev-parse", "--verify", "--quiet", pos[0] + "^{commit}", where=where)
            if code == 0:
                bind(names=pos)
                return "branch", []
        return "destructive", []
    if sub == "switch":
        if flags & {"-C", "--force-create", "-f", "--force", "--discard-changes", "-m", "--merge"}:
            return "destructive", []
        extra = flags - {"-c", "--create", "--orphan", "-d", "--detach", "-q", "--quiet", "-t",
                         "--track", "--no-track", "--guess", "--no-guess", "--progress", "--no-progress"}
        if extra or not 1 <= len(pos) <= 2:
            return unsupported(sub, sorted(extra)[0] if extra else "argumentos")
        bind(names=pos[:1])
        scope["cria_branch"] = bool(flags & {"-c", "--create"}) and safe_start(pos[1] if len(pos) > 1 else None)
        return "branch", []
    if sub == "branch":
        if flags & {"-D", "-f", "--force", "-M", "-C", "-d", "--delete"}:
            return "destructive", []
        write = {"-m", "--move", "-c", "--copy", "-u", "--set-upstream-to",
                 "--unset-upstream", "--edit-description", "-t", "--track", "--no-track", "--create-reflog"}
        listing = {"-l", "--list", "-a", "--all", "-r", "--remotes", "--contains", "--no-contains",
                   "--merged", "--no-merged", "--points-at", "--show-current"}
        display = {"-v", "--verbose", "-q", "--quiet", "--sort", "--format", "--color", "--no-color",
                   "--column", "--no-column", "-i", "--ignore-case", "--abbrev", "--no-abbrev", "--omit-empty"}
        extra = flags - write - listing - display
        if extra:
            return unsupported(sub, sorted(extra)[0])
        names = positionals(rest, {"--sort", "--format", "--points-at", "-u", "--set-upstream-to"})
        if flags & write or (names and not flags & listing):
            # Sem nome explícito, upstream, descrição, rename e cópia afetam a branch atual.
            if not names or (flags & {"-m", "--move", "-c", "--copy"} and len(names) == 1):
                names = [branch or "HEAD"] + names
            bind(names=names)
            return "branch", []
        return "read", []
    if sub == "tag":
        if flags & {"-d", "--delete", "-f", "--force"}:
            return "destructive", []
        listing = {"-l", "--list", "-n", "--contains", "--no-contains", "--merged", "--no-merged",
                   "--points-at", "-v", "--verify"}
        display = {"--sort", "--format", "--color", "--column", "--no-column", "-i", "--ignore-case", "--omit-empty"}
        create = {"-a", "--annotate", "-s", "--sign", "--no-sign", "-m", "--message", "-F", "--file",
                  "-u", "--local-user", "-e", "--edit", "--cleanup", "--create-reflog"}
        extra = flags - listing - display - create
        if extra:
            return unsupported(sub, sorted(extra)[0])
        names = positionals(rest, {"-m", "--message", "-F", "--file", "-u", "--local-user", "--sort",
                                   "--format", "--points-at", "--cleanup"})
        if flags & create or (names and not flags & listing):
            bind(names=names)
            return "branch", []
        return "read", []
    if sub == "stash":
        action = rest[0] if rest and not rest[0].startswith("-") else "push"
        mapped = {"list": "read", "show": "read", "drop": "destructive", "clear": "destructive",
                  "pop": "destructive", "push": "edit", "save": "edit", "apply": "edit",
                  "branch": "branch", "create": "edit", "store": "edit"}.get(action)
        if mapped == "edit":
            paths = rest[rest.index("--") + 1:] if action == "push" and "--" in rest else []
            bind(paths, broad=None if paths else "stash " + action)
        elif mapped == "branch":
            bind(names=pos[1:2])
        return (mapped, []) if mapped else unsupported(sub, action)
    if sub == "worktree" and pos[:1] == ["add"]:
        if flags & {"-f", "--force", "-B"}:
            return "destructive", []
        found = positionals(rest, {"-b", "-B", "--reason"})
        created = [rest[k + 1] for k, arg in enumerate(rest[:-1]) if arg == "-b"]
        if not created and "--detach" not in flags and len(found) > 1:
            created = found[2:3] or [pathlib.PurePath(found[1]).name]
        bind(paths=found[1:2], names=created)
        return "branch", []
    if sub == "worktree":
        action = pos[0] if pos else ""
        mapped = {"list": "read", "add": "branch", "remove": "destructive", "prune": "destructive",
                  "lock": "edit", "unlock": "edit", "move": "edit", "repair": "edit"}.get(action)
        if mapped in {"branch", "edit"}:
            bind(broad="worktree " + action)
        return (mapped, []) if mapped else unsupported(sub, action or "sem ação")
    if sub == "remote":
        if not pos:
            extra = flags - {"-v", "--verbose"}
            return unsupported(sub, sorted(extra)[0]) if extra else ("read", [])
        mapped = {"show": "read", "get-url": "read", "add": "remote", "rename": "remote",
                  "set-url": "remote", "set-head": "remote", "set-branches": "remote",
                  "update": "remote", "prune": "destructive", "remove": "destructive",
                  "rm": "destructive"}.get(pos[0])
        if pos[0] == "prune" and flags & {"-n", "--dry-run"}:
            mapped = "read"
        if pos[0] == "update" and flags & {"-p", "--prune"}:
            mapped = "destructive"
        scope["altera_remote"] = pos[0] in {"add", "rename", "set-url", "set-head", "set-branches"}
        if scope["altera_remote"]:
            bind(names=pos[1:3] if pos[0] == "rename" else pos[1:2])
        return (mapped, []) if mapped else unsupported(sub, pos[0])
    if sub == "config":
        getters = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "-l", "--list",
                   "--get-color", "--get-colorbool"}
        neutral = {"--global", "--local", "--system", "--worktree", "--show-origin", "--show-scope",
                   "--null", "-z", "--name-only", "--includes", "--no-includes", "--bool", "--int", "--path"}
        if not flags - getters - neutral and (flags & getters or pos[:1] in (["get"], ["list"]) or len(pos) == 1):
            return "read", []
        return None, ["escrita de configuração Git exige classificação humana"]
    if sub == "reflog":
        mapped = {"show": "read", "exists": "read", "expire": "destructive",
                  "delete": "destructive"}.get(pos[0] if pos else "show")
        return (mapped, []) if mapped else unsupported(sub, pos[0])
    if sub == "symbolic-ref":
        if flags <= {"-q", "--quiet", "--short"} and len(pos) == 1:
            return "read", []
        return None, ["escrita de configuração Git exige classificação humana"]
    if sub in {"fetch", "pull"}:
        for arg in rest:
            if shorts([arg]) & {"--upload-pack", "--refmap", "--exec"}:
                return unsupported(sub, arg)
        if sub == "pull":
            scope["integra"] = True
            bind(broad="pull")
        if (flags & {"-f", "--force", "-r", "--rebase", "-p", "--prune", "-P", "--prune-tags"}
                or any(spec.startswith("+") or ":" in spec for spec in pos[1:])):
            return "destructive", []
        return "remote", remote_problem(sub, pos[0] if pos else None)
    return None, []


def analyze(text):
    """Deriva a operação efetiva sem executar o comando; ambiguidade bloqueia."""
    detail = {"operacao_efetiva": None, "executavel": None, "subcomando": None, "diretorio_alvo": None}
    if SHELL_META.search(text):
        return detail, ["comando composto, redirecionado ou com expansão de shell"]
    try:
        parts = shlex.split(text)
    except ValueError:
        return detail, ["comando pretendido inválido"]
    i = 0
    while i < len(parts):
        word = parts[i]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", word, re.S):
            if not ENV_ALLOWED.match(word):
                return detail, ["variável de ambiente não permitida: " + word.split("=", 1)[0]]
        elif word in WRAPPERS:
            if i + 1 < len(parts) and parts[i + 1].startswith("-"):
                return detail, ["wrapper com opção não suportada: " + word + " " + parts[i + 1]]
        else:
            break
        i += 1
    if i >= len(parts):
        return detail, ["comando pretendido inválido"]
    exe, args = parts[i], parts[i + 1:]
    detail["executavel"] = exe
    if exe in DECLARATIVE and args and not any(arg.startswith("-") for arg in args):
        detail["operacao_efetiva"] = DECLARATIVE[exe]
        if DECLARATIVE[exe] == "edit":
            bind(args)
        return detail, []
    if pathlib.PurePosixPath(exe).name not in {"git", "git.exe"}:
        return detail, ["executável não reconhecido: " + exe]
    where, git_dir, work_tree, j = cwd, None, None, 0
    while j < len(args) and args[j].startswith("-"):
        option, has_value, value = args[j].partition("=")
        if option in {"--git-dir", "--work-tree"} and has_value:
            j += 1
        elif args[j] in GLOBAL_WITH_VALUE:
            if j + 1 >= len(args):
                return detail, ["opção global do Git sem valor: " + args[j]]
            option, value = args[j], args[j + 1]
            j += 2
        elif args[j] in GLOBAL_FLAGS:
            j += 1
            continue
        elif args[j] in {"--version", "-v", "--help", "-h"}:
            detail["operacao_efetiva"] = "read"
            return detail, []
        else:
            return detail, ["opção global do Git desconhecida: " + args[j]]
        if option == "-C":
            where = (where / value).resolve() if value else where
        elif option == "-c" and not CONFIG_ALLOWED.match(value):
            return detail, ["configuração -c não permitida: " + value.split("=", 1)[0]]
        elif option == "--git-dir":
            git_dir = value
        elif option == "--work-tree":
            work_tree = value
    detail["diretorio_alvo"] = str(where)
    same = root is not None and where.is_dir()
    if same and git_dir is None and where != cwd:
        code, top = git("rev-parse", "--show-toplevel", where=where)
        same = code == 0 and pathlib.Path(top).resolve() == root
    if same and git_dir is not None:
        code, absolute = git("rev-parse", "--absolute-git-dir")
        same = (code == 0 and (where / git_dir).resolve() == pathlib.Path(absolute).resolve()
                and (work_tree is not None or where == root))
    if same and work_tree is not None:
        same = (where / work_tree).resolve() == root
    if not same:
        return detail, ["comando aponta para repositório não verificado"]
    if j >= len(args):
        return detail, ["git sem subcomando"]
    detail["subcomando"] = args[j]
    effective, problems = classify(args[j], args[j + 1:], where)
    if effective is None and not problems:
        problems = ["subcomando Git desconhecido ou alias: " + args[j]]
    detail["operacao_efetiva"] = effective
    return detail, problems


# Perfil miguel-day1 (GG_MODE=miguel-day1): allowlist fechada comparada por argv.
# Não há prefixo, substring nem "comando reconhecido = seguro": o que não
# coincidir exatamente com uma forma abaixo devolve operação None e bloqueia.
mode = e.get("GG_MODE", "").strip()
day1 = mode == "miguel-day1"
if mode not in {"", "miguel-day1"}:
    block.append("modo do Git Guardian desconhecido: " + mode)
DAY1_OUT = "comando fora da allowlist miguel-day1"
DAY1_META = re.compile(r"[;&|<>`$\\(){}#\n\r]")
DAY1_READ = {("status",), ("status", "--short"), ("diff",), ("diff", "--cached"),
             ("rev-parse", "HEAD"), ("rev-parse", "--show-toplevel"),
             ("rev-parse", "--abbrev-ref", "HEAD"), ("branch", "--show-current"),
             ("worktree", "list"), ("ls-files",)}
DAY1_LOG_FLAGS = {"--oneline", "--stat", "--graph", "--decorate"}
DAY1_BRANCH = re.compile(r"piloto/[a-z0-9]+(?:-[a-z0-9]+)*")


def stage_evidence():
    """Prova do stage para a decisão humana: lista exata, numstat, check e hash."""
    # O hash cobre os bytes crus de `git diff --cached --binary`, sem strip.
    try:
        raw = subprocess.run(["git", "diff", "--cached", "--binary"], cwd=cwd,
                             capture_output=True, timeout=12, check=False)
        diff_code, diff_bytes = raw.returncode, raw.stdout
    except (OSError, subprocess.TimeoutExpired):
        diff_code, diff_bytes = 124, b""
    evidence.append({"comando": "git diff --cached --binary", "exit_code": diff_code,
                     "sha256_saida": hashlib.sha256(diff_bytes).hexdigest()})
    _, names = git("diff", "--cached", "--name-status")
    _, numstat = git("diff", "--cached", "--numstat")
    check_code, _ = git("diff", "--cached", "--check")
    return {"arquivos": names.splitlines(), "numstat": numstat.splitlines(),
            "sha256_diff": hashlib.sha256(diff_bytes).hexdigest() if diff_code == 0 else None,
            "check_exit": check_code, "inspecao": "git diff --cached"}


def day1_log(args):
    seen, k = set(), 0
    while k < len(args):
        if (args[k] == "-n" and "-n" not in seen and k + 1 < len(args)
                and re.fullmatch(r"[1-9][0-9]{0,2}", args[k + 1])):
            seen.add("-n")
            k += 2
        elif args[k] in DAY1_LOG_FLAGS and args[k] not in seen:
            seen.add(args[k])
            k += 1
        else:
            return False
    return True


def day1_ref(ref):
    if not re.fullmatch(r"HEAD(?:~[1-9][0-9]?)?|[0-9a-f]{7,40}", ref):
        return False
    return git("rev-parse", "--verify", "--quiet", ref + "^{commit}")[0] == 0


def day1_paths(paths):
    problems = []
    for path in paths:
        full = os.path.realpath(os.path.join(cwd, path)) if path else ""
        relative = os.path.relpath(full, root) if root is not None and full else ".."
        if (not path or path != path.strip() or path.startswith(("-", ":", "@"))
                or any(char in path for char in "*?[]\\")
                or relative == "." or relative.split(os.sep)[0] in {"..", ".git"}):
            problems.append("path proibido no perfil miguel-day1: " + repr(path))
        elif not os.path.lexists(os.path.join(cwd, path)) and git("ls-files", "--error-unmatch", "--", path)[0] != 0:
            problems.append("path inexistente no perfil miguel-day1: " + path)
    return problems


def analyze_day1(text):
    detail = {"operacao_efetiva": None, "executavel": None, "subcomando": None, "diretorio_alvo": str(cwd)}
    if DAY1_META.search(text) or not text.startswith("git ") or text != text.strip():
        return detail, [DAY1_OUT + ": composição, wrapper ou caractere proibido"]
    try:
        argv = shlex.split(text)
    except ValueError:
        return detail, ["comando pretendido inválido"]
    detail["executavel"] = argv[0]
    if argv[0] != "git" or len(argv) < 2:
        return detail, [DAY1_OUT]
    sub, args = argv[1], argv[2:]
    detail["subcomando"] = sub
    if sub == "push":
        return detail, ["push nunca é permitido no perfil miguel-day1; usar procedimento separado de publicação"]
    if tuple(argv[1:]) in DAY1_READ or (sub == "log" and day1_log(args)) or (
            sub == "show" and (len(args) == 1 or args[:1] == ["--stat"] and len(args) == 2)
            and day1_ref(args[-1])):
        detail["operacao_efetiva"] = "read"
        return detail, []
    if sub == "switch" and len(args) == 2 and args[0] == "-c":
        name = args[1]
        if (not DAY1_BRANCH.fullmatch(name) or len(name) > 60 or name in {"main", "master", "deco/v0.2"}
                or git("check-ref-format", "--branch", name)[0] != 0):
            return detail, ["nome de branch fora do padrão piloto/<slug>: " + name]
        if git("rev-parse", "--verify", "--quiet", "refs/heads/" + name)[0] == 0:
            return detail, ["branch já existe: " + name]
        scope["cria_branch"] = True
        detail["operacao_efetiva"] = "branch"
        return detail, []
    if sub == "add" and len(args) >= 2 and args[0] == "--":
        problems = day1_paths(args[1:])
        if problems:
            return detail, problems
        detail["operacao_efetiva"] = "edit"
        return detail, []
    if sub == "commit" and len(args) == 2 and args[0] == "-m":
        problems = [] if args[1].strip() else ["mensagem de commit vazia"]
        if not STAGE["arquivos"]:
            problems.append("stage vazio")
        if STAGE["check_exit"] != 0:
            problems.append("git diff --cached --check falhou")
        inspected = e.get("GG_STAGE_SHA256", "").strip()
        if not inspected:
            problems.append("stage não inspecionado: informar GG_STAGE_SHA256 da inspeção humana")
        elif inspected != STAGE["sha256_diff"]:
            problems.append("stage mudou após a inspeção")
        detail["operacao_efetiva"] = "commit"
        return detail, problems
    return detail, [DAY1_OUT]


STAGE = stage_evidence() if day1 else None
if day1:
    # Texto bruto de GG_COMMAND, antes do strip de need(): bordas e quebras bloqueiam.
    command_detail, command_problems = analyze_day1(e.get("GG_COMMAND", "")) if command else (
        {"operacao_efetiva": None, "executavel": None, "subcomando": None, "diretorio_alvo": None}, [])
    declared = pathlib.Path(target) if target else None
    if declared is None or root is None or (declared if declared.is_absolute() else root / declared).resolve() != root:
        block.append("alvo do perfil miguel-day1 deve ser a raiz do repositório")
else:
    command_detail, command_problems = analyze(command) if command else (
        {"operacao_efetiva": None, "executavel": None, "subcomando": None, "diretorio_alvo": None}, [])
block.extend(command_problems)
effective = command_detail["operacao_efetiva"]
if effective is not None and operation and effective != operation:
    block.append("operação declarada (" + operation + ") não corresponde ao comando efetivo (" + effective + ")")
if scope["altera_remote"] and approval != "yes":
    block.append("aprovação humana obrigatória para alterar remote")
# GG_TARGET delimita escrita local: paths efetivos ficam dentro do alvo
# declarado, nomes de branch/tag coincidem literalmente e escopo amplo exige ".".
if not day1 and (effective in {"edit", "commit", "branch"} or scope["altera_remote"] or scope["integra"]) and target:
    try:
        targets = shlex.split(target)
    except ValueError:
        targets = []
        block.append("alvo declarado inválido")
    if scope["amplo"] and "." not in targets:
        block.append("escopo amplo exige GG_TARGET=.: " + scope["amplo"])
    for name in scope["nomes"]:
        if name not in targets:
            block.append("alvo efetivo fora do alvo declarado: " + name)
    base = pathlib.Path(command_detail["diretorio_alvo"] or cwd)
    for path in scope["caminhos"]:
        resolved = (base / path).resolve()
        inside = root is not None and resolved.is_relative_to(root) and any(
            resolved.is_relative_to((root / item).resolve()) for item in targets)
        if not inside:
            block.append("alvo efetivo fora do alvo declarado: " + path)

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
creating_safe_branch = scope["cria_branch"] and operation == "branch" and effective == "branch"
reading = operation == "read" and effective == "read"
main_auth = e.get("GG_MAIN_AUTH") == "yes" and not day1
if branch in {"main", "master"} and not main_auth and not (creating_safe_branch or reading):
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

# Comparação exata: GG_EXPECTED_REMOTE é "<nome> <URL>" e precisa coincidir
# com as linhas fetch e push de `git remote -v`, nunca por substring.
remote_table = {}
for line in remotes.splitlines():
    name, _, rest = line.partition("\t")
    url, _, kind = rest.rpartition(" ")
    remote_table.setdefault(name, {})[kind.strip("()")] = url
if expected_remote == "AUSENTE":
    remote_ok = not remote_table
    if not remote_ok:
        block.append("remote inesperado")
else:
    expected_url = expected_remote.partition(" ")[2]
    remote_ok = bool(expected_url) and remote_table.get(expected_remote_name) == {
        "fetch": expected_url, "push": expected_url}
    if not remote_ok:
        block.append("remote divergente")
if operation in {"remote", "publish"}:
    remote_name = need("GG_REMOTE_NAME")
    remote_sha = need("GG_EXPECTED_REMOTE_SHA")
    remote_mismatch = remote_problem("push" if operation == "publish" else "fetch", remote_name or None)
    block.extend(remote_mismatch)
    if remote_name and remote_sha and not remote_mismatch:
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

if day1 and effective == "commit" and not block:
    conditional.append("commit exige aprovação de Deco sobre o stage inspecionado (sha256 "
                       + str(STAGE["sha256_diff"]) + "); repetir o GG imediatamente antes de executar")
verdict = "GG-BLOQUEADO" if block else "GG-CONDICIONAL" if conditional else "GG-SEGURO"
dirty_paths = [line[3:].split(" -> ")[-1] for line in status.splitlines() if len(line) > 3]
stage_paths = [line.split("\t")[-1] for line in stage.splitlines() if "\t" in line]
dimensions = {
    "1": {"pasta": str(cwd), "raiz": str(root) if root else "NÃO VERIFICADO"},
    "2": {"branch": branch, "HEAD": head},
    "3": {"working_tree_suja": dirty},
    "4": {"stage_sujo": bool(stage), "paths_stage": stage_paths,
          "modificados_ou_nao_rastreados": dirty, "paths_modificados_ou_nao_rastreados": dirty_paths},
    "5": {"upstream": upstream, "ahead": ahead, "behind": behind},
    "6": {"remote_corresponde": remote_ok, "remotes": sorted(remote_table)},
    "7": {"worktrees": worktree_count, "origem_conhecida": worktrees_known == "yes"},
    "8": {"stashes": len(stashes.splitlines()) if stashes else 0},
    "9": {"tags_no_HEAD": len(tags.splitlines()) if tags else 0},
    "10": {"operacao": operation, "comando": command, "alvo": target, **command_detail,
           "alvos_efetivos": scope["caminhos"] + scope["nomes"], "escopo_amplo": scope["amplo"]},
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
    "perfil": "miguel-day1" if day1 else "geral" if not mode else "desconhecido", "stage_evidencia": STAGE,
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
