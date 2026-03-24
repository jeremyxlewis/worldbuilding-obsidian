# Troubleshooting Guide

Common errors and how to fix them.

## RAG / Search Issues

### "Missing dependency: chromadb"

**Cause:** RAG dependencies not installed.

**Fix:**
```bash
pip install -r requirements.txt
```

### "Missing dependency: sentence-transformers"

**Cause:** Embedding library not installed.

**Fix:**
```bash
pip install sentence-transformers
```

### "No results found" from search

**Cause:** Vault not indexed yet.

**Fix:**
```bash
python scripts/index_vault.py --vault /path/to/vault
```

### Search is slow with large vault

**Cause:** Single-threaded indexing.

**Fix:**
```bash
python scripts/index_vault.py --vault /path/to/vault --workers 4
```

### Index out of date

**Cause:** Files changed since last index.

**Fix:**
```bash
python scripts/index_vault.py --vault /path/to/vault --full
```

## Entity Creation Issues

### "Template not found"

**Cause:** Using entity type that doesn't have a template.

**Fix:** Check available types:
```bash
ls assets/templates/
```

### "File already exists"

**Cause:** Entity with that name already exists.

**Fix:** Use a different name or use `--force` flag if creating manually.

### Links not connecting entities

**Cause:** Case sensitivity or special characters in names.

**Fix:** Use simple names without special characters. Obsidian wikilinks are case-sensitive.

## Validation Issues

### "Vault not found"

**Cause:** Path doesn't exist or is incorrect.

**Fix:** Verify the path exists:
```bash
ls /path/to/vault
```

### Too many orphan warnings

**Cause:** New frontier zones naturally have orphans.

**Fix:**
```bash
python scripts/validate_world.py --vault /path --orphan-whitelist "frontier*" --orphan-ignore-tag "location/unexplored"
```

### Humanizer warnings on existing content

**Cause:** Old content may have AI patterns.

**Fix:** These are informational. Use as guidance for rewriting, not errors to fix immediately.

## Performance Issues

### Memory errors with large vault

**Cause:** Loading too much into memory.

**Fix:**
- Use pagination: `--offset 100 --n 20`
- Index with fewer workers: `--workers 2`
- Increase Python's memory limit if needed

### Validator is slow

**Cause:** Single-threaded validation on large vaults.

**Fix:** This is a known limitation. For very large vaults, consider:
- Running validation only on recently changed files
- Splitting validation into smaller regions

## Import/Export Issues

### CSV import fails

**Cause:** Wrong CSV format.

**Fix:** Ensure CSV has a `name` column:
```csv
name,description,role
Thoren,dwarven blacksmith,Shop Owner
```

### JSON import fails

**Cause:** Wrong JSON structure.

**Fix:** Use array format:
```json
[
  {"name": "Thoren", "description": "dwarven blacksmith"},
  {"name": "Elara", "description": "merchant"}
]
```

## General Tips

### Backing up your vault

Always backup before bulk operations:
```bash
python scripts/rollback.py --vault /path --create --description "Before bulk import"
```

### Getting help

1. Check the diagnostics output
2. Run with `--verbose` if available
3. Check Obsidian's console for JavaScript errors
4. Review the skill documentation in SKILL.md
