#!/usr/bin/env python3
"""Thursday 19 November 2026, in one picture.

This entry's program copies the front page it ships with (entry.png, a
1024x1024 newspaper page drawn with PIL) to the output directory the
grader reads. Standard library only, no network, and the copy is checked
byte for byte, so repeated runs always produce the same file.

Outside the grader, set MAKEFUN_OUTPUT_DIR to a scratch directory:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"


def digest_file(path):
    """SHA-256 of a file, read in 64 KiB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def main():
    if not SOURCE.is_file():
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    if DEST.stat().st_size != SOURCE.stat().st_size:
        print("copied image has the wrong size", file=sys.stderr)
        return 1
    digest = digest_file(DEST)
    if digest != digest_file(SOURCE):
        print("copied image failed its checksum", file=sys.stderr)
        return 1
    print(f"wrote {DEST} ({DEST.stat().st_size} bytes, sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
