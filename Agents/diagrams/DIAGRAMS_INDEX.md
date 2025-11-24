# Agent Diagrams Index

## Overview
This directory contains comprehensive Mermaid.js diagrams showing the relationships and workflows between agents and their sub-agents in the LLM Agents Framework.

## Diagram Files Created

### 1. Agent-to-Agent Relationships
**File**: `agent-to-agent-relationships.md`
- **ERD**: Shows data relationships between all 11 primary agents
- **Class Diagram**: Illustrates the inheritance and composition structure
- **Sequence Diagram**: Demonstrates inter-agent communication flow

### 2. Product Manager Agent SubAgent Relationships
**File**: `product-manager-subagent-relationships.md`
- **ERD**: PM Agent relationships with 14 sub-agents
- **Class Diagram**: PM sub-agent architecture and methods
- **Sequence Diagram**: Product feature development workflow

### 3. Engineering Agent SubAgent Relationships
**File**: `engineering-subagent-relationships.md`
- **ERD**: Engineering Agent relationships with 11 sub-agents
- **Class Diagram**: Engineering sub-agent architecture
- **Sequence Diagram**: Feature implementation workflow

## Remaining Agents to Document

### Priority 1 - Core Product Development
- [ ] Research Agent (10 sub-agents)
- [ ] UX Design Agent (9 sub-agents)
- [ ] Business Review Agent (11 sub-agents)

### Priority 2 - Supporting Functions
- [ ] Content Strategy Agent (11 sub-agents)
- [ ] Project Management Agent (5 sub-agents)
- [ ] Context Agent (12 sub-agents)

### Priority 3 - Technical Infrastructure
- [ ] Cloud Agents (AWS, Azure, GCP - 30+ sub-agents)
- [ ] Google Apps Script Agent (11 sub-agents)
- [ ] Public Relations Agent (2 sub-agents)

## Diagram Types per Agent

Each agent documentation includes:
1. **Entity Relationship Diagram (ERD)**
   - Data models and relationships
   - Cardinality and dependencies
   - Key attributes

2. **Class Diagram**
   - Object-oriented structure
   - Methods and properties
   - Inheritance relationships

3. **Sequence Diagram**
   - Workflow interactions
   - Message passing
   - Process phases

## Color Coding Standards

Consistent color scheme across all diagrams:
- **Blue** (rgb(240, 240, 255)): Initialization/Setup phases
- **Red** (rgb(255, 240, 240)): Critical decision phases
- **Green** (rgb(240, 255, 240)): Execution phases
- **Yellow** (rgb(255, 255, 240)): Documentation phases
- **Cyan** (rgb(240, 255, 255)): Finalization phases

## How to View Diagrams

These Mermaid.js diagrams can be viewed in:
- GitHub (automatic rendering)
- VS Code with Mermaid extension
- Obsidian with Mermaid support
- Online Mermaid Live Editor
- Any Markdown viewer with Mermaid support

## Usage Guidelines

1. **For Development Teams**: Use class diagrams to understand agent architecture
2. **For Product Managers**: Use sequence diagrams to understand workflows
3. **For System Architects**: Use ERDs to understand data relationships
4. **For Integration**: Reference agent-to-agent diagrams for communication patterns

## Next Steps

To complete the diagram documentation:
1. Create remaining agent-to-subagent diagrams
2. Add flow charts for each agent (as per requirements)
3. Create consolidated system architecture diagram
4. Add deployment and infrastructure diagrams
5. Create user journey diagrams for key workflows

---

*Last Updated: 2025-09-03*
*Total Diagrams: 9 (3 files × 3 diagram types)*
*Agents Documented: 3 of 11 primary agents*
