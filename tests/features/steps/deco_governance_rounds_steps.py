"""BDD executável de SPEC-0002/T002, ligado explicitamente ao unittest."""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

from behave import given, then, use_step_matcher, when


ROOT = Path(__file__).resolve().parents[3]
FEATURE = ROOT / "tests/features/deco_governance_rounds.feature"
TEST_FILE = ROOT / "tests/test_deco_governance_rounds.py"

SCENARIO_CASES = {
    "Abertura encontra um único contexto ativo": ("AC-014", "test_ac014_single_active_context_is_validated_offline"),
    "Dois contextos ativos bloqueiam a abertura": ("AC-014", "test_ac014_ambiguous_active_context_blocks"),
    "Identidade divergente bloqueia continuidade": ("AC-014", "test_ac014_unexplained_identity_divergence_blocks"),
    "Transcript não substitui contexto curado": ("AC-015", "test_ac015_transcript_is_never_canonical"),
    "Mudança material abre nova rodada": ("AC-016", "test_ac016_material_change_opens_new_round"),
    "Correção reversível preserva SESSION_CURRENT": ("AC-016", "test_ac016_reversible_metadata_fix_is_conditional"),
    "Fechamento preserva contexto superado": ("AC-017", "test_ac017_closure_preserves_superseded_context"),
    "Estado não observado bloqueia fechamento": ("AC-018", "test_ac018_unverified_state_blocks_closure"),
    "Decisão sem motivo é recusada": ("AC-018", "test_ac018_decision_without_reason_is_rejected"),
    "Perda de contexto não permite retomada automática": ("AC-018", "test_ac018_context_loss_cannot_auto_resume"),
    "Terceira compactação inicia nova sessão": ("AC-018", "test_ac018_third_compaction_starts_new_session"),
    "Session Guardian Git Guardian e handoff não se substituem": ("AC-019", "test_ac019_guardians_and_handoff_are_distinct"),
    "Unidade de revisão é um pacote consolidado": ("AC-020", "test_ac020_review_unit_is_one_consolidated_package"),
    "Review Request registra estado e proveniência": ("AC-021", "test_ac021_request_has_fields_provenance_and_no_transcript"),
    "Review Verdict é separado e assinado": ("AC-022", "test_ac022_verdict_is_separate_and_signed"),
    "Mesma sessão não pode aprovar": ("AC-022", "test_ac022_same_session_cannot_approve"),
    "Correções ocorrem em lote na mesma rodada": ("AC-023", "test_ac023_corrections_are_batched_in_same_round"),
    "CURRENT ambíguo é rejeitado": ("AC-024", "test_ac024_current_rejects_multiple_active_rounds"),
    "Rodada concluída é imutável": ("AC-025", "test_ac025_completed_round_is_immutable"),
    "Mudança material reposiciona CURRENT": ("AC-026", "test_ac026_material_change_repoints_current"),
}


def _case_for(context: object) -> str:
    scenario = context.scenario
    if scenario.name not in SCENARIO_CASES:
        raise AssertionError(f"SPEC-0002/T002: cenário não mapeado: {scenario.name}")
    ac, method = SCENARIO_CASES[scenario.name]
    if ac not in scenario.tags:
        raise AssertionError(f"SPEC-0002/T002: {scenario.name} sem tag {ac}")
    return method


def _run_contract(method: str) -> None:
    module_spec = importlib.util.spec_from_file_location("deco_governance_rounds_t002", TEST_FILE)
    if module_spec is None or module_spec.loader is None:
        raise AssertionError("SPEC-0002/T002: suíte unittest indisponível")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    case = module.GovernanceRoundsTest(method)
    result = unittest.TestResult()
    case.run(result)
    failures = [*result.failures, *result.errors]
    if result.testsRun != 1 or failures or result.skipped:
        details = [traceback.splitlines()[-1] for _, traceback in failures]
        raise AssertionError(
            f"SPEC-0002/T002/{method}: {len(result.failures)} obrigações RED, "
            f"{len(result.errors)} erros, {len(result.skipped)} skips; "
            + "; ".join(details[:5])
        )


def _given(context: object) -> None:
    context.deco_round_method = _case_for(context)
    context.deco_round_phase = "given"


def _when(context: object) -> None:
    method = _case_for(context)
    if getattr(context, "deco_round_phase", None) != "given":
        raise AssertionError(f"SPEC-0002/T002/{method}: Given não executado")
    context.deco_round_phase = "when"


def _then(context: object) -> None:
    method = _case_for(context)
    if getattr(context, "deco_round_phase", None) not in ("when", "then"):
        raise AssertionError(f"SPEC-0002/T002/{method}: When não executado")
    _run_contract(method)
    context.deco_round_phase = "then"


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
            raise AssertionError(f"SPEC-0002/T002: step fora de fase: {phrase}")
        phrases[phase].add(phrase)
    if not all(phrases.values()):
        raise AssertionError("SPEC-0002/T002: feature sem Given, When ou Then")
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
