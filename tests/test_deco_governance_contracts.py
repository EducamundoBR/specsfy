"""SPEC-0002/T001: contratos transversais de AC-001 a AC-013.

As skills são os mecanismos normativos executáveis da Camada Potestatem.
Esta suíte verifica as obrigações declaradas nessas interfaces. A reconferência
de T004 também exercita o preflight em repositórios Git isolados.
"""

from __future__ import annotations

import hashlib
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


class GitGuardianRepoCase(unittest.TestCase):
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

class GitGuardianCommandTest(GitGuardianRepoCase):
    """Perfil geral: operação efetiva derivada do comando."""

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
            ("git fetch --prune origin", "remote"), ("git fetch -p", "remote"),
            ("git fetch --prune-tags origin", "remote"), ("git remote update --prune", "remote"),
            ("git remote update -p", "remote"), ("git pull --prune", "remote"),
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
            "git remote prune --dry-run origin", "git remote prune -n origin",
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
                      GG_EXPECTED_REMOTE_SHA=self.remote_sha)
        for command, target in (("git remote set-url origin /tmp/outro.git", "origin"),
                                ("git remote add backup /tmp/b.git", "backup"),
                                ("git remote rename origin antigo", "origin antigo"),
                                ("git remote set-head origin deco/test", "origin")):
            with self.subTest(command=command):
                self.assert_only(self.run_gg(GG_COMMAND=command, GG_TARGET=target, **remote), "GG-BLOQUEADO",
                                 "aprovação humana obrigatória para alterar remote")
                approved = self.run_gg(GG_COMMAND=command, GG_TARGET=target, GG_HUMAN_APPROVAL="yes", **remote)
                self.assertEqual("GG-SEGURO", approved["veredito"], approved["motivos"])
        self.assert_only(
            self.run_gg(GG_COMMAND="git remote add backup /tmp/b.git", GG_TARGET="origin",
                        GG_HUMAN_APPROVAL="yes", **remote),
            "GG-BLOQUEADO", "alvo efetivo fora do alvo declarado: backup",
        )
        fetch = self.run_gg(GG_COMMAND="git fetch origin", GG_TARGET="origin", **remote)
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
            ("git add --pathspec-from-file=/tmp/lista", "edit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git add -p", "edit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git add --interactive", "edit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git commit -p -m x", "commit", "AGENTS.md", "escopo amplo exige GG_TARGET=."),
            ("git restore --staged --pathspec-from-file=l", "edit", "AGENTS.md",
             "escopo amplo exige GG_TARGET=."),
        )
        for command, declared, target, fragment in blocked:
            with self.subTest(command=command, target=target):
                self.assert_only(self.run_gg(GG_OPERATION=declared, GG_COMMAND=command, GG_TARGET=target),
                                 "GG-BLOQUEADO", fragment)
        allowed = (
            ("git add -A", "edit", "."), ("git add AGENTS.md", "edit", "AGENTS.md"),
            ("git add docs/a.md", "edit", "docs"), ("git add a.md b.md", "edit", "a.md b.md"),
            ("git commit -m x", "commit", "AGENTS.md"), ("git commit -am x", "commit", "."),
            ("edit 'docs/com espaço.md'", "edit", "docs"), ("git add -p AGENTS.md", "edit", "AGENTS.md"),
        )
        for command, declared, target in allowed:
            with self.subTest(command=command, target=target):
                result = self.run_gg(GG_OPERATION=declared, GG_COMMAND=command, GG_TARGET=target)
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])

    def test_commit_is_bound_to_effective_stage(self) -> None:
        (self.repo / "outro.txt").write_text("x\n", encoding="utf-8")
        git(self.repo, "add", "outro.txt")
        staged = dict(GG_OPERATION="commit", GG_COMMAND="git commit -m x",
                      GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        self.assert_only(self.run_gg(GG_TARGET="AGENTS.md", **staged), "GG-BLOQUEADO",
                         "alvo efetivo fora do alvo declarado: outro.txt")
        result = self.run_gg(GG_TARGET="outro.txt", **staged)
        self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        self.assertIn("outro.txt", result["dimensoes"]["10"]["alvos_efetivos"])

    def test_main_allows_only_safe_branch_creation_without_authorization(self) -> None:
        git(self.repo, "checkout", "-q", "-b", "main")
        main = dict(GG_EXPECTED_BRANCH="main", GG_EXPECTED_UPSTREAM="AUSENTE")
        for command in ("git switch -c piloto/demo", "git checkout -b piloto/demo"):
            with self.subTest(command=command):
                result = self.run_gg(**main, GG_OPERATION="branch", GG_COMMAND=command,
                                     GG_TARGET="piloto/demo")
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        for start in ("HEAD", self.head, "main"):
            with self.subTest(start=start):
                result = self.run_gg(**main, GG_OPERATION="branch", GG_TARGET="piloto/demo",
                                     GG_COMMAND="git switch -c piloto/demo " + start)
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        read = self.run_gg(**main, GG_OPERATION="read", GG_COMMAND="git status")
        self.assertEqual("GG-SEGURO", read["veredito"], read["motivos"])
        for command, declared in (("git commit -m x", "commit"), ("edit AGENTS.md", "edit"),
                                  ("git branch piloto/demo", "branch"),
                                  ("git switch -c piloto/demo HEAD~1", "branch"),
                                  ("git checkout -b piloto/demo " + self.remote_sha, "branch")):
            with self.subTest(command=command):
                target = "piloto/demo" if declared == "branch" else "AGENTS.md"
                self.assert_only(self.run_gg(**main, GG_OPERATION=declared, GG_COMMAND=command,
                                             GG_TARGET=target),
                                 "GG-BLOQUEADO", "branch principal sem autorização")

    def test_push_resolves_configured_destination(self) -> None:
        git(self.repo, "remote", "add", "backup", str(self.bare))
        cases = (
            (("branch.deco/test.pushRemote", "backup"), "remote do push diverge do remote verificado: backup"),
            (("remote.pushDefault", "backup"), "remote do push diverge do remote verificado: backup"),
            (("push.default", "matching"), "push.default não suportado: matching"),
            (("remote.origin.push", "refs/heads/*:refs/heads/*"), "refspec de push configurado no remote: origin"),
        )
        for (key, value), fragment in cases:
            with self.subTest(key=key):
                git(self.repo, "config", key, value)
                try:
                    self.assert_only(self.publish("git push"), "GG-BLOQUEADO", fragment)
                finally:
                    git(self.repo, "config", "--unset", key)
        self.assertEqual("GG-SEGURO", self.publish("git push")["veredito"])

    def test_pull_worktree_and_upstream_changes_are_bound_to_target(self) -> None:
        remote = dict(GG_REMOTE_NAME="origin", GG_EXPECTED_REMOTE_SHA=self.remote_sha)
        self.assert_only(
            self.run_gg(GG_OPERATION="remote", GG_COMMAND="git pull origin deco/test",
                        GG_TARGET="AGENTS.md", **remote),
            "GG-BLOQUEADO", "escopo amplo exige GG_TARGET=.: pull",
        )
        pulled = self.run_gg(GG_OPERATION="remote", GG_COMMAND="git pull origin deco/test",
                             GG_TARGET=".", **remote)
        self.assertEqual("GG-SEGURO", pulled["veredito"], pulled["motivos"])
        self.assert_only(
            self.run_gg(GG_OPERATION="branch", GG_COMMAND=f"git worktree add -b other {self.outside / 'wt'}",
                        GG_TARGET=". other"),
            "GG-BLOQUEADO", "alvo efetivo fora do alvo declarado: " + str(self.outside / "wt"),
        )
        self.assert_only(
            self.run_gg(GG_OPERATION="branch", GG_COMMAND="git worktree add -b other wt", GG_TARGET="wt"),
            "GG-BLOQUEADO", "alvo efetivo fora do alvo declarado: other",
        )
        inside = self.run_gg(GG_OPERATION="branch", GG_COMMAND="git worktree add -b other wt",
                             GG_TARGET="wt other")
        self.assertEqual("GG-SEGURO", inside["veredito"], inside["motivos"])
        self.assertEqual("GG-BLOQUEADO", self.run_gg(
            GG_OPERATION="branch", GG_COMMAND="git worktree add -f wt", GG_TARGET="wt")["veredito"])
        for command in ("git branch --unset-upstream", "git branch -u origin/deco/test",
                        "git branch --edit-description"):
            with self.subTest(command=command):
                self.assert_only(self.run_gg(GG_OPERATION="branch", GG_COMMAND=command, GG_TARGET="AGENTS.md"),
                                 "GG-BLOQUEADO", "alvo efetivo fora do alvo declarado: deco/test")
                result = self.run_gg(GG_OPERATION="branch", GG_COMMAND=command, GG_TARGET="deco/test")
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])

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
        edit = dict(GG_OPERATION="edit", GG_COMMAND="edit AGENTS.md", GG_TARGET="AGENTS.md")
        self.assert_only(self.run_gg(**main, **edit), "GG-BLOQUEADO", "branch principal sem autorização")
        self.assertEqual("GG-SEGURO", self.run_gg(**main, **edit, GG_MAIN_AUTH="yes")["veredito"])


class GitGuardianDay1Test(GitGuardianRepoCase):
    """Perfil miguel-day1: allowlist fechada por argv; o resto bloqueia."""

    def gg(self, command: str, operation: str = "read", **changes: str) -> dict[str, object]:
        return self.run_gg(**{"GG_MODE": "miguel-day1", "GG_OPERATION": operation,
                              "GG_COMMAND": command, "GG_TARGET": ".", **changes})

    def assert_blocked(self, command: str, operation: str = "read", fragment: str = "", **changes: str) -> None:
        result = self.gg(command, operation, **changes)
        self.assertEqual("GG-BLOQUEADO", result["veredito"], (command, result["motivos"]))
        self.assertEqual("miguel-day1", result["perfil"])
        if fragment:
            self.assertTrue(any(fragment in m for m in result["motivos"]), (command, result["motivos"]))

    def stage(self, name: str = "novo.txt", content: str = "conteúdo\n") -> None:
        (self.repo / name).write_text(content, encoding="utf-8")
        git(self.repo, "add", "--", name)

    def staged_sha(self) -> str:
        result = self.gg("git diff --cached", GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        return result["stage_evidencia"]["sha256_diff"]

    def test_positive_read_matrix(self) -> None:
        for command in (
            "git status", "git status --short", "git diff", "git diff --cached", "git log",
            "git log --oneline", "git log --oneline -n 5", "git log --stat --graph --decorate",
            "git show HEAD", "git show HEAD~1", "git show --stat HEAD", f"git show {self.head[:12]}",
            "git rev-parse HEAD", "git rev-parse --show-toplevel", "git rev-parse --abbrev-ref HEAD",
            "git branch --show-current", "git worktree list", "git ls-files",
        ):
            with self.subTest(command=command):
                result = self.gg(command)
                self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
                self.assertEqual("read", result["dimensoes"]["10"]["operacao_efetiva"])

    def test_positive_local_writes(self) -> None:
        result = self.gg("git switch -c piloto/demo-miguel", "branch")
        self.assertEqual("GG-SEGURO", result["veredito"], result["motivos"])
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "a.md").write_text("a\n", encoding="utf-8")
        (self.repo / "AGENTS.md").write_text("# Perfil alterado\n", encoding="utf-8")
        dirty = dict(GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        for command in ("git add -- AGENTS.md", "git add -- docs/a.md", "git add -- AGENTS.md docs"):
            with self.subTest(command=command):
                added = self.gg(command, "edit", **dirty)
                self.assertEqual("GG-SEGURO", added["veredito"], added["motivos"])
                self.assertEqual("edit", added["dimensoes"]["10"]["operacao_efetiva"])
        self.assertEqual("", git(self.repo, "diff", "--cached", "--name-only"))
        self.assertEqual("", git(self.repo, "branch", "--list", "piloto/demo-miguel"))

    def test_commit_is_only_conditional_with_stage_proof(self) -> None:
        dirty = dict(GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        self.assert_blocked("git commit -m 'registro'", "commit", "stage vazio", **dirty)
        self.stage()
        sha = self.staged_sha()
        result = self.gg("git commit -m 'registro do ensaio'", "commit", GG_STAGE_SHA256=sha, **dirty)
        self.assertEqual("GG-CONDICIONAL", result["veredito"], result["motivos"])
        self.assertTrue(any("aprovação de Deco" in m for m in result["motivos"]), result["motivos"])
        evidence = result["stage_evidencia"]
        self.assertEqual(["A\tnovo.txt"], evidence["arquivos"])
        self.assertEqual(sha, evidence["sha256_diff"])
        self.assertEqual(0, evidence["check_exit"])
        self.assertEqual(["1\t0\tnovo.txt"], evidence["numstat"])
        self.assertEqual(self.head, git(self.repo, "rev-parse", "HEAD"), "o commit não pode ser executado")
        self.assert_blocked("git commit -m 'registro'", "commit", "stage não inspecionado", **dirty)
        self.assert_blocked("git commit -m 'registro'", "commit", "stage mudou após a inspeção",
                            GG_STAGE_SHA256="0" * 64, **dirty)
        self.stage("depois.txt")
        self.assert_blocked("git commit -m 'registro'", "commit", "stage mudou após a inspeção",
                            GG_STAGE_SHA256=sha, **dirty)
        for command in ("git commit", "git commit -m ''", "git commit -m '   '", "git commit -m x --no-verify",
                        "git commit --amend -m x", "git commit -m x -- novo.txt", "git commit -am x",
                        "git commit -m x -m y", "git commit --message=x", "git commit -mx"):
            with self.subTest(command=command):
                self.assert_blocked(command, "commit", GG_STAGE_SHA256=self.staged_sha(), **dirty)

    def test_stage_hash_is_raw_bytes_of_binary_diff(self) -> None:
        self.stage()
        raw = subprocess.run(["git", "-C", str(self.repo), "diff", "--cached", "--binary"],
                             check=True, capture_output=True).stdout
        independent = hashlib.sha256(raw).hexdigest()
        self.assertEqual(independent, self.staged_sha())
        result = self.gg("git commit -m 'registro'", "commit", GG_STAGE_SHA256=independent,
                         GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        self.assertEqual("GG-CONDICIONAL", result["veredito"], result["motivos"])

    def test_raw_command_text_is_checked_before_normalization(self) -> None:
        for command in ("git status\n", "\ngit status", " git status", "git status ", "\tgit status",
                        "git status\r", "git\tstatus"):
            with self.subTest(command=repr(command)):
                self.assert_blocked(command)

    def test_commit_blocks_whitespace_errors(self) -> None:
        self.stage("espaco.txt", "linha com espaço final \n")
        dirty = dict(GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        self.assert_blocked("git commit -m 'registro'", "commit", "diff --cached --check",
                            GG_STAGE_SHA256=self.staged_sha(), **dirty)

    def test_push_is_always_blocked(self) -> None:
        for command in ("git push", "git push origin deco/test", "git push -u origin deco/test",
                        "git push --force", "git push --dry-run"):
            with self.subTest(command=command):
                self.assert_blocked(
                    command, "publish", "push nunca é permitido no perfil miguel-day1",
                    GG_HUMAN_APPROVAL="yes", GG_REMOTE_NAME="origin",
                    GG_EXPECTED_REMOTE_SHA=self.remote_sha,
                )

    def test_findings_of_last_rejection_block(self) -> None:
        outside_link = self.repo / "atalho"
        outside_link.symlink_to(self.outside, target_is_directory=True)
        (self.outside / "x.txt").write_text("x\n", encoding="utf-8")
        dirty = dict(GG_DIRTY_ORIGIN="known", GG_PROTECTION="verified")
        cases = (
            ("git status --sho", "read"), ("git log --onel", "read"), ("git status --porcelain", "read"),
            ("git log --format=%H", "read"), ("git log -p", "read"), ("git diff -- ../fora", "read"),
            ("git diff HEAD", "read"), ("git show HEAD:AGENTS.md", "read"), ("git show -- HEAD", "read"),
            ("git show inexistente", "read"), ("git show --output=x HEAD", "read"),
            ("git rev-parse --git-path x", "read"), ("git ls-files --others", "read"),
            ("git worktree list --porcelain", "read"), ("git branch", "read"),
            ("git add AGENTS.md", "edit"), ("git add -- ", "edit"), ("git add -- ''", "edit"),
            ("git add -- .", "edit"), ("git add -- *.md", "edit"), ("git add -- ':(glob)*'", "edit"),
            ("git add -- :/AGENTS.md", "edit"), ("git add -- @lista", "edit"), ("git add -- ../fora.txt", "edit"),
            ("git add -- -x", "edit"), ("git add -- atalho/x.txt", "edit"), ("git add -- atalho", "edit"),
            ("git add -- .git/config", "edit"), ("git add -- inexistente.txt", "edit"),
            ("git add --pathspec-from-file=lista", "edit"), ("git add -p -- AGENTS.md", "edit"),
            ("git add -A", "edit"), ("git add -- AGENTS.md -A", "edit"),
            ("git switch deco/test", "branch"), ("git switch -c main", "branch"),
            ("git switch -c master", "branch"), ("git switch -c deco/v0.2", "branch"),
            ("git switch -c Piloto/Demo", "branch"), ("git switch -c piloto/demo HEAD~1", "branch"),
            ("git switch -c piloto/demo --track", "branch"), ("git switch -C piloto/demo", "branch"),
            ("git switch --create piloto/demo", "branch"), ("git switch -c piloto/../x", "branch"),
        )
        for command, operation in cases:
            with self.subTest(command=command):
                self.assert_blocked(command, operation, **dirty)
        git(self.repo, "branch", "piloto/existente")
        self.assert_blocked("git switch -c piloto/existente", "branch", "branch já existe")

    def test_wrappers_composition_and_global_options_block(self) -> None:
        for command in (
            "env git status", "/usr/bin/git status", "command git status", "sudo git status",
            "\\git status", "git -C . status", "git -c color.ui=never status", "git --git-dir=.git status",
            "git --work-tree=. status", "git --no-pager status", "git status && git push",
            "git status || true", "git status; ls", "git status | cat", "$(git status)", "(git status)",
            "git status > saida", "git status\ngit push", "git status # x", "git  status --short --short",
            "GIT_DIR=.git git status", "git st", "git stat",
        ):
            with self.subTest(command=command):
                self.assert_blocked(command)

    def test_target_and_label_are_strict(self) -> None:
        self.assert_blocked("git status", "read", "alvo do perfil miguel-day1", GG_TARGET="AGENTS.md")
        self.assert_blocked("git status", "read", "alvo do perfil miguel-day1", GG_TARGET=str(self.outside))
        root = self.gg("git status", GG_TARGET=str(self.repo))
        self.assertEqual("GG-SEGURO", root["veredito"], root["motivos"])
        self.assert_blocked("git status", "edit", "não corresponde ao comando efetivo")
        unknown = self.gg("git status", GG_MODE="miguel-day2")
        self.assertEqual("GG-BLOQUEADO", unknown["veredito"])
        self.assertEqual("desconhecido", unknown["perfil"])
        self.assertIn("modo do Git Guardian desconhecido: miguel-day2", unknown["motivos"])

    def test_main_rejects_writes_even_with_authorization(self) -> None:
        git(self.repo, "checkout", "-q", "-b", "main")
        main = dict(GG_EXPECTED_BRANCH="main", GG_EXPECTED_UPSTREAM="AUSENTE", GG_MAIN_AUTH="yes")
        self.assertEqual("GG-SEGURO", self.gg("git status", **main)["veredito"])
        self.assertEqual("GG-SEGURO", self.gg("git switch -c piloto/demo", "branch", **main)["veredito"])
        self.assert_blocked("git add -- AGENTS.md", "edit", "branch principal", **main)

    def test_deny_by_default_for_valid_unlisted_git_commands(self) -> None:
        """Propriedade: comandos Git válidos fora da allowlist sempre bloqueiam."""
        unlisted = (
            "git fetch", "git fetch origin", "git pull", "git pull origin deco/test", "git merge deco/test",
            "git rebase HEAD~1", "git cherry-pick HEAD", "git revert HEAD", "git reset", "git reset --hard",
            "git reset HEAD -- AGENTS.md", "git clean -n", "git clean -fd", "git checkout deco/test",
            "git checkout -b piloto/x", "git checkout -- AGENTS.md", "git restore --staged AGENTS.md",
            "git branch -d x", "git branch -D x", "git branch piloto/x", "git branch -a", "git stash",
            "git stash list", "git tag", "git tag v1", "git remote -v", "git remote add b /tmp/b",
            "git worktree add wt", "git worktree remove wt", "git worktree move a b", "git worktree prune",
            "git prune", "git gc", "git maintenance run", "git submodule status", "git config --get user.name",
            "git config user.name x", "git update-ref -d refs/heads/x", "git replace HEAD HEAD~1",
            "git notes add -m x", "git bisect start", "git rm AGENTS.md", "git mv AGENTS.md B.md",
            "git apply x.patch", "git am x.patch", "git format-patch -1", "git grep x", "git blame AGENTS.md",
            "git describe", "git reflog", "git shortlog", "git ls-remote origin", "git cat-file -p HEAD",
            "git archive HEAD", "git init", "git clone /tmp/x", "git help", "git version", "git --version",
            "git whatchanged", "git show-ref", "git for-each-ref", "git count-objects", "git fsck",
            "git symbolic-ref HEAD", "git diff --stat", "git diff --cached --stat", "git status -s",
            "git log --all", "git log --oneline --all", "git rev-parse --verify HEAD", "git ls-files -s",
            "git worktree lock wt", "git sparse-checkout list", "git lfs ls-files", "git difftool",
            "git mergetool", "git request-pull HEAD origin", "git send-email x", "git bundle create x HEAD",
        )
        for command in unlisted:
            with self.subTest(command=command):
                result = self.gg(command, "read", GG_HUMAN_APPROVAL="yes")
                self.assertEqual("GG-BLOQUEADO", result["veredito"], (command, result["motivos"]))
                self.assertIsNone(result["dimensoes"]["10"]["operacao_efetiva"], command)

    def test_general_profile_is_unchanged_without_mode(self) -> None:
        general = self.run_gg(GG_COMMAND="git fetch origin", GG_OPERATION="remote", GG_TARGET="origin",
                              GG_REMOTE_NAME="origin", GG_EXPECTED_REMOTE_SHA=self.remote_sha)
        self.assertEqual("GG-SEGURO", general["veredito"], general["motivos"])
        self.assertEqual("geral", general["perfil"])


if __name__ == "__main__":
    unittest.main()
