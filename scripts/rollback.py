#!/usr/bin/env python3
"""Undo recent changes to the vault using snapshots.

Usage:
    python rollback.py --vault /path --list
    python rollback.py --vault /path --undo abc123
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def get_snapshots_dir(vault_path: Path) -> Path:
    """Get or create the snapshots directory."""
    return vault_path / ".rag" / "snapshots"


def list_snapshots(vault_path: Path) -> list[dict]:
    """List all available snapshots."""
    snapshots_dir = get_snapshots_dir(vault_path)

    if not snapshots_dir.exists():
        return []

    snapshots = []
    for snapshot_dir in sorted(
        snapshots_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True
    ):
        if not snapshot_dir.is_dir():
            continue

        meta_file = snapshot_dir / "meta.json"
        if meta_file.exists():
            meta = json.loads(meta_file.read_text())
            snapshots.append(
                {
                    "id": snapshot_dir.name,
                    "timestamp": meta.get("timestamp", ""),
                    "description": meta.get("description", ""),
                    "files": meta.get("file_count", 0),
                }
            )

    return snapshots


def create_snapshot(vault_path: Path, description: str = "") -> str:
    """Create a snapshot of the current vault state."""
    snapshots_dir = get_snapshots_dir(vault_path)
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    snapshot_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_dir = snapshots_dir / snapshot_id
    snapshot_dir.mkdir(exist_ok=True)

    files_copied = 0
    for md_file in vault_path.rglob("*.md"):
        if any(part.startswith(".") for part in md_file.parts):
            continue
        if ".rag" in md_file.parts:
            continue

        rel_path = md_file.relative_to(vault_path)
        dest_path = snapshot_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md_file, dest_path)
        files_copied += 1

    meta = {
        "timestamp": datetime.now().isoformat(),
        "description": description,
        "file_count": files_copied,
    }
    (snapshot_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    print(f"[+] Created snapshot {snapshot_id} with {files_copied} files")
    return snapshot_id


def restore_snapshot(vault_path: Path, snapshot_id: str) -> bool:
    """Restore a specific snapshot."""
    snapshots_dir = get_snapshots_dir(vault_path)
    snapshot_dir = snapshots_dir / snapshot_id

    if not snapshot_dir.exists():
        print(f"[!] Snapshot not found: {snapshot_id}")
        return False

    print(f"[*] Restoring snapshot {snapshot_id}...")

    for md_file in snapshot_dir.rglob("*.md"):
        rel_path = md_file.relative_to(snapshot_dir)
        dest_path = vault_path / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md_file, dest_path)

    print(f"[+] Restored snapshot {snapshot_id}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Undo vault changes using snapshots")
    parser.add_argument(
        "--vault",
        required=True,
        help="Path to the Obsidian vault",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available snapshots",
    )
    parser.add_argument(
        "--snapshot",
        help="Snapshot ID to restore",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create a snapshot before making changes",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Description for the snapshot",
    )

    args = parser.parse_args()

    vault_path = Path(args.vault)
    if not vault_path.exists():
        print(f"[!] Vault not found: {vault_path}")
        sys.exit(1)

    if args.list:
        snapshots = list_snapshots(vault_path)
        if not snapshots:
            print("No snapshots found.")
            return

        print("\n# Available Snapshots\n")
        for s in snapshots:
            print(f"## {s['id']}")
            print(f"   Date: {s['timestamp']}")
            print(f"   Files: {s['files']}")
            print(f"   Description: {s['description'] or '(none)'}")
            print()

    elif args.snapshot:
        restore_snapshot(vault_path, args.snapshot)

    elif args.create:
        create_snapshot(vault_path, args.description)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
