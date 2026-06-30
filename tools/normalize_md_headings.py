#!/usr/bin/env python3
"""Normalize Markdown headings: preserve the first H1 per file, demote other H1 to H2.

Usage: python tools/normalize_md_headings.py <path> [<path>...]
"""
import sys
from pathlib import Path


def normalize_file(p: Path) -> bool:
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    seen_h1 = False
    changed = False
    out_lines = []
    for i, line in enumerate(lines):
        if line.startswith("# "):
            if not seen_h1:
                seen_h1 = True
                out_lines.append(line)
            else:
                # demote to H2
                new = "## " + line[2:].lstrip()
                if new != line:
                    changed = True
                out_lines.append(new)
        elif line.startswith("#") and line.lstrip().startswith("# "):
            # handles lines like '##' with leading spaces
            out_lines.append(line)
        else:
            out_lines.append(line)

    if changed:
        p.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return changed


def main(argv):
    if len(argv) < 2:
        print("Usage: normalize_md_headings.py <file> [file...]")
        return 2
    any_changed = False
    for path in argv[1:]:
        p = Path(path)
        if not p.exists():
            print(f"Missing: {p}")
            continue
        changed = normalize_file(p)
        print(f"{p}: {'changed' if changed else 'ok'}")
        any_changed = any_changed or changed
    return 0 if any_changed else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
