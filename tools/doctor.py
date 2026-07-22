#!/usr/bin/env python3
"""检查 patent-disclosure-codex 的本地运行环境。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str
    required: bool


def _module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def collect_checks() -> list[Check]:
    checks = [
        Check("Python", "ok" if sys.version_info >= (3, 9) else "fail", sys.version.split()[0], True),
        Check("SKILL.md", "ok" if (ROOT / "SKILL.md").is_file() else "fail", str(ROOT / "SKILL.md"), True),
        Check("prompts", "ok" if (ROOT / "prompts").is_dir() else "fail", str(ROOT / "prompts"), True),
        Check("python-docx", "ok" if _module("docx") else "fail", "Word 交付", True),
        Check("mammoth", "ok" if _module("mammoth") else "warn", "Word 转 Markdown", False),
        Check("python-pptx", "ok" if _module("pptx") else "warn", "PowerPoint 转 Markdown", False),
        Check("matplotlib", "ok" if _module("matplotlib") else "warn", "公式渲染", False),
        Check("Node.js", "ok" if shutil.which("node") else "warn", "Mermaid 图渲染", False),
        Check("npm", "ok" if shutil.which("npm") else "warn", "Mermaid 依赖安装", False),
        Check("Playwright", "ok" if _module("playwright") else "warn", "国知局查新（可选）", False),
    ]
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--strict", action="store_true", help="把可选项缺失也视为失败")
    args = parser.parse_args()
    checks = collect_checks()

    if args.json:
        print(json.dumps([asdict(item) for item in checks], ensure_ascii=False, indent=2))
    else:
        for item in checks:
            print(f"[{item.status.upper():4}] {item.name}: {item.detail}")

    required_failed = any(item.required and item.status == "fail" for item in checks)
    optional_missing = any(not item.required and item.status != "ok" for item in checks)
    return 1 if required_failed or (args.strict and optional_missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
