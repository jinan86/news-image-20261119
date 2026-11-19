#!/usr/bin/env python3
"""News-image entry (Python 3.13, standard library only).

Writes the one picture of Thursday 19 November 2026's world news to
/output/entry.png. The image is the entry.png beside this file, drawn
with PIL as a newspaper front page; this program copies it byte for byte,
so two runs always write the same bytes and no network is needed.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

SOURCE = HERE / "entry.png"
DEST = OUTPUT_DIR / "entry.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, DEST)

# Verify the copy byte for byte: a truncated or failed write must fail
# loudly instead of handing the grader a corrupt image.
if sha256(DEST) != sha256(SOURCE):
    print("entry.png copy failed verification", file=sys.stderr)
    sys.exit(1)
print(f"wrote {DEST} ({DEST.stat().st_size} bytes, sha256 {sha256(DEST)[:16]}...)")
