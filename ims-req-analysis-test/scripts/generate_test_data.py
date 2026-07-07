"""
Smart Test Data Generator — auto-generates boundary datasets from field constraints.

Reads requirements specification and generates:
  - Boundary trios for numeric thresholds
  - Enum coverage datasets (all valid values + 1 invalid)
  - Pairwise combinations to reduce combinatorial explosion

Usage:
  python scripts/generate_test_data.py requirements_spec.md --output test_data.json
"""
import re, json, itertools, sys, io
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_constraints(text: str) -> dict:
    """Extract field constraints from requirements spec."""
    constraints = []

    # Numeric thresholds: "X > N", "X >= N", "X < N", "X <= N"
    patterns = [
        (r'(\S+)\s*[>＞]\s*(\d+(?:\.\d+)?)', 'gt'),
        (r'(\S+)\s*[≥>=]\s*(\d+(?:\.\d+)?)', 'gte'),
        (r'(\S+)\s*[<＜]\s*(\d+(?:\.\d+)?)', 'lt'),
        (r'(\S+)\s*[≤<=]\s*(\d+(?:\.\d+)?)', 'lte'),
        (r'(\S+)\s*范围\s*(\d+)\s*[~～-]\s*(\d+)', 'range'),
        (r'最多\s*(\d+)\s*次', 'max_count'),
        (r'至少\s*(\d+)\s*', 'min_count'),
        (r'不超过\s*(\d+)', 'max'),
        (r'不能超过\s*(\d+)', 'max'),
    ]

    for pattern, ptype in patterns:
        for m in re.finditer(pattern, text):
            if ptype in ('gt', 'gte', 'lt', 'lte'):
                field = m.group(1).strip()
                value = float(m.group(2))
                constraints.append({'field': field, 'type': ptype, 'value': value})
            elif ptype == 'range':
                field = m.group(1).strip()
                lo, hi = float(m.group(2)), float(m.group(3))
                constraints.append({'field': field, 'type': 'range', 'min': lo, 'max': hi})
            elif ptype in ('max_count', 'max'):
                value = int(m.group(1))
                constraints.append({'field': f'count_{m.group(0)[:20]}', 'type': 'max', 'value': value})

    return constraints

def generate_boundary_trios(constraints: list) -> list:
    """Generate boundary value trios for each constraint."""
    datasets = {}

    for c in constraints:
        name = f"boundary_{c['field'].replace(' ','_')}"
        rows = []
        if c['type'] == 'gt':  # X > N
            n = c['value']
            rows = [
                {'value': n-1 if isinstance(n,int) else n-0.01, 'expected': 'reject'},
                {'value': n, 'expected': 'reject'},  # boundary: equal
                {'value': n+1 if isinstance(n,int) else n+0.01, 'expected': 'pass'},
            ]
        elif c['type'] == 'gte':  # X >= N
            n = c['value']
            rows = [
                {'value': n-1 if isinstance(n,int) else n-0.01, 'expected': 'reject'},
                {'value': n, 'expected': 'pass'},
                {'value': n+1 if isinstance(n,int) else n+0.01, 'expected': 'pass'},
            ]
        elif c['type'] == 'lt':  # X < N
            n = c['value']
            rows = [
                {'value': n-1 if isinstance(n,int) else n-0.01, 'expected': 'pass'},
                {'value': n, 'expected': 'reject'},  # boundary: equal
                {'value': n+1 if isinstance(n,int) else n+0.01, 'expected': 'reject'},
            ]
        elif c['type'] == 'lte':  # X <= N
            n = c['value']
            rows = [
                {'value': n-1 if isinstance(n,int) else n-0.01, 'expected': 'pass'},
                {'value': n, 'expected': 'pass'},
                {'value': n+1 if isinstance(n,int) else n+0.01, 'expected': 'reject'},
            ]
        elif c['type'] == 'range':
            lo, hi = c['min'], c['max']
            rows = [
                {'value': lo-1, 'expected': 'reject'},
                {'value': lo, 'expected': 'pass'},
                {'value': lo+1, 'expected': 'pass'},
                {'value': hi-1, 'expected': 'pass'},
                {'value': hi, 'expected': 'pass'},
                {'value': hi+1, 'expected': 'reject'},
            ]
        elif c['type'] == 'max':
            n = c['value']
            rows = [
                {'value': n-1, 'expected': 'pass'},
                {'value': n, 'expected': 'pass'},
                {'value': n+1, 'expected': 'reject'},
            ]
        if rows:
            datasets[name] = {'description': f'Boundary trio for {c["field"]} ({c["type"]})', 'dataset': rows}

    return datasets

def extract_enums(text: str) -> dict:
    """Extract enum definitions from requirements text."""
    enums = {}

    # Pattern: "XX: A/B/C" or "XX ∈ {A,B,C}" or markdown enum tables
    # Simplified: look for pipe-separated values in tables
    enum_tables = re.findall(r'\|.*\|.*\|', text)
    for table_line in enum_tables:
        cells = [c.strip() for c in table_line.split('|') if c.strip()]
        if len(cells) >= 3 and all(len(c) < 30 for c in cells):
            # Could be an enum row
            pass

    # Also extract from "取值: A/B/C" patterns
    for m in re.finditer(r'(\S+(?:类型|状态|模式|方式))\s*[:：]\s*([^。，\n]+)', text):
        name = m.group(1)
        values = re.split(r'[\\/、,]', m.group(2))
        values = [v.strip() for v in values if v.strip() and len(v.strip()) < 30]
        if len(values) >= 2:
            enums[name] = values

    return enums

def generate_enum_coverage(enums: dict) -> list:
    """Generate: all valid enum values + 1 invalid."""
    datasets = {}
    invalid_examples = ['INVALID', '非法值', '不存在的类型', '电子元件', '木托盘']

    for name, values in enums.items():
        rows = []
        for v in values:
            rows.append({'value': v, 'expected': 'pass'})
        rows.append({'value': invalid_examples[len(rows) % len(invalid_examples)], 'expected': 'reject'})
        datasets[f'enum_{name}'] = {'description': f'Enum coverage for {name}: {values}', 'dataset': rows}

    return datasets

def pairwise_combine(datasets: dict, max_combos: int = 20) -> dict:
    """Reduce combinatorial explosion using pairwise (2-way) combinations."""
    # For simplicity: if a dataset has >3 dimensions with >3 values each, keep only the boundary rows
    large_datasets = {k: v for k, v in datasets.items() if len(v.get('dataset', [])) > 10}
    if len(large_datasets) <= 1:
        return datasets

    # Keep only first + last + middle for large datasets
    for k in large_datasets:
        ds = datasets[k]['dataset']
        if len(ds) > 6:
            datasets[k]['dataset'] = [ds[0], ds[len(ds)//2], ds[-1]]
            datasets[k]['description'] += ' [pairwise reduced]'

    return datasets

def main():
    import argparse
    p = argparse.ArgumentParser(description='Smart test data generator')
    p.add_argument('spec', help='Path to requirements_spec.md')
    p.add_argument('--output', '-o', default='test_data_auto.json', help='Output JSON file')
    p.add_argument('--pairwise', action='store_true', help='Apply pairwise reduction')
    args = p.parse_args()

    text = Path(args.spec).read_text(encoding='utf-8')

    # Extract
    constraints = extract_constraints(text)
    enums = extract_enums(text)

    print(f'Extracted: {len(constraints)} constraints, {len(enums)} enums')

    # Generate
    datasets = {}
    datasets.update(generate_boundary_trios(constraints))
    datasets.update(generate_enum_coverage(enums))

    # Pairwise reduction
    if args.pairwise:
        datasets = pairwise_combine(datasets)

    # Output
    output = {
        '_meta': {
            'generator': 'generate_test_data.py',
            'source': args.spec,
            'constraints_found': len(constraints),
            'enums_found': len(enums),
        },
        **datasets
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total_rows = sum(len(v['dataset']) for v in datasets.values())
    print(f'Generated: {len(datasets)} datasets, {total_rows} data rows → {args.output}')

if __name__ == '__main__':
    main()
