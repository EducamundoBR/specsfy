"""SPEC-0002/T003: entrega, evidência e escalonamento (AC-027–AC-038).

Esta tarefa é exclusivamente TDD: os contratos e mecanismos permanecem
ausentes, e a suíte deve produzir RED comportamental até suas tarefas donas.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DELIVERY = Path("deco/skills/review-delivery/SKILL.md")
DELIVERY_CONTRACT = Path("deco/rules/delivery-contract.md")
GOVERNANCE_VALIDATOR = Path("deco/scripts/validate-governance.mjs")
REVIEW_HANDOFF = Path("deco/skills/review-handoff/SKILL.md")
GIT_GUARDIAN = Path("deco/skills/git-guardian/SKILL.md")


def normative_section(content: str, ac: str) -> str:
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


def executable_checks(
    ac: str,
    clauses: dict[str, str],
    *,
    sample: str | None = None,
) -> list[tuple[str, bool]]:
    artifact = ROOT / GOVERNANCE_VALIDATOR
    exists = artifact.is_file() if sample is None else True
    content = artifact.read_text(encoding="utf-8") if exists and sample is None else sample or ""
    regions = associated_executable_regions(content, ac)
    executable_regions = [
        region
        for region in regions
        if re.search(r"\b(?:if|switch|return|throw)\b|process\.exit", region)
    ]
    return [
        ("validador presente", exists),
        (f"contexto executável {ac}", bool(regions)),
        ("decisão associada ao AC", bool(executable_regions)),
        *[
            (
                obligation,
                any(
                    re.search(expression, region, re.IGNORECASE | re.DOTALL)
                    for region in executable_regions
                ),
            )
            for obligation, expression in clauses.items()
        ],
    ]


def strip_javascript_comments(source: str) -> str:
    """Remove comentários JS sem transformar texto em código executável."""
    output: list[str] = []
    index = 0
    state = "code"
    quote = ""
    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if state == "code":
            if char in ("'", '"', "`"):
                state, quote = "string", char
                output.append(char)
            elif char == "/" and following == "/":
                state = "line-comment"
                output.extend((" ", " "))
                index += 1
            elif char == "/" and following == "*":
                state = "block-comment"
                output.extend((" ", " "))
                index += 1
            else:
                output.append(char)
        elif state == "string":
            output.append(char)
            if char == "\\" and following:
                output.append(following)
                index += 1
            elif char == quote:
                state = "code"
        elif state == "line-comment":
            output.append("\n" if char == "\n" else " ")
            if char == "\n":
                state = "code"
        else:
            output.append("\n" if char == "\n" else " ")
            if char == "*" and following == "/":
                output.append(" ")
                index += 1
                state = "code"
        index += 1
    return "".join(output)


def associated_executable_regions(source: str, ac: str) -> list[str]:
    """Isola decisões explicitamente registradas para um AC, sem fixar a implementação."""
    executable = strip_javascript_comments(source)
    associations: list[tuple[int, int, str, str]] = []
    patterns = (
        ("handler", re.compile(
            r"[\"'](?P<ac>AC-\d{3})[\"']\s*:\s*(?:async\s+)?"
            r"(?:function\b(?:\s+[\w$]+)?\s*\([^)]*\)|"
            r"(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>)"
        )),
        ("statement", re.compile(r"\bif\s*\([^)]*[\"'](?P<ac>AC-\d{3})[\"'][^)]*\)")),
        ("case", re.compile(r"\bcase\s+[\"'](?P<ac>AC-\d{3})[\"']\s*:")),
    )
    for kind, pattern in patterns:
        associations.extend(
            (match.start(), match.end(), match.group("ac"), kind)
            for match in pattern.finditer(executable)
        )
    for match in re.finditer(
        r"\bfunction\s+[\w$]*ac[_-]?(?P<number>\d{3})[\w$]*\s*\([^)]*\)",
        executable,
        re.IGNORECASE,
    ):
        associations.append((match.start(), match.end(), f"AC-{match.group('number')}", "handler"))
    associations.sort()
    regions: list[str] = []
    for start, end, associated_ac, kind in associations:
        if associated_ac != ac:
            continue
        if kind == "case":
            following = re.search(r"\b(?:case\s+[^:]+|default)\s*:", executable[end:])
            region_end = end + following.start() if following else len(executable)
        else:
            cursor = end
            while cursor < len(executable) and executable[cursor].isspace():
                cursor += 1
            if cursor < len(executable) and executable[cursor] == "{":
                depth = 0
                quote = ""
                region_end = len(executable)
                for position in range(cursor, len(executable)):
                    char = executable[position]
                    previous = executable[position - 1] if position else ""
                    if quote:
                        if char == quote and previous != "\\":
                            quote = ""
                    elif char in ("'", '"', "`"):
                        quote = char
                    elif char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                        if depth == 0:
                            region_end = position + 1
                            break
            else:
                terminator = re.search(r"[,;\n]", executable[cursor:])
                region_end = cursor + terminator.end() if terminator else len(executable)
        regions.append(executable[start:region_end])
    return regions


class GovernanceDeliveryTest(unittest.TestCase):
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

    def assert_executable(self, ac: str, clauses: dict[str, str]) -> None:
        for obligation, satisfied in executable_checks(ac, clauses):
            with self.subTest(ac=ac, obligation=obligation):
                self.assertTrue(satisfied, f"{ac}: {GOVERNANCE_VALIDATOR} não satisfaz: {obligation}")

    def test_ac027_incomplete_delivery_contract_never_starts(self) -> None:
        self.assert_contract("AC-027", REVIEW_DELIVERY, {
            "treze campos": r"treze campos.{0,160}obrigat[oó]ri",
            "sem execução": r"campo ausente.{0,160}(?:n[aã]o|sem).{0,100}(?:inici|execu)",
            "erro antes de agir": r"apontad.{0,120}antes.{0,120}(?:execu[cç][aã]o|trabalho)",
        })

    def test_ac028_ready_requires_destination_proof(self) -> None:
        self.assert_contract("AC-028", DELIVERY_CONTRACT, {
            "verde interno produz pronto": r"verifica[cç][oõ]es internas.{0,140}evid[eê]ncia.{0,160}PRONTO",
            "entregue exige alcance": r"ENTREGUE.{0,180}recusad.{0,160}(?:presen[cç]a|alcance).{0,100}destino",
            "falsa conclusão viola contrato": r"conclu[ií]d.{0,160}sem.{0,100}comprova[cç][aã]o.{0,160}viola[cç][aã]o",
        }, exact_tokens=("PRONTO", "ENTREGUE"))

    def test_ac029_delivered_requires_explicit_acceptance(self) -> None:
        self.assert_contract("AC-029", DELIVERY_CONTRACT, {
            "presença produz entregue": r"presen[cç]a.{0,120}destino.{0,160}ENTREGUE",
            "aceite explícito": r"ACEITO.{0,180}recusad.{0,160}aprovador.{0,120}aceite expl[ií]cito",
        }, exact_tokens=("ENTREGUE", "ACEITO"))

    def test_ac029_non_human_approver_is_declared_before_execution(self) -> None:
        self.assert_contract("AC-029", DELIVERY_CONTRACT, {
            "aceite humano inaplicável": r"aceite humano.{0,120}n[aã]o se aplica",
            "papel pré-declarado": r"(?:quem|qual verifica[cç][aã]o).{0,160}aprovador.{0,180}antes da execu[cç][aã]o",
            "sem inferência posterior": r"n[aã]o.{0,100}inferid.{0,120}depois da entrega",
        })

    def test_ac030_ready_regression_requires_correction_and_new_evidence(self) -> None:
        self.assert_contract("AC-030", DELIVERY_CONTRACT, {
            "regressão em pronto": r"PRONTO.{0,160}regress[aã]o.{0,160}CORREÇÃO NECESSÁRIA",
            "retorno exige verde e evidência": r"corre[cç][aã]o.{0,140}verifica[cç][oõ]es internas verdes.{0,140}nova evid[eê]ncia.{0,120}PRONTO",
        }, exact_tokens=("PRONTO", "CORREÇÃO NECESSÁRIA"))

    def test_ac030_delivered_rejection_returns_to_origin(self) -> None:
        self.assert_contract("AC-030", DELIVERY_CONTRACT, {
            "reprovação no destino": r"ENTREGUE.{0,160}reprov.{0,160}ENTREGUE COM CORREÇÕES",
            "motivo e retorno": r"motivo.{0,100}corre[cç][aã]o necess[aá]ria.{0,160}volta.{0,100}origem",
            "nova entrega": r"volta.{0,100}PRONTO.{0,160}nova entrega.{0,160}ENTREGUE",
            "sem salto para aceite": r"nenhuma transi[cç][aã]o direta.{0,120}ACEITO",
        }, exact_tokens=("ENTREGUE", "ENTREGUE COM CORREÇÕES", "PRONTO", "ACEITO"))

    def test_ac030_accepted_regression_revokes_acceptance(self) -> None:
        self.assert_contract("AC-030", DELIVERY_CONTRACT, {
            "aceite revogado": r"ACEITO.{0,160}regress[aã]o.{0,160}ACEITE REVOGADO",
            "reabre com evidência": r"CORREÇÃO NECESSÁRIA.{0,160}motivo.{0,120}nova evid[eê]ncia",
            "percurso completo": r"PRONTO.{0,100}ENTREGUE.{0,100}ACEITO",
            "sem salto": r"nenhuma transi[cç][aã]o direta.{0,120}ACEITO",
        }, exact_tokens=("ACEITO", "ACEITE REVOGADO", "CORREÇÃO NECESSÁRIA"))

    def test_ac030_pre_destination_validation_is_not_acceptance(self) -> None:
        self.assert_contract("AC-030", DELIVERY_CONTRACT, {
            "validação antes da main": r"valida[cç][aã]o humana.{0,160}antes.{0,140}main",
            "somente autorização prévia": r"(?:autoriza[cç][aã]o para entrega|evid[eê]ncia pr[eé]via)",
            "aceite só no destino": r"ACEITO.{0,160}recusad.{0,160}confer[eê]ncia.{0,120}destino",
        }, exact_tokens=("ACEITO",))

    def test_ac031_forbidden_residue_refuses_delivery(self) -> None:
        self.assert_contract("AC-031", DELIVERY_CONTRACT, {
            "quatro resíduos": r"dado falso.{0,100}artefato inerte.{0,140}nome divergente.{0,140}arquivo tempor[aá]rio",
            "remoção ou declaração": r"entrega.{0,120}recusad.{0,160}(?:removid|declarad)",
        })

    def test_ac031_rollback_requires_verified_return_point(self) -> None:
        self.assert_contract("AC-031", DELIVERY_CONTRACT, {
            "rollback nomeado": r"rollback.{0,140}destino.{0,100}comando.{0,100}desfazer",
            "integridade verificada": r"integridade.{0,120}ponto de retorno.{0,180}autoriza[cç][aã]o.{0,120}recusad.{0,180}verificad",
        })

    def test_ac032_green_review_does_not_escalate_without_trigger(self) -> None:
        self.assert_executable("AC-032", {
            "gatilhos materiais": r"neg[oó]cio.{0,100}arquitetura.{0,120}processo transversal.{0,120}risco alto.{0,120}diverg[eê]ncia material",
            "sem consulta externa": r"nenhuma consulta externa|(?:n[aã]o|sem).{0,100}escalon",
            "prossegue offline": r"reposit[oó]rio.{0,160}prossegu",
        })

    def test_ac033_irreversible_action_requires_human_gate(self) -> None:
        self.assert_executable("AC-033", {
            "ações irreversíveis": r"publica.{0,100}hist[oó]rico.{0,100}schema.{0,100}dados.{0,100}acesso.{0,100}segredo.{0,100}remove",
            "para antes": r"para.{0,100}antes.{0,100}(?:agir|a[cç][aã]o)",
            "gate humano": r"gate humano.{0,140}modelo.{0,120}n[aã]o.{0,100}substitui",
        })

    def test_ac033_fourth_attempt_is_refused(self) -> None:
        self.assert_executable("AC-033", {
            "três falhas": r"tr[eê]s tentativas.{0,120}falhas",
            "quarta não inicia": r"quarta tentativa.{0,160}(?:para|recus|devolve)",
            "retorno ao orquestrador": r"devolve.{0,100}decis[aã]o.{0,120}(?:orquestra|humano)",
        })

    def test_ac034_governance_remains_local_when_service_is_offline(self) -> None:
        self.assert_executable("AC-034", {
            "serviço externo indisponível": r"servi[cç]o externo.{0,120}indispon[ií]vel",
            "fluxo local completo": r"classifica[cç][aã]o.{0,100}preflight.{0,120}contexto.{0,100}revis[aã]o.{0,120}contrato de entrega",
            "só escalonamento pendente": r"apenas.{0,120}escalonamento.{0,120}pendente",
        })

    def test_ac035_high_risk_has_distinct_plan_and_result_requests(self) -> None:
        self.assert_contract("AC-035", REVIEW_HANDOFF, {
            "risco alto": r"risco alto",
            "pedido do plano antes": r"Review Request.{0,100}plano.{0,120}antes da escrita",
            "pedido do resultado depois": r"outro Review Request.{0,120}resultado.{0,120}depois da escrita",
            "instantes distintos": r"artefatos.{0,100}instantes distintos.{0,120}mesma unidade",
        }, exact_tokens=("Review Request",))

    def test_ac036_missing_provenance_keeps_exact_unknown_token(self) -> None:
        self.assert_contract("AC-036", REVIEW_HANDOFF, {
            "quatro campos": r"harness.{0,80}modelo.{0,80}effort.{0,80}session ID",
            "rodada não fecha": r"rodada.{0,100}n[aã]o fecha",
            "sem inferência": r"nenhum valor.{0,100}inferid.{0,160}(?:nome|contexto|transcript|ferramenta)",
        }, exact_tokens=("NÃO REGISTRADO",))

    def test_ac037_observed_base_divergence_blocks_review(self) -> None:
        self.assert_contract("AC-037", REVIEW_HANDOFF, {
            "branch ou head diferente": r"branch.{0,100}HEAD.{0,140}diferente",
            "correções solicitadas": r"CORREÇÕES SOLICITADAS",
            "sem aprovação": r"nenhum parecer.{0,120}aprova[cç][aã]o",
            "mudança material nova rodada": r"MUDANÇA MATERIAL.{0,180}nova rodada.{0,160}CURRENT",
            "base declarada obrigatória": r"nenhum parecer.{0,160}base diferente.{0,120}declarad",
        }, exact_tokens=("CORREÇÕES SOLICITADAS", "MUDANÇA MATERIAL", "CURRENT"))

    def test_ac038_formal_git_verdict_requires_executable_evidence(self) -> None:
        self.assert_contract("AC-038", GIT_GUARDIAN, {
            "provisório não é formal": r"PROVISORIAMENTE.{0,200}sem.{0,140}(?:sa[ií]da|evid[eê]ncia).{0,140}mecanismo execut[aá]vel",
            "fechamento recusado": r"veredito formal.{0,160}fechamento.{0,120}recusad",
            "sem GG narrativo": r"nenhum estado GG.{0,120}(?:narrativa|atribu[ií]do)",
        })

    def test_negative_state_tokens_without_decision_are_rejected(self) -> None:
        shallow = "## AC-030\nPRONTO, ENTREGUE e ACEITO.\n"
        checks = dict(contract_checks("AC-030", DELIVERY_CONTRACT, {}, exact_tokens=("PRONTO", "ENTREGUE", "ACEITO"), sample=shallow))
        self.assertTrue(all(checks[f"token exato {token}"] for token in ("PRONTO", "ENTREGUE", "ACEITO")))
        self.assertFalse(checks["estrutura de decisão condição → resultado"])

    def test_negative_ac_headers_and_unrelated_empty_function_are_rejected(self) -> None:
        sample = """
        // AC-032: revisão verde
        // AC-033: gate humano
        /* AC-034: serviço externo */
        function unrelated() {}
        """
        for ac in ("AC-032", "AC-033", "AC-034"):
            with self.subTest(ac=ac):
                self.assertFalse(dict(executable_checks(ac, {}, sample=sample))[f"contexto executável {ac}"])

    def test_negative_commented_ac_tokens_and_generic_branch_are_rejected(self) -> None:
        sample = """
        // AC-032 AC-033 AC-034
        function decide(value) { if (value) return true; return false; }
        """
        for ac in ("AC-032", "AC-033", "AC-034"):
            with self.subTest(ac=ac):
                self.assertFalse(dict(executable_checks(ac, {}, sample=sample))["decisão associada ao AC"])

    def test_negative_unassociated_ac_constants_and_function_are_rejected(self) -> None:
        sample = """
        const contracts = { "AC-032": () => {} };
        function unrelated(value) { if (value) return "continue"; return "stop"; }
        """
        checks = dict(executable_checks("AC-032", {}, sample=sample))
        self.assertTrue(checks["contexto executável AC-032"])
        self.assertFalse(checks["decisão associada ao AC"])

    def test_positive_synthetic_executable_contract_is_accepted(self) -> None:
        sample = """
        const contracts = {
          "AC-032": (context) => {
            if (context.material) return "negócio arquitetura processo transversal risco alto divergência material";
            return "nenhuma consulta externa; repositório prossegue";
          },
          "AC-033": (context) => {
            if (context.irreversible) return "publicação histórico schema dados acesso segredo remove: para antes da ação; gate humano, modelo não substitui";
            if (context.failed) return "três tentativas falhas; quarta tentativa recusada; devolve decisão ao orquestrador humano";
          },
          "AC-034": (context) => {
            if (context.offline) return "serviço externo indisponível; classificação preflight contexto revisão contrato de entrega; apenas escalonamento pendente";
          },
        };
        """
        clause_groups = {
            "AC-032": ({
                "gatilhos materiais": r"neg[oó]cio.{0,100}arquitetura.{0,120}processo transversal.{0,120}risco alto.{0,120}diverg[eê]ncia material",
                "sem consulta externa": r"nenhuma consulta externa|(?:n[aã]o|sem).{0,100}escalon",
                "prossegue offline": r"reposit[oó]rio.{0,160}prossegu",
            },),
            "AC-033": ({
                "ações irreversíveis": r"publica.{0,100}hist[oó]rico.{0,100}schema.{0,100}dados.{0,100}acesso.{0,100}segredo.{0,100}remove",
                "para antes": r"para.{0,100}antes.{0,100}(?:agir|a[cç][aã]o)",
                "gate humano": r"gate humano.{0,140}modelo.{0,120}n[aã]o.{0,100}substitui",
            }, {
                "três falhas": r"tr[eê]s tentativas.{0,120}falhas",
                "quarta não inicia": r"quarta tentativa.{0,160}(?:para|recus|devolve)",
                "retorno ao orquestrador": r"devolve.{0,100}decis[aã]o.{0,120}(?:orquestra|humano)",
            }),
            "AC-034": ({
                "serviço externo indisponível": r"servi[cç]o externo.{0,120}indispon[ií]vel",
                "fluxo local completo": r"classifica[cç][aã]o.{0,100}preflight.{0,120}contexto.{0,100}revis[aã]o.{0,120}contrato de entrega",
                "só escalonamento pendente": r"apenas.{0,120}escalonamento.{0,120}pendente",
            },),
        }
        for ac, groups in clause_groups.items():
            for clauses in groups:
                with self.subTest(ac=ac, clauses=tuple(clauses)):
                    self.assertTrue(all(result for _, result in executable_checks(ac, clauses, sample=sample)))


if __name__ == "__main__":
    unittest.main()
