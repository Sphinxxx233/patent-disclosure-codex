from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_doctor_json_reports_core_files() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "doctor.py"), "--json"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    checks = {item["name"]: item for item in json.loads(result.stdout)}
    assert checks["Python"]["status"] == "ok"
    assert checks["SKILL.md"]["status"] == "ok"
    assert checks["prompts"]["status"] == "ok"
