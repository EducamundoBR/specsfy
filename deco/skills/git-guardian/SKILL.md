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
| `push` rotulado como outra operação; `reset --hard`, `branch -D`, `checkout -- .`, `stash drop`, `clean -f`, `commit --amend` ou `rebase` rotulados como edição | Operação efetiva divergente do rótulo; `GG-BLOQUEADO`. |
| Push com force, `+refspec` ou lease; push fora do remote e da branch verificados; `--all`, `--mirror` ou `--tags` | `GG-BLOQUEADO`; force push nunca é autorizado implicitamente. |
| Leitura real (`status`, `log`, `diff`, `show`, listagens de branch/tag/remote/stash/worktree, `config --get`, `clean -n`) | Operação efetiva `read`; segue a classificação das demais dimensões. |

Formas declarativas sem Git (`edit <alvo>`, `write <alvo>`, `read <alvo>` e
`deploy <alvo>`) mapeiam para a operação homônima. A dimensão 10 registra a
operação efetiva, o executável, o subcomando e o diretório-alvo.

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
                  "--ours", "--theirs", "--pathspec-from-file", "--interactive", "--refmap"}


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
        elif arg in valued:
            skip = True
        elif not arg.startswith("-"):
            found.append(arg)
    return found


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
    problems += remote_problem("push", found[0] if found else None)
    if delete:
        return "destructive", problems
    if force:
        problems.insert(0, "comando com force bloqueado")
    return "publish", problems


def classify(sub, rest, where):
    flags = shorts(rest)
    dashdash = "--" in rest
    pos = positionals(rest)
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
    if sub in {"add", "mv", "apply", "format-patch"}:
        return "edit", []
    if sub == "rm":
        return ("destructive" if flags & {"-f", "--force"} else "edit"), []
    if sub == "commit":
        if "--amend" in flags:
            return "destructive", []
        if flags & {"-n", "--no-verify"}:
            return unsupported(sub, "--no-verify")
        return "commit", []
    if sub in {"merge", "cherry-pick", "revert", "am"}:
        return ("destructive" if "--abort" in flags else "commit"), []
    if sub == "reset":
        if flags & {"--hard", "--merge", "--keep"}:
            return "destructive", []
        if flags & {"-p", "--patch"} or dashdash:
            return "edit", []
        extra = flags - {"-q", "--quiet", "--mixed", "--soft", "-N"}
        if extra:
            return unsupported(sub, sorted(extra)[0])
        return ("edit" if pos in ([], ["HEAD"]) else "destructive"), []
    if sub == "restore":
        staged_only = flags & {"-S", "--staged"} and not flags & {"-W", "--worktree"}
        return ("edit" if staged_only else "destructive"), []
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
            return ("branch" if len(pos) <= 2 else "destructive"), []
        if not pos:
            return ("branch" if "--detach" in flags else "read"), []
        if len(pos) == 1 and pos[0] != "." and not (where / pos[0]).exists():
            code, _ = git("rev-parse", "--verify", "--quiet", pos[0] + "^{commit}", where=where)
            if code == 0:
                return "branch", []
        return "destructive", []
    if sub == "switch":
        if flags & {"-C", "--force-create", "-f", "--force", "--discard-changes", "-m", "--merge"}:
            return "destructive", []
        extra = flags - {"-c", "--create", "--orphan", "-d", "--detach", "-q", "--quiet", "-t",
                         "--track", "--no-track", "--guess", "--no-guess", "--progress", "--no-progress"}
        if extra or not 1 <= len(pos) <= 2:
            return unsupported(sub, sorted(extra)[0] if extra else "argumentos")
        return "branch", []
    if sub == "branch":
        if flags & {"-D", "-f", "--force", "-M", "-C"}:
            return "destructive", []
        write = {"-d", "--delete", "-m", "--move", "-c", "--copy", "-u", "--set-upstream-to",
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
            return "branch", []
        return "read", []
    if sub == "stash":
        action = rest[0] if rest and not rest[0].startswith("-") else "push"
        mapped = {"list": "read", "show": "read", "drop": "destructive", "clear": "destructive",
                  "push": "edit", "save": "edit", "apply": "edit", "pop": "edit", "branch": "branch",
                  "create": "edit", "store": "edit"}.get(action)
        return (mapped, []) if mapped else unsupported(sub, action)
    if sub == "worktree":
        action = pos[0] if pos else ""
        mapped = {"list": "read", "add": "branch", "remove": "destructive", "prune": "destructive",
                  "lock": "edit", "unlock": "edit", "move": "edit", "repair": "edit"}.get(action)
        return (mapped, []) if mapped else unsupported(sub, action or "sem ação")
    if sub == "remote":
        if not pos:
            extra = flags - {"-v", "--verbose"}
            return unsupported(sub, sorted(extra)[0]) if extra else ("read", [])
        mapped = {"show": "read", "get-url": "read", "add": "remote", "rename": "remote",
                  "set-url": "remote", "set-head": "remote", "set-branches": "remote",
                  "update": "remote", "prune": "remote", "remove": "destructive",
                  "rm": "destructive"}.get(pos[0])
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
        if (flags & {"-f", "--force", "-r", "--rebase"}
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


command_detail, command_problems = analyze(command) if command else (
    {"operacao_efetiva": None, "executavel": None, "subcomando": None, "diretorio_alvo": None}, [])
block.extend(command_problems)
effective = command_detail["operacao_efetiva"]
if effective is not None and operation and effective != operation:
    block.append("operação declarada (" + operation + ") não corresponde ao comando efetivo (" + effective + ")")

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
    "10": {"operacao": operation, "comando": command, "alvo": target, **command_detail},
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
