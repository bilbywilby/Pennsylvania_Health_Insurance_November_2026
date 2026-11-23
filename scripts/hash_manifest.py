#!/usr/bin/env python3
"""hash_manifest.py - writes MANIFEST.sha256 (sha256 of every tracked-style file) for backwards auditability."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "dist"}
SKIP_FILES = {"MANIFEST.sha256"}


def main():
    lines = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.name in SKIP_FILES or p.suffix in {".pyc", ".zip"}:
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  {p.relative_to(ROOT).as_posix()}")
    (ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    print(f"[OK] MANIFEST.sha256 written ({len(lines)} files)")


if __name__ == "__main__":
    main()
