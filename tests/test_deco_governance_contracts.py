"""SPEC-0002/T001: contratos transversais de AC-001 a AC-013.

As skills são os mecanismos normativos executáveis da Camada Potestatem.
Esta suíte verifica as obrigações declaradas nessas interfaces. A reconferência
de T004 também exercita o preflight em repositórios Git isolados.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = Path("deco/skills/review-router/SKILL.md")
GIT_GUARDIAN = Path("deco/skills/git-guardian/SKILL.md")


def normative_section(content: str, ac: str) -> str:
    """Isola a decisão de um AC normativo, sem incluir prosa de seções vizinhas."""
    heading = re.search(
        rf"(?m)^#{{2,6}}\s+{re.escape(ac)}(?:\b|[\s:—-]).*$",
        content,
    )
    if heading is None:
        return ""
    remainder = content[heading.end():]
    next_heading = re.search(r"(?m)^#{1,6}\s+", remainder)
    return remainder[:next_heading.start()] if next_heading else remainder


def has_decision_structure(section: str) -> bool:
    """Exige relação entre condição e resultado, não apenas palavras-chave."""
    bdd = (
        re.search(r"(?im)^\s*(?:When|Quando)\s+\S", section)
        and re.search(r"(?im)^\s*(?:Then|Ent[aã]o)\s+\S", section)
    )
    labeled = (
        re.search(r"(?im)^\s*[-*]\s*\*\*Condi[cç][aã]o\*\*\s*:\s*\S", section)
        and re.search(r"(?im)^\s*[-*]\s*\*\*(?:A[cç][aã]o|Resultado)\*\*\s*:\s*\S", section)
    )
    table = re.search(
        r"(?im)^\s*\|\s*Condi[cç][aã]o\s*\|\s*(?:A[cç][aã]o|Resultado)\s*\|",
        section,
    )
    return bool(bdd or labeled or table)


def contract_checks(
    ac: str,
    path: Path,
    clauses: dict[str, str],
    exact_tokens: tuple[str, ...] = (),
    *,
    sample: str | None = None,
) -> list[tuple[str, bool]]:
    artifact = ROOT / path
    exists = artifact.is_file() if sample is None else True
    content = artifact.read_text(encoding="utf-8") if exists and sample is None else sample or ""
    section = normative_section(content, ac)
    checks = [
        ("artefato presente", exists),
        (f"seção normativa {ac}", bool(section)),
        ("estrutura de decisão condição → resultado", has_decision_structure(section)),
    ]
    for obligation, expression in clauses.items():
        checks.append((obligation, bool(re.search(expression, section, re.IGNORECASE | re.DOTALL))))
    for token in exact_tokens:
        checks.append((f"token exato {token}", token in section))
    return checks


class GovernanceContractsTest(unittest.TestCase):
    def assert_contract(
        self,
        ac: str,
        path: Path,
        clauses: dict[str, str],
        exact_tokens: tuple[str, ...] = (),
    ) -> None:
        for obligation, satisfied in contract_checks(ac, path, clauses, exact_tokens):
            with self.subTest(ac=ac, obligation=obligation):
                self.assertTrue(
                    satisfied,
                    f"{ac}: {path} não satisfaz a obrigação: {obligation}",
                )

    def test_ac001_unclassified_work_must_be_refused_and_recorded(self) -> None:
        self.assert_contract("AC-001", ROUTER, {
            "risco antes da execução": r"risco.{0,100}(?:antes|precede).{0,100}execu[cç][aã]o",
            "sem classificação, recusar": r"sem classifica[cç][aã]o.{0,180}(?:recus|bloque)",
            "justificativa registrada": r"(?:justificativa|justificad[oa]).{0,160}registr",
        })

    def test_ac002_low_risk_editorial_work_needs_only_self_check(self) -> None:
        self.assert_contract("AC-002", ROUTER, {
            "correção editorial de risco baixo": r"(?:editorial|formata[cç][aã]o).{0,180}risco baixo|risco baixo.{0,180}(?:editorial|formata[cç][aã]o)",
            "autoverificação suficiente": r"autoverifica[cç][aã]o.{0,150}(?:basta|suficiente)",
            "sem segunda família obrigatória": r"(?:n[aã]o|sem).{0,100}segunda fam[ií]lia",
        })

    def test_ac003_small_sensitive_change_must_raise_risk(self) -> None:
        self.assert_contract("AC-003", ROUTER, {
            "gatilhos sensíveis": r"permiss[aã]o.{0,180}autentica[cç][aã]o.{0,180}segredo.{0,180}dado pessoal.{0,180}migra[cç][aã]o.{0,180}produ[cç][aã]o.{0,180}hist[oó]rico de Git",
            "elevação para alto ou crítico": r"(?:elev|classific).{0,150}(?:alto|cr[ií]tico)",
            "tamanho não rebaixa": r"tamanho.{0,100}n[aã]o.{0,100}rebaix",
        })

    def test_ac004_definition_gate_selects_definition_review_and_timing(self) -> None:
        self.assert_contract("AC-004", ROUTER, {
            "gate de definição": r"gate de defini[cç][aã]o.{0,180}review-definition",
            "momento da revisão": r"(?:pr[eé]via|antes).{0,120}(?:posterior|depois).{0,120}ambas",
        })

    def test_ac005_delivery_auth_composes_profile_without_new_skill(self) -> None:
        self.assert_contract("AC-005", ROUTER, {
            "composição de gate e perfil": r"review-delivery.{0,180}(?:seguran[cç]a|autentica[cç][aã]o).{0,180}privacidade",
            "sem skill combinatória": r"(?:n[aã]o|sem).{0,100}(?:nova skill|skill nova)",
            "perfil não fecha gate": r"perfil.{0,100}n[aã]o.{0,100}(?:fecha|aprova).{0,60}gate",
        })

    def test_ac006_unvalidated_model_cannot_fill_critical_role(self) -> None:
        self.assert_contract("AC-006", ROUTER, {
            "vedação de papel crítico": r"modelo.{0,100}n[aã]o validado.{0,200}(?:recus|vedad|proibid)",
            "papéis críticos": r"seguran[cç]a.{0,250}hist[oó]rico.{0,250}publica[cç][aã]o.{0,250}pagamento.{0,250}autentica[cç][aã]o.{0,250}dado pessoal",
            "tarefas não vinculantes permitidas": r"leitura.{0,200}explora[cç][aã]o.{0,200}classifica[cç][aã]o.{0,200}(?:documenta[cç][aã]o|busca).{0,200}terceira opini[aã]o",
            "promoção com benchmark e decisão": r"benchmark.{0,150}decis[aã]o expl[ií]cita",
        })

    def test_ac007_logical_role_records_actual_runtime_and_unknowns(self) -> None:
        self.assert_contract("AC-007", ROUTER, {
            "mapeamento de execução": r"papel l[oó]gico.{0,200}harness.{0,120}modelo.{0,120}effort.{0,120}data",
            "versão não invalida fluxo": r"vers[aã]o.{0,180}n[aã]o.{0,100}invalida",
        }, exact_tokens=("NÃO REGISTRADO",))

    def test_ac008_distinct_approver_can_close_with_named_roles(self) -> None:
        self.assert_contract("AC-008", ROUTER, {
            "identidades registradas": r"(?:executor|implementador).{0,140}aprovador.{0,140}(?:nome|identific)",
            "aprovação por instância distinta": r"(?:distint[oa]|diferente).{0,160}(?:aprovad|fechamento|gate)",
        })

    def test_ac008_self_approval_keeps_gate_pending(self) -> None:
        self.assert_contract("AC-008", ROUTER, {
            "coincidência recusada": r"(?:mesm[oa]|coincid[eê]ncia).{0,180}(?:recus|bloque|vedad)",
            "gate continua pendente": r"(?:gate|fechamento).{0,150}pendente.{0,150}(?:distint[oa]|independente)",
            "sinalização não substitui revisão": r"sinaliz.{0,150}n[aã]o.{0,100}substitui.{0,100}revis[aã]o",
        })

    def test_ac009_reviewer_starts_read_only_and_checks_claims(self) -> None:
        self.assert_contract("AC-009", ROUTER, {
            "contexto novo somente leitura": r"(?:contexto novo|nova sess[aã]o).{0,150}(?:somente leitura|read.only)",
            "conclusão é alegação": r"conclus[aã]o.{0,160}(?:alega[cç][aã]o|hip[oó]tese).{0,150}(?:verific|test)",
            "achados com correção": r"severidade.{0,150}evid[eê]ncia.{0,150}corre[cç][aã]o",
        })

    def test_ac010_favorable_verdict_without_evidence_cannot_close(self) -> None:
        self.assert_contract("AC-010", ROUTER, {
            "teste, diff e evidência": r"teste.{0,100}diff.{0,100}evid[eê]ncia",
            "fechamento recusado": r"(?:sem|aus[eê]ncia).{0,150}evid[eê]ncia.{0,180}(?:n[aã]o fecha|recus|bloque)",
        })

    def test_ac011_preflight_precedes_sensitive_operations(self) -> None:
        self.assert_contract("AC-011", GIT_GUARDIAN, {
            "preflight antes de escrever": r"preflight.{0,130}(?:antes|precede).{0,150}escrita",
            "outras operações sensíveis": r"branch.{0,130}commit.{0,130}remote.{0,130}(?:publica[cç][aã]o|push)",
            "aprovação humana para operação sensível": r"(?:destrutiv|publica[cç][aã]o|deploy).{0,180}(?:aprova[cç][aã]o|decis[aã]o).{0,100}human",
        })

    def test_ac012_formal_verdict_is_prefixed_and_scope_is_explicit(self) -> None:
        self.assert_contract("AC-012", GIT_GUARDIAN, {
            "três vereditos formais": r"GG-SEGURO.{0,100}GG-CONDICIONAL.{0,100}GG-BLOQUEADO",
            "estado e operações": r"estado observado.{0,150}opera[cç][oõ]es permitidas.{0,150}opera[cç][oõ]es bloqueadas",
            "prefixo distinto do Session Guardian": r"prefixo.{0,150}Session Guardian",
        }, exact_tokens=("GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO"))

    def test_ac012_manual_inspection_is_provisional_only(self) -> None:
        self.assert_contract("AC-012", GIT_GUARDIAN, {
            "três estados manuais": r"PROVISORIAMENTE SEGURO.{0,100}PROVISORIAMENTE CONDICIONAL.{0,100}PROVISORIAMENTE BLOQUEADO",
            "sem veredito formal por narrativa": r"(?:sem|n[aã]o).{0,120}veredito GG.{0,140}(?:narrativa|mecanismo)",
            "sem autoliberação": r"(?:n[aã]o|sem).{0,130}autodeclar.{0,100}liberad",
        })

    def test_ac012_manual_conditional_requires_protection_and_recheck(self) -> None:
        self.assert_contract("AC-012", GIT_GUARDIAN, {
            "proteção reversível": r"PROVISORIAMENTE CONDICIONAL.{0,220}prote[cç][aã]o.{0,120}revers[ií]vel",
            "repetição manual": r"inspe[cç][aã]o manual.{0,120}repetid",
            "avanço somente seguro": r"somente ap[oó]s PROVISORIAMENTE SEGURO",
        })

    def test_ac012_formal_conditional_requires_protection_and_recheck(self) -> None:
        self.assert_contract("AC-012", GIT_GUARDIAN, {
            "proteção no condicional": r"GG-CONDICIONAL.{0,220}prote[cç][aã]o",
            "novo preflight": r"preflight execut[aá]vel.{0,100}repetid",
            "avanço somente GG seguro": r"somente ap[oó]s GG-SEGURO",
        }, exact_tokens=("GG-CONDICIONAL", "GG-SEGURO"))

    def test_ac013_unknown_dirty_worktree_blocks_manual_inspection(self) -> None:
        self.assert_contract("AC-013", GIT_GUARDIAN, {
            "origem desconhecida bloqueia manualmente": r"worktree.{0,140}origem desconhecida.{0,180}PROVISORIAMENTE BLOQUEADO",
            "sem descarte ou redefinição": r"(?:nenhuma|sem).{0,140}(?:descarte|reset|redefini[cç][aã]o).{0,180}(?:branch|limp)",
            "preservar antes de alterar": r"preserv.{0,130}antes de.{0,80}altera[cç][aã]o",
        })

    def test_ac013_unknown_dirty_worktree_blocks_formal_guardian(self) -> None:
        self.assert_contract("AC-013", GIT_GUARDIAN, {
            "origem desconhecida bloqueia formalmente": r"worktree.{0,140}origem desconhecida.{0,180}GG-BLOQUEADO",
            "aguardar explicação e reconciliação": r"(?:nenhuma altera[cç][aã]o|n[aã]o alterar).{0,160}explicad.{0,120}reconciliad",
        }, exact_tokens=("GG-BLOQUEADO",))

    def test_ac012_ac013_formal_preflight_executes_fail_closed(self) -> None:
        """O bloco versionado deve decidir com Git real, não apenas conter tokens."""
        content = (ROOT / GIT_GUARDIAN).read_text(encoding="utf-8")
        program = re.search(
            r"<!-- GG_EXECUTABLE_BEGIN -->\s*```python\n(.*?)\n```\s*<!-- GG_EXECUTABLE_END -->",
            content,
            re.DOTALL,
        )
        self.assertIsNotNone(program, "T004 precisa de saída executável versionada")
        assert program is not None

        with tempfile.TemporaryDirectory(prefix="specsfy-gg-") as temp:
            repo = Path(temp)
            subprocess.run(["git", "init", "-q", "-b", "deco/test", str(repo)], check=True)
            (repo / "AGENTS.md").write_text("# Perfil de teste\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "AGENTS.md"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "-c", "user.name=Teste", "-c",
                 "user.email=test@example.invalid", "commit", "-qm", "base"],
                check=True,
            )
            head = subprocess.check_output(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True,
            ).strip()
            base_env = {
                **os.environ,
                "GG_EXPECTED_ROOT": str(repo), "GG_EXPECTED_BRANCH": "deco/test",
                "GG_EXPECTED_HEAD": head, "GG_EXPECTED_UPSTREAM": "AUSENTE",
                "GG_EXPECTED_REMOTE": "AUSENTE", "GG_OPERATION": "edit",
                "GG_COMMAND": "edit AGENTS.md", "GG_TARGET": "AGENTS.md",
                "GG_DIRTY_ORIGIN": "clean", "GG_PROTECTION": "none",
                "GG_WORKTREES_KNOWN": "yes", "GG_CONTRADICTION": "no",
                "GG_HUMAN_APPROVAL": "no", "GG_PROFILE": str(repo / "AGENTS.md"),
            }

            def verdict(**changes: str) -> dict[str, object]:
                run = subprocess.run(
                    [sys.executable, "-c", program.group(1)], cwd=repo,
                    env={**base_env, **changes}, text=True, capture_output=True,
                    timeout=20, check=False,
                )
                self.assertEqual(0, run.returncode, run.stderr)
                result = json.loads(run.stdout)
                self.assertIn(result["veredito"], ("GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO"))
                self.assertEqual(16, len(result["dimensoes"]))
                return result

            self.assertEqual("GG-SEGURO", verdict()["veredito"])
            self.assertEqual("GG-BLOQUEADO", verdict(GG_EXPECTED_HEAD="0" * 40)["veredito"])
            self.assertEqual("GG-BLOQUEADO", verdict(GG_OPERATION="publish")["veredito"])
            self.assertEqual("GG-BLOQUEADO", verdict(GG_COMMAND="git push --force")["veredito"])
            self.assertEqual("GG-BLOQUEADO", verdict(GG_COMMAND="git push --force=refs/heads/main")["veredito"])
            self.assertEqual("GG-BLOQUEADO", verdict(GG_COMMAND="git push origin +deco/test")["veredito"])
            self.assertEqual("GG-BLOQUEADO", verdict(GG_COMMAND="git push origin deco/test")["veredito"])
            (repo / "nao-rastreado.txt").write_text("mudança\n", encoding="utf-8")
            self.assertEqual("GG-BLOQUEADO", verdict(GG_DIRTY_ORIGIN="unknown")["veredito"])
            self.assertEqual(
                "GG-CONDICIONAL",
                verdict(GG_DIRTY_ORIGIN="known", GG_PROTECTION="required")["veredito"],
            )
            self.assertEqual(
                "GG-BLOQUEADO",
                verdict(GG_DIRTY_ORIGIN="unknown", GG_PROTECTION="required")["veredito"],
            )
            subprocess.run(["git", "-C", str(repo), "add", "nao-rastreado.txt"], check=True)
            staged = verdict(GG_DIRTY_ORIGIN="unknown")
            self.assertEqual("GG-BLOQUEADO", staged["veredito"])
            self.assertTrue(staged["dimensoes"]["4"]["stage_sujo"])
            subprocess.run(
                ["git", "-C", str(repo), "remote", "add", "origin", str(repo)], check=True,
            )
            self.assertEqual(
                "GG-BLOQUEADO", verdict(GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")["veredito"],
            )
            subprocess.run(
                ["git", "-C", str(repo), "checkout", "--detach", "-q", "HEAD"], check=True,
            )
            self.assertEqual("GG-BLOQUEADO", verdict()["veredito"])

    def test_negative_router_shallow_prose_does_not_satisfy_ac001(self) -> None:
        shallow = (
            "## AC-001\nRisco antes da execução. Sem classificação, recusar. "
            "Justificativa registrada.\n"
        )
        checks = dict(contract_checks("AC-001", ROUTER, {
            "risco antes da execução": r"risco.{0,100}antes.{0,100}execu[cç][aã]o",
        }, sample=shallow))
        self.assertTrue(checks["risco antes da execução"])
        self.assertFalse(checks["estrutura de decisão condição → resultado"])

    def test_negative_router_lowercase_unknown_token_is_rejected(self) -> None:
        sample = "## AC-007\n- **Condição**: dado desconhecido\n- **Ação**: usar não registrado\n"
        checks = dict(contract_checks(
            "AC-007", ROUTER, {}, exact_tokens=("NÃO REGISTRADO",), sample=sample,
        ))
        self.assertTrue(checks["estrutura de decisão condição → resultado"])
        self.assertFalse(checks["token exato NÃO REGISTRADO"])

    def test_negative_guardian_token_list_without_decision_is_rejected(self) -> None:
        shallow = "## AC-012\nGG-SEGURO, GG-CONDICIONAL e GG-BLOQUEADO.\n"
        checks = dict(contract_checks(
            "AC-012", GIT_GUARDIAN, {},
            exact_tokens=("GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO"),
            sample=shallow,
        ))
        self.assertTrue(all(checks[f"token exato {token}"] for token in (
            "GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO",
        )))
        self.assertFalse(checks["estrutura de decisão condição → resultado"])

    def test_negative_guardian_lowercase_verdicts_are_rejected(self) -> None:
        sample = (
            "## AC-012\n- **Condição**: preflight realizado\n"
            "- **Resultado**: gg-seguro, gg-condicional ou gg-bloqueado\n"
        )
        checks = dict(contract_checks(
            "AC-012", GIT_GUARDIAN, {},
            exact_tokens=("GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO"),
            sample=sample,
        ))
        self.assertTrue(checks["estrutura de decisão condição → resultado"])
        for token in ("GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO"):
            with self.subTest(token=token):
                self.assertFalse(checks[f"token exato {token}"])


def git_guardian_program() -> str:
    content = (ROOT / GIT_GUARDIAN).read_text(encoding="utf-8")
    program = re.search(
        r"<!-- GG_EXECUTABLE_BEGIN -->\s*```python\n(.*?)\n```\s*<!-- GG_EXECUTABLE_END -->",
        content,
        re.DOTALL,
    )
    if program is None:
        raise AssertionError("T004 precisa de saída executável versionada")
    return program.group(1)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=Teste", "-c",
         "user.email=test@example.invalid", *args],
        check=True, text=True, capture_output=True,
    ).stdout.strip()


class GitGuardianCommandTest(unittest.TestCase):
    """T004/P1: o GG deriva a operação do comando efetivo, sem confiar no rótulo.

    Cada caso isola uma causa: o ambiente-base é GG-SEGURO e a asserção confere
    os motivos emitidos, não apenas o veredito.
    """

    def setUp(self) -> None:
        self.program = git_guardian_program()
        self.temp = tempfile.TemporaryDirectory(prefix="specsfy-gg-cmd-")
        base = Path(self.temp.name).resolve()
        self.outside = base / "fora"
        self.outside.mkdir()
        self.bare = base / "remoto.git"
        subprocess.run(["git", "init", "-q", "--bare", str(self.bare)], check=True)
        self.repo = base / "repo"
        subprocess.run(["git", "init", "-q", "-b", "deco/test", str(self.repo)], check=True)
        (self.repo / "AGENTS.md").write_text("# Perfil de teste\n", encoding="utf-8")
        git(self.repo, "add", "AGENTS.md")
        git(self.repo, "commit", "-qm", "base")
        git(self.repo, "remote", "add", "origin", str(self.bare))
        git(self.repo, "push", "-q", "-u", "origin", "deco/test")
        self.remote_sha = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "commit", "-q", "--allow-empty", "-m", "local")
        self.head = git(self.repo, "rev-parse", "HEAD")
        self.env = {
            **os.environ,
            "GG_EXPECTED_ROOT": str(self.repo), "GG_EXPECTED_BRANCH": "deco/test",
            "GG_EXPECTED_HEAD": self.head, "GG_EXPECTED_UPSTREAM": "origin/deco/test",
            "GG_EXPECTED_AHEAD": "1", "GG_EXPECTED_BEHIND": "0",
            "GG_EXPECTED_REMOTE": f"origin {self.bare}", "GG_OPERATION": "read",
            "GG_COMMAND": "git status", "GG_TARGET": "repo",
            "GG_DIRTY_ORIGIN": "clean", "GG_PROTECTION": "none",
            "GG_WORKTREES_KNOWN": "yes", "GG_CONTRADICTION": "no",
            "GG_HUMAN_APPROVAL": "no", "GG_PROFILE": str(self.repo / "AGENTS.md"),
        }
        for name in ("GG_MAIN_AUTH", "GG_FORCE_PUSH", "GG_REMOTE_NAME", "GG_EXPECTED_REMOTE_SHA"):
            self.env.pop(name, None)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_gg(self, **changes: str) -> dict[str, object]:
        run = subprocess.run(
            [sys.executable, "-B", "-c", self.program], cwd=self.repo,
            env={**self.env, **changes}, text=True, capture_output=True,
            timeout=30, check=False,
        )
        self.assertEqual(0, run.returncode, run.stderr)
        result = json.loads(run.stdout)
        self.assertIn(result["veredito"], ("GG-SEGURO", "GG-CONDICIONAL", "GG-BLOQUEADO"))
        self.assertEqual(16, len(result["dimensoes"]))
        return result

    def publish(self, command: str, **changes: str) -> dict[str, object]:
        return self.run_gg(**{
            "GG_OPERATION": "publish", "GG_COMMAND": command,
            "GG_HUMAN_APPROVAL": "yes", "GG_REMOTE_NAME": "origin",
            "GG_EXPECTED_REMOTE_SHA": self.remote_sha, **changes,
        })

    def assert_only(self, result: dict[str, object], verdict: str, fragment: str) -> None:
        motivos = result["motivos"]
        self.assertEqual(verdict, result["veredito"], motivos)
        self.assertEqual(1, len(motivos), motivos)
        self.assertIn(fragment, motivos[0])

    def test_base_environment_is_safe(self) -> None:
        result = self.run_gg()
        self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        self.assertEqual([], result["motivos"])
        self.assertEqual("read", result["dimensoes"]["10"]["operacao_efetiva"])

    def test_sensitive_command_never_escapes_by_declared_label(self) -> None:
        cases = (
            ("git -C . push", "edit"), ("git -C . push", "read"),
            ("git -C . -c color.ui=never push origin deco/test", "commit"),
            ("git reset --hard", "edit"), ("git reset --hard HEAD~1", "read"),
            ("git --git-dir=.git --work-tree=. reset --hard", "edit"),
            ("git reset HEAD~1", "edit"), ("git branch -D deco/test", "branch"),
            ("git branch -f deco/test HEAD~1", "branch"), ("git checkout -- .", "edit"),
            ("git checkout .", "edit"), ("git checkout -f deco/test", "branch"),
            ("git switch --discard-changes deco/test", "branch"),
            ("git restore AGENTS.md", "edit"), ("git stash drop", "edit"),
            ("git stash clear", "edit"), ("git clean -fdx", "edit"),
            ("git commit --amend -m x", "commit"), ("git rebase HEAD~1", "commit"),
            ("git push --delete origin deco/test", "remote"),
            ("git tag -d v1", "branch"), ("git worktree remove x", "branch"),
            ("git update-ref -d refs/heads/deco/test", "branch"),
            ("git reflog expire --all", "read"), ("git gc --prune=now", "edit"),
            ("env LANG=C git push", "read"), ("nohup git push", "read"),
            ("/usr/bin/git push", "read"), ("\\git push", "read"),
            ("command git push", "read"), ("time git push", "read"),
            ("git push # leitura", "read"), ("git fetch origin deco/test:deco/test", "remote"),
            ("git reset --har", "edit"), ("git commit --amen -m x", "commit"),
            ("git branch --delet --forc deco/test", "branch"), ("git rm --forc AGENTS.md", "edit"),
            ("git restore --stag --work AGENTS.md", "edit"), ("git merge --abo", "commit"),
            ("git pull --reb", "remote"), ("git clean --forc", "edit"),
            ("git branch -d spare", "branch"), ("git branch --delete spare", "branch"),
            ("git stash pop", "edit"), ("git remote prune origin", "remote"),
        )
        for command, declared in cases:
            with self.subTest(command=command, declared=declared):
                result = self.run_gg(GG_OPERATION=declared, GG_COMMAND=command)
                self.assertEqual("GG-BLOQUEADO", result["veredito"], result["motivos"])
                self.assertTrue(
                    any("não corresponde ao comando efetivo" in m for m in result["motivos"]),
                    result["motivos"],
                )
                self.assertNotEqual(declared, result["dimensoes"]["10"]["operacao_efetiva"])

    def test_unknown_or_ambiguous_parsing_blocks(self) -> None:
        cases = (
            ("git st", "subcomando Git desconhecido"),
            ("git -c alias.st=push st", "configuração -c não permitida"),
            ("git -c core.fsmonitor=x status", "configuração -c não permitida"),
            ("git status; git push", "comando composto"),
            ("git status && git push", "comando composto"),
            ("git status | cat", "comando composto"),
            ("git log > saida.txt", "comando composto"),
            ("git push $REMOTO", "comando composto"),
            ("git $(echo push)", "comando composto"),
            ("sh -c 'git push'", "executável não reconhecido"),
            ("sudo git status", "executável não reconhecido"),
            ("python3 -c pass", "executável não reconhecido"),
            ("env -i git status", "wrapper com opção não suportada"),
            ("GIT_DIR=/tmp/x git status", "variável de ambiente não permitida"),
            ("git --exec-path=/tmp status", "opção global do Git desconhecida"),
            ("git --bare status", "opção global do Git desconhecida"),
            ("git -C", "opção global do Git sem valor"),
            ("git", "git sem subcomando"),
            ("git 'status", "comando pretendido inválido"),
            ("git config core.hooksPath /tmp", "escrita de configuração Git"),
            ("git push --no-verify", "opção não suportada em git push"),
            ("git diff --ext-diff", "opção não suportada em git diff"),
            ("git log --output=x.txt", "opção não suportada em git log"),
            ("git log --out=x.txt", "opção não suportada em git log"),
            ("git commit --no-verif -m x", "opção não suportada em git commit"),
            ("git push --no-verify origin deco/test", "opção não suportada em git push"),
        )
        for command, fragment in cases:
            with self.subTest(command=command):
                result = self.run_gg(GG_COMMAND=command)
                self.assert_only(result, "GG-BLOQUEADO", fragment)
                self.assertIsNone(result["dimensoes"]["10"]["operacao_efetiva"])

    def test_command_targeting_unverified_repository_blocks(self) -> None:
        subprocess.run(["git", "init", "-q", str(self.outside / "outro")], check=True)
        cases = (
            f"git -C {self.outside} status", f"git -C {self.outside / 'outro'} status",
            f"git --git-dir={self.outside / 'outro' / '.git'} status",
            f"git --work-tree={self.outside} status", "git -C inexistente status",
        )
        for command in cases:
            with self.subTest(command=command):
                self.assert_only(
                    self.run_gg(GG_COMMAND=command), "GG-BLOQUEADO",
                    "comando aponta para repositório não verificado",
                )

    def test_real_reads_remain_recognized(self) -> None:
        reads = (
            "git status", "git -C . status --short", "git -c color.ui=never log --oneline -3",
            "git --no-pager diff --stat", "git --git-dir=.git --work-tree=. status",
            "env LANG=C git show HEAD", "/usr/bin/git log -1", "git branch", "git branch --list",
            "git branch -vv", "git tag", "git tag --list", "git remote -v", "git stash list",
            "git worktree list --porcelain", "git config --get user.name", "git rev-parse HEAD",
            "git clean -n", "git reflog", "git ls-remote origin", "git -C . -C . log -1",
        )
        for command in reads:
            with self.subTest(command=command):
                result = self.run_gg(GG_COMMAND=command)
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
                self.assertEqual("read", result["dimensoes"]["10"]["operacao_efetiva"])

    def test_matching_label_is_safe_and_command_is_never_executed(self) -> None:
        cases = (
            ("git branch gg-canary", "branch", "gg-canary"),
            ("git switch -c gg-canary", "branch", "gg-canary"),
            ("git tag gg-canary", "branch", "gg-canary"),
            ("git commit --allow-empty -m canary", "commit", "repo"),
            ("git add AGENTS.md", "edit", "AGENTS.md"), ("edit AGENTS.md", "edit", "AGENTS.md"),
            ("git fetch origin", "remote", "origin"),
        )
        for command, declared, target in cases:
            with self.subTest(command=command):
                result = self.run_gg(
                    GG_OPERATION=declared, GG_COMMAND=command, GG_TARGET=target,
                    GG_REMOTE_NAME="origin", GG_EXPECTED_REMOTE_SHA=self.remote_sha,
                )
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
                self.assertEqual(declared, result["dimensoes"]["10"]["operacao_efetiva"])
        self.assertEqual(self.head, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual("", git(self.repo, "branch", "--list", "gg-canary"))
        self.assertEqual("", git(self.repo, "tag", "--list", "gg-canary"))
        blocked = self.run_gg(GG_OPERATION="edit", GG_COMMAND="edit AGENTS.md; touch canary")
        self.assertEqual("GG-BLOQUEADO", blocked["veredito"])
        self.assertFalse((self.repo / "canary").exists())

    def test_publish_matches_verified_target_without_pushing(self) -> None:
        for command in ("git push", "git push origin deco/test", "git -C . push origin HEAD:deco/test",
                        "git -c color.ui=never push -u origin deco/test"):
            with self.subTest(command=command):
                result = self.publish(command)
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
                self.assertEqual("publish", result["dimensoes"]["10"]["operacao_efetiva"])
        remote_ref = subprocess.run(
            ["git", "--git-dir", str(self.bare), "rev-parse", "refs/heads/deco/test"],
            check=True, text=True, capture_output=True,
        ).stdout.strip()
        self.assertEqual(self.remote_sha, remote_ref, "o GG não pode executar o push analisado")

    def test_force_push_is_never_authorized(self) -> None:
        for command in (
            "git push --force", "git push -f origin deco/test", "git push --force-with-lease",
            "git push --force-with-lease=deco/test:abc", "git push --force-if-includes",
            "git push origin +deco/test", "git -c color.ui=never push origin +deco/test",
            "git -C . push -uf origin deco/test", "git push origin +HEAD:deco/test",
            "git push --forc", "git push --force-w", "git push origin deco/test --force",
        ):
            with self.subTest(command=command):
                self.assert_only(self.publish(command), "GG-BLOQUEADO", "comando com force bloqueado")
        self.assert_only(
            self.publish("git push", GG_FORCE_PUSH="yes"), "GG-BLOQUEADO",
            "force push nunca autorizado implicitamente",
        )

    def test_push_outside_verified_target_blocks(self) -> None:
        cases = (
            ("git push origin deco/test:main", "refspec de push fora do alvo verificado"),
            ("git push origin main", "refspec de push fora do alvo verificado"),
            ("git push --all", "escopo de push além do alvo verificado"),
            ("git push --mirror", "escopo de push além do alvo verificado"),
            ("git push --tags", "escopo de push além do alvo verificado"),
            ("git push outro deco/test", "remote do push diverge do remote verificado"),
            ("git push origin :deco/test", "não corresponde ao comando efetivo"),
            ("git push --receive-pack=x", "opção não suportada em git push"),
        )
        for command, fragment in cases:
            with self.subTest(command=command):
                self.assert_only(self.publish(command), "GG-BLOQUEADO", fragment)

    def test_remote_mutation_requires_human_approval(self) -> None:
        remote = dict(GG_OPERATION="remote", GG_REMOTE_NAME="origin",
                      GG_EXPECTED_REMOTE_SHA=self.remote_sha, GG_TARGET="origin")
        for command in ("git remote set-url origin /tmp/outro.git", "git remote add backup /tmp/b.git",
                        "git remote rename origin antigo", "git remote set-head origin deco/test"):
            with self.subTest(command=command):
                self.assert_only(self.run_gg(GG_COMMAND=command, **remote), "GG-BLOQUEADO",
                                 "aprovação humana obrigatória para alterar remote")
                approved = self.run_gg(GG_COMMAND=command, GG_HUMAN_APPROVAL="yes", **remote)
                self.assertEqual("GG-SEGURO", approved["veredito"], approved["motivos"])
        fetch = self.run_gg(GG_COMMAND="git fetch origin", **remote)
        self.assertEqual("GG-SEGURO", fetch["veredito"], fetch["motivos"])

    def test_effective_target_is_bound_to_declared_target(self) -> None:
        blocked = (
            ("git add -A", "edit", "README.md", "escopo amplo exige GG_TARGET=."),
            ("git add .", "edit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git add -u", "edit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git commit -a -m x", "commit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git commit -am x", "commit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git add outro.txt", "edit", "AGENTS.md", "alvo efetivo fora do alvo declarado: outro.txt"),
            ("git add ../fora.txt", "edit", ".", "alvo efetivo fora do alvo declarado: ../fora.txt"),
            ("edit README.md", "edit", "AGENTS.md", "alvo efetivo fora do alvo declarado: README.md"),
            ("git commit -m x -- outro.txt", "commit", "AGENTS.md",
             "alvo efetivo fora do alvo declarado: outro.txt"),
            ("git branch gg-canary", "branch", "outra", "alvo efetivo fora do alvo declarado: gg-canary"),
            ("git switch -c gg-canary", "branch", ".", "alvo efetivo fora do alvo declarado: gg-canary"),
        )
        for command, declared, target, fragment in blocked:
            with self.subTest(command=command, target=target):
                self.assert_only(self.run_gg(GG_OPERATION=declared, GG_COMMAND=command, GG_TARGET=target),
                                 "GG-BLOQUEADO", fragment)
        allowed = (
            ("git add -A", "edit", "."), ("git add AGENTS.md", "edit", "AGENTS.md"),
            ("git add docs/a.md", "edit", "docs"), ("git add a.md b.md", "edit", "a.md b.md"),
            ("git commit -m x", "commit", "AGENTS.md"), ("git commit -am x", "commit", "."),
            ("edit 'docs/com espaço.md'", "edit", "docs"),
        )
        for command, declared, target in allowed:
            with self.subTest(command=command, target=target):
                result = self.run_gg(GG_OPERATION=declared, GG_COMMAND=command, GG_TARGET=target)
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])

    def test_main_allows_only_safe_branch_creation_without_authorization(self) -> None:
        git(self.repo, "checkout", "-q", "-b", "main")
        main = dict(GG_EXPECTED_BRANCH="main", GG_EXPECTED_UPSTREAM="AUSENTE")
        for command in ("git switch -c piloto/demo", "git checkout -b piloto/demo"):
            with self.subTest(command=command):
                result = self.run_gg(**main, GG_OPERATION="branch", GG_COMMAND=command,
                                     GG_TARGET="piloto/demo")
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        for command, declared in (("git commit -m x", "commit"), ("edit AGENTS.md", "edit"),
                                  ("git branch piloto/demo", "branch")):
            with self.subTest(command=command):
                target = "piloto/demo" if declared == "branch" else "AGENTS.md"
                self.assert_only(self.run_gg(**main, GG_OPERATION=declared, GG_COMMAND=command,
                                             GG_TARGET=target),
                                 "GG-BLOQUEADO", "branch principal sem autorização")

    def test_explanation_never_replaces_formal_inputs(self) -> None:
        result = self.publish("git push", GG_HUMAN_APPROVAL="sim, aprovado pelo responsável")
        self.assertEqual("GG-BLOQUEADO", result["veredito"])
        self.assertIn("entrada inválida: GG_HUMAN_APPROVAL", result["motivos"])
        result = self.run_gg(GG_OPERATION="read (é só leitura)")
        self.assertEqual("GG-BLOQUEADO", result["veredito"])
        self.assertIn("entrada inválida: GG_OPERATION", result["motivos"])
        self.assert_only(self.publish("git push", GG_HUMAN_APPROVAL="no"), "GG-BLOQUEADO",
                         "aprovação humana obrigatória")

    def test_each_blocking_cause_is_isolated(self) -> None:
        self.assert_only(self.run_gg(GG_EXPECTED_HEAD="0" * 40), "GG-BLOQUEADO", "HEAD divergente")
        self.assert_only(self.run_gg(GG_EXPECTED_UPSTREAM="origin/outro"), "GG-BLOQUEADO",
                         "upstream divergente")
        self.assert_only(self.run_gg(GG_EXPECTED_AHEAD="0"), "GG-BLOQUEADO", "ahead/behind divergente")
        self.assert_only(self.run_gg(GG_CONTRADICTION="yes"), "GG-BLOQUEADO", "contradição declarada")
        self.assert_only(self.run_gg(GG_EXPECTED_REMOTE=f"origin {str(self.bare)[:-1]}"),
                         "GG-BLOQUEADO", "remote divergente")
        self.assert_only(self.run_gg(GG_EXPECTED_REMOTE="origin"), "GG-BLOQUEADO", "remote divergente")
        self.assert_only(self.publish("git push", GG_EXPECTED_REMOTE_SHA="0" * 40),
                         "GG-BLOQUEADO", "SHA remoto ausente ou divergente")
        self.assert_only(self.publish("git push", GG_REMOTE_NAME="outro"), "GG-BLOQUEADO",
                         "remote do push diverge do remote verificado")
        self.assert_only(self.run_gg(GG_OPERATION="destructive", GG_COMMAND="git reset --hard",
                                     GG_HUMAN_APPROVAL="yes"),
                         "GG-BLOQUEADO", "operação destrutiva requer gate próprio")
        merge_head = Path(git(self.repo, "rev-parse", "--absolute-git-dir")) / "MERGE_HEAD"
        merge_head.write_text(self.head + "\n", encoding="utf-8")
        self.assert_only(self.run_gg(), "GG-BLOQUEADO", "operação Git em andamento")
        merge_head.unlink()
        (self.repo / "novo.txt").write_text("x\n", encoding="utf-8")
        self.assert_only(self.run_gg(GG_DIRTY_ORIGIN="unknown"), "GG-BLOQUEADO",
                         "worktree suja de origem desconhecida")
        self.assert_only(self.run_gg(GG_DIRTY_ORIGIN="known", GG_PROTECTION="none"),
                         "GG-CONDICIONAL", "proteger trabalho conhecido")
        dirty = self.run_gg(GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        self.assertEqual("GG-SEGURO", dirty["veredito"], dirty["motivos"])
        self.assertEqual(["novo.txt"], dirty["dimensoes"]["4"]["paths_modificados_ou_nao_rastreados"])
        (self.repo / "novo.txt").unlink()
        git(self.repo, "checkout", "-q", "--detach", "HEAD")
        self.assert_only(self.run_gg(GG_EXPECTED_UPSTREAM="AUSENTE"), "GG-BLOQUEADO",
                         "branch divergente ou detached HEAD")
        git(self.repo, "checkout", "-q", "-b", "main")
        main = dict(GG_EXPECTED_BRANCH="main", GG_EXPECTED_UPSTREAM="AUSENTE")
        self.assert_only(self.run_gg(**main), "GG-BLOQUEADO", "branch principal sem autorização")
        self.assertEqual("GG-SEGURO", self.run_gg(**main, GG_MAIN_AUTH="yes")["veredito"])


if __name__ == "__main__":
    unittest.main()
