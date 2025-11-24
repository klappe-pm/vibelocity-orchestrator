---
categories:
  - LLM
subCategories:
  - agent definitions
  - agent diagrams
  - agents
  - subagent defintions
topics:
subTopics:
dateCreated: 2025-09-02
dateRevised: 2025-09-02
aliases: []
tags: []
---

# Agent and Sub-Agent Definition Requirements

This document outlines the standardized requirements for defining agents and subagents in the product team ecosystem. Each agent and subagent must have comprehensive, technically detailed documentation in multiple formats, stored in a logical directory structure (e.g., `/agents/` for top-level agents, `/agents/subagents/` for subagents). The goal is to ensure clarity, consistency, and reusability across all definitions.

## Note

These are basic definition that illustrate the frameworks required. Agent and Sub-Agents must be defined granularly, in detail, and include the following basic structure.

### 1. Plain English Definition File

- **Description**: A detailed, technically oriented file written in plain English, describing the agent or subagent's purpose, responsibilities, focus areas, interactions, partnerships, operational guidelines, and technical specifics (e.g., algorithms, frameworks, tools, output formats).
- **Format**: Markdown with the following structure:
    - H1 header matching the filename (without extension).
    - Sections: Overview, Responsibilities, Focus, Subagents (if applicable), Partnerships, Operational Instructions.
    - Emphasize technical depth, such as data handling processes, integration points, or specific methodologies.
- **Filename**:
    - Agents: Lowercase, hyphenated (e.g., `product-manager-agent-definition.md`).
    - Subagents: Parent agent name followed by subagent name (e.g., `product-manager-agent-business-analyst-definition.md`).
- **Example Structure**:

    ```markdown
    # product-manager-agent-definition
    
    ## Overview
    Defines the Product Manager Agent, responsible for synthesizing workstreams and aligning with product goals.
    
    ## Responsibilities
    - Set product strategy.
    - Prioritize features using RICE framework.
    
    ## Focus
    - Interdisciplinary coordination across business, technology, and design.
    
    ## Subagents
    - Product Business Analyst
    - Product Strategist
    
    ## Partnerships
    - Collaborates with UX Design and Engineering Agents.
    
    ## Operational Instructions
    - Outputs PRDs in Markdown.
    - Uses Mermaid.js for roadmaps.
    ```

### 2. XML Format Definition

- **Description**: A structured XML file encapsulating the same details as the plain English definition, using tagged elements for machine-readable format.
- **Format**:
    - Root element: `<agent>` for agents, `<subagent>` for subagents.
    - Child elements: `<name>`, `<description>`, `<responsibilities>` (as a `<list>`), `<focus>`, `<partnerships>`, `<subagents>` (if applicable).
    - Technical details nested in relevant elements (e.g., `<frameworks>` under `<responsibilities>`).
- **Filename**: Matches plain English naming (e.g., `product-manager-agent-definition.xml` or `product-manager-agent-business-analyst-definition.xml`).
- **Example**:

    ```xml
    <agent>
        <name>Product Manager Agent</name>
        <description>Synthesizes workstreams and defines product vision.</description>
        <responsibilities>
            <list>
                <item>Set product strategy</item>
                <item>Prioritize features</item>
            </list>
            <frameworks>
                <item>RICE</item>
                <item>Lean Startup</item>
            </frameworks>
        </responsibilities>
        <focus>Interdisciplinary coordination</focus>
        <partnerships>
            <item>UX Design Agent</item>
            <item>Engineering Agent</item>
        </partnerships>
        <subagents>
            <item>Product Business Analyst</item>
        </subagents>
    </agent>
    ```

### 3. JSON Format Definition

- **Description**: A JSON object mirroring the plain English content, designed for programmatic access.
- **Format**:
    - Keys: `"name"`, `"description"`, `"responsibilities"` (array), `"focus"`, `"partnerships"` (array), `"subagents"` (array of objects, if applicable), `"operationalInstructions"`.
    - Technical details in nested objects (e.g., `"frameworks"` array under `"responsibilities"`).
    - Ensure valid JSON syntax with proper quotes and structure.
- **Filename**: Matches plain English naming (e.g., `product-manager-agent-definition.json` or `product-manager-agent-business-analyst-definition.json`).
- **Example**:

    ```json
    {
        "name": "Product Manager Agent",
        "description": "Synthesizes workstreams and defines product vision.",
        "responsibilities": [
            "Set product strategy",
            "Prioritize features",
            {
                "frameworks": ["RICE", "Lean Startup"]
            }
        ],
        "focus": "Interdisciplinary coordination",
        "partnerships": ["UX Design Agent", "Engineering Agent"],
        "subagents": [
            {"name": "Product Business Analyst"}
        ],
        "operationalInstructions": "Outputs PRDs in Markdown, uses Mermaid.js for roadmaps."
    }
    ```

### 4. YAML Frontmatter

- **Description**: All definition files (Markdown, XML, JSON) must include YAML frontmatter at the top for metadata consistency.
- **Format**:
    - Open with `---` on the first line, close with `---` on a new line.
    - Skip one blank line, then add H1 header matching the filename (without extension).
    - Keys (in this order):
	   - `categories`: Always set to `LLM`.
	   - `subCategories`: Always includes `Agents`, `Agent Definitions`.
	   - `topics`: Array of relevant topics (e.g., `["Product Management", "UX Design"]`; empty `[]` if none).
	   - `subTopics`: Array of subtopics (e.g., `["Metrics Analysis", "Framework Design"]`; empty `[]` if none).
	   - `dateCreated`: File creation date in YYYY-MM-DD (e.g., `2025-09-02`).
	   - `dateRevised`: Initial value empty (`""`) or current date; update on revisions (YYYY-MM-DD).
	   - `aliases`: Array of alternative names (e.g., `["PM Agent", "Product Lead"]`; empty `[]` if none).
	   - `tags`: Array of lowercase, hyphenated tags (e.g., `["product", "strategy", "metrics"]`).
- **Example**:

    ```yaml
    ---
    categories: LLM
    subCategories: 
      - Agents
      - Agent Definitions
    topics: ["Product Management"]
    subTopics: ["Strategy", "Metrics"]
    dateCreated: 2025-09-02
    dateRevised: ""
    aliases: ["PM Agent"]
    tags: 
      - product
      - strategy
      - metrics
    ---
    
    # product-manager-agent-definition
    ```

### 5. Filenames

- **Description**: Use simple, descriptive naming conventions for all files to ensure clarity and consistency.
- **Rules**:
    - **Agents**: Lowercase, hyphenated (e.g., `product-manager-agent-definition.md`).
    - **Subagents**: Parent agent name followed by subagent name (e.g., `product-manager-agent-business-analyst-definition.md`).
    - Applies to all formats (Markdown, XML, JSON).
    - Group files in subdirectories named after the agent (e.g., `/agents/product-manager-agent/` containing `definition.md`, `definition.xml`, `definition.json`).
- **Example Directory Structure**:

    ```javascript
    /agents/
      /product-manager-agent/
        product-manager-agent-definition.md
        product-manager-agent-definition.xml
        product-manager-agent-definition.json
        /subagents/
          product-manager-agent-business-analyst-definition.md
          product-manager-agent-business-analyst-definition.xml
          product-manager-agent-business-analyst-definition.json
    ```
