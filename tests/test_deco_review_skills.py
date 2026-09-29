"""SPEC-0002/T007–T010: obrigações das skills de revisão.

Os contratos AC-001–AC-010 vivem em `test_deco_governance_contracts.py` e o
AC-027 em `test_deco_governance_delivery.py`. Esta suíte cobre os achados da
revisão independente do roteador (T007) e as verificações próprias de T008,
T009 e T010: critérios do gate, achados priorizados, não autoaprovação,
dependências cíclicas, lacunas, escopo adiado e estados de entrega, com
fixtures de Review Verdict conferidas contra o modelo de T006. T011
(`review-handoff`) é coberta pelo ciclo da rodada, pela separação entre
`CURRENT` e `SESSION_CURRENT` e por fixtures de ponteiro de rodada.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = Path("deco/skills/review-router/SKILL.md")


def section(path: Path, heading: str) -> str:
    content = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(rf"(?m)^#{{2,6}}\s+{re.escape(heading)}(?:\b|[\s:—-]).*$", content)
    if match is None:
        return ""
    rest = content[match.end():]
    following = re.search(r"(?m)^#{1,6}\s+", rest)
    return rest[:following.start()] if following else rest


class ReviewRouterReviewFindingsTest(unittest.TestCase):
    """Achados da revisão independente de T007 (ciclo 1)."""

    def test_forwarding_requires_provenance_of_implementer_and_reviewer(self) -> None:
        text = section(ROUTER, "AC-010")
        self.assertRegex(text, r"(?s)harness.{0,60}modelo.{0,60}effort.{0,60}session ID.{0,160}implementador.{0,80}revisor")
        self.assertRegex(text, r"(?s)NÃO REGISTRADO.{0,200}(?:recus|bloque)")

    def test_unobserved_value_can_be_completed_only_by_documented_observation(self) -> None:
        text = section(ROUTER, "AC-007")
        self.assertNotIn("completado depois", text)
        self.assertRegex(text, r"(?s)observa[cç][aã]o posterior.{0,160}(?:documentad|fonte)")

    def test_push_case_follows_real_destination_and_effect(self) -> None:
        text = section(ROUTER, "Casos limítrofes")
        row = next((line for line in text.splitlines() if line.startswith("| Push")), "")
        self.assertRegex(row, r"gatilho 7 apenas.{0,120}produ[cç][aã]o")
        self.assertRegex(row, r"gatilho 8 apenas.{0,120}reescrev")
        self.assertRegex(row, r"parada humana.{0,80}(?:antes de publicar|FR-012)")


DEFINITION = Path("deco/skills/review-definition/SKILL.md")
PLAN = Path("deco/skills/review-plan/SKILL.md")
DELIVERY = Path("deco/skills/review-delivery/SKILL.md")
VERDICT_TEMPLATE = Path("deco/templates/review-verdict.md")
FIXTURES = Path("deco/fixtures/review-skills")
FIELD = re.compile(r"(?m)^- \*\*(.+?)\*\*: (.*?)\s*$")
VERDICTS = {"APROVADO", "CORREÇÕES SOLICITADAS", "REPROVADO"}
TABLE = r"(?m)^\|\s*Condi[cç][aã]o\s*\|\s*(?:A[cç][aã]o|Resultado)\s*\|"


def frontmatter_name(path: Path) -> str:
    content = (ROOT / path).read_text(encoding="utf-8") if (ROOT / path).is_file() else ""
    match = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: .+?\n---\n", content)
    return match.group(1) if match else ""


def verdict_fields(text: str) -> dict[str, str]:
    return dict(FIELD.findall(text))


def verdict_problems(text: str) -> list[str]:
    """Confere um Review Verdict de fixture contra os campos do modelo de T006."""
    template = (ROOT / VERDICT_TEMPLATE).read_text(encoding="utf-8")
    required = [name for name, value in FIELD.findall(template) if value == "<preencher>"]
    values = verdict_fields(text)
    problems = [f"campo ausente ou vazio: {name}" for name in required
                if not values.get(name) or values[name] == "<preencher>"]
    if values.get("Veredito") not in VERDICTS:
        problems.append("veredito fora do vocabulário")
    if values.get("Revisor") and values.get("Revisor") == values.get("Implementador"):
        problems.append("revisor igual ao implementador")
    header = next((line for line in template.splitlines() if line.startswith("| ID ")), "")
    if header not in text.splitlines():
        problems.append("tabela de achados fora do modelo")
    columns = header.count("|") - 1
    for row in finding_rows(text):
        if len(row) != columns or not all(row):
            problems.append("achado com célula ausente: " + " | ".join(row))
        elif row[1] not in {"P0", "P1", "P2", "P3"}:
            problems.append("severidade fora de P0–P3: " + row[1])
    return problems


def finding_rows(text: str) -> list[list[str]]:
    """Todas as linhas da tabela de achados, do separador até a primeira linha fora da tabela."""
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines) if line.startswith("| ID ")), None)
    if start is None:
        return []
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().removeprefix("|").removesuffix("|").split("|")])
    return rows


def findings(text: str) -> list[tuple[str, str]]:
    """Achados da tabela do modelo: (severidade, fonte, impacto e correção)."""
    return [(row[1], " ".join(row[2:])) for row in finding_rows(text)]


def fixture(name: str) -> str:
    path = ROOT / FIXTURES / name
    return path.read_text(encoding="utf-8") if path.is_file() else ""


class ReviewGateSkillsCommonTest(unittest.TestCase):
    """Obrigações comuns às três skills de gate (FR-003, FR-006)."""

    def test_skills_exist_with_canonical_names(self) -> None:
        for path, name in ((DEFINITION, "review-definition"), (PLAN, "review-plan"),
                           (DELIVERY, "review-delivery")):
            with self.subTest(skill=name):
                self.assertEqual(name, frontmatter_name(path))

    def test_each_skill_is_routed_composed_and_never_self_approves(self) -> None:
        for path in (DEFINITION, PLAN, DELIVERY):
            with self.subTest(skill=str(path)):
                text = section(path, "Separação e fechamento")
                self.assertRegex(text, TABLE)
                self.assertRegex(text, r"(?s)review-router.{0,200}perfis?.{0,160}n[aã]o fecha")
                self.assertRegex(text, r"(?s)contexto novo.{0,80}somente leitura")
                self.assertRegex(text, r"(?s)(?:mesma inst[aâ]ncia|mesmo session ID).{0,160}(?:recus|bloque)")
                self.assertRegex(text, r"(?s)n[aã]o (?:marca|aprova|promove).{0,80}Gate")
                self.assertRegex(text, r"review-verdict\.md")

    def test_each_skill_prioritizes_findings(self) -> None:
        for path in (DEFINITION, PLAN, DELIVERY):
            with self.subTest(skill=str(path)):
                text = section(path, "Achados priorizados")
                self.assertRegex(text, TABLE)
                self.assertRegex(text, r"(?s)P0.{0,200}P1.{0,200}P2.{0,200}P3")
                self.assertRegex(text, r"(?s)ordem de severidade.{0,160}evid[eê]ncia.{0,120}corre[cç][aã]o")


class VerdictFixtureValidatorTest(unittest.TestCase):
    """Controles negativos do validador de fixtures de Review Verdict."""

    def test_every_row_of_findings_table_is_checked(self) -> None:
        valid = fixture("delivery-verdict-regression.md")
        self.assertEqual([], verdict_problems(valid))
        extra = valid + "| E-X | P2 | fonte | impacto | correção | célula extra |\n"
        self.assertTrue(verdict_problems(extra), "linha fora do modelo passou")
        empty = valid + "| E-3 | P3 | fonte |  | correção |\n"
        self.assertTrue(verdict_problems(empty), "célula vazia passou")
        free = valid + "| qualquer | coisa |\n"
        self.assertTrue(verdict_problems(free), "linha livre passou")
        severity = valid + "| E-4 | coisa | fonte | impacto | correção |\n"
        self.assertTrue(verdict_problems(severity), "severidade fora de P0–P3 passou")


class ReviewDefinitionTest(unittest.TestCase):
    """T008: problema, requisitos, escopo e decisões do Definition Gate."""

    def test_definition_gate_criteria(self) -> None:
        text = section(DEFINITION, "Critérios do Definition Gate")
        self.assertRegex(text, TABLE)
        for term in (r"problema", r"requisitos", r"escopo inclu[ií]do", r"escopo exclu[ií]do",
                     r"decis[oõ]es", r"cen[aá]rios BDD", r"d[uú]vidas abertas", r"contradi[cç]"):
            with self.subTest(term=term):
                self.assertRegex(text, rf"(?i){term}")

    def test_review_unit_is_one_coherent_package(self) -> None:
        text = section(DEFINITION, "Unidade revisada")
        self.assertRegex(text, r"(?s)uma spec.{0,160}(?:um|único) Review Request")
        self.assertRegex(text, r"(?s)perfis.{0,120}anexos ao mesmo pedido")

    def test_fixture_verdict_is_prioritized_and_not_self_approved(self) -> None:
        text = fixture("definition-verdict.md")
        self.assertTrue(text, "fixture ausente")
        self.assertEqual([], verdict_problems(text))
        self.assertEqual("CORREÇÕES SOLICITADAS", verdict_fields(text)["Veredito"])
        severities = [severity for severity, _ in findings(text)]
        self.assertGreaterEqual(len(severities), 2)
        self.assertEqual(sorted(severities), severities, "achados fora da ordem de severidade")


class ReviewPlanTest(unittest.TestCase):
    """T009: arquitetura, tarefas, ordem, riscos, rollback e testes do Plan Gate."""

    def test_plan_gate_criteria(self) -> None:
        text = section(PLAN, "Critérios do Plan Gate")
        self.assertRegex(text, TABLE)
        for term in (r"arquitetura", r"tarefas", r"ordem", r"riscos", r"rollback", r"testes previstos",
                     r"rastreabilidade"):
            with self.subTest(term=term):
                self.assertRegex(text, rf"(?i){term}")

    def test_cycles_gaps_and_deferred_scope_have_decisions(self) -> None:
        text = section(PLAN, "Dependências, lacunas e escopo adiado")
        self.assertRegex(text, TABLE)
        self.assertRegex(text, r"(?s)depend[eê]ncia c[ií]clica.{0,160}(?:P1|bloque)")
        self.assertRegex(text, r"(?s)lacuna.{0,160}(?:requisito|AC).{0,120}sem.{0,60}(?:tarefa|teste)")
        self.assertRegex(text, r"(?s)escopo adiado.{0,200}(?:declarad|registrad).{0,120}decis[aã]o")
        self.assertRegex(text, r"(?s)n[aã]o promove.{0,80}Plan Gate")

    def test_fixture_verdicts_approve_and_request_corrections(self) -> None:
        approved = fixture("plan-verdict-approved.md")
        corrections = fixture("plan-verdict-corrections.md")
        self.assertTrue(approved and corrections, "fixtures ausentes")
        self.assertEqual([], verdict_problems(approved))
        self.assertEqual([], verdict_problems(corrections))
        self.assertEqual("APROVADO", verdict_fields(approved)["Veredito"])
        self.assertEqual("CORREÇÕES SOLICITADAS", verdict_fields(corrections)["Veredito"])
        self.assertRegex(corrections, r"(?i)depend[eê]ncia c[ií]clica")
        self.assertIn("P1", [severity for severity, _ in findings(corrections)])
        self.assertRegex(verdict_fields(approved)["Gate resultante"], r"(?i)pendente|recomend")


class ReviewDeliveryTest(unittest.TestCase):
    """T010: diff, testes, evidências, regressões, aderência e três estados."""

    def test_delivery_gate_criteria(self) -> None:
        text = section(DELIVERY, "Critérios do Delivery Gate")
        self.assertRegex(text, TABLE)
        for term in (r"diff", r"testes", r"evid[eê]ncias", r"regress", r"ader[eê]ncia", r"Contrato de Entrega"):
            with self.subTest(term=term):
                self.assertRegex(text, rf"(?i){term}")

    def test_three_states_are_not_collapsible(self) -> None:
        text = section(DELIVERY, "Estados de entrega")
        self.assertRegex(text, TABLE)
        for token in ("PRONTO", "ENTREGUE", "ACEITO", "CORREÇÃO NECESSÁRIA"):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertRegex(text, r"(?s)n[aã]o s[aã]o sin[oô]nimos")
        self.assertRegex(text, r"(?s)evid[eê]ncia material ausente.{0,160}(?:n[aã]o aprova|CORREÇÕES SOLICITADAS)")
        self.assertRegex(text, r"(?s)[Nn]enhum estado excepcional.{0,80}diretamente.{0,40}`ACEITO`")

    def test_each_exceptional_transition_keeps_its_origin_state(self) -> None:
        rows = [line for line in section(DELIVERY, "Estados de entrega").splitlines() if line.startswith("| ")]

        def row(pattern: str) -> str:
            found = [line for line in rows if re.search(pattern, line.split("|")[1], re.IGNORECASE)]
            self.assertEqual(1, len(found), pattern)
            return found[0]

        self.assertRegex(row(r"regress[aã]o antes da entrega"), r"CORREÇÃO NECESSÁRIA")
        self.assertRegex(row(r"presen[cç]a ou alcance"), r"(?i)n[aã]o entra em `ENTREGUE`")
        delivered = row(r"reprova[cç][aã]o ap[oó]s a entrega")
        self.assertRegex(delivered, r"`ENTREGUE COM CORREÇÕES` → `CORREÇÃO NECESSÁRIA` → `PRONTO`.{0,120}nova entrega")
        self.assertRegex(delivered, r"motivo.{0,80}corre[cç][aã]o necess[aá]ria")
        accepted = row(r"regress[aã]o ap[oó]s o aceite")
        self.assertRegex(accepted, r"`ACEITE REVOGADO`.{0,120}`CORREÇÃO NECESSÁRIA`.{0,120}motivo.{0,60}nova evid[eê]ncia")
        self.assertRegex(accepted, r"`CORREÇÃO NECESSÁRIA` → `PRONTO` → `ENTREGUE` → `ACEITO`")

    def test_fixture_verdict_records_regression(self) -> None:
        text = fixture("delivery-verdict-regression.md")
        self.assertTrue(text, "fixture ausente")
        self.assertEqual([], verdict_problems(text))
        self.assertEqual("CORREÇÕES SOLICITADAS", verdict_fields(text)["Veredito"])
        self.assertIn("CORREÇÃO NECESSÁRIA", text)
        self.assertRegex(text, r"(?i)regress")


HANDOFF = Path("deco/skills/review-handoff/SKILL.md")
HANDOFF_FIXTURES = Path("deco/fixtures/review-handoff")
ACTIVE = {"RASCUNHO", "PRONTO PARA REVISÃO", "EM REVISÃO", "CORREÇÕES SOLICITADAS", "PRONTO PARA RECONFERÊNCIA"}
CLOSED = {"APROVADO", "REPROVADO", "ENCERRADA SEM APROVAÇÃO"}


def round_state(round_dir: Path) -> str:
    state = round_dir / "estado.md"
    values = verdict_fields(state.read_text(encoding="utf-8")) if state.is_file() else {}
    return values.get("Estado", "")


ROUND_NAME = re.compile(r"(?P<gate>[a-z]+(?:-[a-z]+)*)-(?P<date>\d{4}-\d{2}-\d{2})(?:-r(?P<n>0[2-9]|[1-9]\d))?")
ARTIFACTS_BY_STATE = {
    "RASCUNHO": (),
    "PRONTO PARA REVISÃO": ("review-request.md",),
    "EM REVISÃO": ("review-request.md",),
    "CORREÇÕES SOLICITADAS": ("review-request.md", "review-verdict.md"),
    "PRONTO PARA RECONFERÊNCIA": ("review-request.md", "review-verdict.md", "correction-report.md"),
    "APROVADO": ("review-request.md", "review-verdict.md"),
    "REPROVADO": ("review-request.md", "review-verdict.md"),
    "ENCERRADA SEM APROVAÇÃO": (),
}


def current_problems(reviews: Path, gate: str) -> list[str]:
    """Aplica o layout aprovado no adendo de 29/09/2026 ao Plan Gate (fail-closed)."""
    rounds = sorted(path for path in reviews.iterdir() if path.is_dir() and not path.is_symlink())
    problems = []
    for path in rounds:
        state = round_state(path)
        if state not in ARTIFACTS_BY_STATE:
            problems.append(f"estado desconhecido: {path.name}")
            continue
        problems += [f"artefato ausente: {path.name}/{name}" for name in ARTIFACTS_BY_STATE[state]
                     if not (path / name).is_file()]
    if len([path for path in rounds if round_state(path) in ACTIVE]) > 1:
        problems.append("mais de uma rodada ativa")
    pointer = reviews / "CURRENT"
    if pointer.is_symlink():
        return problems + ["CURRENT é link simbólico"]
    if not pointer.is_file():
        return problems + ["CURRENT ausente"]
    try:
        raw = pointer.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return problems + ["CURRENT não é UTF-8"]
    useful = [line for line in raw.splitlines() if line.strip()]
    if len(useful) != 1:
        return problems + ["CURRENT sem exatamente uma linha útil"]
    name = useful[0]
    target = reviews / name
    if name.startswith("/") or Path(name).is_absolute():
        problems.append("CURRENT com caminho absoluto")
    elif ".." in re.split(r"[\\/]", name):
        problems.append("CURRENT com ..")
    elif "/" in name or "\\" in name:
        problems.append("CURRENT com separador de caminho")
    elif target.is_symlink():
        problems.append("destino de CURRENT é link simbólico")
    elif not target.exists():
        problems.append("CURRENT quebrado")
    elif not target.is_dir():
        problems.append("destino de CURRENT não é pasta")
    elif not (match := ROUND_NAME.fullmatch(name)) or match.group("gate") != gate:
        problems.append("rodada incompatível com o gate esperado")
    elif round_state(target) in CLOSED:
        problems.append("CURRENT aponta rodada encerrada")
    return problems


def next_round_name(reviews: Path, gate: str, date: str) -> str:
    """Nome da próxima rodada do gate no dia: base, depois -r02, -r03 etc., sem sobrescrever."""
    base = f"{gate}-{date}"
    taken = [path.name for path in reviews.iterdir()
             if path.name == base or re.fullmatch(re.escape(base) + r"-r\d{2}", path.name)]
    if not taken:
        return base
    numbers = [int(name.rsplit("-r", 1)[1]) for name in taken if name != base]
    return f"{base}-r{max(numbers, default=1) + 1:02d}"


WRITE_UNLOCK = HANDOFF_FIXTURES / "write-unlock"


def write_unlock_problems(case: Path) -> list[str]:
    """Regra de AC-035/FR-002: escrita de risco alto só após o plano revisado e aprovado."""
    unit = case / "unidade.md"
    risk = verdict_fields(unit.read_text(encoding="utf-8")).get("Risco", "") if unit.is_file() else ""
    if risk not in {"ALTO", "CRÍTICO"}:
        return ["risco ausente ou fora de alto e crítico"]
    plan = case / "plano"
    state = round_state(plan) if plan.is_dir() else ""
    verdict_file = plan / "review-verdict.md"
    verdict = verdict_fields(verdict_file.read_text(encoding="utf-8")).get("Veredito", "") if verdict_file.is_file() else ""
    problems = []
    if not state:
        problems.append("revisão do plano ausente")
    elif not verdict:
        problems.append("plano sem revisão concluída")
    elif (state == "APROVADO") != (verdict == "APROVADO"):
        problems.append("evidência contraditória")
    elif state != "APROVADO":
        problems.append("plano não aprovado")
    if risk == "CRÍTICO":
        gate = case / "gate-humano.md"
        values = verdict_fields(gate.read_text(encoding="utf-8")) if gate.is_file() else {}
        if not gate.is_file():
            problems.append("gate humano ausente")
        elif values.get("Decisão humana") != "APROVADA" or not values.get("Pessoa") or not values.get("Data"):
            problems.append("gate humano incompleto")
    return problems


class ReviewHandoffTest(unittest.TestCase):
    """T011: criação, validação, correção e encerramento de rodada."""

    def test_skill_exists_with_canonical_name(self) -> None:
        self.assertEqual("review-handoff", frontmatter_name(HANDOFF))

    def test_round_cycle_has_decisions_for_each_state(self) -> None:
        text = section(HANDOFF, "Ciclo da rodada")
        self.assertRegex(text, TABLE)
        for state in sorted(ACTIVE | {"APROVADO", "REPROVADO"}):
            with self.subTest(state=state):
                self.assertIn(f"`{state}`", text)
        self.assertRegex(text, r"(?i)exatamente uma rodada ativa")
        self.assertRegex(text, r"(?i)rodada conclu[ií]da.{0,80}imut[aá]vel")

    def test_current_is_distinct_from_session_current(self) -> None:
        text = section(HANDOFF, "CURRENT e SESSION_CURRENT")
        self.assertRegex(text, TABLE)
        self.assertRegex(text, r"(?s)`CURRENT`.{0,160}review-handoff")
        self.assertRegex(text, r"(?s)`SESSION_CURRENT`.{0,160}Session Guardian")
        self.assertRegex(text, r"(?i)n[aã]o (?:se )?substitu")
        self.assertRegex(text, r"reviews/CURRENT")

    def test_pointer_fixtures_follow_documented_rule(self) -> None:
        cases = {
            "valid": ("delivery", []),
            "material-change": ("plan", []),
            "collision": ("plan", []),
            "broken": ("plan", ["CURRENT quebrado"]),
            "ambiguous": ("plan", ["mais de uma rodada ativa"]),
            "closed-target": ("plan", ["CURRENT aponta rodada encerrada"]),
            "absolute": ("plan", ["CURRENT com caminho absoluto"]),
            "dotdot": ("plan", ["CURRENT com .."]),
            "separator": ("plan", ["CURRENT com separador de caminho"]),
            "symlink-current": ("plan", ["CURRENT é link simbólico"]),
            "symlink-target": ("plan", ["destino de CURRENT é link simbólico"]),
            "file-target": ("plan", ["destino de CURRENT não é pasta"]),
            "multiline": ("plan", ["CURRENT sem exatamente uma linha útil"]),
            "wrong-gate": ("plan", ["rodada incompatível com o gate esperado"]),
            "missing-artifact": ("plan", ["artefato ausente: plan-2026-01-10/review-request.md"]),
        }
        for name, (gate, expected) in cases.items():
            with self.subTest(fixture=name):
                reviews = ROOT / HANDOFF_FIXTURES / name / "reviews"
                self.assertTrue(reviews.is_dir(), f"fixture ausente: {name}")
                self.assertEqual(expected, current_problems(reviews, gate))

    def test_same_day_collision_uses_numbered_suffix_without_overwrite(self) -> None:
        reviews = ROOT / HANDOFF_FIXTURES / "collision" / "reviews"
        self.assertEqual("plan-2026-01-10-r03", next_round_name(reviews, "plan", "2026-01-10"))
        self.assertEqual("plan-2026-01-11", next_round_name(reviews, "plan", "2026-01-11"))
        self.assertEqual("delivery-2026-01-10", next_round_name(reviews, "delivery", "2026-01-10"))
        existing = {path.name for path in reviews.iterdir()}
        self.assertNotIn(next_round_name(reviews, "plan", "2026-01-10"), existing)
        self.assertEqual("plan-2026-01-10-r02", (reviews / "CURRENT").read_text(encoding="utf-8").strip())

    def test_skill_documents_approved_layout_and_fail_closed_rules(self) -> None:
        text = section(HANDOFF, "Layout físico da rodada")
        self.assertRegex(text, TABLE)
        self.assertRegex(text, r"adendo de 29/09/2026")
        for rule in (r"caminho absoluto", r"`\.\.`", r"separador", r"link simb[oó]lico", r"inexistente",
                     r"n[aã]o [eé] pasta", r"mais de uma linha [uú]til", r"gate esperado",
                     r"-r02", r"n[aã]o pode ser sobrescrita"):
            with self.subTest(rule=rule):
                self.assertRegex(text, rf"(?i){rule}")

    def test_high_risk_write_requires_reviewed_plan_and_critical_human_gate(self) -> None:
        text = section(HANDOFF, "AC-035")
        self.assertRegex(text, r"(?s)escrita.{0,120}somente depois.{0,120}revis[aã]o do plano.{0,120}`APROVADO`")
        self.assertRegex(text, r"(?s)pedido.{0,80}n[aã]o (?:desbloqueia|basta)")
        self.assertRegex(text, r"(?s)cr[ií]tico.{0,160}gate humano.{0,160}(?:registrad|pessoa)")
        self.assertRegex(text, r"(?s)ausente, incompleta ou contradit[oó]ria.{0,80}bloque")
        cases = {
            "alto-pedido-sem-revisao": ["plano sem revisão concluída"],
            "alto-plano-aprovado": [],
            "alto-plano-correcoes": ["plano não aprovado"],
            "alto-contraditorio": ["evidência contraditória"],
            "critico-sem-gate": ["gate humano ausente"],
            "critico-gate-incompleto": ["gate humano incompleto"],
            "critico-completo": [],
            "risco-ausente": ["risco ausente ou fora de alto e crítico"],
        }
        for name, expected in cases.items():
            with self.subTest(fixture=name):
                case = ROOT / WRITE_UNLOCK / name
                self.assertTrue(case.is_dir(), f"fixture ausente: {name}")
                self.assertEqual(expected, write_unlock_problems(case))

    def test_plan_gate_addendum_is_recorded_without_rewriting_history(self) -> None:
        spec = (ROOT / "deco/specs/0002-governanca-sdd/spec.md").read_text(encoding="utf-8")
        self.assertRegex(spec, r"(?s)Adendo de 29/09/2026.{0,400}reviews/CURRENT.{0,1500}-r02")
        approval = (ROOT / "deco/specs/0002-governanca-sdd/reviews/plan-gate-2026-09-21/plan-gate-approval.md")
        self.assertNotIn("29/09/2026", approval.read_text(encoding="utf-8"))
        self.assertRegex(spec, r"nomes f[ií]sicos e\s+caminhos ser[aã]o definidos somente no Plan Gate")

    def test_material_change_closes_previous_round_without_rewrite(self) -> None:
        reviews = ROOT / HANDOFF_FIXTURES / "material-change" / "reviews"
        states = {path.name: round_state(path) for path in reviews.iterdir() if path.is_dir()}
        self.assertIn("ENCERRADA SEM APROVAÇÃO", states.values())
        closed = next(name for name, state in states.items() if state == "ENCERRADA SEM APROVAÇÃO")
        note = (reviews / closed / "estado.md").read_text(encoding="utf-8")
        self.assertRegex(note, r"MUDANÇA MATERIAL")
        self.assertRegex(note, r"(?i)substitu[ií]da por")
        current = (reviews / "CURRENT").read_text(encoding="utf-8").strip()
        self.assertNotEqual(closed, current)


if __name__ == "__main__":
    unittest.main()
