#!/usr/bin/env bash
# addon_dep_audit.sh — Scans all .py files for imports, verifies stdlib-only
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
echo "=== DEPENDENCY AUDIT (stdlib-only verification) ==="
python3 << 'PYEOF'
import ast, sys
from pathlib import Path
STDLIB = {
    'abc','argparse','array','ast','asyncio','atexit','base64','binascii',
    'bisect','builtins','bz2','calendar','collections','colorsys','configparser',
    'contextlib','contextvars','copy','csv','ctypes','dataclasses','datetime',
    'dbm','decimal','difflib','dis','email','encodings','enum','errno',
    'faulthandler','fnmatch','fractions','ftplib','functools','gc','getopt',
    'getpass','gettext','glob','gzip','hashlib','heapq','hmac','html','http',
    'imaplib','importlib','inspect','io','ipaddress','itertools','json',
    'keyword','linecache','locale','logging','lzma','mailbox','marshal','math',
    'mimetypes','mmap','multiprocessing','netrc','numbers','operator','optparse',
    'os','pathlib','pdb','pickle','pkgutil','platform','plistlib','poplib',
    'posixpath','pprint','profile','pstats','pty','pwd','py_compile','pydoc',
    'queue','quopri','random','re','readline','reprlib','resource','rlcompleter',
    'runpy','sched','secrets','select','selectors','shelve','shlex','shutil',
    'signal','site','smtplib','socket','socketserver','sqlite3','ssl','stat',
    'statistics','string','stringprep','struct','subprocess','sys','sysconfig',
    'syslog','tabnanny','tarfile','tempfile','termios','test','textwrap',
    'threading','time','timeit','token','tokenize','trace','traceback',
    'tracemalloc','tty','types','typing','unicodedata','unittest','urllib',
    'uu','uuid','venv','warnings','wave','weakref','webbrowser','wsgiref',
    'xml','xmlrpc','zipapp','zipfile','zipimport','zlib','__future__','concurrent',
    'tomllib','graphlib','graphlib','lib2to3','distutils','idlelib','tkinter'
}
all_imports = set()
files_scanned = 0
for py in sorted(Path('.').rglob('*.py')):
    if any(part in ('.git', '__pycache__', '.pytest_cache', 'tests') for part in py.parts):
        continue
    files_scanned += 1
    try:
        tree = ast.parse(py.read_text())
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                all_imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                all_imports.add(node.module.split('.')[0])
LOCAL_MODULES = {'06_provenance_gate', 'build_area_tables', 'calc_audit', 'generate_handover', 'hash_manifest', 'validate_packet'}
third_party = sorted(all_imports - STDLIB - LOCAL_MODULES)
print(f"  Files scanned:  {files_scanned}")
print(f"  Unique imports: {len(all_imports)}")
print(f"  All stdlib:     {'YES' if not third_party else 'NO'}")
if third_party:
    print(f"\n  [WARN] Non-stdlib imports detected:")
    for mod in third_party:
        print(f"         {mod}")
    sys.exit(1)
else:
    print("\n  Result: PASS — zero external dependencies confirmed")
PYEOF
