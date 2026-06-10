#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path


def render_fixes(fixes_path: Path):
  if not fixes_path.exists():
    return ''
  try:
    data = fixes_path.read_text(encoding='utf-8', errors='replace')
    # clang-tidy fixes are YAML; include raw
    return f"<h2>Exported fixes (YAML)</h2><pre>{html.escape(data)}</pre>"
  except Exception:
    return ''


def main():
  parser = argparse.ArgumentParser(description="Convert clang-tidy text output to simple HTML report")
  parser.add_argument("input_file", type=Path)
  parser.add_argument("output_dir", type=Path)
  parser.add_argument("fixes_file", type=Path, nargs='?', default=None)
  args = parser.parse_args()

  if not args.input_file.exists():
    print(f"Input file not found: {args.input_file}")
    return 1

  args.output_dir.mkdir(parents=True, exist_ok=True)
  out = args.output_dir / "index.html"

  text = args.input_file.read_text(encoding="utf-8", errors="replace")
  escaped = html.escape(text)

  fixes_html = ''
  if args.fixes_file:
    fixes_html = render_fixes(args.fixes_file)

  html_content = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <title>Clang-Tidy Report</title>
  <style>body{{font-family:Arial,Helvetica,sans-serif;margin:20px}}pre{{background:#f8f9fa;border:1px solid #ddd;padding:12px;white-space:pre-wrap;word-break:break-word}}</style>
</head>
<body>
  <h1>Clang-Tidy Report</h1>
  <h2>Raw output</h2>
  <pre>{escaped}</pre>
  {fixes_html}
</body>
</html>"""

  out.write_text(html_content, encoding="utf-8")
  print(f"Generated HTML: {out}")
  return 0


if __name__ == '__main__':
  raise SystemExit(main())
