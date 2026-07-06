"""
Test Feedback Ingestion — close the loop from execution back to knowledge base.

Reads test_results.json and generates:
  1. lessons_learned.md — patterns, root causes, recommendations
  2. Updates error_messages_catalog.md with new errors found
  3. Feedback summary for continuous improvement

Usage:
  python scripts/ingest_feedback.py test_results.json [--output-dir references/]
"""
import json, hashlib, time, sys, io
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Failure classification rules
CLASSIFICATION_RULES = [
    ("environment", ["Connection refused", "ConnectionResetError", "502", "503", "504",
                     "certificate verify failed", "Name or service not known", "timed out"]),
    ("data", ["404", "does not exist", "冲突", "已存在", "duplicate", "unique constraint"]),
    ("code", ["500", "Internal Server Error", "NullPointerException", "空指针", "traceback"]),
    ("test_design", ["AssertionError", "assert", "expected", "400"]),
    ("unknown", []),  # catch-all
]

def classify_failure(test: dict) -> tuple:
    """Classify a test failure and generate a fingerprint."""
    error = test.get("error", "") or test.get("message", "")
    actual = str(test.get("actual", ""))
    status = str(test.get("expected", ""))
    combined = f"{error} {actual}".lower()

    for category, patterns in CLASSIFICATION_RULES:
        if category == "unknown":
            break
        for p in patterns:
            if p.lower() in combined:
                return category, _fingerprint(test, category)
    return "unknown", _fingerprint(test, "unknown")

def _fingerprint(test: dict, category: str) -> str:
    """Generate dedup fingerprint."""
    path = test.get("path", "")
    expected = str(test.get("expected", ""))
    actual = str(test.get("actual", ""))
    error = (test.get("error", "") or "")[:50]
    raw = f"{path}|{expected}|{actual}|{error}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]

def analyze(results: dict) -> dict:
    """Analyze test results and produce feedback report."""
    cases = results.get("cases", [])
    execution = results.get("execution", {})

    passed = sum(1 for c in cases if c.get("result") == "PASS")
    failed = sum(1 for c in cases if c.get("result") == "FAIL")
    errors = sum(1 for c in cases if c.get("result") == "ERROR")
    total = len(cases)

    failed_cases = [c for c in cases if c.get("result") in ("FAIL", "ERROR")]

    # Classify
    classifications = []
    fingerprints = {}
    for c in failed_cases:
        cat, fp = classify_failure(c)
        c["_category"] = cat
        c["_fingerprint"] = fp
        classifications.append(cat)
        if fp not in fingerprints:
            fingerprints[fp] = []
        fingerprints[fp].append(c["id"])

    # Count by category
    cat_counts = Counter(classifications)

    # Dedup — same fingerprint = same root cause
    unique_issues = len(fingerprints)

    # Generate new error messages
    new_errors = []
    for c in failed_cases:
        body = c.get("body_preview", "") or ""
        error_text = c.get("error", "") or ""
        if body and len(body) > 10 and "html" not in body.lower():
            new_errors.append({
                "endpoint": f"{c.get('method','')} {c.get('path','')}",
                "status": c.get("actual", ""),
                "message": body[:200]
            })
        elif error_text:
            new_errors.append({
                "endpoint": f"{c.get('method','')} {c.get('path','')}",
                "status": c.get("actual", ""),
                "message": error_text[:200]
            })

    return {
        "summary": {
            "timestamp": execution.get("timestamp", ""),
            "total": total, "passed": passed, "failed": failed, "errors": errors,
            "pass_rate": round(100 * passed / total, 1) if total else 0,
        },
        "classification": dict(cat_counts),
        "unique_issues": unique_issues,
        "dedup_count": len(failed_cases) - unique_issues,
        "fingerprints": {fp: ids for fp, ids in fingerprints.items() if len(ids) > 1},
        "new_errors": new_errors[:10],
        "failed_cases": [{"id": c["id"], "name": c.get("name",""),
                          "category": c.get("_category",""),
                          "fingerprint": c.get("_fingerprint","")} for c in failed_cases],
    }

def generate_report(analysis: dict) -> str:
    """Generate lessons_learned.md content."""
    s = analysis["summary"]
    cls = analysis["classification"]

    lines = [
        f"# Test Feedback Report — {s['timestamp']}",
        "",
        "## Summary",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Pass Rate | {s['pass_rate']}% ({s['passed']}/{s['total']}) |",
        f"| Failed | {s['failed']} |",
        f"| Errors | {s['errors']} |",
        f"| Unique Root Causes | {analysis['unique_issues']} |",
        f"| Duplicate Failures | {analysis['dedup_count']} |",
        "",
        "## Failure Classification",
        f"| Category | Count |",
        f"|----------|-------|",
    ]
    for cat in ["environment", "data", "code", "test_design", "unknown"]:
        count = cls.get(cat, 0)
        if count:
            lines.append(f"| {cat} | {count} |")

    # Recommendations
    lines.extend([
        "",
        "## Recommendations",
    ])
    if cls.get("environment", 0) > 0:
        lines.append("- **Environment issues**: Verify target service is running and network is accessible.")
        lines.append("  - Run `python scripts/probe_env.py` before next execution.")
    if cls.get("test_design", 0) > 0:
        lines.append("- **Test design issues**: Review assertions against latest API documentation.")
        lines.append("  - Check for field name changes or response format updates.")
    if cls.get("code", 0) > 0:
        lines.append("- **Server errors (5xx)**: Report to development team with request payloads.")
    if cls.get("data", 0) > 0:
        lines.append("- **Data issues**: Use {{timestamp}}/{{uuid}} for unique values in create tests.")
    if s["pass_rate"] < 80:
        lines.append(f"- **Low pass rate ({s['pass_rate']}%)**: Prioritize fixing environment and test design issues first.")

    # Duplicate failures
    dups = analysis.get("fingerprints", {})
    if dups:
        lines.extend([
            "",
            "## Duplicate Failures (same root cause)",
            "| Fingerprint | Affected Tests |",
            "|-------------|---------------|",
        ])
        for fp, ids in sorted(dups.items()):
            lines.append(f"| {fp} | {', '.join(ids[:5])} |")

    # New errors discovered
    new_errs = analysis.get("new_errors", [])
    if new_errs:
        lines.extend([
            "",
            "## New Error Messages Discovered",
            "> Append these to `references/error_messages_catalog.md` after manual review.",
            "",
            "| Endpoint | Status | Message |",
            "|----------|--------|---------|",
        ])
        seen = set()
        for e in new_errs:
            key = f"{e['endpoint']}|{e['message'][:80]}"
            if key not in seen:
                seen.add(key)
                lines.append(f"| {e['endpoint']} | {e['status']} | {e['message'][:100]} |")

    # Failed case details
    lines.extend([
        "",
        "## Failed Case Details",
        "| ID | Name | Category | Fingerprint |",
        "|----|------|----------|-------------|",
    ])
    for c in analysis["failed_cases"][:20]:
        lines.append(f"| {c['id']} | {c['name'][:40]} | {c['category']} | {c['fingerprint']} |")

    lines.extend([
        "",
        "## Knowledge Base Updates Needed",
        "- [ ] Update `error_messages_catalog.md` with new errors above",
        "- [ ] Update `consolidated_domain_knowledge.md` with any new state transitions discovered",
        "- [ ] Update `references/` with any new business rules inferred from failures",
        "- [ ] Review and update SKILL.md Important Notes if patterns emerge",
    ])

    return "\n".join(lines)


def main():
    import argparse
    p = argparse.ArgumentParser(description="Ingest test results and generate feedback")
    p.add_argument("results", help="Path to test_results.json")
    p.add_argument("--output-dir", "-o", default=None, help="Output directory for feedback files")
    args = p.parse_args()

    results_path = Path(args.results)
    results = json.loads(results_path.read_text(encoding="utf-8"))
    analysis = analyze(results)

    # Print summary
    s = analysis["summary"]
    print(f"Results: {s['passed']} passed, {s['failed']} failed, {s['errors']} errors")
    print(f"Pass rate: {s['pass_rate']}%")
    print(f"Classification: {analysis['classification']}")
    print(f"Unique issues: {analysis['unique_issues']}")

    # Generate report
    report = generate_report(analysis)
    out_dir = Path(args.output_dir) if args.output_dir else results_path.parent
    report_path = out_dir / "lessons_learned.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved: {report_path}")

    # Update console with recommendations
    if analysis["classification"].get("environment", 0) > 0:
        print("\nAction: Run probe_env.py to verify environment before next execution.")


if __name__ == "__main__":
    main()
