#!/usr/bin/env python3
"""Pure-Python stdlib port of FPL subsidy, resilience, and claim variance formulas."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Dict

TWO_PLACES = Decimal("0.01")
FOUR_PLACES = Decimal("0.0001")

FPL_2026_BASE = Decimal("15650")
FPL_2026_STEP = Decimal("5500")
CLIFF_THRESHOLD_PCT = Decimal("400")
ARPA_CAP_RATE = Decimal("0.085")

PASS_VARIANCE_PCT = Decimal("15.00")
AUDIT_VARIANCE_PCT = Decimal("40.00")


def _q2(val: Decimal) -> Decimal:
    return val.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class SubsidyAuditResult:
    household_size: int
    annual_income: Decimal
    fpl_threshold: Decimal
    fpl_percent: Decimal
    is_above_400_cliff: bool
    applicable_percentage: Decimal
    max_annual_contribution: Decimal
    monthly_capped_premium: Decimal
    monthly_benchmark_premium: Decimal
    monthly_subsidy: Decimal


@dataclass(frozen=True)
class ResilienceAuditResult:
    cpt_code: str
    allowed_amount: Decimal
    medicare_benchmark: Decimal
    adjusted_benchmark: Decimal
    allowed_to_benchmark_ratio: Decimal
    resilience_score: Decimal
    status: str


@dataclass(frozen=True)
class ClaimVarianceResult:
    billed_amount: Decimal
    medicare_base: Decimal
    contract_modifier: Decimal
    fair_market_value: Decimal
    variance_amount: Decimal
    variance_pct: Decimal
    risk_level: str
    expected_patient_resp: Decimal
    actual_patient_resp: Decimal
    balance_billing_excess: Decimal


def fpl_applicable_percentage(fpl_pct: Decimal, enhanced_credits_active: bool = False) -> Decimal:
    if enhanced_credits_active:
        if fpl_pct <= Decimal("150"):
            return Decimal("0.0000")
        if fpl_pct <= Decimal("200"):
            return ((fpl_pct - Decimal("150")) / Decimal("50")) * Decimal("0.0200")
        if fpl_pct <= Decimal("250"):
            return Decimal("0.0200") + ((fpl_pct - Decimal("200")) / Decimal("50")) * Decimal("0.0200")
        if fpl_pct <= Decimal("300"):
            return Decimal("0.0400") + ((fpl_pct - Decimal("250")) / Decimal("50")) * Decimal("0.0200")
        if fpl_pct <= Decimal("400"):
            return Decimal("0.0600") + ((fpl_pct - Decimal("300")) / Decimal("100")) * Decimal("0.0250")
        return ARPA_CAP_RATE

    if fpl_pct > CLIFF_THRESHOLD_PCT:
        return Decimal("1.0000")
    if fpl_pct <= Decimal("150"):
        return Decimal("0.0200")
    if fpl_pct <= Decimal("200"):
        return Decimal("0.0400") + ((fpl_pct - Decimal("150")) / Decimal("50")) * Decimal("0.0250")
    if fpl_pct <= Decimal("250"):
        return Decimal("0.0650") + ((fpl_pct - Decimal("200")) / Decimal("50")) * Decimal("0.0180")
    if fpl_pct <= Decimal("300"):
        return Decimal("0.0830") + ((fpl_pct - Decimal("250")) / Decimal("50")) * Decimal("0.0150")
    return Decimal("0.0980")


def calculate_fpl_subsidy(
    annual_income: Decimal | float | str,
    household_size: int,
    monthly_benchmark_premium: Decimal | float | str,
    enhanced_credits_active: bool = False,
) -> SubsidyAuditResult:
    if household_size < 1:
        raise ValueError("household_size must be >= 1")
    inc = Decimal(str(annual_income))
    bench = Decimal(str(monthly_benchmark_premium))
    if inc < 0 or bench < 0:
        raise ValueError("income and premium must be non-negative")

    fpl_thresh = FPL_2026_BASE + (Decimal(household_size - 1) * FPL_2026_STEP)
    fpl_pct = (inc / fpl_thresh) * Decimal("100")
    above_cliff = fpl_pct > CLIFF_THRESHOLD_PCT
    app_pct = fpl_applicable_percentage(fpl_pct, enhanced_credits_active=enhanced_credits_active)

    if above_cliff and not enhanced_credits_active:
        max_annual = bench * Decimal("12")
        monthly_cap = bench
        monthly_sub = Decimal("0.00")
    else:
        max_annual = inc * app_pct
        monthly_cap = max_annual / Decimal("12")
        monthly_sub = max(Decimal("0.00"), bench - monthly_cap)

    return SubsidyAuditResult(
        household_size=household_size,
        annual_income=_q2(inc),
        fpl_threshold=_q2(fpl_thresh),
        fpl_percent=_q2(fpl_pct),
        is_above_400_cliff=above_cliff,
        applicable_percentage=app_pct.quantize(FOUR_PLACES, rounding=ROUND_HALF_UP),
        max_annual_contribution=_q2(max_annual),
        monthly_capped_premium=_q2(monthly_cap),
        monthly_benchmark_premium=_q2(bench),
        monthly_subsidy=_q2(monthly_sub),
    )


def check_allowed_amount_resilience(
    cpt_code: str,
    allowed_amount: Decimal | float | str,
    medicare_benchmark: Decimal | float | str,
    geographic_adjustment: Decimal | float | str = "1.00",
) -> ResilienceAuditResult:
    allowed = Decimal(str(allowed_amount))
    base = Decimal(str(medicare_benchmark))
    geo = Decimal(str(geographic_adjustment))
    if base <= 0 or geo <= 0:
        raise ValueError("medicare_benchmark and geographic_adjustment must be > 0")

    adjusted = base * geo
    ratio = allowed / adjusted
    if ratio <= Decimal("1.25"):
        score = Decimal("100.00")
        status = "RESILIENT"
    elif ratio <= Decimal("2.00"):
        score = Decimal("100") - ((ratio - Decimal("1.25")) / Decimal("0.75")) * Decimal("40")
        status = "MODERATE_MARKUP"
    elif ratio < Decimal("3.00"):
        score = Decimal("60") - ((ratio - Decimal("2.00")) / Decimal("1.00")) * Decimal("60")
        status = "HIGH_EXPOSURE"
    else:
        score = Decimal("0.00")
        status = "CRITICAL_EXPOSURE"

    return ResilienceAuditResult(
        cpt_code=cpt_code.strip(),
        allowed_amount=_q2(allowed),
        medicare_benchmark=_q2(base),
        adjusted_benchmark=_q2(adjusted),
        allowed_to_benchmark_ratio=ratio.quantize(FOUR_PLACES, rounding=ROUND_HALF_UP),
        resilience_score=_q2(score),
        status=status,
    )


def audit_claim_variance(
    billed_amount: Decimal | float | str,
    medicare_base: Decimal | float | str,
    contract_modifier: Decimal | float | str = "1.25",
    allowed_amount: Decimal | float | str | None = None,
    plan_paid: Decimal | float | str = "0.00",
    coinsurance_rate: Decimal | float | str = "0.20",
    remaining_deductible: Decimal | float | str = "0.00",
    copay: Decimal | float | str = "0.00",
    actual_patient_resp: Decimal | float | str | None = None,
) -> ClaimVarianceResult:
    billed = Decimal(str(billed_amount))
    base = Decimal(str(medicare_base))
    mod = Decimal(str(contract_modifier))
    if base <= 0 or mod <= 0:
        raise ValueError("medicare_base and contract_modifier must be > 0")

    fmv = base * mod
    var_amt = billed - fmv
    var_pct = (var_amt / fmv) * Decimal("100")

    if var_pct < PASS_VARIANCE_PCT:
        risk = "PASS"
    elif var_pct <= AUDIT_VARIANCE_PCT:
        risk = "POTENTIAL_AUDIT"
    else:
        risk = "CRITICAL_OVERCHARGE"

    allowed = Decimal(str(allowed_amount)) if allowed_amount is not None else fmv
    paid = Decimal(str(plan_paid))
    coins = Decimal(str(coinsurance_rate))
    rem_ded = Decimal(str(remaining_deductible))
    cop = Decimal(str(copay))

    ded_applied = min(allowed, rem_ded)
    post_ded = max(Decimal("0.00"), allowed - ded_applied)
    expected_resp = ded_applied + (post_ded * coins) + cop
    actual_resp = Decimal(str(actual_patient_resp)) if actual_patient_resp is not None else max(Decimal("0.00"), billed - paid)
    balance_excess = max(Decimal("0.00"), actual_resp - expected_resp)

    return ClaimVarianceResult(
        billed_amount=_q2(billed),
        medicare_base=_q2(base),
        contract_modifier=mod.quantize(FOUR_PLACES, rounding=ROUND_HALF_UP),
        fair_market_value=_q2(fmv),
        variance_amount=_q2(var_amt),
        variance_pct=_q2(var_pct),
        risk_level=risk,
        expected_patient_resp=_q2(expected_resp),
        actual_patient_resp=_q2(actual_resp),
        balance_billing_excess=_q2(balance_excess),
    )


def _serialize(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize(v) for v in obj]
    return obj


def build_advocacy_forensic_summary(repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or Path(__file__).resolve().parents[1]
    fpl_hh2_400 = FPL_2026_BASE + FPL_2026_STEP
    sample_income = (fpl_hh2_400 * Decimal("4.10")).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

    summary: Dict[str, Any] = {
        "schema_version": "1.0",
        "fpl_subsidy_examples": {
            "hh1_200pct_standard": _serialize(asdict(calculate_fpl_subsidy(FPL_2026_BASE * Decimal("2"), 1, "650.00", False))),
            "hh2_410pct_standard_cliff": _serialize(asdict(calculate_fpl_subsidy(sample_income, 2, "1200.00", False))),
            "hh2_410pct_enhanced_cap": _serialize(asdict(calculate_fpl_subsidy(sample_income, 2, "1200.00", True))),
        },
        "resilience_examples": {
            "cpt_99214_moderate": _serialize(asdict(check_allowed_amount_resilience("99214", "210.00", "125.00", "1.00"))),
            "cpt_72148_critical": _serialize(asdict(check_allowed_amount_resilience("72148", "1200.00", "350.00", "1.00"))),
        },
        "claim_variance_examples": {
            "within_threshold": _serialize(asdict(audit_claim_variance("140.00", "100.00", "1.25", "125.00", "100.00", "0.20", actual_patient_resp="25.00"))),
            "overcharge_with_balance_bill": _serialize(asdict(audit_claim_variance("450.00", "100.00", "1.25", "125.00", "100.00", "0.20", actual_patient_resp="350.00"))),
        },
    }

    out_path = root / "audit" / "advocacy_forensic_summary.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(out_path.parent), prefix=".tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=2, sort_keys=True)
            fh.write(chr(10))
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, out_path)
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise

    return summary


if __name__ == "__main__":
    payload = build_advocacy_forensic_summary()
    print(json.dumps(payload, indent=2, sort_keys=True))
