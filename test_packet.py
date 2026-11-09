#!/usr/bin/env python3
"""Unit tests for the November 2026 packet (stdlib unittest)."""
import importlib.util
import json
import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


calc = load("calc_audit")
validate = load("validate_packet")


class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.inp = calc.load_inputs()

    def test_trend_compounding_corrects_draft(self):
        r = calc.c1_trend(self.inp)
        self.assertEqual(r["low"]["compound_pct"], "8.71")
        self.assertEqual(r["high"]["compound_pct"], "12.44")
        self.assertEqual(r["low"]["compound_factor"], "1.087065000")
        self.assertEqual(r["low"]["trend_only_pct_ex_morbidity"], "7.10")
        self.assertEqual(r["high"]["trend_only_pct_ex_morbidity"], "9.70")

    def test_attrition_baselines(self):
        r = calc.c2_attrition(self.inp)
        self.assertEqual(r["A_draft"]["net_loss"], 84301)
        self.assertEqual(r["A_draft"]["attrition_pct"], "16.81")
        self.assertEqual(r["A_draft"]["K"], "0.8319")
        self.assertTrue(r["B_peak2025_to_sep2026"]["K_below_0_85_trigger"])
        self.assertFalse(r["C_oe_close_to_sep2026"]["K_below_0_85_trigger"])

    def test_rate_review(self):
        r = calc.c3_rate_review(self.inp)
        self.assertEqual(r["n_carriers"], 14)
        self.assertEqual(r["n_approved_over_10pct"], 11)
        self.assertEqual(set(r["raised_after_review"]),
                         {"Health Partners Plans Inc", "Keystone Health Plan East", "QCC Insurance Company"})
        self.assertEqual(r["statewide_individual"]["delta_pp"], "-1.17")
        self.assertEqual(r["statewide_individual"]["share_of_requested_increase_removed_pct"], "6.83")
        self.assertEqual(r["cumulative_py2026_py2027_individual_pct_illustrative"], "40.90")

    def test_decomposition(self):
        r = calc.c4_decomposition(self.inp)
        self.assertEqual((r["additive_low"], r["additive_high"], r["additive_mid"]), ("13.5", "17.5", "15.5"))
        self.assertTrue(r["requested_inside_compound_range"] and r["approved_inside_compound_range"])

    def test_oop_and_counties_and_race(self):
        o = calc.c5_oop(self.inp)
        self.assertEqual(o["self_only_change_pct"], "13.21")
        self.assertEqual(o["bronze_cap_130pct_usd"], "15600")
        c = calc.c6_counties()
        self.assertEqual((c["total"], c["unique"], c["areas"]), (67, 67, 9))
        self.assertEqual(c["by_area"], {"1": 8, "2": 3, "3": 13, "4": 10, "5": 7, "6": 10, "7": 4, "8": 5, "9": 7})
        self.assertEqual(calc.c7_race(self.inp)["sum_pct"], "100.3")

    def test_pid_rows_are_internally_consistent(self):
        for c in calc.c3_rate_review(self.inp)["carriers"]:
            self.assertEqual(D(c["approved"]) - D(c["requested"]), D(c["delta_pp"]))


class TestValidator(unittest.TestCase):
    def test_validator_passes_on_packet(self):
        calc.main()
        validate.FAILS.clear()
        for fn in (validate.check_crosswalk, validate.check_tiers_and_urls, validate.check_rates,
                   validate.check_report_numbers, validate.check_json):
            fn()
        self.assertEqual(validate.FAILS, [])


if __name__ == "__main__":
    unittest.main()
