#!/usr/bin/env python3
"""One picture of Thursday 19 November 2026.

The entry is a single image file, entry.png: a 1024 by 1024 newspaper
front page drawn with PIL. This script only puts an exact copy of it
where the grader looks, at /output/entry.png, and then proves the copy
is identical. Standard library only, no network, no randomness, so two
runs always produce the same bytes.

To try it outside the grader, set MAKEFUN_OUTPUT_DIR to a folder:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

from hashlib import sha256
from pathlib import Path
import os

IMAGE = Path(__file__).resolve().parent / "entry.png"
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"


def checksum(path):
    """SHA-256 hex digest of a file, streamed in 64 KiB pieces."""
    total = sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(65536):
            total.update(chunk)
    return total.hexdigest()


def main():
    if not IMAGE.is_file():
        print(f"missing {IMAGE}")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(IMAGE.read_bytes())
    if OUT.stat().st_size != IMAGE.stat().st_size:
        print("the copy has the wrong size")
        return 1
    digest = checksum(OUT)
    if digest != checksum(IMAGE):
        print("the copy does not match the original")
        return 1
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
