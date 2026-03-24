#!/usr/bin/env python3
"""Analyze 'what if?' scenarios by tracing consequences through a vault."""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            fm[key] = value
    return fm


def extract_wikilinks(content: str) -> list:
    """Extract all wikilinks from content."""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


def build_connection_graph(vault_path: Path) -> dict:
    """Build a graph of entity connections from wikilinks."""
    graph = defaultdict(
        lambda: {"incoming": set(), "outgoing": set(), "content": "", "folder": ""}
    )

    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.parent.name.startswith("."):
            continue
        if md_file.parent.name in ("_Templates", "_Resources", "00_Dashboard"):
            continue

        name = md_file.stem
        try:
            content = md_file.read_text()
        except Exception:
            continue

        graph[name]["content"] = content
        graph[name]["folder"] = md_file.parent.name

        links = extract_wikilinks(content)
        for link in links:
            base_link = link.split("#")[0].split("^")[0].strip()
            if base_link and base_link != name:
                graph[name]["outgoing"].add(base_link)
                graph[base_link]["incoming"].add(name)

    return graph


def trace_consequences(graph: dict, subject: str, depth: int = 3) -> dict:
    """Trace consequences of a change to a subject entity."""
    results = {
        "subject": subject,
        "1st_order": [],  # Direct effects
        "2nd_order": [],  # Systemic adaptations
        "3rd_order": [],  # Cultural evolution
    }

    if subject not in graph:
        return results

    # 1st order: entities directly connected to subject
    direct_connections = graph[subject]["outgoing"] | graph[subject]["incoming"]
    results["1st_order"] = list(direct_connections)

    if depth < 2:
        return results

    # 2nd order: entities connected to 1st order entities
    second_order = set()
    for entity in direct_connections:
        if entity in graph:
            connections = graph[entity]["outgoing"] | graph[entity]["incoming"]
            second_order.update(connections)
    second_order -= direct_connections
    second_order.discard(subject)
    results["2nd_order"] = list(second_order)

    if depth < 3:
        return results

    # 3rd order: entities connected to 2nd order entities
    third_order = set()
    for entity in second_order:
        if entity in graph:
            connections = graph[entity]["outgoing"] | graph[entity]["incoming"]
            third_order.update(connections)
    third_order -= direct_connections
    third_order -= second_order
    third_order.discard(subject)
    results["3rd_order"] = list(third_order)

    return results


def generate_cascade_report(
    subject: str,
    change: str,
    results: dict,
    graph: dict,
) -> str:
    """Generate a human-readable cascade report."""
    report = f"# Cascade Analysis: {change}\n\n"
    report += f"**Subject:** [[{subject}]]\n"
    report += f"**Change:** {change}\n\n"

    # 1st Order
    report += "## 1st Order: Direct Effects\n\n"
    report += "> [!info] These entities are directly connected to the subject.\n\n"
    if results["1st_order"]:
        for entity in results["1st_order"]:
            folder = graph.get(entity, {}).get("folder", "Unknown")
            report += f"- [[{entity}]] ({folder})\n"
        report += f"\n**Impact:** These entities will be immediately affected.\n"
        report += "**Action:** Review and update each note to reflect the change.\n\n"
    else:
        report += "*No direct connections found.*\n\n"

    # 2nd Order
    report += "## 2nd Order: Systemic Adaptations\n\n"
    report += "> [!warning] These entities connect through the 1st order effects.\n\n"
    if results["2nd_order"]:
        for entity in results["2nd_order"]:
            folder = graph.get(entity, {}).get("folder", "Unknown")
            report += f"- [[{entity}]] ({folder})\n"
        report += f"\n**Impact:** These entities will adapt to the systemic changes.\n"
        report += "**Action:** Consider how these entities respond. Power structures may shift.\n\n"
    else:
        report += "*No 2nd order effects identified.*\n\n"

    # 3rd Order
    report += "## 3rd Order: Cultural Evolution\n\n"
    report += "> [!danger] These entities represent broader cultural shifts.\n\n"
    if results["3rd_order"]:
        for entity in results["3rd_order"]:
            folder = graph.get(entity, {}).get("folder", "Unknown")
            report += f"- [[{entity}]] ({folder})\n"
        report += (
            f"\n**Impact:** These represent long-term cultural/social evolution.\n"
        )
        report += "**Action:** These changes may take months or years in-world. Consider language, ethics, norms.\n\n"
    else:
        report += "*No 3rd order effects identified.*\n\n"

    # Summary
    total = (
        len(results["1st_order"])
        + len(results["2nd_order"])
        + len(results["3rd_order"])
    )
    report += "## Summary\n\n"
    report += f"| Order | Count | Description |\n"
    report += f"|-------|-------|-------------|\n"
    report += f"| 1st (Direct) | {len(results['1st_order'])} | Immediately affected |\n"
    report += f"| 2nd (Systemic) | {len(results['2nd_order'])} | System adaptations |\n"
    report += (
        f"| 3rd (Cultural) | {len(results['3rd_order'])} | Long-term evolution |\n"
    )
    report += f"| **Total** | **{total}** | |\n\n"

    report += "> [!tip] Next Steps\n"
    report += "> 1. Review each affected entity\n"
    report += "> 2. Apply changes that make sense\n"
    report += "> 3. Update wikilinks and cross-references\n"
    report += "> 4. Run validation to check for broken links\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Cascade consequence analysis")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="The entity being changed (note name without .md)",
    )
    parser.add_argument(
        "--change",
        required=True,
        help="Description of the change (e.g., 'the king dies')",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Cascade depth: 1=direct, 2=+systemic, 3=+cultural (default: 3)",
    )
    parser.add_argument(
        "--output",
        help="Output report file (default: print to stdout)",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    print(f"[*] Analyzing cascade for: {args.subject}")
    print(f"[*] Change: {args.change}")
    print(f"[*] Depth: {args.depth}")
    print()

    # Build connection graph
    print("[*] Building connection graph...")
    graph = build_connection_graph(vault_path)
    print(f"[*] Found {len(graph)} entities with connections")

    # Trace consequences
    print("[*] Tracing consequences...")
    results = trace_consequences(graph, args.subject, args.depth)

    # Generate report
    report = generate_cascade_report(args.subject, args.change, results, graph)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\n[✓] Report written to: {args.output}")
    else:
        print("\n" + report)

    total = (
        len(results["1st_order"])
        + len(results["2nd_order"])
        + len(results["3rd_order"])
    )
    print(f"\n[✓] Found {total} affected entities")


if __name__ == "__main__":
    main()
