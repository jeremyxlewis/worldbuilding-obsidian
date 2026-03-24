#!/usr/bin/env python3
"""Track and advance faction progress across the vault.

Simple session-based tracking. No frontmatter complexity.

Usage:
    python advance_clocks.py --vault /path --status
    python advance_clocks.py --vault /path --faction "Cult of Orcus" --advance 1
    python advance_clocks.py --vault /path --all --advance 1
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path


def find_factions_with_progress(vault_path: Path) -> list[dict]:
    """Find all notes with faction progress notation."""
    factions = []
    org_folder = vault_path / "03_Organizations"

    if not org_folder.exists():
        return factions

    progress_pattern = re.compile(r"([░█]*)(\d+)/(\d+)", re.IGNORECASE)

    for md_file in org_folder.rglob("*.md"):
        if md_file.name.startswith("."):
            continue

        try:
            content = md_file.read_text()
        except Exception:
            continue

        matches = progress_pattern.findall(content)
        if matches:
            for filled, current, total in matches:
                factions.append(
                    {
                        "file": str(md_file.relative_to(vault_path)),
                        "name": md_file.stem,
                        "filled": len(filled),
                        "current": int(current),
                        "total": int(total),
                        "progress_bar": filled
                        + "░" * (int(total) - len(filled) - 1)
                        + "█"
                        if int(current) < int(total)
                        else "█" * int(total),
                    }
                )

    return factions


def advance_faction(
    vault_path: Path,
    faction_name: str,
    amount: int,
) -> bool:
    """Advance a specific faction's progress."""
    org_folder = vault_path / "03_Organizations"

    if not org_folder.exists():
        return False

    for md_file in org_folder.rglob("*.md"):
        if md_file.stem.lower() == faction_name.lower():
            try:
                content = md_file.read_text()

                progress_pattern = re.compile(r"([░█]*)(\d+)/(\d+)")
                match = progress_pattern.search(content)

                if match:
                    current = int(match.group(2))
                    total = int(match.group(3))
                    new_current = min(current + amount, total)

                    new_content = content.replace(
                        match.group(0),
                        f"{'█' * new_current}{'░' * (total - new_current)} {new_current}/{total}",
                    )

                    md_file.write_text(new_content)
                    print(
                        f"[+] Advanced {faction_name}: {current}/{total} -> {new_current}/{total}"
                    )
                    return True
                else:
                    print(f"[!] No progress found for {faction_name}")
                    return False

            except Exception as e:
                print(f"[!] Error updating {faction_name}: {e}")
                return False

    print(f"[!] Faction not found: {faction_name}")
    return False


def main():
    parser = argparse.ArgumentParser(description="Track faction progress")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status of all factions",
    )
    parser.add_argument(
        "--faction",
        help="Specific faction to advance",
    )
    parser.add_argument(
        "--advance",
        type=int,
        default=1,
        help="Amount to advance (default: 1)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Advance all factions found",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    if args.status:
        factions = find_factions_with_progress(vault_path)
        if not factions:
            print("[*] No faction progress found.")
            print("    Use notation like: Faction: ███░░ 3/6 in your notes")
            return

        print(f"\n# Faction Progress\n")
        for f in factions:
            status = "COMPLETE" if f["current"] >= f["total"] else "IN PROGRESS"
            print(f"## {f['name']}")
            print(
                f"   Progress: {'█' * f['current']}{'░' * (f['total'] - f['current'])} {f['current']}/{f['total']}"
            )
            print(f"   File: {f['file']}")
            print(f"   Status: {status}")
            print()

    elif args.faction:
        advance_faction(vault_path, args.faction, args.advance)

    elif args.all:
        factions = find_factions_with_progress(vault_path)
        for f in factions:
            if f["current"] < f["total"]:
                advance_faction(vault_path, f["name"], args.advance)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
