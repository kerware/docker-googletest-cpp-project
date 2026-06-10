#!/usr/bin/env python3
import argparse
import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

def format_duration(value: str) -> str:
    try:
        return f"{float(value):.3f}s"
    except (ValueError, TypeError):
        return value or "0.000s"


def render_status(failures: int, errors: int, skipped: int) -> str:
    if failures or errors:
        return "failed"
    if skipped:
        return "skipped"
    return "passed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a GoogleTest/CTest JUnit XML file to HTML.")
    parser.add_argument("xml_path", type=Path, help="Input JUnit XML file.")
    parser.add_argument("output_dir", type=Path, help="Output directory for the HTML report.")
    args = parser.parse_args()

    if not args.xml_path.exists():
        print(f"ERROR: XML file not found: {args.xml_path}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = args.output_dir / "index.html"

    tree = ET.parse(args.xml_path)
    root = tree.getroot()
    suites = []
    if root.tag == "testsuites":
        suites = root.findall("testsuite")
    elif root.tag == "testsuite":
        suites = [root]
    else:
        print(f"ERROR: Unsupported root element '{root.tag}' in XML.", file=sys.stderr)
        return 1

    total = 0
    passed = 0
    failures = 0
    errors = 0
    skipped = 0
    suite_rows = []
    case_rows = []

    for suite in suites:
        suite_name = suite.attrib.get("name", "<unnamed>")
        suite_tests = int(suite.attrib.get("tests", "0"))
        suite_failures = int(suite.attrib.get("failures", "0"))
        suite_errors = int(suite.attrib.get("errors", "0"))
        suite_skipped = int(suite.attrib.get("skipped", "0"))
        suite_time = format_duration(suite.attrib.get("time", "0"))
        suite_status = render_status(suite_failures, suite_errors, suite_skipped)

        total += suite_tests
        failures += suite_failures
        errors += suite_errors
        skipped += suite_skipped
        passed += suite_tests - suite_failures - suite_errors - suite_skipped

        suite_rows.append((suite_name, suite_tests, suite_failures, suite_errors, suite_skipped, suite_time, suite_status))

        for case in suite.findall("testcase"):
            case_name = case.attrib.get("name", "<unnamed>")
            case_class = case.attrib.get("classname", "<unnamed>")
            case_time = format_duration(case.attrib.get("time", "0"))
            failure = case.find("failure")
            error = case.find("error")
            skipped_element = case.find("skipped")
            case_status = render_status(1 if failure is not None else 0, 1 if error is not None else 0, 1 if skipped_element is not None else 0)
            message = ""
            details = ""
            element = failure or error or skipped_element
            if element is not None:
                message = element.attrib.get("message", "")
                details = html.escape((element.text or "").strip())

            case_rows.append((suite_name, case_class, case_name, case_status, case_time, message, details))

    summary_html = f"<strong>{total}</strong> tests, <strong>{passed}</strong> passed, <strong>{failures}</strong> failed, <strong>{errors}</strong> errors, <strong>{skipped}</strong> skipped"

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>Rapport GoogleTest</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #202124; }}
    h1, h2 {{ color: #1a73e8; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 24px; }}
    th, td {{ border: 1px solid #dfe1e5; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #f1f3f4; }}
    tr.pass td {{ background: #ecf8ef; }}
    tr.failed td {{ background: #fbe9e7; }}
    tr.error td {{ background: #fff3cd; }}
    tr.skipped td {{ background: #f1f3f4; }}
    .status-pass {{ color: #188038; font-weight: 600; }}
    .status-failed {{ color: #b00020; font-weight: 600; }}
    .status-error {{ color: #b35c00; font-weight: 600; }}
    .status-skipped {{ color: #5f6368; font-weight: 600; }}
    .details {{ white-space: pre-wrap; font-family: Consolas, monospace; background: #f8f9fa; padding: 10px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Rapport GoogleTest</h1>
  <p>{summary_html}</p>
  <h2>Suites</h2>
  <table>
    <thead>
      <tr><th>Suite</th><th>Tests</th><th>Failures</th><th>Errors</th><th>Skipped</th><th>Durée</th><th>Statut</th></tr>
    </thead>
    <tbody>
"""

    for row in suite_rows:
        suite_name, tests, fails, errs, skips, time, status = row
        html_content += f"      <tr class=\"{status}\"><td>{html.escape(suite_name)}</td><td>{tests}</td><td>{fails}</td><td>{errs}</td><td>{skips}</td><td>{time}</td><td class=\"status-{status}\">{status}</td></tr>\n"

    html_content += """    </tbody>
  </table>
  <h2>Cas de test</h2>
  <table>
    <thead>
      <tr><th>Suite</th><th>Classe</th><th>Test</th><th>Statut</th><th>Durée</th><th>Message</th><th>Détails</th></tr>
    </thead>
    <tbody>
"""

    for suite_name, case_class, case_name, status, time, message, details in case_rows:
        html_content += f"      <tr class=\"{status}\"><td>{html.escape(suite_name)}</td><td>{html.escape(case_class)}</td><td>{html.escape(case_name)}</td><td class=\"status-{status}\">{status}</td><td>{time}</td><td>{html.escape(message)}</td><td>{details}</td></tr>\n"

    html_content += """    </tbody>
  </table>
</body>
</html>
"""

    output_file.write_text(html_content, encoding="utf-8")
    print(f"HTML report generated: {output_file}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
