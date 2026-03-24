"""Markdown-aware chunking for worldbuilding notes."""

import re
from dataclasses import dataclass, field


@dataclass
class Chunk:
    """A single chunk of text with metadata."""

    text: str
    metadata: dict = field(default_factory=dict)
    chunk_id: str = ""


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (metadata, body)."""
    match = re.match(r"^---\n(.*?)\n---\n?", content, re.DOTALL)
    if not match:
        return {}, content

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

    body = content[match.end() :]
    return fm, body


def chunk_by_headers(
    content: str, filepath: str, min_chunk_size: int = 50
) -> list[Chunk]:
    """Split markdown content by h1/h2/h3 headers.

    Each section under a header becomes a separate chunk.
    Sections smaller than min_chunk_size are merged with the previous chunk.
    """
    fm, body = parse_frontmatter(content)
    entity_type = fm.get("type", "unknown")
    entity_title = fm.get(
        "title", filepath.stem if hasattr(filepath, "stem") else filepath
    )
    tags = fm.get("tags", [])

    # Split by headers (h1, h2, h3)
    header_pattern = r"^(#{1,3})\s+(.+)$"
    lines = body.split("\n")

    chunks = []
    current_header = "Overview"
    current_header_level = 0
    current_lines = []
    header_path = [entity_title]

    for line in lines:
        header_match = re.match(header_pattern, line, re.MULTILINE)

        if header_match:
            # Save previous section as chunk
            if current_lines:
                text = "\n".join(current_lines).strip()
                if len(text) >= min_chunk_size:
                    chunks.append(
                        Chunk(
                            text=text,
                            metadata={
                                "source": str(filepath),
                                "entity_type": entity_type,
                                "entity_title": entity_title,
                                "heading": current_header,
                                "heading_path": " > ".join(header_path),
                                "tags": tags if isinstance(tags, list) else [tags],
                            },
                            chunk_id=f"{filepath}::{current_header}",
                        )
                    )

            # Start new section
            level = len(header_match.group(1))
            current_header = header_match.group(2).strip()
            current_header_level = level

            # Update header path
            if level == 1:
                header_path = [entity_title, current_header]
            elif level == 2:
                if len(header_path) > 1:
                    header_path = header_path[:1] + [current_header]
                else:
                    header_path.append(current_header)
            elif level == 3:
                if len(header_path) > 2:
                    header_path = header_path[:2] + [current_header]
                else:
                    header_path.append(current_header)

            # Include header in chunk text for context
            current_lines = [line]
        else:
            current_lines.append(line)

    # Don't forget the last section
    if current_lines:
        text = "\n".join(current_lines).strip()
        if len(text) >= min_chunk_size:
            chunks.append(
                Chunk(
                    text=text,
                    metadata={
                        "source": str(filepath),
                        "entity_type": entity_type,
                        "entity_title": entity_title,
                        "heading": current_header,
                        "heading_path": " > ".join(header_path),
                        "tags": tags if isinstance(tags, list) else [tags],
                    },
                    chunk_id=f"{filepath}::{current_header}",
                )
            )

    # If no chunks created (short note), create one from the whole body
    if not chunks and body.strip():
        chunks.append(
            Chunk(
                text=body.strip(),
                metadata={
                    "source": str(filepath),
                    "entity_type": entity_type,
                    "entity_title": entity_title,
                    "heading": "Full Note",
                    "heading_path": entity_title,
                    "tags": tags if isinstance(tags, list) else [tags],
                },
                chunk_id=f"{filepath}::full",
            )
        )

    return chunks


def chunk_file(filepath: str, min_chunk_size: int = 50) -> list[Chunk]:
    """Chunk a single markdown file."""
    from pathlib import Path

    path = Path(filepath)
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8")
    return chunk_by_headers(content, filepath, min_chunk_size)
