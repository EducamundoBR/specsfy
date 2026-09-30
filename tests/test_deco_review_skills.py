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

import html
import importlib.util
import re
import shutil
import tempfile
import unicodedata
import unittest
from datetime import date, datetime, timedelta
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


DECLARED = re.compile(r"(?m)^\s*[-*+]\s*\*\*(.+?)\*\*\s*:")


def verdict_fields(text: str) -> dict[str, str]:
    """Campos `- **Nome**: valor`; campo declarado mais de uma vez fica vazio (fail-closed)."""
    declared = [" ".join(name.split()) for name in DECLARED.findall(text)]
    return {name: "" if declared.count(name) > 1 else value for name, value in FIELD.findall(text)}


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
    problems.extend("linha de achado não interpretável: " + line for line in unparsed_finding_lines(text))
    return problems


def normalized(line: str) -> str:
    """NFKC, sem caracteres invisíveis de formatação e com espaços colapsados."""
    line = "".join(char for char in unicodedata.normalize("NFKC", line) if unicodedata.category(char) != "Cf")
    return " ".join(line.split())


LINK = re.compile(r"""!?\[([^\]]*)\](?:\(\s*(?:<[^>]*>|(?:[^()\s]|\([^()\s]*\))*)"""
                  r"""(?:\s+(?:"[^"]*"|'[^']*'|\([^()]*\)))?\s*\)|\[[^\]]*\])""")
TAG = re.compile(r"""<!--.*?-->|<[A-Za-z/!?](?:"[^"]*"|'[^']*'|[^'">])*>""")


def without_markup(line: str) -> str:
    """Links, imagens e colchetes restantes (referência abreviada ou texto literal) reduzidos ao texto
    visível; definições de referência, comentários e tags omitidos."""
    line = LINK.sub(r"\1", re.sub(r"^\s*\[[^\]]+\]:\s*\S.*$", "", line))
    return TAG.sub("", re.sub(r"\[([^\[\]]*)\](?!\()", r"\1", line))


def ambiguous_markup(line: str) -> bool:
    """Fail-closed: link ou tag que não fecha de forma determinável deixa a apresentação indeterminada."""
    rest = without_markup(line)
    return re.search(r"\]\(|<(?:[A-Za-z/!?])", rest) is not None


def rendered(line: str) -> str:
    """Texto como o Markdown o exibe: sem marcação, marcas inline e escapes; entidades decodificadas."""
    return normalized(re.sub(r"[*_`~\\]", "", html.unescape(without_markup(line))))


def table_lines(text: str) -> tuple[list[str], int | None]:
    """Linhas normalizadas e posição do cabeçalho da tabela de achados."""
    lines = [normalized(line) for line in text.splitlines()]
    start = next((index for index, line in enumerate(lines) if line.startswith("| ID ")), None)
    return lines, start


def table_end(lines: list[str], start: int) -> int:
    end = start + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    return end


SEPARATOR = r"\|(?: ?:?-+:? ?\|)+"
FINDINGS_HEADING = re.compile(r"(?i)^#{1,6}\s.*achad")


def cells(line: str) -> list[str]:
    """Células da linha de tabela; `\\|` é pipe literal dentro da célula, não separador."""
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.removeprefix("|").removesuffix("|"))]


def finding_rows(text: str) -> list[list[str]]:
    """Linhas da tabela de achados do modelo e de toda seção posterior de achados."""
    lines, start = table_lines(text)
    if start is None:
        return []
    return [cells(line) for line in lines[start + 1:table_end(lines, start)]
            if not re.fullmatch(SEPARATOR, line)] + other_finding_lines(text)[0]


def unparsed_finding_lines(text: str) -> list[str]:
    """Fail-closed: linha com aparência de achado que não pode ser lida como achado bloqueia."""
    return other_finding_lines(text)[1]


def other_finding_lines(text: str) -> tuple[list[list[str]], list[str]]:
    """Fora da tabela do modelo, nenhum cabeçalho encerra a busca por achados.

    Em seção cujo título fala de achados, cada linha de tabela é achado e qualquer outra linha
    com `|` é não interpretável. Fora dela, tabelas de outras finalidades (como a de condições do
    parecer) são ignoradas quando são tabela válida (cabeçalho seguido de separador, todas as linhas
    com a largura do cabeçalho) cujo cabeçalho não é de achados (`ID` ou `Severidade`). Linha solta
    sem separador, linha de outra largura, tabela com cabeçalho de achados e célula iniciada por
    severidade `P<n>` são não interpretáveis. Na seção da tabela, depois dela,
    vale a regra anterior.
    Achado só existe em tabela: severidade `P<n>` citada em texto, lista ou valor de campo, fora de
    linha idêntica ao modelo de T006, também é não interpretável.
    """
    lines, start = table_lines(text)
    if start is None:
        return [], []
    template = {normalized(line) for line in (ROOT / VERDICT_TEMPLATE).read_text(encoding="utf-8").splitlines()}

    def cites_severity(line: str) -> bool:
        field = re.fullmatch(r"- \*\*.+?\*\*: (.*)", line)
        return line not in template and re.search(r"(?i)\bP\s*\d+\b", rendered(field.group(1) if field else line)) is not None

    end = table_end(lines, start)
    rows, unparsed, in_findings, same_section, foreign_table, width = [], [], False, False, False, 0
    for index, line in enumerate(lines):
        if start <= index < end:
            continue
        same_section = same_section or index == end
        heading = re.match(r"#{1,6}(?:\s|$)", line) is not None
        if heading:
            in_findings, same_section = FINDINGS_HEADING.match(line) is not None, False
        if line not in template and ambiguous_markup(line):
            unparsed.append(line)
            continue
        if index and re.search(r"(?i)\bP$", rendered(lines[index - 1])) and re.match(r"\d", rendered(line)):
            unparsed.append(line)
            continue
        if "|" not in line:
            if cites_severity(line):
                unparsed.append(line)
            continue
        in_table = line.startswith("|")
        if in_table and (index == 0 or not lines[index - 1].startswith("|")):
            header, width = [cell.lower() for cell in cells(line)], len(cells(line))
            foreign_table = (index + 1 < len(lines) and re.fullmatch(SEPARATOR, lines[index + 1]) is not None
                             and header[0] != "id" and not any("severidade" in cell for cell in header))
        shaped = ((in_table and (not foreign_table or len(cells(line)) != width)) or any(re.match(r"(?i)P\s*\d", rendered(cell)) for cell in cells(line))
                  or cites_severity(line))
        if in_findings and not same_section and not heading and line.startswith("|"):
            if not line.startswith("| ID ") and not re.fullmatch(SEPARATOR, line):
                rows.append(cells(line))
        elif same_section or in_findings or shaped:
            unparsed.append(line)
    return rows, unparsed


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


ROUND_NAME = re.compile(r"(?P<gate>[a-z]+(?:-[a-z]+)*)-(?P<date>\d{4}-\d{2}-\d{2})(?:-r(?P<n>0[2-9]|[1-9]\d+))?")
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


def t006_fields_filled(name: str, text: str) -> bool:
    """Artefato completo: todo campo do modelo de T006 presente e preenchido (`NÃO REGISTRADO` persiste)."""
    rounds = t006_rounds_module()
    template = {"review-request.md": rounds.REVIEW_REQUEST, "review-verdict.md": rounds.REVIEW_VERDICT,
                "correction-report.md": rounds.CORRECTION_REPORT}[name]
    values = {field: " ".join(value.split()) for field, value in FIELD.findall(text)}
    return all(values.get(field) not in {None, "", "<preencher>"} for field in rounds.template_fields(template))


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
        problems += [f"artefato fora do modelo de T006: {path.name}/{name}" for name in ARTIFACTS_BY_STATE[state]
                     if (path / name).is_file() and not t006_fields_filled(name, (path / name).read_text(encoding="utf-8"))]
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
             if path.name == base or re.fullmatch(re.escape(base) + r"-r\d{2,}", path.name)]
    if not taken:
        return base
    numbers = [int(name.rsplit("-r", 1)[1]) for name in taken if name != base]
    return f"{base}-r{max(numbers, default=1) + 1:02d}"


WRITE_UNLOCK = HANDOFF_FIXTURES / "write-unlock"


def t006_rounds_module():
    """Carrega o validador de T006 do próprio módulo de testes, sem duplicar a regra."""
    spec = importlib.util.spec_from_file_location(
        "deco_governance_rounds_t006", ROOT / "tests/test_deco_governance_rounds.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_unlock_problems(case: Path) -> list[str]:
    """Regra de AC-035/FR-002: escrita de risco alto só após o plano revisado e aprovado."""
    unit = case / "unidade.md"
    unit_fields = verdict_fields(unit.read_text(encoding="utf-8")) if unit.is_file() else {}
    risk = unit_fields.get("Risco", "")
    if risk not in {"ALTO", "CRÍTICO"}:
        return ["risco ausente ou fora de alto e crítico"]
    plan = case / "plano"
    state = round_state(plan) if plan.is_dir() else ""
    request_file = plan / "review-request.md"
    request_text = request_file.read_text(encoding="utf-8") if request_file.is_file() else ""
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
    else:
        rounds = t006_rounds_module()
        observed_file = case / "base-observada.md"
        observed = verdict_fields(observed_file.read_text(encoding="utf-8")) if observed_file.is_file() else {}
        verdict_text = verdict_file.read_text(encoding="utf-8")
        checks = [
            rounds.validate_round_artifact(
                template, text, observed_head=observed.get("HEAD", ""),
                observed_branch=observed.get("Branch", ""), request=request_text,
            )
            for template, text in ((rounds.REVIEW_REQUEST, request_text), (rounds.REVIEW_VERDICT, verdict_text))
        ]
        requested, reviewed = verdict_fields(request_text), verdict_fields(verdict_text)
        same_unit = (
            requested.get("Unidade") == unit_fields.get("Unidade") == reviewed.get("Unidade")
            and requested.get("Risco", "").upper() == risk
            and re.fullmatch(r"(?i)plan(?: gate)?", requested.get("Gate", "")) is not None
        )
        if not observed or any(checks) or verdict_problems(verdict_text):
            problems.append("artefatos do plano fora do contrato de T006")
        elif not same_unit:
            problems.append("revisão do plano não corresponde à unidade")
        elif any(severity in {"P0", "P1"} for severity, _ in findings(verdict_text)):
            problems.append("Verdict APROVADO com achado P0 ou P1")
        elif any(row[1] == "P2" and not p2_accepted(row[0], reviewed.get("Condições", ""))
                 for row in finding_rows(verdict_text)):
            problems.append("Verdict APROVADO com achado P2 sem correção ou justificativa aceita")
    if risk == "CRÍTICO":
        gate = case / "gate-humano.md"
        values = verdict_fields(gate.read_text(encoding="utf-8")) if gate.is_file() else {}
        person = " ".join(values.get("Pessoa", "").split())
        if not gate.is_file():
            problems.append("gate humano ausente")
        elif values.get("Decisão humana") != "APROVADA" or not person or not values.get("Data"):
            problems.append("gate humano incompleto")
        elif person.upper().startswith(("NÃO REGISTRADO", "<PREENCHER>")):
            problems.append("gate humano sem pessoa registrada")
        elif (decided := calendar_date(" ".join(values["Data"].split()))) is None:
            problems.append("gate humano sem data válida")
        elif decided > date.today():
            problems.append("gate humano com data futura")
    return problems


def p2_accepted(finding_id: str, conditions: str) -> bool:
    """Aceite inequívoco: toda cláusula de `Condições` que cita o ID é exatamente `<ID>: justificativa aceita`."""
    cited = [clause.strip() for clause in normalized(conditions).split(";")
             if re.search(rf"(?<![\w-]){re.escape(finding_id)}(?![\w-])", clause)]
    return bool(cited) and all(
        re.fullmatch(rf"(?i){re.escape(finding_id)}\s*[:—–-]?\s*justificativa aceita\.?", clause) for clause in cited)


def calendar_date(value: str) -> date | None:
    """Data do gate humano: somente data de calendário real, em ISO ou DD/MM/AAAA."""
    for pattern in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, pattern).date()
        except ValueError:
            pass
    return None


def result_request_problems(case: Path) -> list[str]:
    """AC-035: o resultado de risco alto tem Review Request próprio, gravado depois da escrita."""
    request = case / "resultado" / "review-request.md"
    if not request.is_file():
        return ["resultado sem Review Request próprio"]
    plan = case / "plano" / "review-request.md"
    text = request.read_text(encoding="utf-8")
    result, planned = verdict_fields(text), verdict_fields(plan.read_text(encoding="utf-8"))
    unit = verdict_fields((case / "unidade.md").read_text(encoding="utf-8"))
    if (request.is_symlink() or request.resolve() == plan.resolve() or text == plan.read_text(encoding="utf-8")
            or re.fullmatch(r"(?i)plan(?: gate)?", result.get("Gate", "")) or result.get("HEAD") == planned.get("HEAD")):
        return ["um único Review Request para plano e resultado"]
    if result.get("Unidade") != unit.get("Unidade"):
        return ["pedido do resultado de outra unidade"]
    if normalized(result.get("Risco", "")).upper() != normalized(unit.get("Risco", "")).upper():
        return ["pedido do resultado com risco divergente da unidade"]
    if normalized(result.get("Risco", "")).upper() != normalized(planned.get("Risco", "")).upper():
        return ["pedido do resultado com risco divergente do plano"]
    if not re.fullmatch(r"(?i)delivery(?: gate)?", result.get("Gate", "")):
        return ["pedido do resultado fora do Delivery Gate"]
    if result.get("Base") != planned.get("HEAD"):
        return ["pedido do resultado não parte do HEAD revisado do plano"]
    observed_file = case / "resultado" / "base-observada.md"
    observed = verdict_fields(observed_file.read_text(encoding="utf-8")) if observed_file.is_file() else {}
    rounds = t006_rounds_module()
    if not observed or rounds.validate_round_artifact(
            rounds.REVIEW_REQUEST, text, observed_head=observed.get("HEAD", ""),
            observed_branch=observed.get("Branch", ""), request=text):
        return ["pedido do resultado fora do contrato de T006"]
    return []


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

    def test_required_artifacts_follow_t006_fields(self) -> None:
        cases = {
            "pedido só com placeholder": ("delivery-2026-01-20/review-request.md",
                                          lambda text: "# review-request.md\n\nConteúdo completo nos modelos de T006.\n"),
            "campo do pedido ausente": ("delivery-2026-01-20/review-request.md",
                                        lambda text: re.sub(r"(?m)^- \*\*Testes\*\*: .*\n", "", text)),
            "campo do parecer em branco": ("plan-2026-01-10/review-verdict.md",
                                           lambda text: re.sub(r"(?m)^(- \*\*Session ID\*\*:) .*$", r"\1 <preencher>", text)),
        }
        for name, (artifact, change) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                reviews = Path(tmp) / "reviews"
                shutil.copytree(ROOT / HANDOFF_FIXTURES / "valid" / "reviews", reviews)
                self.assertEqual([], current_problems(reviews, "delivery"))
                path = reviews / artifact
                path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")
                self.assertEqual([f"artefato fora do modelo de T006: {artifact}"], current_problems(reviews, "delivery"))

    def test_round_suffix_beyond_two_digits_is_never_reused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            reviews = Path(tmp)
            for name in ("plan-2026-01-10", "plan-2026-01-10-r02", "plan-2026-01-10-r99"):
                (reviews / name).mkdir()
            self.assertEqual("plan-2026-01-10-r100", next_round_name(reviews, "plan", "2026-01-10"))
            (reviews / "plan-2026-01-10-r100").mkdir()
            self.assertEqual("plan-2026-01-10-r101", next_round_name(reviews, "plan", "2026-01-10"))
            (reviews / "plan-2026-01-10-r100" / "estado.md").write_text("- **Estado**: RASCUNHO\n", encoding="utf-8")
            for name in ("plan-2026-01-10", "plan-2026-01-10-r02", "plan-2026-01-10-r99"):
                (reviews / name / "estado.md").write_text("- **Estado**: ENCERRADA SEM APROVAÇÃO\n", encoding="utf-8")
            (reviews / "CURRENT").write_text("plan-2026-01-10-r100\n", encoding="utf-8")
            self.assertEqual([], current_problems(reviews, "plan"))

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
            "alto-artefatos-incompletos": ["artefatos do plano fora do contrato de T006"],
            "alto-verdict-nao-registrado": ["artefatos do plano fora do contrato de T006"],
            "alto-mesma-sessao": ["artefatos do plano fora do contrato de T006"],
            "alto-branch-divergente": ["artefatos do plano fora do contrato de T006"],
            "alto-unidade-divergente": ["revisão do plano não corresponde à unidade"],
            "alto-risco-divergente": ["revisão do plano não corresponde à unidade"],
            "alto-gate-divergente": ["revisão do plano não corresponde à unidade"],
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

    def test_approved_verdict_with_blocking_finding_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "alto-aprovado-com-p1"
        self.assertTrue(case.is_dir(), "fixture ausente: alto-aprovado-com-p1")
        self.assertEqual(["Verdict APROVADO com achado P0 ou P1"], write_unlock_problems(case))

    def test_critical_gate_without_registered_person_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "critico-gate-sem-pessoa"
        self.assertTrue(case.is_dir(), "fixture ausente: critico-gate-sem-pessoa")
        self.assertEqual(["gate humano sem pessoa registrada"], write_unlock_problems(case))

    def test_indented_blocking_finding_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "alto-aprovado-com-p1-indentado"
        self.assertTrue(case.is_dir(), "fixture ausente: alto-aprovado-com-p1-indentado")
        self.assertEqual(["Verdict APROVADO com achado P0 ou P1"], write_unlock_problems(case))
        approved = (ROOT / WRITE_UNLOCK / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        self.assertEqual([("P-1", "P3")], [(row[0], row[1]) for row in finding_rows(approved)])
        unreadable = approved + "P-2 | P1 | spec §14 T004 | escrita indevida\n"
        self.assertIn("linha de achado não interpretável: P-2 | P1 | spec §14 T004 | escrita indevida",
                      verdict_problems(unreadable))

    def test_critical_gate_with_spaced_unregistered_person_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "critico-gate-pessoa-espacada"
        self.assertTrue(case.is_dir(), "fixture ausente: critico-gate-pessoa-espacada")
        self.assertEqual(["gate humano sem pessoa registrada"], write_unlock_problems(case))
        self.assertEqual([], write_unlock_problems(ROOT / WRITE_UNLOCK / "critico-completo"))

    def test_blocking_finding_after_new_heading_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "alto-aprovado-com-p1-apos-cabecalho"
        self.assertTrue(case.is_dir(), "fixture ausente: alto-aprovado-com-p1-apos-cabecalho")
        self.assertEqual(["Verdict APROVADO com achado P0 ou P1"], write_unlock_problems(case))
        hidden = (case / "plano/review-verdict.md").read_text(encoding="utf-8")
        self.assertEqual([("P-1", "P3"), ("P-2", "P1")], [(row[0], row[1]) for row in finding_rows(hidden)])
        approved = (ROOT / WRITE_UNLOCK / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        blocked = {
            "achado malformado em seção de achados": "\n## Achados complementares\n\nP-2 | P1 | fonte | impacto\n",
            "achado em seção sem título de achados": "\n## Notas do revisor\n\n| P-2 | P1 | fonte | impacto | correção |\n",
        }
        for name, tail in blocked.items():
            with self.subTest(case=name):
                self.assertTrue([problem for problem in verdict_problems(approved + tail)
                                 if problem.startswith("linha de achado não interpretável")])
        template = (ROOT / VERDICT_TEMPLATE).read_text(encoding="utf-8")
        accepted = {
            "P3 depois de novo cabeçalho": ("\n## Achados complementares\n\n| P-2 | P3 | fonte | impacto | correção |\n",
                                            ["P3", "P3"]),
            "P2 depois de novo cabeçalho": ("\n## Achados complementares\n\n| ID | Severidade P0–P3 | Fonte | Impacto | Correção |\n"
                                            "| --- | --- | --- | --- | --- |\n| P-2 | P2 | fonte | impacto | correção |\n",
                                            ["P3", "P2"]),
            "texto e tabela do parecer": ("\n## Parecer e encaminhamento\n\n" + template[template.index("Valores permitidos"):],
                                          ["P3"]),
        }
        for name, (tail, severities) in accepted.items():
            with self.subTest(case=name):
                self.assertEqual([], verdict_problems(approved + tail))
                self.assertEqual(severities, [severity for severity, _ in findings(approved + tail)])
        for name, expected in (("alto-aprovado-com-p1-indentado", "Verdict APROVADO com achado P0 ou P1"),
                               ("alto-verdict-sessao-espacada", "artefatos do plano fora do contrato de T006"),
                               ("critico-gate-pessoa-espacada", "gate humano sem pessoa registrada")):
            with self.subTest(ciclo7=name):
                self.assertEqual([expected], write_unlock_problems(ROOT / WRITE_UNLOCK / name))

    def test_critical_gate_without_valid_date_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "critico-gate-data-nao-registrada"
        self.assertTrue(case.is_dir(), "fixture ausente: critico-gate-data-nao-registrada")
        self.assertEqual(["gate humano sem data válida"], write_unlock_problems(case))
        complete = ROOT / WRITE_UNLOCK / "critico-completo"
        gate = (complete / "gate-humano.md").read_text(encoding="utf-8")
        for value in ("  NÃO REGISTRADO", "<preencher>", "2026-13-45", "ontem", "2026-01-10 talvez"):
            with self.subTest(data=value), tempfile.TemporaryDirectory() as tmp:
                copy = Path(tmp) / "caso"
                shutil.copytree(complete, copy)
                (copy / "gate-humano.md").write_text(gate.replace("2026-01-10", value), encoding="utf-8")
                self.assertEqual(["gate humano sem data válida"], write_unlock_problems(copy))
        self.assertEqual([], write_unlock_problems(complete))

    def test_high_risk_result_needs_its_own_request_after_the_write(self) -> None:
        text = section(HANDOFF, "AC-035")
        self.assertRegex(text, r"(?m)^\| Resultado de risco alto sem Review Request próprio depois da escrita \| Recusar o fechamento")
        self.assertRegex(text, r"(?m)^\| Um único Review Request cobrindo plano e resultado \| Recusar; separar em dois artefatos")
        source = ROOT / WRITE_UNLOCK / "alto-plano-aprovado"
        plan = (source / "plano/review-request.md").read_text(encoding="utf-8")
        result = (plan.replace("- **Gate**: Plan", "- **Gate**: Delivery")
                  .replace("- **HEAD**: " + "a" * 40, "- **HEAD**: " + "c" * 40)
                  .replace("- **Base**: " + "b" * 40, "- **Base**: " + "a" * 40))
        observed = "- **Branch**: fixture/rodada\n- **HEAD**: " + "c" * 40 + "\n"
        contract = ["pedido do resultado fora do contrato de T006"]
        cases = {
            "pedido próprio do resultado": (result, observed, []),
            "sem pedido do resultado": (None, observed, ["resultado sem Review Request próprio"]),
            "cópia do pedido do plano": (plan, observed, ["um único Review Request para plano e resultado"]),
            "link para o pedido do plano": ("link", observed, ["um único Review Request para plano e resultado"]),
            "mesmo HEAD do plano": (result.replace("c" * 40, "a" * 40), observed.replace("c" * 40, "a" * 40),
                                    ["um único Review Request para plano e resultado"]),
            "outra unidade": (result.replace("SPEC-9999 — plano da página de boas-vindas", "SPEC-9998 — outra unidade"),
                              observed, ["pedido do resultado de outra unidade"]),
            "risco rebaixado": (result.replace("- **Risco**: alto", "- **Risco**: baixo"), observed,
                                ["pedido do resultado com risco divergente da unidade"]),
            "risco ausente": (result.replace("- **Risco**: alto\n", ""), observed,
                              ["pedido do resultado com risco divergente da unidade"]),
            "gate de definição": (result.replace("- **Gate**: Delivery", "- **Gate**: Definition"), observed,
                                  ["pedido do resultado fora do Delivery Gate"]),
            "base anterior ao plano": (result.replace("- **Base**: " + "a" * 40, "- **Base**: " + "b" * 40), observed,
                                       ["pedido do resultado não parte do HEAD revisado do plano"]),
            "branch divergente": (result.replace("- **Branch**: fixture/rodada", "- **Branch**: outra/branch"),
                                  observed, contract),
            "HEAD arbitrário": (result.replace("c" * 40, "d" * 40), observed, contract),
            "sem base observada": (result, None, contract),
            "campo em branco": (re.sub(r"(?m)^(- \*\*Testes\*\*:) .*$", r"\1 <preencher>", result), observed, contract),
        }
        self.assertNotEqual(plan, result)
        for name, (content, base, expected) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                case = Path(tmp) / "caso"
                shutil.copytree(source, case)
                if content is not None:
                    (case / "resultado").mkdir()
                    request = case / "resultado/review-request.md"
                    if content == "link":
                        request.symlink_to(case / "plano/review-request.md")
                    else:
                        request.write_text(content, encoding="utf-8")
                    if base is not None:
                        (case / "resultado/base-observada.md").write_text(base, encoding="utf-8")
                self.assertEqual(expected, result_request_problems(case))
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / "caso"
            shutil.copytree(source, case)
            unit = case / "unidade.md"
            unit.write_text(unit.read_text(encoding="utf-8").replace("- **Risco**: ALTO", "- **Risco**: CRÍTICO"),
                            encoding="utf-8")
            (case / "resultado").mkdir()
            (case / "resultado/review-request.md").write_text(
                result.replace("- **Risco**: alto", "- **Risco**: crítico"), encoding="utf-8")
            (case / "resultado/base-observada.md").write_text(observed, encoding="utf-8")
            self.assertEqual(["pedido do resultado com risco divergente do plano"], result_request_problems(case))

    def test_approved_verdict_with_untreated_p2_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "alto-aprovado-com-p2-sem-condicao"
        self.assertTrue(case.is_dir(), "fixture ausente: alto-aprovado-com-p2-sem-condicao")
        self.assertEqual(["Verdict APROVADO com achado P2 sem correção ou justificativa aceita"],
                         write_unlock_problems(case))
        verdict = (case / "plano/review-verdict.md").read_text(encoding="utf-8")
        blocked = ["Verdict APROVADO com achado P2 sem correção ou justificativa aceita"]
        conditions = {
            "justificativa aceita": ("P-2: justificativa aceita; rollback coberto em T013", []),
            "justificativa aceita sem pontuação": ("P-2 justificativa aceita", []),
            "aceite condicionado a decisão futura": ("P-2: justificativa aceita somente após aprovação humana", blocked),
            "aceite com ressalva": ("P-2: justificativa aceita, exceto rollback", blocked),
            "aceite reaberto em outra cláusula": ("P-2: justificativa aceita; P-2 reaberto pelo decisor", blocked),
            "aceite seguido de negação": ("P-2: justificativa aceita? não", blocked),
            "correção pendente": ("corrigir P-2 antes da escrita", blocked),
            "ID citado sem aceite": ("P-2 em análise; justificativa aceita para outro ponto", blocked),
            "aceite de outro achado": ("P-20: justificativa aceita", blocked),
            "aceite negado": ("P-2: justificativa não aceita", blocked),
        }
        for name, (condition, expected) in conditions.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                accepted = Path(tmp) / "caso"
                shutil.copytree(case, accepted)
                (accepted / "plano/review-verdict.md").write_text(
                    verdict.replace("- **Condições**: nenhuma", f"- **Condições**: {condition}"), encoding="utf-8")
                self.assertEqual(expected, write_unlock_problems(accepted))

    def test_critical_gate_dated_after_the_write_keeps_write_locked(self) -> None:
        complete = ROOT / WRITE_UNLOCK / "critico-completo"
        gate = (complete / "gate-humano.md").read_text(encoding="utf-8")
        today = date.today()
        cases = {
            "2099-01-01": ["gate humano com data futura"],
            (today + timedelta(days=1)).isoformat(): ["gate humano com data futura"],
            (today + timedelta(days=1)).strftime("%d/%m/%Y"): ["gate humano com data futura"],
            today.isoformat(): [],
        }
        for value, expected in cases.items():
            with self.subTest(data=value), tempfile.TemporaryDirectory() as tmp:
                case = Path(tmp) / "caso"
                shutil.copytree(complete, case)
                (case / "gate-humano.md").write_text(gate.replace("2026-01-10", value), encoding="utf-8")
                self.assertEqual(expected, write_unlock_problems(case))

    def test_blocking_finding_declared_outside_table_keeps_write_locked(self) -> None:
        case = ROOT / WRITE_UNLOCK / "alto-aprovado-com-p1-em-texto"
        self.assertTrue(case.is_dir(), "fixture ausente: alto-aprovado-com-p1-em-texto")
        self.assertEqual(["artefatos do plano fora do contrato de T006"], write_unlock_problems(case))
        approved = (ROOT / WRITE_UNLOCK / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        blocked = {
            "campo Achados P0-P3": approved.replace("ver tabela, em ordem de severidade", "P1 em T004; demais na tabela"),
            "texto após novo cabeçalho": approved + "\n## Achados complementares\n\nP-2 P1 tarefa sem critério\n",
            "lista em outra seção": approved + "\n## Notas do revisor\n\n- P1: tarefa T004 sem critério\n",
            "tabulação": approved + "\n\tp0 — escrita sem plano\n",
        }
        for name, text in blocked.items():
            with self.subTest(case=name):
                self.assertTrue([problem for problem in verdict_problems(text)
                                 if problem.startswith("linha de achado não interpretável")])
        template = (ROOT / VERDICT_TEMPLATE).read_text(encoding="utf-8")
        prose = template[template.index("Usar `Nenhum`"):template.index("## Parecer")]
        self.assertEqual([], verdict_problems(approved + "\n" + prose))

    def test_duplicated_fields_keep_write_locked(self) -> None:
        source = ROOT / WRITE_UNLOCK / "critico-completo"
        cases = {
            "veredito do plano": ("plano/review-verdict.md", "- **Veredito**: APROVADO",
                                  "- **Veredito**: CORREÇÕES SOLICITADAS\n- **Veredito**: APROVADO"),
            "estado da rodada": ("plano/estado.md", "- **Estado**: APROVADO",
                                 "- **Estado**: CORREÇÕES SOLICITADAS\n- **Estado**: APROVADO"),
            "risco da unidade": ("unidade.md", "- **Risco**: CRÍTICO", "- **Risco**: BAIXO\n- **Risco**: CRÍTICO"),
            "decisão humana": ("gate-humano.md", "- **Decisão humana**: APROVADA",
                               "- **Decisão humana**: REPROVADA\n  - **Decisão humana**: APROVADA"),
        }
        self.assertEqual([], write_unlock_problems(source))
        for name, (artifact, old, new) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                case = Path(tmp) / "caso"
                shutil.copytree(source, case)
                text = (case / artifact).read_text(encoding="utf-8")
                self.assertIn(old, text)
                (case / artifact).write_text(text.replace(old, new), encoding="utf-8")
                self.assertTrue(write_unlock_problems(case), "campo duplicado liberou a escrita")

    def test_foreign_tables_are_told_apart_from_findings_by_header(self) -> None:
        approved = (ROOT / WRITE_UNLOCK / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        tests_table = ("\n## Testes\n\n| Comando | Resultado | Duração | Ambiente | Observação |\n"
                       "| --- | --- | --- | --- | --- |\n| python3 -B -m unittest | 67 OK | 0,4 s | local | sem rede |\n"
                       "| make verify-version | 0.22.2 | 1 s | local | sem rede |\n")
        self.assertEqual([], verdict_problems(approved + tests_table))
        self.assertEqual(["P3"], [severity for severity, _ in findings(approved + tests_table)])
        escaped = "\n## Regras\n\n| Regra | Resultado |\n| --- | --- |\n| A \\| B | ok |\n"
        self.assertEqual([], verdict_problems(approved + escaped))
        extra = "\n## Achados complementares\n\n| P-2 | P3 | spec §3: A \\| B | leitura | reescrever |\n"
        self.assertEqual([], verdict_problems(approved + extra))
        self.assertEqual([("P-2", "P3", "spec §3: A \\| B")],
                         [(row[0], row[1], row[2]) for row in finding_rows(approved + extra)][1:])
        blocked = {
            "tabela com cabeçalho de achados": "\n## Evidências\n\n| ID | Severidade P0–P3 | Fonte | Impacto | Correção |\n"
                                               "| --- | --- | --- | --- | --- |\n| E-1 | alta | fonte | impacto | correção |\n",
            "coluna de severidade": "\n## Evidências\n\n| Item | Severidade |\n| --- | --- |\n| E-1 | alta |\n",
            "linha solta sem separador": "\n## Notas do revisor\n\n| E-2 | alta | fonte | impacto | correção |\n",
            "severidade em tabela alheia": tests_table + "| teste extra | P1 aberto | 1 s | local | sem rede |\n",
            "linha mais larga que o cabeçalho": "\n## Testes\n\n| Teste | Resultado |\n| --- | --- |\n"
                                                "| E-1 | alta | fonte | impacto | correção |\n",
            "linha mais estreita que o cabeçalho": "\n## Testes\n\n| Teste | Resultado |\n| --- | --- |\n| E-1 |\n",
            "separador de outra largura": "\n## Testes\n\n| Teste | Resultado |\n| --- | --- | --- |\n| contrato | ok |\n",
        }
        for name, tail in blocked.items():
            with self.subTest(case=name):
                self.assertTrue([problem for problem in verdict_problems(approved + tail)
                                 if problem.startswith("linha de achado não interpretável")])

    def test_severity_hidden_by_markup_keeps_write_locked(self) -> None:
        approved = (ROOT / WRITE_UNLOCK / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        for name, severity in {"entidade decimal": "&#80;1", "entidade hexadecimal": "&#x50;1",
                               "entidades nos dois caracteres": "&#80;&#49;", "negrito": "**P**1",
                               "comentário HTML": "P<!-- x -->1", "tag HTML": "P<span>1</span>",
                               "código inline": "`P1`", "escape de barra": "P\\1",
                               "quebra de linha suave": "P\n1", "link": "[P](#)1", "imagem": "![P](x.png)1",
                               "link por referência": "[P][r]1", "link com parênteses": "[P](docs/item(v2).md)1",
                               "atributo com >": 'P<span title=">">1</span>', "atributo com > em aspas simples":
                               "P<span title='>'>1</span>", "link de apresentação indeterminada": "[P](a(b(c)))1",
                               "tag sem fechamento": "P<span 1",
                               "referência abreviada": "[P]1", "referência recolhida": "[P][]1"}.items():
            for tail in (f"\n## Achados complementares\n\n{severity}: contrato crítico aberto\n",
                         f"\n## Testes\n\n| Teste | Resultado |\n| --- | --- |\n| contrato | {severity} aberto |\n"):
                with self.subTest(case=name, tail=tail), tempfile.TemporaryDirectory() as tmp:
                    self.assertTrue([problem for problem in verdict_problems(approved + tail)
                                     if problem.startswith("linha de achado não interpretável")])
                    case = Path(tmp) / "caso"
                    shutil.copytree(ROOT / WRITE_UNLOCK / "alto-plano-aprovado", case)
                    (case / "plano/review-verdict.md").write_text(approved + tail, encoding="utf-8")
                    self.assertEqual(["artefatos do plano fora do contrato de T006"], write_unlock_problems(case))
        links = ("\n## Notas do revisor\n\nVer [relatório](docs/P1-contrato.md), ![diagrama](img/P0.png) e [notas][P1].\n"
                 "\n[P1]: docs/p1.md\n")
        self.assertEqual([], verdict_problems(approved + links))
        nested = ("\n## Testes\n\n| Teste | Evidência |\n| --- | --- |\n| contrato | [detalhes](docs/item(v2)-P1.md) |\n"
                  "\nVer [detalhes](docs/item(v2)-P1.md \"título\") e <span title=\">P1\">nota</span>.\n")
        self.assertEqual([], verdict_problems(approved + nested))

    def test_spaced_or_disguised_severity_keeps_write_locked(self) -> None:
        approved = (ROOT / WRITE_UNLOCK / "alto-plano-aprovado/plano/review-verdict.md").read_text(encoding="utf-8")
        for name, severity in {"espaço": "P 1", "tabulação": "P\t1", "espaço não separável": "P\u00a01",
                               "largura zero": "P\u200b1", "largura total": "\uff30\uff11"}.items():
            for tail in (f"\n## Notas do revisor\n\n{severity} escondido depois do cabeçalho\n",
                         f"\n## Notas do revisor\n\n| P-2 | {severity} | fonte | impacto |\n"):
                with self.subTest(case=name, tail=tail), tempfile.TemporaryDirectory() as tmp:
                    self.assertTrue([problem for problem in verdict_problems(approved + tail)
                                     if problem.startswith("linha de achado não interpretável")])
                    case = Path(tmp) / "caso"
                    shutil.copytree(ROOT / WRITE_UNLOCK / "alto-plano-aprovado", case)
                    (case / "plano/review-verdict.md").write_text(approved + tail, encoding="utf-8")
                    self.assertEqual(["artefatos do plano fora do contrato de T006"], write_unlock_problems(case))

    def test_plan_gate_addendum_is_recorded_without_rewriting_history(self) -> None:
        spec = (ROOT / "deco/specs/0002-governanca-sdd/spec.md").read_text(encoding="utf-8")
        self.assertRegex(spec, r"(?s)Adendo de 29/09/2026.{0,400}reviews/CURRENT.{0,1500}-r02")
        addendum = spec[spec.index("Adendo de 29/09/2026"):spec.index("#### Gate do Ato III")]
        self.assertRegex(addendum, r"(?s)Aplica[cç][aã]o por T011.{0,200}n[aã]o altera a decis[aã]o")
        self.assertRegex(addendum, r"(?s)`review-request\.md`.{0,80}`PRONTO PARA REVISÃO`")
        self.assertRegex(addendum, r"(?s)`review-verdict\.md`.{0,120}`APROVADO`")
        self.assertRegex(addendum, r"(?s)`correction-report\.md`.{0,80}`PRONTO PARA RECONFERÊNCIA`")
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
