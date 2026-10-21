#!/usr/bin/env python3
"""Compatibility wrapper for poc/exploit.py (php2shell CVE-2026-109618)."""
import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    exploit_script = Path(__file__).parent / "exploit.py"
    if not exploit_script.exists():
        sys.exit("Error: poc/exploit.py not found.")
    runpy.run_path(str(exploit_script), run_name="__main__")
