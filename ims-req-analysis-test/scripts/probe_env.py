"""
Environment Probe — discovers available API endpoints before test generation.

Usage:
    python scripts/probe_env.py <spec.md> [--base-url URL] [--filter-spec]

Output:
    - Compatibility report (which endpoints exist, which don't)
    - Optionally generates a filtered spec with only available cases
"""
import yaml, json, sys, time, os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

class EnvironmentProbe:
    def __init__(self, spec_path: str, base_url: str = None):
        text = Path(spec_path).read_text(encoding="utf-8")
        parts = text.split("---")
        if len(parts) < 3:
            raise ValueError("Spec must have YAML frontmatter")
        self.spec = yaml.safe_load(parts[1])
        self.spec_text = text
        self.base_url = base_url or self.spec.get("base_url", "")
        if not self.base_url:
            raise ValueError("base_url required (in spec or via --base-url)")

        # Extract unique endpoints from cases
        self.endpoints = set()
        for c in self.spec.get("cases", []):
            self.endpoints.add((c["method"], c["path"]))
        for s in self.spec.get("scenarios", []):
            for step in s.get("steps", []):
                self.endpoints.add((step["method"], step["path"]))

        print(f"Spec: {len(self.spec.get('cases',[]))} cases, {len(self.spec.get('scenarios',[]))} scenarios")
        print(f"Unique endpoints: {len(self.endpoints)}")
        print(f"Target: {self.base_url}\n")

    def probe(self) -> dict:
        """Probe all endpoints and return compatibility report."""
        results = {}
        for method, path in self.endpoints:
            url = f"{self.base_url}{path}"
            status, content_type, body, error = self._request(method, url)
            results[f"{method} {path}"] = {
                "url": url, "method": method, "path": path,
                "status": status, "content_type": content_type or "",
                "body_preview": (body or "")[:150], "error": error
            }
        return results

    def _request(self, method: str, url: str) -> tuple:
        """Make a lightweight probe request."""
        try:
            req = Request(url, method=method)
            resp = urlopen(req, timeout=10)
            ct = resp.headers.get("Content-Type", "")
            body = resp.read().decode("utf-8", errors="replace")[:500]
            return resp.status, ct, body, None
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:500] if e.fp else ""
            return e.code, "", body, None
        except URLError as e:
            return 0, "", "", str(e.reason)
        except Exception as e:
            return 0, "", "", str(e)

    def classify(self, result: dict) -> str:
        """Classify endpoint availability."""
        s = result["status"]
        ct = result.get("content_type", "")
        body = result.get("body_preview", "")

        if s == 0:
            return "unreachable"
        if s in (401, 403):
            return "auth_required"
        if s == 404:
            return "not_found"
        if s == 405:
            return "method_not_allowed"
        if s in (200, 201, 204):
            # Check if it's a real API (JSON) or HTML SPA page
            if "json" in ct.lower() or body.strip().startswith("{"):
                return "available"
            if "<html" in body.lower() or "<!doctype" in body.lower():
                return "spa_page"  # SPA frontend, not API
            return "available"
        if 500 <= s < 600:
            return "server_error"
        return f"http_{s}"

    def report(self, results: dict) -> str:
        """Generate human-readable compatibility report."""
        classified = {}
        for ep, r in results.items():
            cls = self.classify(r)
            if cls not in classified:
                classified[cls] = []
            classified[cls].append(ep)

        lines = [
            "# Environment Compatibility Report",
            f"Target: {self.base_url}",
            f"Probed: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Endpoints: {len(results)} total",
            "",
        ]

        # Summary counts
        total = len(results)
        available = len(classified.get("available", []))
        lines.append("## Summary")
        lines.append(f"| Status | Count | % |")
        lines.append(f"|--------|-------|---|")
        for cls in ["available", "auth_required", "not_found", "method_not_allowed",
                     "spa_page", "server_error", "unreachable"]:
            count = len(classified.get(cls, []))
            if count:
                pct = round(100 * count / total)
                lines.append(f"| {cls} | {count} | {pct}% |")
        lines.append("")

        # Detailed per-class
        for cls in ["available", "auth_required", "not_found", "spa_page",
                     "method_not_allowed", "server_error", "unreachable"]:
            eps = classified.get(cls, [])
            if eps:
                lines.append(f"## {cls} ({len(eps)})")
                for ep in sorted(eps):
                    lines.append(f"  - {ep}")
                lines.append("")

        # Recommendations
        lines.append("## Recommendations")
        if len(classified.get("available", [])) == 0:
            lines.append("- **No API endpoints found.** The target may be an SPA frontend or the base_url is incorrect.")
            lines.append("- Try: verify base_url, check if API gateway is on a different port/host.")
        if len(classified.get("spa_page", [])) > 0:
            lines.append("- **Detected SPA frontend.** These paths return HTML pages, not JSON APIs.")
            lines.append("- The backend API may be on a different server. Check for /gateway/ prefix or separate API host.")
        if len(classified.get("not_found", [])) > 0:
            lines.append("- **Some endpoints not found.** They may use a different path prefix.")
            lines.append("- Probe the actual system to discover correct paths, then update the spec.")

        return "\n".join(lines)

    def filter_cases(self, results: dict) -> list:
        """Return list of case IDs that are executable."""
        executable = set()
        for ep, r in results.items():
            if self.classify(r) == "available":
                executable.add(ep)
        available_ids = []
        for c in self.spec.get("cases", []):
            ep = f"{c['method']} {c['path']}"
            if ep in executable:
                available_ids.append(c["id"])
            else:
                status = results.get(ep, {}).get("status", "?")
                print(f"  SKIP {c['id']}: {ep} → {self.classify(results.get(ep, {}))} ({status})")
        return available_ids


def main():
    import argparse
    p = argparse.ArgumentParser(description="Probe API environment compatibility")
    p.add_argument("spec", help="Path to api_pytest spec YAML file")
    p.add_argument("--base-url", help="Override base_url in spec")
    p.add_argument("--filter-spec", action="store_true",
                   help="Output filtered spec with only available cases")
    p.add_argument("--output", "-o", default=None, help="Output file for report/filtered spec")
    args = p.parse_args()

    probe = EnvironmentProbe(args.spec, args.base_url)
    results = probe.probe()

    # Print live results
    for cls_name in ["available", "auth_required", "not_found", "spa_page",
                      "method_not_allowed", "server_error", "unreachable"]:
        count = 0
        for ep, r in results.items():
            if probe.classify(r) == cls_name:
                count += 1
                if count <= 3:
                    print(f"  [{cls_name}] {ep} → {r['status']}")

    # Generate report
    report = probe.report(results)
    out = args.output or str(Path(args.spec).with_suffix("")) + "_env_report.md"
    Path(out).write_text(report, encoding="utf-8")
    print(f"\nReport saved: {out}")

    # Filter spec if requested
    if args.filter_spec:
        available = probe.filter_cases(results)
        print(f"\nExecutable cases: {len(available)}/{len(probe.spec.get('cases',[]))}")

        if available:
            # Build filtered spec
            filtered = dict(probe.spec)
            filtered["cases"] = [c for c in probe.spec.get("cases", [])
                                 if c["id"] in available]
            # Also filter scenarios (keep if all steps available)
            filtered_scenarios = []
            for s in probe.spec.get("scenarios", []):
                all_available = True
                for step in s.get("steps", []):
                    ep = f"{step['method']} {step['path']}"
                    if ep not in [k for k,v in results.items() if probe.classify(v) == "available"]:
                        all_available = False
                        break
                if all_available:
                    filtered_scenarios.append(s)
            filtered["scenarios"] = filtered_scenarios

            filtered_out = args.output or str(Path(args.spec).with_suffix("")) + "_filtered.md"
            parts = probe.spec_text.split("---")
            parts[1] = "\n" + yaml.dump(filtered, allow_unicode=True, default_flow_style=False)
            Path(filtered_out).write_text("---".join(parts), encoding="utf-8")
            print(f"Filtered spec: {filtered_out}")
            print(f"  Cases: {len(filtered['cases'])}/{len(probe.spec.get('cases',[]))}")
            print(f"  Scenarios: {len(filtered['scenarios'])}/{len(probe.spec.get('scenarios',[]))}")


if __name__ == "__main__":
    main()
