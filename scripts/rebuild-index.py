#!/usr/bin/env python3
"""
pinky-memory: rebuild .brain/index.md

Scans all .brain/{slug}/meta.md files and regenerates index.md.
Called by the AI when it detects .brain/.needs-reindex at session start.

Usage:
    python3 scripts/rebuild-index.py [brain_root]

    brain_root defaults to the repo root (parent of this script's directory).
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def extract_field(content: str, field: str) -> str:
    """Extract a value from a '## Field\\nvalue' markdown section."""
    pattern = rf"##\s+{re.escape(field)}\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def first_sentence(text: str) -> str:
    """Return the first sentence (or first line) of a block of text."""
    for sep in (".", "\n"):
        idx = text.find(sep)
        if idx != -1:
            return text[: idx + (1 if sep == "." else 0)].strip()
    return text.strip()


def rebuild_index(brain_root: Path) -> None:
    brain_dir = brain_root / ".brain"

    if not brain_dir.is_dir():
        print(f"[pinky] .brain/ not found at {brain_dir}", file=sys.stderr)
        sys.exit(1)

    entries = []

    for meta_file in sorted(brain_dir.glob("*/meta.md")):
        slug = meta_file.parent.name
        content = meta_file.read_text(encoding="utf-8")

        source = extract_field(content, "Source Repository")
        purpose_block = extract_field(content, "Purpose")
        purpose = first_sentence(purpose_block) if purpose_block else "—"
        indexed = extract_field(content, "First Indexed") or "—"

        entries.append((slug, source, purpose, indexed))

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        "# Brain Index\n",
        f"_Last rebuilt: {now}_\n",
        "",
    ]

    if not entries:
        lines.append("_No projects indexed yet._\n")
    else:
        for slug, source, purpose, indexed in entries:
            lines.append(f"## {slug}")
            lines.append(f"- **Source**: {source}")
            lines.append(f"- **Purpose**: {purpose}")
            lines.append(f"- **Indexed**: {indexed}")
            lines.append("")

    index_path = brain_dir / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[pinky] rebuilt index.md ({len(entries)} project(s))")

    # Remove the reindex flag
    flag = brain_dir / ".needs-reindex"
    if flag.exists():
        flag.unlink()
        print("[pinky] cleared .needs-reindex flag")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
    else:
        # Default: two levels up from this script (scripts/ → repo root)
        root = Path(__file__).resolve().parent.parent

    rebuild_index(root)
