#!/usr/bin/env python3
"""Unit tests for advocacy_forensic_math pipeline integration."""
from decimal import Decimal
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from advocacy_forensic_math import (
    FPL_2026_BASE,
    FPL_2026_STEP,
    audit_claim_variance,
    build_advocacy_forensic_summary,
    calculate_fpl_subsidy,
    check_allowed_amount_resilience,
)


class TestAdvocacyForensicMathPipeline(unittest.TestCase):
    def test_fpl_subsidy_cliff_and_enhanced(self) -> None:
        income_200 = (FPL_2026_BASE * Decimal("2")).quantize(Decimal("0.01"))
        std = calculate_fpl_subsidy(income_200, 1, "650.00", enhanced_credits_active=False)
        self.assertEqual(std.fpl_percent, Decimal("200.00"))
        self.assertFalse(std.is_above_400_cliff)
        self.assertGreater(std.monthly_subsidy, Decimal("0.00"))

        fpl_hh2 = FPL_2026_BASE + FPL_2026_STEP
        over_cliff = (fpl_hh2 * Decimal("4.05")).quantize(Decimal("0.01"))
        cliff = calculate_fpl_subsidy(over_cliff, 2, "1200.00", enhanced_credits_active=False)
        self.assertTrue(cliff.is_above_400_cliff)
        self.assertEqual(cliff.monthly_subsidy, Decimal("0.00"))

        arpa = calculate_fpl_subsidy(over_cliff, 2, "1200.00", enhanced_credits_active=True)
        self.assertEqual(arpa.applicable_percentage, Decimal("0.0850"))
        self.assertGreater(arpa.monthly_subsidy, Decimal("0.00"))

    def test_resilience_and_claim_variance(self) -> None:
        res = check_allowed_amount_resilience("72148", "1200.00", "350.00", "1.00")
        self.assertEqual(res.status, "CRITICAL_EXPOSURE")
        self.assertEqual(res.resilience_score, Decimal("0.00"))

        var = audit_claim_variance(
            billed_amount="450.00",
            medicare_base="100.00",
            contract_modifier="1.25",
            allowed_amount="125.00",
            plan_paid="100.00",
            coinsurance_rate="0.20",
            actual_patient_resp="350.00",
        )
        self.assertEqual(var.risk_level, "CRITICAL_OVERCHARGE")
        self.assertEqual(var.balance_billing_excess, Decimal("325.00"))

    def test_summary_artifact_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            summary = build_advocacy_forensic_summary(Path(tmpdir))
            written = Path(tmpdir) / "audit" / "advocacy_forensic_summary.json"
            self.assertTrue(written.is_file())
            loaded = json.loads(written.read_text(encoding="utf-8"))
            self.assertEqual(loaded["schema_version"], "1.0")
            self.assertEqual(loaded, summary)


if __name__ == "__main__":
    unittest.main()
