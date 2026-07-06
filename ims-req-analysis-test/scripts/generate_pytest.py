"""
api_pytest Spec → pytest Code Generator

Converts YAML frontmatter API spec into executable pytest scripts.
Usage: python generate_pytest.py <spec.md> [--output test_file.py]
"""
import yaml, json, re, sys, os, uuid, time
from pathlib import Path
from textwrap import dedent

class SpecCompiler:
    def __init__(self, spec_path: str):
        text = Path(spec_path).read_text(encoding="utf-8")
        parts = text.split("---")
        if len(parts) < 3:
            raise ValueError("Spec must have YAML frontmatter between --- markers")
        self.spec = yaml.safe_load(parts[1])
        self.vars = {}  # compile-time variable tracking
        self.validate()

    def validate(self):
        """Basic spec validation."""
        assert self.spec.get("kind") == "api_pytest", "kind must be api_pytest"
        assert self.spec.get("base_url"), "base_url required"
        cases = self.spec.get("cases", [])
        for c in cases:
            for f in ["id", "method", "path", "expect_status"]:
                assert f in c, f"Case {c.get('id','?')} missing {f}"
        print(f"Spec valid: {len(cases)} cases, {len(self.spec.get('scenarios',[]))} scenarios")

    def _var_name(self, case_id: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '_', case_id)

    def _resolve_value(self, val, var_pool: dict):
        """Resolve {{timestamp}}, {{uuid}}, ${var} placeholders."""
        if not isinstance(val, str):
            return val
        val = val.replace("{{timestamp}}", str(int(time.time())))
        val = val.replace("{{uuid}}", uuid.uuid4().hex[:8])
        for k, v in var_pool.items():
            val = val.replace(f"${{{k}}}", str(v))
        return val

    def _generate_case_test(self, case: dict, indent: str = "") -> str:
        """Generate a single test function for a case."""
        cid = case["id"]
        func_name = f"test_{self._var_name(cid)}"
        method = case["method"]
        path = case["path"]
        expected = case["expect_status"]
        name = case.get("name", cid)

        lines = [f'{indent}def {func_name}(api_client, var_pool):']
        lines.append(f'{indent}    """{cid}: {name}"""')

        # Build URL
        base_path = path
        if case.get("query"):
            query_items = []
            for qk, qv in case["query"].items():
                if isinstance(qv, str) and ("${" in qv):
                    query_items.append(f'{qk}={{{qv.lstrip("${").rstrip("}")}}}')
                else:
                    query_items.append(f'{qk}={qv}')
            query_str = "&".join(query_items)
            url_line = f'{indent}    url = BASE_URL + "{base_path}?" + f"{query_str}"'
        else:
            url_line = f'{indent}    url = BASE_URL + "{base_path}"'

        lines.append(url_line)

        if case.get("json_body"):
            body_dict = {}
            for k, v in case["json_body"].items():
                body_dict[k] = v
            lines.append(f'{indent}    payload = {{}}')
            for k, v in body_dict.items():
                val_repr = json.dumps(v, ensure_ascii=False)
                if isinstance(v, str) and ("{{" in v or "${" in v):
                    lines.append(f'{indent}    payload[{json.dumps(k,ensure_ascii=False)}] = _resolve("{v}", var_pool)')
                else:
                    lines.append(f'{indent}    payload[{json.dumps(k,ensure_ascii=False)}] = {val_repr}')

        # Headers
        if case.get("no_auth"):
            lines.append(f'{indent}    headers = {{}}')
        else:
            lines.append(f'{indent}    headers = _auth_header()')

        if case.get("json_body"):
            lines.append(f'{indent}    headers["Content-Type"] = "application/json"')

        # Make request
        if method == "GET":
            lines.append(f'{indent}    r = api_client.get(url, headers=headers)')
        elif method == "POST":
            body_var = "json=payload" if case.get("json_body") else ""
            lines.append(f'{indent}    r = api_client.post(url, {body_var}, headers=headers)')
        elif method == "PUT":
            lines.append(f'{indent}    r = api_client.put(url, json=payload, headers=headers)')
        elif method == "DELETE":
            lines.append(f'{indent}    r = api_client.delete(url, headers=headers)')
        else:
            lines.append(f'{indent}    r = api_client.request("{method}", url, json=payload, headers=headers)')

        # Assert status
        lines.append(f'{indent}    assert r.status_code == {expected}, f"{cid}: expected {expected}, got {{r.status_code}} {{r.text[:200]}}"')

        # Extra assertions
        if case.get("expect_json_subset"):
            for k, v in case["expect_json_subset"].items():
                lines.append(f'{indent}    data = r.json()')
                lines.append(f'{indent}    assert data.get({json.dumps(k,ensure_ascii=False)}) == {json.dumps(v,ensure_ascii=False)}, f"{cid}: field {k} mismatch"')
                break  # Only need to parse JSON once
            for k, v in list(case["expect_json_subset"].items())[1:]:
                lines.append(f'{indent}    assert data.get({json.dumps(k,ensure_ascii=False)}) == {json.dumps(v,ensure_ascii=False)}, f"{cid}: field {k} mismatch"')

        if case.get("expect_body_substrings"):
            for sub in case["expect_body_substrings"]:
                resolved = self._resolve_value(sub, {})
                lines.append(f'{indent}    assert {json.dumps(resolved,ensure_ascii=False)} in r.text, f"{cid}: missing substring"')

        # Extract vars
        if case.get("extract_vars"):
            lines.append(f'{indent}    data = r.json() if "data" not in dir() else data')
            for var, jpath in case["extract_vars"].items():
                # Simple JSON path (supports $.field or just field)
                if jpath.startswith("$."):
                    field = jpath[2:]
                    lines.append(f'{indent}    var_pool[{json.dumps(var,ensure_ascii=False)}] = data.get({json.dumps(field,ensure_ascii=False)}, "")')
                else:
                    lines.append(f'{indent}    var_pool[{json.dumps(var,ensure_ascii=False)}] = data.get({json.dumps(jpath,ensure_ascii=False)}, "")')

        # depends_on marker
        if case.get("depends_on"):
            deps = ", ".join(f'"{d}"' for d in case["depends_on"])
            lines.append(f'{indent}    _deps_pass({deps})  # skip if upstream failed')

        lines.append("")
        return "\n".join(lines)

    def _generate_scenario(self, scenario: dict) -> str:
        """Generate a multi-step scenario as a single test function."""
        name = re.sub(r'[^a-zA-Z0-9_]', '_', scenario["name"])
        lines = [f'def test_scenario_{name}(api_client, var_pool):']
        lines.append(f'    """Scenario: {scenario["name"]}"""')
        lines.append(f'    sc_var = {{}}  # scenario-local variable pool')

        for i, step in enumerate(scenario.get("steps", [])):
            method = step["method"]
            path = self._resolve_value(step["path"], {})
            expected = step["expect_status"]
            url = f"{{BASE_URL}}{path}"

            lines.append(f'    # Step {i+1}: {method} {path}')
            lines.append(f'    url = f"{url}"')

            if step.get("json_body"):
                lines.append(f'    payload = {{}}')
                for k, v in step["json_body"].items():
                    if isinstance(v, str) and ("{{" in v or "${" in v):
                        lines.append(f'    payload[{json.dumps(k,ensure_ascii=False)}] = _resolve("{v}", {{**var_pool, **sc_var}})')
                    else:
                        lines.append(f'    payload[{json.dumps(k,ensure_ascii=False)}] = {json.dumps(v,ensure_ascii=False)}')

            lines.append(f'    headers = _auth_header()')
            if step.get("json_body"):
                lines.append(f'    headers["Content-Type"] = "application/json"')

            body_var = "json=payload, " if step.get("json_body") else ""
            lines.append(f'    r = api_client.{method.lower()}(url, {body_var}headers=headers)')
            lines.append(f'    assert r.status_code == {expected}, f"Step {i+1}: expected {expected}, got {{r.status_code}}"')

            if step.get("capture"):
                lines.append(f'    data = r.json()')
                for var, jpath in step["capture"].items():
                    field = jpath.split(".")[-1] if "." in jpath else jpath
                    lines.append(f'    sc_var[{json.dumps(var,ensure_ascii=False)}] = data.get({json.dumps(field,ensure_ascii=False)}, "")')

            lines.append("")
        return "\n".join(lines)

    def compile(self) -> str:
        """Generate complete pytest file content."""
        cases = self.spec.get("cases", [])
        scenarios = self.spec.get("scenarios", [])
        base_url = self.spec["base_url"]
        auth = self.spec.get("auth", {})
        timeout = self.spec.get("timeout_default", 30)

        # Header
        output = f'''"""
Generated by api_pytest Spec Compiler
Source: {len(cases)} cases, {len(scenarios)} scenarios
Target: {base_url}
"""
import pytest, requests, time, uuid, json, os

BASE_URL = "{base_url}"
TIMEOUT = {timeout}
_deferred_failures = set()  # tracks failed upstream tests

def _resolve(val, var_pool):
    """Resolve marker placeholders in generated code."""
    val = val.replace("{{timestamp}}", str(int(time.time())))
    val = val.replace("{{uuid}}", uuid.uuid4().hex[:8])
    if var_pool:
        for kv_key, kv_val in var_pool.items():
            val = val.replace("${" + kv_key + "}", str(kv_val))
    return val

def _auth_header():
    """Get auth header. Override in conftest if needed."""
    token = os.environ.get("API_TOKEN", "")
    if token:
        return {{"Authorization": f"Bearer {{token}}"}}
    return {{}}

def _deps_pass(*dep_ids):
    """Skip if any upstream dependency failed."""
    failed = set(_deferred_failures)
    if set(dep_ids) & failed:
        pytest.skip(f"Upstream dependency failed: {{set(dep_ids) & failed}}")

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update({{"User-Agent": "api_pytest/1.0"}})
    yield session
    session.close()

@pytest.fixture(scope="session")
def var_pool():
    return {{}}

def _load_csv(path):
    """Load CSV for parametrize."""
    import csv
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

'''

        # Login fixture if auth configured
        if auth.get("type") == "bearer_login":
            login_path = auth["login_path"]
            user_env = auth.get("username_env", "TEST_USERNAME")
            pass_env = auth.get("password_env", "TEST_PASSWORD")
            user_field = auth.get("username_field", "username")
            pass_field = auth.get("password_field", "password")
            token_path = auth.get("token_json_path", "token")

            output += f'''
@pytest.fixture(scope="session", autouse=True)
def _login(api_client):
    """Auto-login and store token."""
    username = os.environ.get("{user_env}", "admin")
    password = os.environ.get("{pass_env}", "")
    r = api_client.post(f"{{BASE_URL}}{login_path}",
                        json={{"{user_field}": username, "{pass_field}": password}})
    if r.status_code == 200:
        token = r.json().get("{token_path}", "")
        if token:
            api_client.headers["Authorization"] = f"Bearer {{token}}"
            print(f"Logged in: token={{token[:20]}}...")
    yield
'''

        # Generate case tests
        output += "\n# ======== Cases ========\n"
        for case in cases:
            # Handle data_source parametrize
            if case.get("data_source"):
                csv_path = case["data_source"]
                cid = case["id"]
                spec_dir = Path(self.spec.get("_spec_dir", "."))
                csv_file = spec_dir / csv_path
                func_name = f"test_{self._var_name(cid)}"

                if csv_file.exists():
                    output += f'\n# Data-driven from {csv_path}'
                    csv_path_str = str(csv_file).replace('\\', '/')
                    output += f'\n@pytest.mark.parametrize("csv_row", _load_csv(r"{csv_path_str}"))'
                    output += f'\ndef {func_name}(api_client, var_pool, csv_row):'
                    output += f'\n    """{cid}: {case.get("name",cid)} (CSV-driven)"""'
                    output += f'\n    url = f"{{BASE_URL}}{case["path"]}"'
                    output += f'\n    headers = _auth_header()'
                    if case.get("json_body"):
                        output += f'\n    headers["Content-Type"] = "application/json"'
                        output += f'\n    payload = {{k: _resolve(v, var_pool) for k,v in json.loads({json.dumps(json.dumps(case["json_body"],ensure_ascii=False))}).items()}}'
                        output += f'\n    payload.update(csv_row)'
                    if case.get("depends_on"):
                        deps = ", ".join(f'"{d}"' for d in case["depends_on"])
                        output += f'\n    _deps_pass({deps})'
                    output += f'\n    r = api_client.{case["method"].lower()}(url, json=payload, headers=headers)'
                    # expect_status from CSV row
                    output += f'\n    expected = int(csv_row.get("expect_status", {case["expect_status"]}))'
                    output += f'\n    assert r.status_code == expected, f"{cid}: expected {{expected}}, got {{r.status_code}}"'
                    output += '\n'
                    continue

            output += self._generate_case_test(case)

        # Generate scenarios
        if scenarios:
            output += "\n# ======== Scenarios ========\n"
            for sc in scenarios:
                output += self._generate_scenario(sc)

        # Main
        output += '''
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
'''
        return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_pytest.py <spec.md> [--output test_file.py]")
        sys.exit(1)

    spec_path = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_path = sys.argv[idx + 1]

    compiler = SpecCompiler(spec_path)
    # Store spec dir for resolving relative paths
    compiler.spec["_spec_dir"] = str(Path(spec_path).parent)
    code = compiler.compile()

    if output_path:
        Path(output_path).write_text(code, encoding="utf-8")
        print(f"Generated: {output_path} ({len(code)} chars)")
    else:
        # Default: output next to spec
        out = Path(spec_path).with_suffix(".py")
        out.write_text(code, encoding="utf-8")
        print(f"Generated: {out} ({len(code)} chars)")

    print(f"Run: pytest {output_path or out} -v")


if __name__ == "__main__":
    main()
