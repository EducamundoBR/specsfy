"""BDD executável de SPEC-0002/T003, ligado explicitamente ao unittest."""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

from behave import given, then, use_step_matcher, when


ROOT = Path(__file__).resolve().parents[3]
FEATURE = ROOT / "tests/features/deco_governance_delivery.feature"
TEST_FILE = ROOT / "tests/test_deco_governance_delivery.py"

SCENARIO_CASES = {
    "Contrato incompleto não inicia trabalho": ("AC-027", "test_ac027_incomplete_delivery_contract_never_starts"),
    "PRONTO não prova alcance no destino": ("AC-028", "test_ac028_ready_requires_destination_proof"),
    "ENTREGUE não prova aceite": ("AC-029", "test_ac029_delivered_requires_explicit_acceptance"),
    "Papel de aceite não humano é pré-declarado": ("AC-029", "test_ac029_non_human_approver_is_declared_before_execution"),
    "Regressão em PRONTO exige nova evidência": ("AC-030", "test_ac030_ready_regression_requires_correction_and_new_evidence"),
    "Reprovação em ENTREGUE retorna à origem": ("AC-030", "test_ac030_delivered_rejection_returns_to_origin"),
    "Regressão em ACEITO revoga o aceite": ("AC-030", "test_ac030_accepted_regression_revokes_acceptance"),
    "Validação anterior ao destino não é aceite": ("AC-030", "test_ac030_pre_destination_validation_is_not_acceptance"),
    "Resíduo proibido recusa entrega": ("AC-031", "test_ac031_forbidden_residue_refuses_delivery"),
    "Rollback exige ponto de retorno verificado": ("AC-031", "test_ac031_rollback_requires_verified_return_point"),
    "Revisão verde não escala sem gatilho": ("AC-032", "test_ac032_green_review_does_not_escalate_without_trigger"),
    "Ação irreversível exige gate humano": ("AC-033", "test_ac033_irreversible_action_requires_human_gate"),
    "Quarta tentativa falha é recusada": ("AC-033", "test_ac033_fourth_attempt_is_refused"),
    "Governança funciona com serviço externo desligado": ("AC-034", "test_ac034_governance_remains_local_when_service_is_offline"),
    "Risco alto separa revisão de plano e resultado": ("AC-035", "test_ac035_high_risk_has_distinct_plan_and_result_requests"),
    "Proveniência ausente impede fechamento": ("AC-036", "test_ac036_missing_provenance_keeps_exact_unknown_token"),
    "Base observada divergente bloqueia revisão": ("AC-037", "test_ac037_observed_base_divergence_blocks_review"),
    "Veredito Git formal exige evidência executável": ("AC-038", "test_ac038_formal_git_verdict_requires_executable_evidence"),
}


def _case_for(context: object) -> str:
    scenario = context.scenario
    if scenario.name not in SCENARIO_CASES:
        raise AssertionError(f"SPEC-0002/T003: cenário não mapeado: {scenario.name}")
    ac, method = SCENARIO_CASES[scenario.name]
    if ac not in scenario.tags:
        raise AssertionError(f"SPEC-0002/T003: {scenario.name} sem tag {ac}")
    return method


def _run_contract(method: str) -> None:
    module_spec = importlib.util.spec_from_file_location("deco_governance_delivery_t003", TEST_FILE)
    if module_spec is None or module_spec.loader is None:
        raise AssertionError("SPEC-0002/T003: suíte unittest indisponível")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    case = module.GovernanceDeliveryTest(method)
    result = unittest.TestResult()
    case.run(result)
    failures = [*result.failures, *result.errors]
    if result.testsRun != 1 or failures or result.skipped:
        details = [traceback.splitlines()[-1] for _, traceback in failures]
        raise AssertionError(
            f"SPEC-0002/T003/{method}: {len(result.failures)} obrigações RED, "
            f"{len(result.errors)} erros, {len(result.skipped)} skips; "
            + "; ".join(details[:5])
        )


def _given(context: object) -> None:
    context.deco_delivery_method = _case_for(context)
    context.deco_delivery_phase = "given"


def _when(context: object) -> None:
    method = _case_for(context)
    if getattr(context, "deco_delivery_phase", None) != "given":
        raise AssertionError(f"SPEC-0002/T003/{method}: Given não executado")
    context.deco_delivery_phase = "when"


def _then(context: object) -> None:
    method = _case_for(context)
    if getattr(context, "deco_delivery_phase", None) not in ("when", "then"):
        raise AssertionError(f"SPEC-0002/T003/{method}: When não executado")
    _run_contract(method)
    context.deco_delivery_phase = "then"


def _feature_step_phrases() -> dict[str, set[str]]:
    phrases: dict[str, set[str]] = {"Given": set(), "When": set(), "Then": set()}
    phase = ""
    for line in FEATURE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*(Given|When|Then|And)\s+(.+)$", line)
        if match is None:
            continue
        keyword, phrase = match.groups()
        if keyword != "And":
            phase = keyword
        if phase not in phrases:
            raise AssertionError(f"SPEC-0002/T003: step fora de fase: {phrase}")
        phrases[phase].add(phrase)
    if not all(phrases.values()):
        raise AssertionError("SPEC-0002/T003: feature sem Given, When ou Then")
    return phrases


use_step_matcher("parse")
for keyword, phrases in _feature_step_phrases().items():
    register, handler = {
        "Given": (given, _given),
        "When": (when, _when),
        "Then": (then, _then),
    }[keyword]
    for phrase in sorted(phrases):
        register(phrase)(handler)
