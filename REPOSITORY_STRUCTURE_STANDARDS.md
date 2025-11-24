# Repository Structure Standards

This document mandates file naming conventions, folder structures, and file storage locations for the Vibelocity Orchestrator repository. **All contributions must adhere to these standards.**

**Version:** 1.0.0  
**Last Updated:** 2025-01-15  
**Status:** MANDATORY - All files must follow these conventions

---

## Table of Contents

1. [Root Directory Structure](#root-directory-structure)
2. [File Naming Conventions](#file-naming-conventions)
3. [Folder Organization Standards](#folder-organization-standards)
4. [Agent Definition Structure](#agent-definition-structure)
5. [Documentation Standards](#documentation-standards)
6. [Configuration Files](#configuration-files)
7. [Code Organization](#code-organization)
8. [Migration and Versioning](#migration-and-versioning)
9. [Prohibited Patterns](#prohibited-patterns)
10. [Enforcement](#enforcement)

---

## Root Directory Structure

### Mandatory Root-Level Files

```
vibelocity-orchestrator/
├── .gitignore                          # Git ignore patterns (MANDATORY)
├── LICENSE.md                          # Project license (MANDATORY)
├── README.md                           # Project overview (MANDATORY)
├── REPOSITORY_STRUCTURE_STANDARDS.md   # This file (MANDATORY)
├── CONTRIBUTING.md                     # Contribution guidelines (RECOMMENDED)
├── CHANGELOG.md                        # Version history (RECOMMENDED)
└── .github/                            # GitHub workflows (if applicable)
    └── workflows/
```

### Root-Level Directories (Standard Structure)

```
vibelocity-orchestrator/
├── Agents/                             # Legacy agent definitions (v1) - READ-ONLY
├── Agents-v2/                          # Current agent definitions (v2) - ACTIVE
├── Developer Docs/                     # Developer documentation
├── scripts/                            # Utility scripts (NEW - to be created)
├── tests/                              # Test files (NEW - to be created)
├── tools/                              # Development tools (NEW - to be created)
└── .github/                            # GitHub configuration (if applicable)
```

**DO NOT CREATE:**
- `gitignore/` folder (this should be `.gitignore` file, not a folder)
- Temporary files at root level
- Personal/private files at root level

---

## File Naming Conventions

### General Rules

1. **Use lowercase with hyphens (kebab-case)** for all files and directories
   - ✅ `agent-definition.yaml`
   - ✅ `business-review-agent-definition.yaml`
   - ❌ `Agent Definition.yaml`
   - ❌ `agent_definition.yaml`
   - ❌ `agentDefinition.yaml`

2. **Use descriptive, full words** (avoid abbreviations unless standard)
   - ✅ `engineering-agent-database-administrator-definition.yaml`
   - ❌ `eng-agent-dba-def.yaml`

3. **File extensions must match content type**
   - `.yaml` or `.yml` for YAML files
   - `.md` for Markdown files
   - `.json` for JSON files
   - `.py` for Python scripts
   - `.sh` for shell scripts

### Agent Definition Files

**Pattern:** `{agent-category}-{agent-name}-definition.{ext}`

**Examples:**
- ✅ `engineering-agent-backend-developer-definition.yaml`
- ✅ `business-review-agent-definition.yaml`
- ✅ `cloud-agent-aws-task-coordinator-definition.yaml`
- ❌ `backend-developer.yaml` (missing category prefix)
- ❌ `engineering_backend.yaml` (wrong separator, missing suffix)

**Rules:**
- Primary agent: `{category}-agent-definition.yaml`
- Sub-agent: `{category}-agent-{sub-role}-definition.yaml`
- Coordinator: `{category}-agent-{type}-coordinator-definition.yaml`
- Recurring tasks: `{category}-agent-recurring-tasks-coordinator-definition.yaml`

### Documentation Files

**Pattern:** `{PREFIX}-{descriptive-name}.md`

**Prefixes:**
- `AGENT_` - Agent specifications and definitions
- `REPOSITORY_` - Repository standards (this file)
- `CHANGELOG` - Version history
- `CONTRIBUTING` - Contribution guidelines
- `README` - Overview documents

**Examples:**
- ✅ `AGENT_SPECIFICATION_v2.1.md`
- ✅ `REPOSITORY_STRUCTURE_STANDARDS.md`
- ✅ `README.md`
- ❌ `agent-spec-v2.1.md` (wrong prefix)
- ❌ `Repository Structure.md` (spaces, wrong case)

### Script Files

**Pattern:** `{purpose}-{action}.{ext}`

**Examples:**
- ✅ `orchestrate-transformations.py`
- ✅ `validate-agents.sh`
- ✅ `setup-environment.sh`
- ❌ `script.py` (not descriptive)
- ❌ `transformation_script.py` (wrong separator)

### Configuration Files

**Pattern:** Standard names with appropriate extensions

**Examples:**
- ✅ `.gitignore` (with leading dot)
- ✅ `pyproject.toml`
- ✅ `requirements.txt`
- ✅ `docker-compose.yml`
- ❌ `gitignore.txt` (should be `.gitignore`)
- ❌ `config.json` (too generic)

---

## Folder Organization Standards

### Agents-v2/ Directory Structure

**MANDATORY STRUCTURE:**

```
Agents-v2/
├── {agent-category}/                   # One folder per agent category
│   └── yaml/                           # ONLY yaml format allowed
│       ├── {category}-agent-definition.yaml
│       ├── {category}-agent-{sub-agent}-definition.yaml
│       └── ...
├── research/                           # Research and planning documents
│   ├── {topic}-research.md
│   └── ...
├── {PREFIX}_{NAME}.md                  # Cross-cutting documentation
│   ├── AGENT_INDEX.md
│   ├── AGENT_MAPPING.md
│   └── OLLAMA_LOCAL_MODELS.md
└── validation-report.json              # Generated (should be in .gitignore)
```

**Rules:**
- ✅ ONLY `.yaml` files in agent category folders
- ✅ NO `.json`, `.xml`, `.toml`, or `.md` files in agent category folders
- ✅ NO scripts, logs, or temporary files in `Agents-v2/`
- ✅ Research documents go in `Agents-v2/research/`
- ✅ Index and mapping files at root of `Agents-v2/`

**PROHIBITED:**
- ❌ `Agents-v2/*.log` (logs should be in `.gitignore`)
- ❌ `Agents-v2/*.py` (scripts should be in `scripts/`)
- ❌ `Agents-v2/validation-report.json` (generated file, in `.gitignore`)
- ❌ Mixed formats in agent folders

### Developer Docs/ Directory Structure

**MANDATORY STRUCTURE:**

```
Developer Docs/
├── Architecture/
│   └── {descriptive-name}.md
├── Commands/
│   └── {command-category}.md
├── Development/
│   └── {topic}.md
├── Features/
│   └── {feature-name}.md
├── Getting Started/
│   └── {tutorial-name}.md
├── Models/
│   └── {model-topic}.md
└── Testing/
    └── {test-category}.md
```

**Rules:**
- ✅ All files must be `.md` (Markdown)
- ✅ Use Title Case for folder names
- ✅ Use descriptive names with hyphens for files
- ✅ One topic per file

### Scripts/ Directory (To Be Created)

**MANDATORY STRUCTURE:**

```
scripts/
├── setup/
│   └── {setup-script}.sh
├── validation/
│   └── {validation-script}.py
├── transformation/
│   └── {transformation-script}.py
└── utilities/
    └── {utility-script}.{ext}
```

**Rules:**
- ✅ All scripts must have appropriate shebang
- ✅ Python scripts: `#!/usr/bin/env python3`
- ✅ Shell scripts: `#!/bin/bash` or `#!/usr/bin/env bash`
- ✅ Scripts must be executable (`chmod +x`)

---

## Agent Definition Structure

### File Location Rules

**MANDATORY:**
- All v2 agent definitions: `Agents-v2/{category}/yaml/`
- One agent category per top-level folder
- Only YAML format allowed

**Example:**
```
Agents-v2/
├── engineering-agent/
│   └── yaml/
│       ├── engineering-agent-definition.yaml
│       ├── engineering-agent-backend-developer-definition.yaml
│       └── engineering-agent-frontend-developer-definition.yaml
├── business-review-agent/
│   └── yaml/
│       ├── business-review-agent-definition.yaml
│       └── ...
```

**FORBIDDEN:**
- ❌ Agent definitions outside of `Agents-v2/`
- ❌ Multiple formats for same agent (v2 is YAML-only)
- ❌ Agent files directly in category folder (must be in `yaml/` subfolder)

### Agent Category Naming

**Pattern:** `{category-name}-agent`

**Standard Categories:**
- `business-review-agent`
- `cloud-agent`
- `content-agent`
- `context-agent`
- `engineering-agent`
- `google-apps-script-agent`
- `product-agents` (note: plural)
- `project-agent`
- `public-relations-agent`
- `research-agent`
- `ux-agent`

**Rules:**
- ✅ Use kebab-case
- ✅ Always end with `-agent` (singular) or `-agents` (plural for multi-agent categories)
- ✅ Be descriptive (e.g., `google-apps-script-agent`, not `gas-agent`)

---

## Documentation Standards

### Markdown File Naming

**Pattern:** `{PREFIX}_{Descriptive-Title}.md` or `{descriptive-name}.md`

**Prefixes for Root-Level Docs:**
- `AGENT_` - Agent specifications
- `REPOSITORY_` - Repository standards
- `CHANGELOG` - Version history
- `CONTRIBUTING` - Contribution guidelines
- `README` - Overview documents

**Prefixes for Sub-Directories:**
- Use descriptive names without prefixes
- Use Title Case for file names in `Developer Docs/`

**Examples:**
- ✅ `Agents-v2/AGENT_INDEX.md` (root-level agent doc)
- ✅ `Developer Docs/Architecture/High-Level Architecture.md`
- ✅ `README.md` (standard name)
- ❌ `Agents-v2/agent-index.md` (wrong prefix format)
- ❌ `Developer Docs/architecture.md` (should be in subdirectory)

### Documentation Content Structure

All Markdown documentation must include:

1. **Title** (H1): Clear, descriptive title
2. **Metadata** (optional frontmatter for YAML docs)
3. **Table of Contents** (for documents >500 lines)
4. **Sections** with clear headings (H2, H3)
5. **Examples** where applicable
6. **Last Updated** date in footer

---

## Configuration Files

### Location Rules

**Root-Level Configs:**
- ✅ `.gitignore` (with leading dot)
- ✅ `LICENSE.md`
- ✅ `README.md`
- ✅ `pyproject.toml` (if Python project)
- ✅ `requirements.txt` (if Python project)
- ✅ `docker-compose.yml` (if using Docker)

**Environment Configs:**
- ❌ DO NOT commit `.env` files
- ❌ DO NOT commit `*.local.*` files
- ✅ Use `.env.example` as template
- ✅ Document required environment variables in `README.md`

### Naming Rules

**Standard Names (DO NOT RENAME):**
- `.gitignore` (exact name required)
- `LICENSE.md` (or `LICENSE`)
- `README.md` (exact name required)
- `CHANGELOG.md` (standard name)
- `CONTRIBUTING.md` (standard name)

---

## Code Organization

### Python Files

**Location:**
- Main code: `{module-name}/` (to be created)
- Scripts: `scripts/`
- Tests: `tests/`

**Naming:**
- ✅ Use `snake_case` for Python files and modules
- ✅ Use `PascalCase` for class names
- ✅ Use descriptive names

**Examples:**
- ✅ `scripts/orchestrate_transformations.py`
- ✅ `scripts/validate_agents.py`
- ❌ `Agents-v2/orchestrate_transformations.py` (wrong location)

### Shell Scripts

**Location:**
- ✅ `scripts/` directory

**Naming:**
- ✅ Use kebab-case: `setup-environment.sh`
- ✅ Include `.sh` extension
- ✅ Make executable

---

## Migration and Versioning

### Legacy Files (Agents/)

**Status:** READ-ONLY
- ✅ Keep for reference
- ❌ DO NOT modify
- ❌ DO NOT add new files
- ✅ Reference in migration documentation

### Active Files (Agents-v2/)

**Status:** ACTIVE DEVELOPMENT
- ✅ Only YAML format
- ✅ Follow v2 specification
- ✅ All new agents go here

### Versioning Strategy

**File Names:**
- ✅ Do NOT include version numbers in filenames
- ✅ Use folders for version separation (`Agents/` vs `Agents-v2/`)
- ✅ Document versions in content/metadata

**Examples:**
- ✅ `Agents/` (v1) and `Agents-v2/` (v2)
- ❌ `agent-v1.yaml` and `agent-v2.yaml` (wrong approach)

---

## Prohibited Patterns

### File and Folder Names

**FORBIDDEN:**
- ❌ Spaces in file/folder names (use hyphens)
- ❌ Special characters except hyphens and dots: `!@#$%^&*()`
- ❌ Uppercase in folder names (use kebab-case)
- ❌ Abbreviations unless standard (e.g., `README.md`, `API.md`)
- ❌ Version numbers in filenames (use folders instead)
- ❌ Personal names or identifiers
- ❌ Temporary or scratch file names: `temp.md`, `test.txt`, `scratch.py`

### File Locations

**FORBIDDEN:**
- ❌ Root-level temporary files
- ❌ Root-level personal files
- ❌ Scripts in `Agents-v2/` (use `scripts/`)
- ❌ Logs in repository (use `.gitignore`)
- ❌ Mixed formats in agent folders
- ❌ Documentation mixed with code without organization

### Content

**FORBIDDEN:**
- ❌ API keys, secrets, or credentials in any file
- ❌ Personal information in public files
- ❌ Hardcoded paths (use relative paths or environment variables)
- ❌ System-specific configurations (use `.gitignore`)

---

## Enforcement

### Pre-Commit Checks

Before committing, verify:

1. ✅ File names follow kebab-case or Title Case standards
2. ✅ Files are in correct directories
3. ✅ No prohibited patterns in file names
4. ✅ No temporary or personal files
5. ✅ Agent definitions in correct format and location
6. ✅ Documentation follows structure standards

### Automated Validation

**Future Implementation:**
- Script to validate file naming: `scripts/validate-structure.py`
- Pre-commit hooks to check conventions
- CI/CD checks for structure compliance

### Review Checklist

**Pull Request Reviewers Must Check:**
- [ ] File names follow conventions
- [ ] Files are in correct directories
- [ ] No prohibited patterns
- [ ] Agent definitions follow structure
- [ ] Documentation is properly formatted
- [ ] No credentials or secrets committed

---

## Migration Guidelines

### Moving Existing Files

**For files that don't conform:**

1. **Agent Definitions:**
   - Move to `Agents-v2/{category}/yaml/`
   - Rename to follow convention
   - Convert to YAML if needed

2. **Scripts:**
   - Move to `scripts/` directory
   - Organize into subdirectories by purpose

3. **Documentation:**
   - Move to appropriate `Developer Docs/` subdirectory
   - Rename to follow Title Case convention
   - Update cross-references

4. **Temporary/Generated Files:**
   - Add to `.gitignore`
   - Remove from repository

### Renaming Strategy

**Process:**
1. Create new file with correct name
2. Copy content from old file
3. Update all cross-references
4. Commit new file
5. Remove old file in separate commit
6. Update documentation

---

## Special Cases

### Obsidian Configuration

**IF using Obsidian for documentation:**
- ✅ Keep `.obsidian/` in `.gitignore` (personal workspace)
- ❌ DO NOT commit workspace configurations
- ✅ Consider using `.obsidian.example/` if sharing config

### Generated Files

**Files that can be regenerated:**
- Validation reports
- Build artifacts
- Log files
- Coverage reports

**Action:** Add to `.gitignore`, document generation process

### Large Files

**Model files, datasets, etc.:**
- ❌ DO NOT commit to repository
- ✅ Use Git LFS if needed
- ✅ Document location in `README.md`
- ✅ Provide download instructions

---

## Quick Reference

### File Naming
- ✅ `agent-definition.yaml` (kebab-case, lowercase)
- ✅ `README.md` (standard name, uppercase)
- ✅ `AGENT_SPECIFICATION_v2.1.md` (uppercase prefix)
- ❌ `Agent Definition.yaml` (spaces, mixed case)
- ❌ `agent_definition.yaml` (underscores)

### Directory Structure
- ✅ `Agents-v2/{category}/yaml/` (agent definitions)
- ✅ `Developer Docs/{Category}/` (documentation)
- ✅ `scripts/{purpose}/` (scripts)
- ❌ `Agents-v2/{category}/*.py` (scripts in agent folder)

### Location Rules
- Agent definitions → `Agents-v2/{category}/yaml/`
- Documentation → `Developer Docs/`
- Scripts → `scripts/`
- Configs → Root level (standard names)
- Tests → `tests/`

---

## Changelog

### Version 1.0.0 (2025-01-15)
- Initial repository structure standards
- Defined file naming conventions
- Established folder organization rules
- Mandated agent definition structure
- Set documentation standards

---

## Questions or Clarifications

If you have questions about these standards:
1. Check this document first
2. Review existing repository structure
3. Open an issue for clarification
4. Propose changes via pull request

**Remember:** Consistency is key. When in doubt, follow existing patterns in the repository.

