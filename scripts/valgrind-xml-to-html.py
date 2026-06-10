#!/usr/bin/env python3
import argparse
import html
import xml.etree.ElementTree as ET
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Convert Valgrind XML to a simple HTML report")
    parser.add_argument("xml_file", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    if not args.xml_file.exists():
        print(f"Valgrind XML not found: {args.xml_file}")
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "index.html"

    tree = ET.parse(args.xml_file)
    root = tree.getroot()

    # Preamble and args
    preamble_lines = [l.text for l in root.findall('./preamble/line') if l.text]
    argv = [e.text for e in root.findall('.//args/vargv/arg') if e.text]
    cmd = ' '.join(argv)

    errors = list(root.findall('.//error'))

    # errorcounts: map unique -> count
    counts = {}
    for pair in root.findall('.//errorcounts/pair'):
        cnt = pair.findtext('count')
        uniq = pair.findtext('unique')
        if cnt and uniq:
            counts[uniq] = int(cnt)

    total_errors = len(errors)

    # Build detailed rows
    detail_sections = ''
    for i, err in enumerate(errors, start=1):
        unique = err.findtext('unique') or ''
        tid = err.findtext('tid') or ''
        kind = err.findtext('kind') or ''
        what = err.findtext('what') or ''

        # stack as table rows
        stack_rows = ''
        frames = err.findall('.//stack/frame')
        for fi, frame in enumerate(frames, start=1):
            obj = frame.findtext('obj') or ''
            fn = frame.findtext('fn') or ''
            file = frame.findtext('file') or ''
            line = frame.findtext('line') or ''
            dirn = frame.findtext('dir') or ''
            stack_rows += f"<tr><td>{fi}</td><td>{html.escape(fn)}</td><td>{html.escape(obj)}</td><td>{html.escape(dirn)}</td><td>{html.escape(file)}</td><td>{html.escape(line)}</td></tr>\n"

        count_for_unique = counts.get(unique, '')

        detail_sections += f"""
  <section>
    <h2>Error #{i} — {html.escape(kind)}</h2>
    <p><strong>Unique:</strong> {html.escape(unique)} &nbsp; <strong>Count:</strong> {count_for_unique} &nbsp; <strong>TID:</strong> {html.escape(tid)}</p>
    <p><strong>What:</strong> {html.escape(what)}</p>
    <h3>Stack (top to bottom)</h3>
    <table>
      <thead><tr><th>#</th><th>Function</th><th>Object</th><th>Dir</th><th>File</th><th>Line</th></tr></thead>
      <tbody>
{stack_rows}
      </tbody>
    </table>
  </section>
"""

    # Compose errorcounts table
    errorcount_rows = ''
    for uniq, cnt in counts.items():
        errorcount_rows += f"<tr><td>{html.escape(uniq)}</td><td>{cnt}</td></tr>\n"

    html_content = f"""<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <title>Valgrind Report</title>
    <style>body{{font-family:Arial,Helvetica,sans-serif;margin:20px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:6px;vertical-align:top}}pre{{white-space:pre-wrap}}</style>
</head>
<body>
    <h1>Valgrind Report</h1>
    <h2>Preamble</h2>
    <pre>{html.escape('\n'.join(preamble_lines))}</pre>
    <h2>Command</h2>
    <pre>{html.escape(cmd)}</pre>
    <h2>Summary</h2>
    <p>Total errors: {total_errors}</p>
    <h3>Error counts</h3>
    <table>
        <thead><tr><th>Unique</th><th>Count</th></tr></thead>
        <tbody>
{errorcount_rows}
        </tbody>
    </table>

{detail_sections}

</body>
</html>"""

    out.write_text(html_content, encoding='utf-8')
    print(f"Generated HTML: {out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
