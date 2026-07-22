from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_codex_frontmatter_has_only_supported_keys() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "SKILL.md must start with YAML frontmatter"
    keys = {
        line.split(":", 1)[0].strip()
        for line in match.group(1).splitlines()
        if line.strip() and not line.startswith((" ", "\t"))
    }
    assert keys == {"name", "description"}
    assert "name: patent-disclosure-codex" in match.group(1)


def test_ui_metadata_invokes_the_same_skill() -> None:
    metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "$patent-disclosure-codex" in metadata


def test_required_prompts_exist() -> None:
    required = {
        "intake.md",
        "project_scan.md",
        "patent_points_analyzer.md",
        "prior_art_search.md",
        "disclosure_preview.md",
        "disclosure_builder.md",
        "template_reference.md",
        "disclosure_self_check.md",
    }
    assert required <= {path.name for path in (ROOT / "prompts").glob("*.md")}
