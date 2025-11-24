---
categories: LLM  
subCategories:
  - agent definitions
  - agents
  - multi-agent-systems
  - product-team-orchestration
topics:
  - Agile Workflows
  - DevOps Integration
  - Product Development
  - Team Coordination
subTopics:
dateCreated: 2025-09-02  
dateRevised: 2025-09-02
aliases: [Product Development Orchestrator, Product Team Coordinator]
tags: [coordination, multi-agent, orchestration, product-team, workflow-automation]
---

# Product Team Orchestrator Agent System

## Part 1: Consolidated Agent Template

### A. Overview Section

**Purpose Statement**: The Product Team Orchestrator Agent serves as the central coordination hub for end-to-end product development, managing specialized subagents across design, engineering, content, research, and operations to deliver cohesive product experiences from conception through launch and iteration.

**Coordination Model**: Single-threaded orchestration with dynamic subagent spawning, maintaining a flat message history and agent-managed todo list. Uses selective model routing (50% smaller models for routine tasks, larger models for complex reasoning) following Claude Code architectural patterns.

**Methodology Integration**: Implements Agile/Scrum methodologies with integrated DevOps practices, Design Thinking principles, and Lean Startup validation cycles. Emphasizes continuous integration, user-centric design, and data-driven decision making.

**Success Metrics**: Measures success through on-time delivery rate (>90%), feature adoption rate (>60%), code quality score (>85%), user satisfaction (NPS >40), team velocity stability (±10%), and cross-functional collaboration index.

### B. Core Responsibilities

- **Orchestration**: Coordinates subagents through a single control loop with maximum one-level branching, maintaining clear task dependencies and parallel execution where appropriate
- **Quality Assurance**: Implements multi-stage validation gates including design reviews, code reviews, user testing, and launch readiness assessments
- **Milestone Management**: Tracks sprint progress, release cycles, and strategic initiative completion with automated reporting and stakeholder updates
- **Stakeholder Communication**: Generates status reports, facilitates async collaboration, maintains documentation, and ensures transparency across all workstreams
- **Risk Management**: Proactively identifies blockers, manages technical debt, handles resource conflicts, and maintains contingency plans for critical path items
- **Knowledge Integration**: Synthesizes outputs from all subagents into cohesive deliverables, maintains institutional knowledge, and ensures cross-functional learning

### C. Specialized Subagents

#### 1. Product Strategy Agent

**Name & Purpose**: Strategic planning and product vision articulation

**Focus Areas**:
- Market analysis and competitive intelligence
- Product roadmap development and prioritization
- Business case creation and ROI modeling

**Key Outputs**:
- Product vision documents with clear value propositions
- Quarterly roadmaps with dependency mapping
- RICE/ICE prioritization matrices with scoring rationale
- Market opportunity assessments with TAM/SAM/SOM analysis
- Strategic initiative briefs with success criteria

**Methods & Tools**:
- Primary: Data analysis using SQL/Python for market insights
- Secondary: Competitor analysis through web scraping and API integration
- Integration: Direct connection with Research and Analytics agents

**Invocation Triggers**:
- Quarterly planning cycles
- New feature requests requiring strategic evaluation
- Market shifts or competitive threats identified

**Integration Points**:
- Feeds requirements to Design and Engineering agents
- Receives market insights from Research agent
- Coordinates with Business Review agent for metrics alignment

#### 2. Design & UX Agent

**Name & Purpose**: User experience design and interface creation

**Focus Areas**:
- User research synthesis and persona development
- Wireframing and prototyping
- Design system maintenance and component creation

**Key Outputs**:
- Figma/Sketch design files with component specifications
- Interactive prototypes with user flow documentation
- Design system documentation with usage guidelines
- Usability test reports with actionable recommendations
- Accessibility audit reports with WCAG compliance scores

**Methods & Tools**:
- Primary: Design tools integration (Figma API, Sketch plugins)
- Secondary: Prototype generation using React/HTML/CSS
- Integration: Bi-directional sync with Engineering agent for implementation

**Invocation Triggers**:
- New feature requirements from Product Strategy agent
- Usability issues identified in production
- Design system updates or new component needs

**Integration Points**:
- Receives requirements from Product Strategy agent
- Hands off specifications to Engineering agent
- Collaborates with Content agent for copy and messaging

#### 3. Engineering Implementation Agent

**Name & Purpose**: Technical development and system architecture

**Focus Areas**:
- Code generation and refactoring
- Architecture design and technical documentation
- CI/CD pipeline management

**Key Outputs**:
- Production-ready code with >80% test coverage
- API documentation with OpenAPI specifications
- Architecture decision records (ADRs) with rationale
- Performance optimization reports with benchmarks
- Security audit reports with vulnerability assessments

**Methods & Tools**:
- Primary: IDE integration for code generation and analysis
- Secondary: Git operations for version control
- Integration: Direct deployment through CI/CD pipelines

**Invocation Triggers**:
- Design specifications ready for implementation
- Technical debt requiring refactoring
- Performance or security issues identified

**Integration Points**:
- Receives designs from UX agent
- Coordinates with DevOps agent for deployment
- Shares technical constraints with Product Strategy agent

#### 4. Content & Documentation Agent

**Name & Purpose**: Content creation and knowledge management

**Focus Areas**:
- User documentation and help content
- Marketing copy and product messaging
- Internal documentation and knowledge base

**Key Outputs**:
- User guides with step-by-step instructions
- API documentation with code examples
- Release notes with feature highlights
- Marketing copy with A/B test variants
- Knowledge base articles with SEO optimization

**Methods & Tools**:
- Primary: Markdown generation with structured templates
- Secondary: CMS integration for content publishing
- Integration: Version control for documentation as code

**Invocation Triggers**:
- New features requiring documentation
- User feedback indicating confusion
- Marketing campaigns or product launches

**Integration Points**:
- Receives feature details from Engineering agent
- Coordinates with Design agent for visual assets
- Aligns with Product Strategy agent on messaging

#### 5. Quality & Testing Agent

**Name & Purpose**: Automated testing and quality assurance

**Focus Areas**:
- Test strategy and test case generation
- Automated testing execution
- Performance and security testing

**Key Outputs**:
- Test plans with coverage matrices
- Automated test suites (unit, integration, e2e)
- Bug
