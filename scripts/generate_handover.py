#!/usr/bin/env python3
"""generate_handover.py - writes HANDOVER.json from the packet's own files so it cannot drift or claim
features that do not exist. Deterministic (no clock): bump AS_OF when you cut a release.
Run from anywhere:  python3 scripts/generate_handover.py
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AS_OF = "2026-11-11"
OWNER, NAME = "bilbywilby", "Pennsylvania_Health_Insurance_November_2026"


MANAGED_DIRS = {"audit", "data", "docs", "report", "scripts", "templates", "tests"}
MANAGED_ROOT = {"README.md", "CHANGELOG.md", "VERSION", "HANDOVER.json", "MANIFEST.sha256", ".gitattributes", ".gitignore"}


def managed_files(root=ROOT):
    """Files this packet owns. Repo extras such as LICENSE, SECURITY.md or .github/actions-scripts are NOT managed."""
    out = []
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if set(rel.split("/")) & {".git", "__pycache__", ".pytest_cache"}:
            continue
        if rel in MANAGED_ROOT or rel.split("/")[0] in MANAGED_DIRS or rel.startswith(".github/workflows/"):
            out.append(rel)
    return out


def rows(rel):
    with open(ROOT / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    version = (ROOT / "VERSION").read_text().strip()
    ledger = rows("data/claims_ledger.csv")
    inventory = rows("data/public/source_inventory.csv")
    conflicts = rows("audit/conflicts_register.csv")
    rates = rows("data/public/py2027_individual_rates_pid_2026-09-18.csv")
    calc = json.loads((ROOT / "audit" / "calc_results.json").read_text())
    audit = json.loads((ROOT / "audit" / "monthly_audit_2026-11.json").read_text())
    n_tests = len(re.findall(r"^\s+def test_", (ROOT / "tests" / "test_packet.py").read_text(), re.M))
    files = managed_files()
    scripts = sorted(f for f in files if f.startswith("scripts/"))
    for needed in ("scripts/calc_audit.py", "scripts/validate_packet.py", "scripts/06_provenance_gate.py", "scripts/hash_manifest.py", "scripts/build_area_tables.py"):
        assert needed in scripts, needed
    r3 = calc["C3_rate_review"]
    open_conf = [c for c in conflicts if c["status"] == "OPEN"]
    h = {
        "handover_version": "2.0",
        "as_of": AS_OF,
        "project": {
            "name": "Pennsylvania ACA individual and small-group market audit, plan year 2027 (November 2026 packet)",
            "version": version,
            "release_stage": "beta" if "beta" in version else "release",
            "operator": OWNER,
            "purpose": "Public-interest, fully sourced reference on PY2027 rates, enrollment and open enrollment, with every claim tiered by evidence.",
            "secrets_stored_in_file": False,
        },
        "repository": {
            "slug": "%s/%s" % (OWNER, NAME), "url": "https://github.com/%s/%s" % (OWNER, NAME), "default_branch": "main",
            "intended_work_dir": "~/%s (internal Termux storage; never run git inside /sdcard)" % NAME,
            "last_known_remote_state": "origin/main held three web-upload commits (6707268, 2a3d251, bf09895) with about 50 flat files including chat-transcript .txt files, a 2.4 MB PNG and duplicate copies of packet files; LICENSE, SECURITY.md and .github/actions-scripts/fetch-issues.mjs also present (observed 2026-11-11).",
            "remote_state_needs_confirmation": True,
            "publish_tool": "scripts/ez_reconcile_repo.sh (delivered separately; plan-only by default, never force-pushes)",
        },
        "current_state": {
            "key_findings": {
                "individual_requested_pct": 17.14, "individual_approved_pct": 15.97,
                "small_group_requested_pct": 11.49, "small_group_approved_pct": 10.28,
                "denied_million_usd": 94.7, "carriers_in_pid_release": r3["n_carriers"],
                "carriers_approved_over_10pct": r3["n_approved_over_10pct"], "carriers_raised_after_review": r3["raised_after_review"],
                "open_enrollment": "2026-11-01 to 2027-01-15; enroll by 2026-12-15 for 2027-01-01 coverage",
            },
            "evidence_tiers": {"VERIFIED": "primary document read", "SECONDARY": "credible reporting", "CARRIED": "earlier project work, not re-checked",
                               "UNVERIFIED": "no source; must be bracketed", "CONTRADICTED": "a retrieved source disagrees", "NOT_FOUND": "searched, not located"},
            "publication_rule": "Only VERIFIED items, or items shown with their tier, may appear in public text.",
            "claims_ledger_rows": len(ledger), "claims_by_tier": dict(sorted(Counter(r["tier"] for r in ledger).items())),
            "source_inventory_rows": len(inventory), "sources_by_tier": dict(sorted(Counter(r["tier"] for r in inventory).items())),
            "conflicts_total": len(conflicts), "conflicts_open": [c["id"] + " " + c["topic"] for c in open_conf],
            "monthly_audit_status": audit["overall_status"],
            "calculations": sorted(calc.keys()),
            "files_in_packet": len(files),
        },
        "implemented_capabilities": {
            "calculations_reproducible": "scripts/calc_audit.py (Decimal arithmetic; writes audit/calc_results.json and audit/calc_schedule.csv)",
            "area_tables_and_one_pagers": "scripts/build_area_tables.py",
            "consistency_validator": "scripts/validate_packet.py",
            "provenance_gate": "scripts/06_provenance_gate.py (stray AI transcripts, duplicate county lists, excluded citations)",
            "manifest": "scripts/hash_manifest.py -> MANIFEST.sha256",
            "handover_generator": "scripts/generate_handover.py",
            "ci": ".github/workflows/validate.yml (regenerate, git diff --exit-code, validate, gate, tests)",
            "not_implemented": ["automated PID or Pennie data collection", "crosswalk test execution (template only)", "PDF one-pagers (markdown only)"],
        },
        "environment": {
            "observed_at": "2026-11-09 (ez_repo_recon report)",
            "device": "Termux on Android aarch64", "python": "3.14.x", "bash": "5.3.x", "git": "2.56.x", "gh": "2.103.x",
            "sh_is_dash": True,
            "rule": "Run scripts with bash (or let them re-exec); `sh script.sh` fails on bash-only syntax. Paste-safe scripts are ASCII only.",
            "paths": {"downloads": "/sdcard/Download", "review_and_backups": "~/pa_nov2026_review/<timestamp>/", "backup_bundle": "~/pa_nov2026_backup.bundle"},
        },
        "known_issues": [
            {"id": "AUTH-001", "priority": "high", "status": "open as of 2026-11-11", "description": "git over SSH failed with 'Permission denied (publickey)' (~/.ssh changed 2026-11-10 23:10).",
             "next_action": "Run `gh auth login -p https -w` (reconcile script falls back to HTTPS automatically) or re-add an SSH key at github.com/settings/keys."},
            {"id": "REMOTE-001", "priority": "high", "status": "open", "description": "Remote main carries web-uploaded flat files; local main (packet commit plus an ours-merge) is unpushed.",
             "next_action": "Run the reconcile script in plan mode, read the plan, then run with --push."},
            {"id": "ZIP-001", "priority": "medium", "status": "open", "description": "The reconcile script needs a v3.0.1-or-later packet zip in Downloads.", "next_action": "Download the beta zip to /sdcard/Download."},
            {"id": "SCRIPT-001", "priority": "low", "status": "open", "description": "~/ez_reconcile_repo.sh on the device was about 4 KB, far smaller than the delivered script; ~/ez_reconcile_repo.py was the first, unpatched version.", "next_action": "Re-download and re-paste the current script."},
            {"id": "HOME-001", "priority": "medium", "status": "standing", "description": "Sensitive files live in the Termux home (.ssh, .secrets, .wg_private_key, .pa_audit_salt, .npmrc).", "next_action": "Never `git add -A` from ~; keep them in .gitignore_global."},
            {"id": "PATH-001", "priority": "low", "status": "open", "description": "PATH was prefixed with /storage/emulated/0/root (shared storage).", "next_action": "Append instead of prepend, or remove."},
            {"id": "DATA-001", "priority": "medium", "status": "open", "description": "Pennie's primary enrollment dataset was not located; exact September 2026 count unverified.", "next_action": "Find the Pennie dataset; replace the rounded 417,000."},
            {"id": "DATA-002", "priority": "medium", "status": "open", "description": "CMS 2027 cost-sharing PDF not opened; enhanced-credit contribution caps not re-sourced.", "next_action": "Open the PDF; cite IRS or KFF for the caps."},
            {"id": "DATA-003", "priority": "medium", "status": "open", "description": "KRI formulas were blank in the submitted draft; packet definitions are reconstructions.", "next_action": "Owner to confirm definitions."},
        ],
        "decisions_needed_from_owner": [
            "Repository visibility and license (a LICENSE file already exists on the remote; confirm it is the intended one).",
            "Whether removed upload files (including chat transcripts) justify a history rewrite. Default: no; the cleanup is a normal commit and history is preserved.",
            "KRI definitions (known_issues DATA-003).",
        ],
        "verification": {
            "commands": [
                {"command": "python3 scripts/calc_audit.py && python3 scripts/build_area_tables.py && python3 scripts/generate_handover.py", "expected": "files regenerate; git diff is empty"},
                {"command": "python3 scripts/validate_packet.py", "expected": "exit 0"},
                {"command": "python3 scripts/06_provenance_gate.py", "expected": "exit 0"},
                {"command": "python3 -m unittest discover -s tests", "expected": "%d tests, OK" % n_tests},
                {"command": "sha256sum -c MANIFEST.sha256", "expected": "all OK"},
            ],
            "caveat": "A clean run means internal consistency and no known contamination; it does not confirm any figure against a primary source.",
        },
        "integrity": {"algorithm": "sha256", "manifest": "MANIFEST.sha256", "generate_command": "python3 scripts/hash_manifest.py", "note": "HANDOVER.json is covered by the manifest; regenerate it before the manifest."},
        "backup_policy": {
            "required_before_destructive_operations": True,
            "recommended_bundle_command": "git bundle create ~/pa_nov2026_backup.bundle --all",
            "existing": ["~/pa_nov2026_backup.bundle (created 2026-11-11 before the ours-merge)", "~/pa_nov2026_review/<timestamp>/work_dir_backup.bundle (created by the reconcile script)"],
            "never_without_backup_and_explicit_consent": ["git clean -fd", "git reset --hard", "git push --force", "rm -rf", "history rewrite"],
        },
        "recovery_procedure": [
            "Do nothing destructive. Check `git -C ~/%s status -sb` and `git log --oneline -5`." % NAME,
            "If a rebase or merge is half-done: `git rebase --abort` (or merge --abort) restores the pre-operation state.",
            "Restore from a bundle: `git clone ~/pa_nov2026_backup.bundle ~/restore_test`.",
            "Re-run the reconcile script in plan mode; it clones fresh and never needs your work dir to be clean.",
        ],
        "quarantined_documents": ["Cross-Sectional Metadata Analysis", "Geographic Rating Area Summaries: Pennsylvania PY2027 ACA Market Analysis"],
        "excluded_citations": "see data/statutes_2026.json (excluded_citations) and docs/source_reliability.md; never write them outside those two files",
        "working_agreements": [
            "Verify against a primary source before a claim enters any output; pasted AI output is never ground truth.",
            "Label every rate with plan year and requested or approved.",
            "Run code before calling it ready; paste raw output when something fails.",
        ],
        "pending_actions": [
            "Authenticate to GitHub (AUTH-001).",
            "Download the beta zip to /sdcard/Download (ZIP-001).",
            "Run ez_reconcile_repo.sh (plan), read the plan, then run with --push.",
            "Open https://github.com/%s/%s and confirm the tree matches this packet." % (OWNER, NAME),
        ] + audit["action_items"],
        "test_matrix": [
            {"name": "validator", "command": "python3 scripts/validate_packet.py", "expected_exit_code": 0},
            {"name": "gate", "command": "python3 scripts/06_provenance_gate.py", "expected_exit_code": 0},
            {"name": "unit tests", "command": "python3 -m unittest discover -s tests", "expected_exit_code": 0},
        ],
        "file_inventory": files,
    }
    (ROOT / "HANDOVER.json").write_text(json.dumps(h, indent=2) + "\n")
    print("[OK] HANDOVER.json written (%d packet files listed, %d tests)" % (len(files), n_tests))


if __name__ == "__main__":
    main()
