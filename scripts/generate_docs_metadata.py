#!/usr/bin/env python3
"""Generate docs/metadata.json from repository files (VERSION, AUTHORS, git).

Runs quickly and writes docs/metadata.json used by the docs viewer.
"""
import json
import os
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(ROOT, "VERSION")
AUTHORS_FILE = os.path.join(ROOT, "AUTHORS")
OUT = os.path.join(ROOT, "docs", "metadata.json")

def read_file(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""

def git_commit():
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""

def main():
    version = read_file(VERSION_FILE) or "0.0.0"
    authors = read_file(AUTHORS_FILE) or ""
    commit = git_commit()
    metadata = {
        "version": version,
        "authors": [a.strip() for a in authors.splitlines() if a.strip()],
        "last_commit": commit,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "downloads": 0
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print("Wrote", OUT)

if __name__ == '__main__':
    main()
