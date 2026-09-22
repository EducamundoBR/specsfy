"""BDD de SPEC-0002/T001: cada cenário executa seu contrato unittest.

As frases registradas são exatas para esta feature, evitando um step curinga
que poderia tornar outros cenários da regressão artificialmente verdes.
"""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

from behave import given, then, use_step_matcher, when


ROOT = Path(__file__).resolve().parents[3]
FEATURE = ROOT / "tests/features/deco_governance_contracts.feature"
TEST_FILE = ROOT / "tests/test_deco_governance_contracts.py"

# O vínculo é explícito: uma mudança de nome/tag de cenário não é aceita em silêncio.
SCENARIO_CASES = {
    "Unidade iniciada sem classificação de risco": ("AC-001", "test_ac001_unclassified_work_must_be_refused_and_recorded"),
    "Correção editorial de risco baixo": ("AC-002", "test_ac002_low_risk_editorial_work_needs_only_self_check"),
    "Mudança pequena que toca assunto sensível": ("AC-003", "test_ac003_small_sensitive_change_must_raise_risk"),
    "Gate de definição seleciona a revisão correspondente": ("AC-004", "test_ac004_definition_gate_selects_definition_review_and_timing"),
    "Entrega de autenticação compõe gate e perfil": ("AC-005", "test_ac005_delivery_auth_composes_profile_without_new_skill"),
    "Modelo não validado indicado a papel crítico": ("AC-006", "test_ac006_unvalidated_model_cannot_fill_critical_role"),
    "Papel lógico usa execução concreta rastreável": ("AC-007", "test_ac007_logical_role_records_actual_runtime_and_unknowns"),
    "Aprovador distinto assina o fechamento": ("AC-008", "test_ac008_distinct_approver_can_close_with_named_roles"),
    "Executor é o único aprovador disponível": ("AC-008", "test_ac008_self_approval_keeps_gate_pending"),
    "Revisor verifica a conclusão em vez de herdá-la": ("AC-009", "test_ac009_reviewer_starts_read_only_and_checks_claims"),
    "Veredito favorável sem evidência não fecha o gate": ("AC-010", "test_ac010_favorable_verdict_without_evidence_cannot_close"),
    "Preflight precede escrita e operação sensível": ("AC-011", "test_ac011_preflight_precedes_sensitive_operations"),
    "Mecanismo formal emite veredito prefixado": ("AC-012", "test_ac012_formal_verdict_is_prefixed_and_scope_is_explicit"),
    "Inspeção manual não inventa veredito formal": ("AC-012", "test_ac012_manual_inspection_is_provisional_only"),
    "Condição manual exige proteção e nova inspeção": ("AC-012", "test_ac012_manual_conditional_requires_protection_and_recheck"),
    "Condição formal exige proteção e novo preflight": ("AC-012", "test_ac012_formal_conditional_requires_protection_and_recheck"),
    "Origem desconhecida bloqueia inspeção manual": ("AC-013", "test_ac013_unknown_dirty_worktree_blocks_manual_inspection"),
    "Origem desconhecida bloqueia mecanismo formal": ("AC-013", "test_ac013_unknown_dirty_worktree_blocks_formal_guardian"),
}


def _case_for(context: object) -> str:
    scenario = context.scenario
    if scenario.name not in SCENARIO_CASES:
        raise AssertionError(f"SPEC-0002/T001: cenário não mapeado: {scenario.name}")
    ac, method = SCENARIO_CASES[scenario.name]
    if ac not in scenario.tags:
        raise AssertionError(f"SPEC-0002/T001: {scenario.name} sem tag {ac}")
    return method


def _run_contract(method: str) -> None:
    module_spec = importlib.util.spec_from_file_location("deco_governance_contracts_t001", TEST_FILE)
    if module_spec is None or module_spec.loader is None:
        raise AssertionError("SPEC-0002/T001: suíte unittest indisponível")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    case = module.GovernanceContractsTest(method)
    result = unittest.TestResult()
    case.run(result)
    failures = [*result.failures, *result.errors]
    if result.testsRun != 1 or failures or result.skipped:
        details = [traceback.splitlines()[-1] for _, traceback in failures]
        raise AssertionError(
            f"SPEC-0002/T001/{method}: {len(result.failures)} obrigações RED, "
            f"{len(result.errors)} erros, {len(result.skipped)} skips; "
            + "; ".join(details[:5])
        )


def _given(context: object) -> None:
    context.deco_governance_method = _case_for(context)
    context.deco_governance_phase = "given"


def _when(context: object) -> None:
    method = _case_for(context)
    if getattr(context, "deco_governance_phase", None) != "given":
        raise AssertionError(f"SPEC-0002/T001/{method}: Given não executado")
    context.deco_governance_phase = "when"


def _then(context: object) -> None:
    method = _case_for(context)
    if getattr(context, "deco_governance_phase", None) not in ("when", "then"):
        raise AssertionError(f"SPEC-0002/T001/{method}: When não executado")
    _run_contract(method)
    context.deco_governance_phase = "then"


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
            raise AssertionError(f"SPEC-0002/T001: step fora de fase: {phrase}")
        phrases[phase].add(phrase)
    if not all(phrases.values()):
        raise AssertionError("SPEC-0002/T001: feature sem Given, When ou Then")
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
