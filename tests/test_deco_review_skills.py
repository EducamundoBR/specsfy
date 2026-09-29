"""SPEC-0002/T007–T010: obrigações das skills de revisão além de AC-001–AC-027.

Os contratos AC-001–AC-010 vivem em `test_deco_governance_contracts.py`. Esta
suíte cobre os achados da revisão independente do roteador e as verificações
próprias de T008, T009 e T010 (achados priorizados, não autoaprovação,
dependências cíclicas, estados de entrega) com fixtures de Review Verdict.
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


if __name__ == "__main__":
    unittest.main()
