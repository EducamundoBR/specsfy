"""SPEC-0002/T002: contratos de sessão, rodada e ponteiros (AC-014–AC-026).

Os oráculos de contrato foram publicados em T002. A reconferência de T006
também exige os dois modelos preenchíveis previstos pelo Plan Gate.
"""

from __future__ import annotations

import re
import unicodedata
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SESSION_GUARDIAN = Path("deco/skills/session-guardian/SKILL.md")
REVIEW_REQUEST = Path("deco/templates/review-request.md")
REVIEW_VERDICT = Path("deco/templates/review-verdict.md")
CORRECTION_REPORT = Path("deco/templates/correction-report.md")


def normative_section(content: str, ac: str) -> str:
    """Isola um AC sem aceitar texto de seções vizinhas como evidência."""
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
    bdd = all(re.search(rf"(?im)^\s*{term}\b", section) for term in ("Given", "When", "Then"))
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
    checks.extend(
        (obligation, bool(re.search(expression, section, re.IGNORECASE | re.DOTALL)))
        for obligation, expression in clauses.items()
    )
    checks.extend((f"token exato {token}", token in section) for token in exact_tokens)
    return checks


FIELD = re.compile(r"(?m)^- \*\*(.+?)\*\*: (.*?)\s*$")
DECLARED = re.compile(r"(?m)^\s*[-*+]\s*\*\*(.+?)\*\*\s*:")
VERDICTS = {"APROVADO", "CORREÇÕES SOLICITADAS", "REPROVADO"}


def template_fields(template: Path) -> list[str]:
    content = (ROOT / template).read_text(encoding="utf-8")
    return [name for name, value in FIELD.findall(content) if value == "<preencher>"]


VERDICT_TABLE_HEADER = "| ID | Severidade P0–P3 | Fonte e trecho verificável | Impacto | Correção proposta |"
TABLE_SEPARATOR = re.compile(r"\|(?: ?:?-+:? ?\|)+")
MARKUP = re.compile(r"""[\[\]<>`*~$\\]|&(?:#\d+|#[xX][0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);|(?<![^\W_])_|_(?![^\W_])""")
BLOCK_START = re.compile(r"\s|[-+*>](?:\s|$)|\d{1,9}[.)](?:\s|$)|[=-]+$")


def markup_free(value: str) -> bool:
    """Sem marcação capaz de alterar a apresentação e sem caractere invisível de formatação."""
    return MARKUP.search(value) is None and all(unicodedata.category(char) != "Cf" for char in value)


def plain_text(value: str) -> bool:
    """Texto simples do contrato estrutural: sem marcação, sem `|`, sem citar severidade `P<n>` e sem
    terminar em `P` isolado, que a quebra de linha suave juntaria ao dígito da linha seguinte."""
    value = unicodedata.normalize("NFKC", value)
    return (markup_free(value) and "|" not in value and re.search(r"(?i)\bP\s*\d+\b", value) is None
            and re.search(r"(?i)\bP\s*$", value) is None)


def finding_row_allowed(line: str) -> bool:
    """Linha da tabela canônica: cinco células, severidade exatamente P0–P3 e as demais em texto simples,
    sem citar severidade; `\\|` é o único escape aceito dentro da célula."""
    row = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.removeprefix("|").removesuffix("|"))]
    return (line.endswith("|") and len(row) == VERDICT_TABLE_HEADER.count("|") - 1
            and row[1] in {"P0", "P1", "P2", "P3"}
            and all(plain_text(cell.replace("\\|", "")) for index, cell in enumerate(row) if index != 1))


def verdict_structure_problems(text: str) -> list[str]:
    """Adendo de 30/09/2026 à T006: o Verdict só aceita a estrutura do modelo (fail-closed).

    Aceita linhas em branco, título `#` inicial, linhas idênticas às do modelo (cabeçalhos `##`,
    prosa e tabela de condições), campos do modelo com valor em texto simples e uma única tabela
    canônica de achados. Qualquer outra linha é conteúdo fora do contrato.
    """
    model = (ROOT / REVIEW_VERDICT).read_text(encoding="utf-8").splitlines()
    verbatim = {line for line in model if line.strip() and not FIELD.fullmatch(line)
                and line != VERDICT_TABLE_HEADER and "<preencher>" not in line}
    fields = set(template_fields(REVIEW_VERDICT))
    problems, table, started = [], "ausente", False
    for line in (raw.rstrip() for raw in text.splitlines()):
        if table in {"cabeçalho", "linhas"} and not line.startswith("|"):
            table = "encerrada"
        field = re.fullmatch(r"- \*\*(.+?)\*\*: (.*)", line)
        if line == VERDICT_TABLE_HEADER and table == "ausente":
            allowed, table = True, "cabeçalho"
        elif table == "cabeçalho":
            allowed, table = TABLE_SEPARATOR.fullmatch(line) is not None, "linhas"
        elif table == "linhas":
            allowed = finding_row_allowed(line)
        elif not line or line in verbatim:
            allowed = True
        elif line.startswith("# ") and not started:
            allowed = plain_text(line[2:])
        elif field and field.group(1) in fields:
            allowed = plain_text(field.group(2))
        else:
            allowed = not BLOCK_START.match(line) and not line.startswith("#") and plain_text(line)
        started = started or bool(line)
        if not allowed:
            problems.append(f"linha fora do contrato do Verdict: {line}")
    return problems


def validate_round_artifact(
    template: Path, text: str, *, observed_head: str, observed_branch: str, request: str,
) -> list[str]:
    """Confere um artefato preenchido contra os campos obrigatórios do modelo."""
    values = dict(FIELD.findall(text))
    declared = [" ".join(name.split()) for name in DECLARED.findall(text)]
    problems = []
    for field in template_fields(template):
        value = " ".join(values.get(field, "").split())
        if declared.count(field) > 1:
            problems.append(f"campo duplicado: {field}")
        elif field not in values:
            problems.append(f"campo ausente: {field}")
        elif not value or value == "<preencher>":
            problems.append(f"campo não preenchido: {field}")
        elif re.search(r"(?i)n[aã]o registrado", value):
            problems.append(f"campo NÃO REGISTRADO: {field}")
    if template == REVIEW_REQUEST and "Branch" in values and values["Branch"] != observed_branch:
        problems.append("branch divergente da base observada")
    if template == REVIEW_REQUEST and "HEAD" in values and values["HEAD"] != observed_head:
        problems.append("HEAD divergente da base observada")
    if template == REVIEW_VERDICT:
        requested = dict(FIELD.findall(request))
        if values.get("Veredito") and values["Veredito"] not in VERDICTS:
            problems.append(f"veredito fora do vocabulário: {values['Veredito']}")
        if values.get("Session ID") == requested.get("Session ID") or values.get("Revisor") == requested.get("Implementador"):
            problems.append("revisor e implementador na mesma sessão")
        problems.extend(verdict_structure_problems(text))
    return problems


class GovernanceRoundsTest(unittest.TestCase):
    def assert_contract(
        self,
        ac: str,
        path: Path,
        clauses: dict[str, str],
        exact_tokens: tuple[str, ...] = (),
    ) -> None:
        for obligation, satisfied in contract_checks(ac, path, clauses, exact_tokens):
            with self.subTest(ac=ac, obligation=obligation):
                self.assertTrue(satisfied, f"{ac}: {path} não satisfaz: {obligation}")

    def test_ac014_single_active_context_is_validated_offline(self) -> None:
        self.assert_contract("AC-014", SESSION_GUARDIAN, {
            "um contexto por ponteiro": r"SESSION_CURRENT.{0,160}exatamente um.{0,120}contexto",
            "estado observado": r"projeto.{0,100}branch.{0,100}HEAD.{0,160}estado observado",
            "cinco campos e escopo": r"cinco campos.{0,160}(?:superad|escopo)",
            "funciona offline": r"sem (?:acesso (?:à|a) )?(?:rede|servi[cç]o externo)",
        }, exact_tokens=("SESSION_CURRENT", "SG-VÁLIDO"))

    def test_ac014_ambiguous_active_context_blocks(self) -> None:
        self.assert_contract("AC-014", SESSION_GUARDIAN, {
            "dois ativos bloqueiam": r"dois contextos.{0,120}ATUAL.{0,160}SG-BLOQUEADO",
            "sem escolha silenciosa": r"nenhum contexto.{0,100}escolhid.{0,80}silencios",
        }, exact_tokens=("ATUAL", "SG-BLOQUEADO"))

    def test_ac014_unexplained_identity_divergence_blocks(self) -> None:
        self.assert_contract("AC-014", SESSION_GUARDIAN, {
            "identidade divergente": r"(?:projeto|branch|HEAD).{0,160}diverg.{0,160}SG-BLOQUEADO",
            "reconciliação obrigatória": r"continuidade.{0,120}recusad.{0,120}reconcili",
        }, exact_tokens=("SG-BLOQUEADO",))

    def test_ac015_transcript_is_never_canonical(self) -> None:
        self.assert_contract("AC-015", SESSION_GUARDIAN, {
            "transcript ou resumo recusado": r"transcript.{0,120}resumo autom[aá]tico.{0,180}n[aã]o.{0,80}fonte can[oô]nica",
            "fonte única bloqueia": r"[uú]nica fonte.{0,160}SG-BLOQUEADO",
            "arquivo curado obrigatório": r"arquivo curado.{0,120}SESSION_CURRENT",
        }, exact_tokens=("SESSION_CURRENT", "SG-BLOQUEADO"))

    def test_ac016_material_change_opens_new_round(self) -> None:
        self.assert_contract("AC-016", SESSION_GUARDIAN, {
            "três gatilhos materiais": r"decis[aã]o.{0,100}escopo.{0,140}classe de risco",
            "nova rodada antes de seguir": r"MUDANÇA MATERIAL.{0,180}SG-BLOQUEADO.{0,220}nova rodada.{0,140}CURRENT",
            "histórico não reescrito": r"contexto anterior.{0,140}n[aã]o.{0,80}reescrit",
        }, exact_tokens=("MUDANÇA MATERIAL", "SG-BLOQUEADO", "CURRENT"))

    def test_ac016_reversible_metadata_fix_is_conditional(self) -> None:
        self.assert_contract("AC-016", SESSION_GUARDIAN, {
            "correção não material": r"metadado.{0,100}evid[eê]ncia.{0,100}proveni[eê]ncia.{0,180}sem alterar.{0,180}(?:decis[aã]o|escopo|risco)",
            "correção reversível": r"SG-CONDICIONAL.{0,180}revers[ií]vel",
            "ponteiro preservado e recheck": r"SESSION_CURRENT.{0,160}[uú]nico contexto.{0,180}verifica[cç][aã]o.{0,80}repetid",
        }, exact_tokens=("SG-CONDICIONAL", "SESSION_CURRENT"))

    def test_ac017_closure_preserves_superseded_context(self) -> None:
        self.assert_contract("AC-017", SESSION_GUARDIAN, {
            "cinco campos com porquê": r"cinco campos.{0,180}porqu[eê].{0,100}decis[aã]o",
            "um ativo": r"exatamente um contexto.{0,100}ativ",
            "anterior superado e imutável": r"anterior.{0,120}superad.{0,160}sem.{0,80}reescrit",
            "snapshot e ponteiro atômicos": r"snapshot.{0,120}SESSION_CURRENT.{0,160}(?:conjunta|at[oô]mic)",
        }, exact_tokens=("SESSION_CURRENT",))

    def test_ac018_unverified_state_blocks_closure(self) -> None:
        self.assert_contract("AC-018", SESSION_GUARDIAN, {
            "estado não observado": r"branch.{0,80}HEAD.{0,80}stage.{0,80}worktree.{0,140}sem observa[cç][aã]o",
            "bloqueio até observação": r"SG-BLOQUEADO.{0,180}impedid.{0,180}observad.{0,100}registrad",
        }, exact_tokens=("SG-BLOQUEADO",))

    def test_ac018_decision_without_reason_is_rejected(self) -> None:
        self.assert_contract("AC-018", SESSION_GUARDIAN, {
            "decisão sem motivo": r"decis[oõ]es.{0,140}apenas.{0,100}decidid",
            "porquê obrigatório": r"recusad.{0,160}porqu[eê].{0,120}obrigat[oó]ri",
        })

    def test_ac018_context_loss_cannot_auto_resume(self) -> None:
        self.assert_contract("AC-018", SESSION_GUARDIAN, {
            "perda impede continuidade": r"compress[aã]o.{0,100}perda de contexto.{0,180}SG-BLOQUEADO",
            "handoff estruturado": r"retomada autom[aá]tica.{0,160}n[aã]o.{0,120}handoff estruturado",
        }, exact_tokens=("SG-BLOQUEADO",))

    def test_ac018_third_compaction_starts_new_session(self) -> None:
        self.assert_contract("AC-018", SESSION_GUARDIAN, {
            "terceira compactação": r"duas compacta[cç][oõ]es.{0,160}terceira.{0,160}SG-CONDICIONAL",
            "nova sessão e recheck": r"nova sess[aã]o.{0,120}handoff estruturado.{0,160}verifica[cç][aã]o.{0,80}repetid",
        }, exact_tokens=("SG-CONDICIONAL",))

    def test_ac019_guardians_and_handoff_are_distinct(self) -> None:
        self.assert_contract("AC-019", SESSION_GUARDIAN, {
            "vereditos SG": r"SG-VÁLIDO.{0,100}SG-CONDICIONAL.{0,100}SG-BLOQUEADO",
            "vereditos GG": r"reposit[oó]rio.{0,140}prefixo GG",
            "handoff administra pacote": r"review-handoff.{0,160}Review Request.{0,100}Review Verdict.{0,100}Correction Report.{0,100}rodada",
            "sem substituição": r"nenhum.{0,140}substitui.{0,140}demais",
        }, exact_tokens=("SG-VÁLIDO", "SG-CONDICIONAL", "SG-BLOQUEADO"))

    def test_ac020_review_unit_is_one_consolidated_package(self) -> None:
        self.assert_contract("AC-020", REVIEW_REQUEST, {
            "pacote em vez de prompt": r"tr[eê]s prompts.{0,180}uma [uú]nica unidade",
            "um pedido consolidado": r"exatamente um.{0,100}(?:Review Request|pedido de revis[aã]o).{0,100}consolidad",
            "sem revisão por prompt": r"n[aã]o.{0,120}tr[eê]s revis[oõ]es.{0,120}prompt",
        })

    def test_ac021_request_has_fields_provenance_and_no_transcript(self) -> None:
        self.assert_contract("AC-021", REVIEW_REQUEST, {
            "estado e diff": r"unidade.{0,80}risco.{0,80}justificativa.{0,100}branch.{0,80}HEAD.{0,100}base.{0,80}escopo do diff",
            "conteúdo do pacote": r"arquivos.{0,80}testes.{0,80}decis[oõ]es.{0,80}d[uú]vidas.{0,80}fontes.{0,80}restri[cç][oõ]es",
            "proveniência do implementador": r"harness.{0,80}modelo.{0,80}effort.{0,80}session ID.{0,120}implementador",
            "sem histórico de conversa": r"(?:nenhum|sem).{0,120}(?:hist[oó]rico de conversa|transcript)",
        })

    def test_ac022_verdict_is_separate_and_signed(self) -> None:
        self.assert_contract("AC-022", REVIEW_REQUEST, {
            "verdict separado": r"Review Verdict.{0,180}(?:separad|distint).{0,140}Review Request",
            "proveniência do revisor": r"harness.{0,80}modelo.{0,80}effort.{0,80}session ID.{0,120}revisor",
            "achados e decisão": r"evid[eê]ncias.{0,100}P0.{0,60}P1.{0,60}P2.{0,60}P3.{0,100}veredito.{0,80}condi[cç][oõ]es.{0,80}gate",
        }, exact_tokens=("Review Request", "Review Verdict"))

    def test_ac022_same_session_cannot_approve(self) -> None:
        self.assert_contract("AC-022", REVIEW_REQUEST, {
            "mesma sessão bloqueia": r"mesmo session ID.{0,180}aprova[cç][aã]o.{0,120}bloquead",
        }, exact_tokens=("session ID",))

    def test_ac023_corrections_are_batched_in_same_round(self) -> None:
        self.assert_contract("AC-023", REVIEW_REQUEST, {
            "correções em lote": r"corre[cç][oõ]es.{0,100}(?:em lote|lote)",
            "report na mesma rodada": r"Correction Report.{0,160}mesma rodada",
            "aplicado e não aplicado": r"achados tratados.{0,120}corre[cç][oõ]es aplicadas.{0,160}n[aã]o aplicados.{0,100}justificativa",
            "mesmo revisor uma vez": r"mesmo revisor.{0,140}(?:uma [uú]nica vez|uma vez)",
            "sem revisão por correção": r"nenhuma revis[aã]o.{0,140}cada corre[cç][aã]o",
        }, exact_tokens=("Correction Report",))

    def test_ac024_current_rejects_multiple_active_rounds(self) -> None:
        self.assert_contract("AC-024", REVIEW_REQUEST, {
            "ambiguidade rejeitada": r"CURRENT.{0,140}mais de uma rodada ativa.{0,180}rejeitad",
            "sem escolha silenciosa": r"nenhuma rodada.{0,100}escolhid.{0,80}silencios",
            "antes do parecer": r"ambiguidade.{0,120}antes.{0,100}parecer",
        }, exact_tokens=("CURRENT",))

    def test_ac025_completed_round_is_immutable(self) -> None:
        self.assert_contract("AC-025", REVIEW_REQUEST, {
            "aprovada ou reprovada": r"veredito.{0,100}aprovad.{0,100}reprovad",
            "alteração recusada": r"altera[cç][aã]o.{0,120}recusad",
            "revisão adicional em nova rodada": r"revis[aã]o adicional.{0,140}rodada nova",
        })

    def test_ac026_material_change_repoints_current(self) -> None:
        self.assert_contract("AC-026", REVIEW_REQUEST, {
            "gatilhos materiais": r"decis[aã]o.{0,100}escopo.{0,140}classe de risco",
            "nova rodada e ponteiro": r"MUDANÇA MATERIAL.{0,160}nova rodada.{0,160}CURRENT",
            "anterior encerrada sem rewrite": r"rodada anterior.{0,140}encerrad.{0,140}sem.{0,80}reescrit",
        }, exact_tokens=("MUDANÇA MATERIAL", "CURRENT"))

    def test_ac022_ac023_three_separate_fillable_templates(self) -> None:
        """Cada papel recebe campos próprios no artefato correspondente."""
        expected = {
            REVIEW_REQUEST: ("implementador", ("Unidade", "Risco", "Justificativa", "Gate", "Perfil", "Branch", "HEAD", "Base", "Escopo do diff")),
            REVIEW_VERDICT: ("revisor", ("Harness", "Modelo", "Effort", "Session ID", "Evidências", "Achados P0-P3", "Veredito", "Condições", "Gate resultante")),
            CORRECTION_REPORT: ("implementador", ("Achados tratados", "Correções aplicadas", "Não aplicados e justificativa", "Novo diff", "Testes", "Estado Git", "Pedido de reconferência")),
        }
        self.assertEqual(3, len(expected))
        for path, (owner, fields) in expected.items():
            with self.subTest(path=path):
                artifact = ROOT / path
                self.assertTrue(artifact.is_file(), f"modelo ausente: {path}")
                content = artifact.read_text(encoding="utf-8")
                self.assertRegex(content, rf"(?im)^Responsável:\s*{owner}\s*$")
                for field in fields:
                    self.assertRegex(
                        content,
                        rf"(?m)^- \*\*{re.escape(field)}\*\*: <preencher>\s*$",
                        f"{path}: campo preenchível ausente: {field}",
                    )

    def test_ac022_verdict_enumerates_allowed_values(self) -> None:
        """O modelo do revisor fixa o vocabulário do veredito da rodada."""
        content = (ROOT / REVIEW_VERDICT).read_text(encoding="utf-8")
        self.assertRegex(
            content,
            r"Valores permitidos para `Veredito`: `APROVADO`, `CORREÇÕES SOLICITADAS` ou `REPROVADO`",
        )

    def test_t006_fixtures_follow_template_schema(self) -> None:
        """T006: fixtures válidas/inválidas conferidas contra os campos dos modelos.

        O modelo é o schema; o validador integrado e o inventário são de T013.
        """
        observed_head = "a" * 40
        observed_branch = "fixture/rodada"
        request = self.round_fixture("request-valid.md")
        cases = {
            "request-valid.md": (REVIEW_REQUEST, []),
            "request-missing-field.md": (REVIEW_REQUEST, ["campo ausente: Session ID"]),
            "request-placeholder.md": (REVIEW_REQUEST, ["campo não preenchido: Testes"]),
            "request-divergent-head.md": (REVIEW_REQUEST, ["HEAD divergente da base observada"]),
            "request-divergent-branch.md": (REVIEW_REQUEST, ["branch divergente da base observada"]),
            "request-unregistered-session.md": (REVIEW_REQUEST, ["campo NÃO REGISTRADO: Session ID"]),
            "verdict-unregistered-session.md": (REVIEW_VERDICT, ["campo NÃO REGISTRADO: Session ID"]),
            "verdict-annotated-unregistered.md": (REVIEW_VERDICT, ["campo NÃO REGISTRADO: Session ID"]),
            "verdict-valid.md": (REVIEW_VERDICT, []),
            "verdict-invalid-value.md": (REVIEW_VERDICT, ["veredito fora do vocabulário: OK"]),
            "verdict-same-session.md": (REVIEW_VERDICT, ["revisor e implementador na mesma sessão"]),
            "correction-valid.md": (CORRECTION_REPORT, []),
            "correction-missing-field.md": (CORRECTION_REPORT, ["campo ausente: Estado Git"]),
        }
        for name, (template, expected) in cases.items():
            with self.subTest(fixture=name):
                problems = validate_round_artifact(
                    template, self.round_fixture(name), observed_head=observed_head,
                    observed_branch=observed_branch, request=request,
                )
                self.assertEqual(expected, problems)

    def test_spaced_unregistered_session_blocks_high_risk_plan(self) -> None:
        unlock = ROOT / "deco/fixtures/review-handoff/write-unlock"
        observed = dict(FIELD.findall((unlock / "alto-plano-aprovado/base-observada.md").read_text(encoding="utf-8")))
        request = (unlock / "alto-plano-aprovado/plano/review-request.md").read_text(encoding="utf-8")
        valid = (unlock / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        spaced = (unlock / "alto-verdict-sessao-espacada/plano/review-verdict.md").read_text(encoding="utf-8")
        cases = {
            "sessão registrada": (valid, []),
            "espaço duplo": (spaced, ["campo NÃO REGISTRADO: Session ID"]),
            "tab interno": (spaced.replace("NÃO  REGISTRADO", "NÃO\tREGISTRADO"), ["campo NÃO REGISTRADO: Session ID"]),
        }
        for name, (text, expected) in cases.items():
            with self.subTest(case=name):
                self.assertEqual(expected, validate_round_artifact(
                    REVIEW_VERDICT, text, observed_head=observed["HEAD"],
                    observed_branch=observed["Branch"], request=request,
                ))

    def test_verdict_structural_contract_addendum(self) -> None:
        """Adendo de 30/09/2026: o Verdict aceita só a estrutura do modelo, sem interpretar o Markdown."""
        template = (ROOT / REVIEW_VERDICT).read_text(encoding="utf-8")
        section = normative_section(template, "Contrato estrutural")
        self.assertRegex(section, r"Adendo de 30/09/2026")
        self.assertRegex(section, r"(?s)única fonte de P0, P1, P2 e P3")
        self.assertRegex(section, r"(?s)Qualquer outra linha bloqueia")
        for name in ("verdict-valid.md", "verdict-same-session.md", "verdict-invalid-value.md"):
            with self.subTest(fixture=name):
                self.assertEqual([], verdict_structure_problems(self.round_fixture(name)))
        valid = self.round_fixture("verdict-valid.md")
        request = self.round_fixture("request-valid.md")
        for change in ("\n[P]1 contrato aberto\n", "\n## Seção fora do modelo\n", "\n- **Notas**: nenhuma\n"):
            with self.subTest(change=change):
                problems = validate_round_artifact(REVIEW_VERDICT, valid + change, observed_head="a" * 40,
                                                   observed_branch="fixture/rodada", request=request)
                self.assertEqual([f"linha fora do contrato do Verdict: {change.strip()}"], problems)

    def test_duplicated_field_is_rejected_instead_of_last_value_winning(self) -> None:
        unlock = ROOT / "deco/fixtures/review-handoff/write-unlock"
        observed = dict(FIELD.findall((unlock / "alto-plano-aprovado/base-observada.md").read_text(encoding="utf-8")))
        request = (unlock / "alto-plano-aprovado/plano/review-request.md").read_text(encoding="utf-8")
        verdict = (unlock / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        corrections = verdict.replace("- **Veredito**: APROVADO", "- **Veredito**: CORREÇÕES SOLICITADAS\n- **Veredito**: APROVADO")
        indented = verdict.replace("- **Veredito**: APROVADO", "- **Veredito**: APROVADO\n  - **Veredito**: REPROVADO")
        branches = request.replace("- **Branch**: fixture/rodada", "- **Branch**: outra/branch\n- **Branch**: fixture/rodada")
        cases = {
            "veredito contraditório": (REVIEW_VERDICT, corrections, ["campo duplicado: Veredito"]),
            "veredito duplicado com recuo": (REVIEW_VERDICT, indented, [
                "campo duplicado: Veredito", "linha fora do contrato do Verdict:   - **Veredito**: REPROVADO"]),
            "branch contraditória": (REVIEW_REQUEST, branches, ["campo duplicado: Branch"]),
        }
        for name, (template, text, expected) in cases.items():
            with self.subTest(case=name):
                self.assertEqual(expected, validate_round_artifact(
                    template, text, observed_head=observed["HEAD"],
                    observed_branch=observed["Branch"], request=request,
                ))

    def round_fixture(self, name: str) -> str:
        path = ROOT / "deco/fixtures/review-round" / name
        self.assertTrue(path.is_file(), f"fixture ausente: {path}")
        return path.read_text(encoding="utf-8")

    def test_negative_tokens_without_decision_are_rejected(self) -> None:
        shallow = "## AC-024\nCURRENT e rodada ativa.\n"
        checks = dict(contract_checks("AC-024", REVIEW_REQUEST, {}, exact_tokens=("CURRENT",), sample=shallow))
        self.assertTrue(checks["token exato CURRENT"])
        self.assertFalse(checks["estrutura de decisão condição → resultado"])

    def test_negative_lowercase_session_verdict_is_rejected(self) -> None:
        sample = "## AC-014\n- **Condição**: sessão aberta\n- **Resultado**: sg-válido\n"
        checks = dict(contract_checks("AC-014", SESSION_GUARDIAN, {}, exact_tokens=("SG-VÁLIDO",), sample=sample))
        self.assertTrue(checks["estrutura de decisão condição → resultado"])
        self.assertFalse(checks["token exato SG-VÁLIDO"])


if __name__ == "__main__":
    unittest.main()
