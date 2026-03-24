#!/usr/bin/env python3
"""Validate an Obsidian worldbuilding vault for consistency issues."""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


class Diagnostic:
    """A single diagnostic finding."""

    def __init__(
        self, code: str, name: str, severity: str, file: str, issue: str, fix: str
    ):
        self.code = code
        self.name = name
        self.severity = severity
        self.file = file
        self.issue = issue
        self.fix = fix

    def __str__(self):
        icon = {"high": "danger", "medium": "warning", "low": "note"}.get(
            self.severity, "note"
        )
        return (
            f"> [!{icon}] {self.code}: {self.name}\n"
            f"> **File:** {self.file}\n"
            f"> **Issue:** {self.issue}\n"
            f"> **Fix:** {self.fix}\n"
        )


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
            if value.startswith("[") and value.endswith("]"):
                value = [
                    v.strip().strip('"').strip("'") for v in value[1:-1].split(",")
                ]
            fm[key] = value
    return fm


def extract_wikilinks(content: str) -> list:
    """Extract all wikilinks from content."""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


def check_broken_links(vault_path: Path) -> list:
    """Check for broken wikilinks."""
    diagnostics = []
    all_notes = {f.stem for f in vault_path.rglob("*.md") if not f.name.startswith(".")}

    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.parent.name.startswith("."):
            continue
        try:
            content = md_file.read_text()
        except Exception:
            continue

        links = extract_wikilinks(content)
        for link in links:
            # Handle heading/block references
            base_link = link.split("#")[0].split("^")[0].strip()
            if base_link and base_link not in all_notes:
                diagnostics.append(
                    Diagnostic(
                        "LINK",
                        "Broken Wikilink",
                        "medium",
                        str(md_file.relative_to(vault_path)),
                        f"Link to [[{base_link}]] but that note doesn't exist",
                        f"Create the note or fix the link",
                    )
                )
    return diagnostics


def check_empty_entities(vault_path: Path) -> list:
    """Check for entity notes with minimal content."""
    diagnostics = []
    content_folders = [
        "01_Characters",
        "02_Locations",
        "03_Organizations",
        "04_Cultures_and_Races",
        "07_Quests_and_Adventures",
        "09_Creatures",
    ]

    for folder in content_folders:
        folder_path = vault_path / folder
        if not folder_path.exists():
            continue
        for md_file in folder_path.rglob("*.md"):
            try:
                content = md_file.read_text()
            except Exception:
                continue

            # Remove frontmatter
            body = re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)
            # Count non-empty lines
            lines = [
                l
                for l in body.strip().split("\n")
                if l.strip() and not l.startswith("#")
            ]
            if len(lines) < 2:
                diagnostics.append(
                    Diagnostic(
                        "EMPTY",
                        "Empty Entity",
                        "low",
                        str(md_file.relative_to(vault_path)),
                        "This note has almost no content beyond frontmatter",
                        "Add description, details, or delete the stub",
                    )
                )
    return diagnostics


def check_duplicate_entities(vault_path: Path) -> list:
    """Check for potential duplicate entities."""
    diagnostics = []
    descriptions = defaultdict(list)

    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.parent.name.startswith("."):
            continue
        try:
            content = md_file.read_text()
        except Exception:
            continue

        fm = parse_frontmatter(content)
        desc = fm.get("description", "")
        if desc and len(desc) > 20:
            descriptions[desc.lower()[:100]].append(
                str(md_file.relative_to(vault_path))
            )

    for desc, files in descriptions.items():
        if len(files) > 1:
            diagnostics.append(
                Diagnostic(
                    "DUPE",
                    "Potential Duplicate",
                    "medium",
                    ", ".join(files),
                    f"These entities have very similar descriptions",
                    "Review and merge if they represent the same thing",
                )
            )
    return diagnostics


def check_orphaned_notes(vault_path: Path) -> list:
    """Check for notes with no incoming links."""
    diagnostics = []
    all_links = defaultdict(int)

    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.parent.name.startswith("."):
            continue
        try:
            content = md_file.read_text()
        except Exception:
            continue

        links = extract_wikilinks(content)
        for link in links:
            base_link = link.split("#")[0].split("^")[0].strip()
            if base_link:
                all_links[base_link] += 1

    content_folders = [
        "01_Characters",
        "02_Locations",
        "03_Organizations",
        "04_Cultures_and_Races",
        "07_Quests_and_Adventures",
    ]

    for folder in content_folders:
        folder_path = vault_path / folder
        if not folder_path.exists():
            continue
        for md_file in folder_path.rglob("*.md"):
            if md_file.stem not in all_links:
                diagnostics.append(
                    Diagnostic(
                        "ORPHAN",
                        "Orphaned Note",
                        "low",
                        str(md_file.relative_to(vault_path)),
                        "This note has no incoming links from other notes",
                        "Link to this note from related entities or delete it",
                    )
                )
    return diagnostics


def check_missing_frontmatter(vault_path: Path) -> list:
    """Check for notes missing frontmatter."""
    diagnostics = []

    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.parent.name.startswith("."):
            continue
        if md_file.parent.name in ("_Templates", "_Resources"):
            continue
        try:
            content = md_file.read_text()
        except Exception:
            continue

        if not content.startswith("---"):
            diagnostics.append(
                Diagnostic(
                    "META",
                    "Missing Frontmatter",
                    "medium",
                    str(md_file.relative_to(vault_path)),
                    "This note has no YAML frontmatter",
                    "Add frontmatter with type, tags, and other metadata",
                )
            )
    return diagnostics


def check_humanizer_issues(vault_path: Path) -> list:
    """Check for AI writing patterns in generated content."""
    banned_patterns = [
        (r"\bdelve(?:d|s)?\b", "delve"),
        (r"\btapestry\b", "tapestry"),
        (r"\bvibrant\b", "vibrant"),
        (r"\bserves as\b", "serves as"),
        (r"\bstands as\b", "stands as"),
        (r"\bpivotal role\b", "pivotal role"),
        (r"\bnestled in\b", "nestled in"),
        (r"\brich history\b", "rich history"),
        (r"\bancient civilization\b", "ancient civilization"),
        (r"\blooms\b", "looms"),
        (r"\bancient prophecy\b", "ancient prophecy"),
    ]

    diagnostics = []
    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.parent.name.startswith("."):
            continue
        if md_file.parent.name == "_Templates":
            continue
        try:
            content = md_file.read_text()
        except Exception:
            continue

        # Remove frontmatter for checking
        body = re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)

        for pattern, word in banned_patterns:
            matches = re.finditer(pattern, body, re.IGNORECASE)
            for match in matches:
                # Get line number
                line_num = content[: match.start()].count("\n") + 1
                diagnostics.append(
                    Diagnostic(
                        "HUMAN",
                        "AI Writing Pattern",
                        "low",
                        f"{md_file.relative_to(vault_path)}:{line_num}",
                        f"Contains '{word}' — a common AI writing tell",
                        "Replace with more specific, concrete language",
                    )
                )
    return diagnostics


def check_quest_orphans(vault_path: Path) -> list:
    """Check for quests with no connections to other world elements."""
    diagnostics = []
    quest_folder = vault_path / "07_Quests_and_Adventures"
    if not quest_folder.exists():
        return diagnostics

    all_notes = set()
    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith("."):
            continue
        all_notes.add(md_file.stem)

    for md_file in quest_folder.rglob("*.md"):
        try:
            content = md_file.read_text()
        except Exception:
            continue

        links = extract_wikilinks(content)
        valid_links = [l for l in links if l in all_notes]

        if len(valid_links) < 2:
            diagnostics.append(
                Diagnostic(
                    "W10",
                    "Quest Hook Orphaned",
                    "medium",
                    str(md_file.relative_to(vault_path)),
                    f"Quest has only {len(valid_links)} connection(s) to other entities",
                    "Link to at least 2 other entities (NPCs, locations, factions)",
                )
            )
    return diagnostics


def check_npc_motivation_gaps(vault_path: Path) -> list:
    """Check for NPCs missing motivation fields."""
    diagnostics = []
    char_folder = vault_path / "01_Characters"
    if not char_folder.exists():
        return diagnostics

    motivation_keywords = ["want", "fear", "secret", "motivation", "goal", "desire"]

    for md_file in char_folder.rglob("*.md"):
        try:
            content = md_file.read_text()
        except Exception:
            continue

        body = re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)
        body_lower = body.lower()

        found_motivation = any(kw in body_lower for kw in motivation_keywords)
        if not found_motivation:
            diagnostics.append(
                Diagnostic(
                    "W11",
                    "NPC Motivation Gap",
                    "medium",
                    str(md_file.relative_to(vault_path)),
                    "NPC has no clear motivation (want, fear, or secret)",
                    "Add at least one want, one fear, and optionally a secret",
                )
            )
    return diagnostics


def check_encounter_balance(vault_path: Path) -> list:
    """Check for encounters without proper stat blocks."""
    diagnostics = []
    encounter_folder = vault_path / "07_Quests_and_Adventures"
    if not encounter_folder.exists():
        return diagnostics

    for md_file in encounter_folder.rglob("*.md"):
        try:
            content = md_file.read_text()
        except Exception:
            continue

        fm = parse_frontmatter(content)
        if fm.get("type") == "encounter":
            has_cr = "cr" in content.lower() or "challenge" in content.lower()
            has_hp = "hp" in content.lower() or "hit points" in content.lower()
            has_ac = "ac" in content.lower() or "armor class" in content.lower()

            if not (has_cr and has_hp and has_ac):
                diagnostics.append(
                    Diagnostic(
                        "W8",
                        "Encounter Missing Stats",
                        "low",
                        str(md_file.relative_to(vault_path)),
                        "Encounter may be missing CR, HP, or AC information",
                        "Add stat block or reference creature stats",
                    )
                )
    return diagnostics


def check_canon_continuity(vault_path: Path) -> list:
    """Check for continuity issues in novel mode (canon conflicts)."""
    diagnostics = []
    manuscript_folder = vault_path / "11_Manuscript"
    if not manuscript_folder.exists():
        return diagnostics

    character_eyes = {}

    for md_file in manuscript_folder.rglob("*.md"):
        try:
            content = md_file.read_text()
        except Exception:
            continue

        fm = parse_frontmatter(content)
        if fm.get("canon_status") in ["draft", "beta"]:
            body = re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)

            eye_matches = re.findall(
                r"\b(blue|green|brown|hazel|gray|amber|red|black)\s+eyes?",
                body,
                re.IGNORECASE,
            )
            for match in eye_matches:
                character_in_file = fm.get("character", "")
                if character_in_file:
                    if character_in_file not in character_eyes:
                        character_eyes[character_in_file] = []
                    character_eyes[character_in_file].append(
                        (match.lower(), str(md_file.name))
                    )

    for char, appearances in character_eyes.items():
        colors = set([c[0] for c in appearances])
        if len(colors) > 1:
            locations = ", ".join([f"{c[1]}" for c in appearances[:3]])
            diagnostics.append(
                Diagnostic(
                    "W13",
                    "Character Eye Color Changed",
                    "high",
                    locations,
                    f"Character '{char}' has multiple eye colors: {colors}",
                    "Standardize eye color across all mentions",
                )
            )
    return diagnostics


def main():
    parser = argparse.ArgumentParser(description="Validate worldbuilding vault")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--level",
        choices=["basic", "full"],
        default="full",
        help="Diagnostic level (default: full)",
    )
    parser.add_argument(
        "--output",
        help="Output report file (default: print to stdout)",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )
    parser.add_argument(
        "--orphan-whitelist",
        action="append",
        default=[],
        help="Patterns to ignore for orphan detection (e.g., 'frontier*', 'wilderness*')",
    )
    parser.add_argument(
        "--orphan-ignore-tag",
        action="append",
        default=[],
        help="Tags to ignore for orphan detection (e.g., 'location/unexplored')",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    print(f"[*] Validating vault: {vault_path}")
    print(f"[*] Level: {args.level}")
    print()

    all_diagnostics = []

    # Always run these
    all_diagnostics.extend(check_broken_links(vault_path))
    all_diagnostics.extend(check_missing_frontmatter(vault_path))
    all_diagnostics.extend(check_empty_entities(vault_path))

    if args.level == "full":
        all_diagnostics.extend(check_duplicate_entities(vault_path))
        all_diagnostics.extend(check_orphaned_notes(vault_path))
        all_diagnostics.extend(check_humanizer_issues(vault_path))
        all_diagnostics.extend(check_quest_orphans(vault_path))
        all_diagnostics.extend(check_npc_motivation_gaps(vault_path))
        all_diagnostics.extend(check_encounter_balance(vault_path))
        all_diagnostics.extend(check_canon_continuity(vault_path))

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_diagnostics.sort(key=lambda d: severity_order.get(d.severity, 3))

    # Generate report
    report = f"# World Validation Report\n\n"
    report += f"**Vault:** {vault_path.name}\n"
    report += f"**Level:** {args.level}\n"
    report += f"**Issues Found:** {len(all_diagnostics)}\n\n"

    if not all_diagnostics:
        report += "> [!success] No Issues Found\n> Your world looks consistent!\n"
    else:
        # Group by severity
        for severity in ["high", "medium", "low"]:
            issues = [d for d in all_diagnostics if d.severity == severity]
            if issues:
                report += f"## {severity.title()} ({len(issues)})\n\n"
                for issue in issues:
                    report += str(issue) + "\n"

    if args.output:
        Path(args.output).write_text(report)
        print(f"[✓] Report written to: {args.output}")
    else:
        print(report)

    print(f"\n[✓] Found {len(all_diagnostics)} issues")


if __name__ == "__main__":
    main()
