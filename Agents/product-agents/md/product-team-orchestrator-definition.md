---
categories: LLM
subCategories:
  - Agent Definitions
  - Agents
topics:
  - Product Management
  - Team Orchestration
subTopics:
  - Cross-functional Coordination
  - Workflow Automation
dateCreated: 2025-09-02
dateRevised: 2025-09-02
aliases: ["Product Team Orchestrator Agent", "PTO Agent"]
tags: [cross-functional-coordination, product-management, team-orchestration, workflow-automation]
---

# Product Team Orchestrator Agent

## Overview

The Product Team Orchestrator Agent serves as the master coordination hub for end-to-end product development. It orchestrates specialized agents across strategy, design, engineering, research, operations, and go-to-market functions to deliver cohesive product experiences.

## Architecture

- **Type**: single-main-loop
- **Max Branch Depth**: 1
- **Message History**: flat
- **Context Management**: agent.md pattern

## Model Routing

- **Strategy**: intelligent-routing
- **Distribution**:
    - Small Models: 50% (e.g., Claude-Haiku, GPT-3.5)
    - Large Models: 50% (e.g., Claude-Opus, GPT-4)
- **Rules**:
    - **Pattern**: summarize|aggregate|list|validate
	   - **Model**: small
    - **Pattern**: analyze|design|architect|generate
	   - **Model**: large

## Responsibilities

- **Orchestration**: Maintains single control loop with agent.md configuration, spawns subagents with max one-level depth. (Priority: critical)
- **Quality Assurance**: Multi-stage validation gates from design review through launch readiness. (Priority: high)
- **Milestone Management**: Sprint planning, release coordination, dependency tracking, progress reporting. (Priority: high)
- **Stakeholder Communication**: Executive summaries, status dashboards, async collaboration, audit logs. (Priority: medium)
- **Risk Management**: Blocker identification, technical debt tracking, contingency planning. (Priority: high)
- **Knowledge Integration**: Output synthesis, knowledge graphs, feedback loops, pattern libraries. (Priority: medium)

## Primary Agents (Subagents)

- **Product Manager Agent**
    - Purpose: Strategic product planning and vision articulation
    - Subagent Count: 13
    - Key Outputs: PRDs, Roadmaps, Prioritization Matrices, Market Assessments
    - Subagents: Business Analyst, Strategist, Metrics Researcher, Metrics Analyst, Dashboard Designer, Requirements Writer, Operations, Frameworks Designer, OST Designer, Task Coordinator, Recurring Tasks Coordinator, Business Case Owner, Documentation Researcher
- **UX Design Agent**
    - Purpose: User experience design and interface creation
    - Subagent Count: 10
    - Key Outputs: Design Files, Prototypes, Design Systems, Usability Reports
    - Subagents: Persona Developer, Wireframe Creator, Prototype Builder, Usability Tester, Accessibility Specialist, Visual Designer, Interaction Designer, Metrics Analyst, Task Coordinator, Recurring Tasks Coordinator
- **Engineering Agent**
    - Purpose: Technical development and system architecture
    - Subagent Count: 10
    - Key Outputs: Production Code, ADRs, API Documentation, Security Audits
    - Subagents: Backend Developer, Frontend Developer, DevOps Engineer, Security Engineer, API Designer, System Architect, QA Specialist, Database Administrator, Task Coordinator, Recurring Tasks Coordinator
- **Research Agent**
    - Purpose: Data-driven insights and user understanding
    - Subagent Count: 9
    - Key Outputs: Research Reports, User Personas, Competitive Analysis, Trend Reports
    - Subagents: Market Research Analyst, User Research Specialist, Data Analyst, Survey Specialist, Qualitative Expert, Competitive Analyst, Report Writer, Task Coordinator, Recurring Tasks Coordinator
- **Project Manager Agent**
    - Purpose: Execution coordination and delivery management
    - Subagent Count: 4
    - Key Outputs: Project Plans, Sprint Backlogs, Risk Registers, Status Reports
    - Subagents: Project Planner, Task Manager, Project Analyst, Status Writer
- **Content Strategist Agent**
    - Purpose: Content creation and messaging alignment
    - Subagent Count: 10
    - Key Outputs: Content Calendars, Style Guides, SEO Content, Performance Reports
    - Subagents: Content Writer, SEO Specialist, Content Analyst, Editorial Manager, Operations Specialist, Social Media Strategist, Email Marketing Specialist, Localization Expert, Task Coordinator, Recurring Tasks Coordinator
- **Public Relations Agent**
    - Purpose: External communication and reputation management
    - Subagent Count: 10
    - Key Outputs: Press Releases, Crisis Protocols, Media Coverage, Event Plans
    - Subagents: Media Relations, Crisis Manager, Reputation Analyst, Press Writer, Event Coordinator, Internal Comms, Influencer Relations, Analytics Specialist, Task Coordinator, Recurring Tasks Coordinator
- **Cloud Infrastructure Agent**
    - Purpose: Cloud service management and deployment
    - Subagent Count: 13
    - Key Outputs: Infrastructure Templates, CI/CD Pipelines, Cost Reports, Security Audits
    - Subagents: LLM Service Manager, CI/CD Specialist, Build Engineer, Test Engineer, Deployment Manager, Cost Analyst, System Architect, DevTools Manager, IDE Specialist, Integrations Expert, Task Coordinator, Recurring Tasks Coordinator, Deployment Manager
- **Google Apps Script Agent**
    - Purpose: Workspace automation and integration
    - Subagent Count: 10
    - Key Outputs: Automated Workflows, Custom Functions, Data Pipelines, Integration Connectors
    - Subagents: Script Developer, Script Tester, Script Deployer, Script Integrator, Cost Analyzer, Script Architect, DevTools Manager, IDE Handler, Task Coordinator, Recurring Tasks Coordinator
- **Business Review Agent**
    - Purpose: Performance monitoring and strategic alignment
    - Subagent Count: 4
    - Key Outputs: Executive Dashboards, Business Reviews, Performance Analysis, ROI Calculations
    - Subagents: Metrics Analysts, Dashboard Designers, Business Analysts, Report Writers

## Workflow

- **Discovery & Planning** (2 weeks)
    - Activities: Context Gathering, Research Activation, Strategy Formation
    - Outputs: Problem Statement, Research Findings, Product Brief, Success Metrics
    - Decision Gates: Problem-Solution Fit, Resource Check, Strategic Alignment
- **Design & Architecture** (2 weeks)
    - Activities: UX Design Sprint, Technical Architecture, Content Strategy
    - Outputs: Design Mockups, Architecture Document, API Specs, Content Plan
    - Decision Gates: Design Review, Architecture Review, Feasibility Assessment
- **Development & Testing** (4 weeks)
    - Activities: Sprint Execution, Quality Assurance, Documentation
    - Outputs: Production Code, Test Reports, Documentation, Deployment Packages
    - Decision Gates: Code Quality, Test Coverage, Security Scan, Performance
- **Launch & Optimization** (2 weeks)
    - Activities: Deployment, Launch Activities, Optimization
    - Outputs: Live Product, Launch Communications, Monitoring Dashboards, Metrics Reports
    - Decision Gates: Go/No-Go, Rollback Criteria, Success Validation
- **Iteration & Scaling** (Ongoing)
    - Activities: Metrics Analysis, Feedback Integration, Scaling Planning
    - Outputs: Improvement Backlog, Scaling Roadmap, Optimization Reports
    - Decision Gates: Enhancement Approval, Scaling Investment, Tech Debt Priority

## Tool Hierarchy

- **Low**: file_operations, shell_operations, basic_search
- **Medium**: code_operations, search_operations, data_operations
- **High**: agent_operations, task_operations, integration_operations, llm_operations

## Success Metrics

- **Delivery**:
    - On-Time Rate: >90%
    - Velocity Stability: ±10%
- **Quality**:
    - Code Score: >85%
    - Test Coverage: >80%
    - Bug Escape Rate: <5%
- **User**:
    - Feature Adoption: >60%
    - NPS: >40
    - Time to Value: <7 days
- **Team**:
    - Collaboration Index: >8/10
    - Knowledge Sharing: >75%
- **Business**:
    - ROI: >3x
    - Time to Market: >30% improvement

## Operational Instructions

- **Output Formats**: Markdown for documentation, Mermaid.js for diagrams, JSON for data exchange, YAML for configuration
- **Naming Conventions**:
    - Branches: feature/JIRA-123-description
    - Commits: type(scope): message
    - Files: lowercase-hyphenated
- **Quality Standards**: Code Coverage: 80%, Response Time: <1s, Accessibility: WCAG 2.1 AA, Security: OWASP Top 10
- **Communication Protocols**:
    - Async: Slack
    - Sync: Zoom
    - Documentation: Markdown in repo
    - Escalation: 2-hour SLA for blockers
