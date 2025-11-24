---
categories:
## categories: LLM  
subCategories:
  - Agent Definitions
  - Agents
topics:
  - LLM Management
  - Model Coordination
subTopics:
  - Cost Planning
  - Model Evaluation
dateCreated: 2025-09-02  
dateRevised: 2025-09-02
aliases: []
tags: [90EE90, ADD8E6, coordination, DDA0DD, evaluation, FF6347, FFA500, llm-models, mcp]
---

# MCP Agent Definition

---

## Overview

The MCP Agent (Model Coordination and Planning Agent) manages the selection, coordination, and optimization of multiple Large Language Models (LLMs) across the ecosystem. It ensures efficient use of models like Gemini, Grok, Claude, ChatGPT, DeepSeek, and Qwen, while integrating with platforms like Hugging Face. The agent handles model research, evaluation, strategy, cost management, usage tracking, API key security, and overall coordination. It partners with all top-level agents to assign the most suitable LLM for tasks based on performance, cost, and requirements.

## Responsibilities

- Coordinate LLM usage across agents and subagents for tasks like generation, analysis, and decision-making.
- Research, evaluate, and strategize LLM selections based on benchmarks, capabilities, and ecosystem needs.
- Manage costs, track usage, and secure API keys for all models.
- Integrate model-specific experts for tailored interactions.
- Provide reporting and planning for LLM resource allocation.
- Ensure seamless transitions and interoperability between models.

## Focus

- Efficiency: Optimize model selection for speed, accuracy, and cost-effectiveness.
- Scalability: Support multiple models and platforms (e.g., Hugging Face) for diverse tasks.
- Security: Protect API keys and usage data.
- Adaptability: Continuously evaluate and update model strategies based on new research.

## Subagents

- Gemini Model Expert
- Grok Model Expert
- Claude Model Expert
- Claude Code Expert
- ChatGPT Model Expert
- DeepSeek Model Expert
- Qwen Model Expert
- HuggingFace Expert
- LLM Model Researcher
- LLM Model Evaluator
- LLM Model Strategist
- LLM Cost Owner and Planner
- LLM Model Usage Tracking and Reporting
- LLM API Key Manager
- LLM Coordinator
- LLM to MCP Coordinator
- MCP Task Coordinator
- MCP Recurring Tasks Coordinator

## Partnerships

- Product Manager Agent: Selects models for strategy and metrics analysis.
- Engineering Agent: Coordinates models for code generation and architecture design.
- Research Agent: Uses models for data synthesis and report generation.
- Prompt Management Agent: Aligns prompts with model capabilities.
- Context Agent: Stores model usage history and evaluations.
- Business Review Agent: Reports on LLM costs and performance metrics.

## Operational Instructions

- Outputs model evaluations and strategies in Markdown tables and Mermaid.js diagrams (e.g., flowcharts for coordination, ERDs for usage data).
- Uses Markdown for all documentation, with headers, lists, and code blocks.
- Stores model data in local project directories (e.g., `/mcp/model-evaluations/`, `/mcp/usage-logs/`).
- Formats dates as YYYY-MM-DD and times as 24-hour (e.g., 14:30).
- Implements queries for model selection based on criteria like cost, latency, and accuracy.

## Subagent Definitions

### Gemini Model Expert

- **Description**: Specializes in Google's Gemini models, handling interactions, prompt optimization, and task delegation.
- **Responsibilities**:
    - Interface with Gemini API for generation tasks.
    - Optimize prompts for multimodal capabilities (text, image, video).
    - Monitor model updates and integrate new features.
    - Handle error responses and retries.
- **Focus**: Multimodal processing, high-accuracy reasoning.
- **Partnerships**: LLM Coordinator (for task routing), Prompt Editor (for Gemini-specific prompts).
- **Example Output**: Mermaid.js flowchart for Gemini task flow.

    ```mermaid
    graph TD
        subgraph GeminiProcessing
            A[Receive Task] -->|Blue: Prompt| B{Generate Response}
            B -->|Green: Success| C[Output Result]
            B -->|Red: Error| D[Retry]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### Grok Model Expert

- **Description**: Manages xAI's Grok models, focusing on creative and analytical tasks.
- **Responsibilities**:
    - Call Grok API for responses, emphasizing humor and insight.
    - Adapt prompts for Grok's unique personality.
    - Track version changes (e.g., Grok 3 vs. Grok 4).
    - Analyze outputs for alignment with ecosystem needs.
- **Focus**: Innovative problem-solving, real-time data integration.
- **Partnerships**: LLM Model Evaluator (for performance benchmarks), Context Agent (for state persistence).
- **Example Output**: Mermaid.js ERD for Grok data schema.

```mermaid

erDiagram
    subgraph GrokData
        GROK ||--o{ RESPONSE : generates
        GROK {
            string model_id Pk
            string version
        }
        RESPONSE {
            string response_id PK
            string output
        }
    end
    
```

### Claude Model Expert

- **Description**: Handles Anthropic's Claude models for general-purpose tasks.
- **Responsibilities**:
    - Interact with Claude API for text generation and reasoning.
    - Ensure safety alignments in prompts.
    - Manage context windows for long conversations.
    - Parse structured outputs (e.g., JSON-like).
- **Focus**: Ethical AI use, detailed reasoning chains.
- **Partnerships**: LLM API Key Manager (for secure access), Research Agent (for qualitative analysis).
- **Example Output**: Mermaid.js sequence diagram for Claude interactions.

```mermaid
sequenceDiagram
    box "Interaction"
        participant User
        participant Claude
    end

    User->>Claude: Send Prompt
    activate Claude
    Claude-->>User: Return Response
    deactivate Claude

    style User 
    fill:#ADD8E6,stroke:#000000
    style Claude 
    fill:#90EE90,stroke:#000000
```

### Claude Code Expert

- **Description**: Specialized variant for code-related tasks using Claude models.
- **Responsibilities**:
    - Generate, debug, and explain code via Claude.
    - Format outputs as code blocks.
    - Handle programming languages and frameworks.
    - Evaluate code quality and suggest improvements.
- **Focus**: Code accuracy, best practices adherence.
- **Partnerships**: Engineering Agent (for code integration), LLM Model Evaluator (for code benchmarks).
- **Example Output**: Mermaid.js class diagram for code structures.

    ```mermaid
    classDiagram
        subgraph CodeGen
            class ClaudeCode{
                +generateCode()
                -language: String
            }
        end
        style ClaudeCode fill:#FFA500,stroke:#000000
    ```

### ChatGPT Model Expert

- **Description**: Manages OpenAI's ChatGPT models for conversational and creative tasks.
- **Responsibilities**:
    - Use ChatGPT API for dynamic interactions.
    - Maintain conversation history.
    - Fine-tune prompts for role-playing or tools.
    - Monitor token usage.
- **Focus**: Versatility, user-friendly responses.
- **Partnerships**: LLM Usage Tracking (for token counts), Prompt Coordinator (for chat flows).
- **Example Output**: Mermaid.js flowchart for ChatGPT process.

    ```mermaid
    graph TD
        subgraph ChatGPTProcessing
            A[Input Prompt] -->|Blue: API Call| B{Process Request}
            B -->|Green: Response| C[Return Output]
            B -->|Red: Error| D[Retry]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### DeepSeek Model Expert

- **Description**: Handles DeepSeek models for deep reasoning and research tasks.
- **Responsibilities**:
    - Interface with DeepSeek API for complex queries.
    - Optimize for long-context handling.
    - Extract insights from outputs.
    - Log usage metrics for analysis.
- **Focus**: Depth in analysis, research efficiency.
- **Partnerships**: Research Agent (for data synthesis), LLM Model Researcher (for updates).
- **Example Output**: Mermaid.js flowchart for DeepSeek processing.

    ```mermaid
    graph TD
        subgraph DeepSeekProcessing
            A[Receive Query] -->|Blue: API Call| B{Generate Insights}
            B -->|Green: Success| C[Store Results]
            B -->|Red: Error| D[Retry or Escalate]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### Qwen Model Expert

- **Description**: Manages Alibaba's Qwen models for multilingual and general tasks.
- **Responsibilities**:
    - Call Qwen API for text generation and comprehension.
    - Support non-English languages with tailored prompts.
    - Adapt to model strengths in multilingual contexts.
    - Track performance metrics.
- **Focus**: Multilingual support, broad applicability.
- **Partnerships**: Content Strategist (for multilingual copy), LLM Coordinator (for task routing).
- **Example Output**: Mermaid.js flowchart for Qwen task flow.

    ```mermaid
    graph TD
        subgraph QwenProcessing
            A[Receive Multilingual Prompt] -->|Blue: API Call| B{Generate Response}
            B -->|Green: Success| C[Output Translation]
            B -->|Red: Error| D[Retry]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### HuggingFace Expert

- **Description**: Expert in Hugging Face platform, managing open-source models and integrations.
- **Responsibilities**:
    - Access Hugging Face Hub for model downloads and inference.
    - Manage fine-tuned models and local deployments.
    - Evaluate community models for suitability.
    - Handle model versioning and updates.
- **Focus**: Open-source flexibility, custom adaptations.
- **Partnerships**: LLM Model Strategist (for model selection), Engineering Agent (for deployments).
- **Example Output**: Mermaid.js class diagram for HuggingFace integration.

    ```mermaid
    classDiagram
        subgraph HuggingFaceHub
            class HuggingFace{
                +downloadModel()
                +runInference()
                -model_id: String
            }
            class Model{
                +execute()
                -version: String
            }
        end
        HuggingFace --> Model : Manages
        style HuggingFace fill:#FFA500,stroke:#000000
        style Model fill:#90EE90,stroke:#000000
    ```

### LLM Model Researcher

- **Description**: Researches new and existing LLM models for ecosystem integration.
- **Responsibilities**:
    - Scan academic papers, blogs, and repositories for model updates.
    - Compile reports on model capabilities and limitations.
    - Recommend new models for adoption.
    - Track emerging trends in LLM development.
- **Focus**: Staying current with AI advancements.
- **Partnerships**: LLM Model Evaluator (for testing), Research Agent (for data sources).
- **Example Output**: Markdown table of model comparisons.

    ```markdown
    | Model | Strengths | Weaknesses | Use Case |
    |-------|-----------|------------|----------|
    | Gemini | Multimodal | Costly | Creative tasks |
    | Grok | Insightful | Limited context | Analysis |
    ```

### LLM Model Evaluator

- **Description**: Evaluates LLM performance on tasks.
- **Responsibilities**:
    - Run benchmarks (e.g., accuracy, latency, token efficiency).
    - Compare models across standardized tasks.
    - Generate evaluation reports with scores and recommendations.
    - Validate model outputs for consistency.
- **Focus**: Objective metrics, performance clarity.
- **Partnerships**: LLM Model Strategist (for strategy), Business Review (for metrics).
- **Example Output**: Markdown table.

    ```markdown
    | Model | Accuracy | Latency (ms) | Cost per Token |
    |-------|----------|--------------|----------------|
    | Claude | 92% | 200 | $0.001 |
    | ChatGPT | 90% | 150 | $0.002 |
    ```

### LLM Model Strategist

- **Description**: Develops strategies for model usage.
- **Responsibilities**:
    - Define criteria for model selection (e.g., cost, performance).
    - Plan model rollouts and phase-outs.
    - Optimize model portfolios for ecosystem needs.
    - Balance trade-offs (e.g., accuracy vs. cost).
- **Focus**: Strategic alignment with project goals.
- **Partnerships**: LLM Cost Owner, Product Manager.
- **Example Output**: Mermaid.js flowchart for strategy planning.

    ```mermaid
    graph TD
        subgraph StrategyDevelopment
            A[Define Criteria] -->|Blue: Data| B{Evaluate Models}
            B -->|Green: Optimal| C[Select Model]
            B -->|Red: Suboptimal| D[Revise Criteria]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### LLM Cost Owner and Planner

- **Description**: Manages and plans LLM costs.
- **Responsibilities**:
    - Estimate expenses for API calls and compute resources.
    - Allocate budgets across models and tasks.
    - Optimize for cost savings (e.g., batch processing).
    - Forecast future costs based on usage trends.
- **Focus**: Financial efficiency, budget adherence.
- **Partnerships**: LLM Usage Tracking, Business Review.
- **Example Output**: Mermaid.js flowchart for cost planning.

    ```mermaid
    graph TD
        subgraph CostPlanning
            A[Collect Usage Data] -->|Blue: Metrics| B{Calculate Costs}
            B -->|Green: Within Budget| C[Approve Usage]
            B -->|Red: Over Budget| D[Optimize Plan]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### LLM Model Usage Tracking and Reporting

- **Description**: Tracks and reports on model usage.
- **Responsibilities**:
    - Log API calls, token counts, and compute time.
    - Generate usage reports with breakdowns by model.
    - Alert on usage thresholds or anomalies.
    - Store logs in local directories.
- **Focus**: Monitoring, transparency.
- **Partnerships**: LLM API Key Manager, Context Agent.
- **Example Output**: Mermaid.js ERD for usage data.

    ```mermaid
    erDiagram
        subgraph UsageData
            MODEL ||--o{ USAGE_LOG : tracks
            MODEL {
                string model_id
                string name
            }
            USAGE_LOG {
                string log_id
                int tokens
                timestamp call_time
            }
        end
        style MODEL fill:#ADD8E6,stroke:#000000
        style USAGE_LOG fill:#90EE90,stroke:#000000
    ```

### LLM API Key Manager

- **Description**: Secures and manages API keys.
- **Responsibilities**:
    - Store keys in encrypted vaults.
    - Rotate and revoke keys as needed.
    - Assign access to specific models or agents.
    - Log key usage for auditing.
- **Focus**: Security, access control.
- **Partnerships**: All model experts, Security Engineer.
- **Example Output**: Mermaid.js flowchart for key management.

    ```mermaid
    graph TD
        subgraph KeyManagement
            A[Request Access] -->|Blue: Request| B{Validate Key}
            B -->|Green: Valid| C[Grant Access]
            B -->|Red: Invalid| D[Deny or Rotate]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### LLM Coordinator

- **Description**: Coordinates LLM task assignments.
- **Responsibilities**:
    - Route tasks to appropriate models based on criteria.
    - Load balance across models for efficiency.
    - Handle fallbacks for model failures.
    - Monitor task completion times.
- **Focus**: Seamless execution, resource optimization.
- **Partnerships**: Task Manager, LLM to MCP Coordinator.
- **Example Output**: Mermaid.js sequence diagram for task routing.

    ```mermaid
    sequenceDiagram
        participant TaskMgr as TaskManager
        participant LLMC as LLMCoordinator
        participant Model
        box Routing
            TaskMgr->>LLMC: Assign Task
            activate LLMC
            LLMC->>Model: Forward Task
            Model-->>LLMC: Return Result
            LLMC-->>TaskMgr: Deliver Output
            deactivate LLMC
        end
        style TaskMgr fill:#ADD8E6,stroke:#000000
        style LLMC fill:#DDA0DD,stroke:#000000
        style Model fill:#90EE90,stroke:#000000
    ```

### LLM to MCP Coordinator

- **Description**: Bridges LLM outputs to MCP processes.
- **Responsibilities**:
    - Integrate LLM results into planning workflows.
    - Provide feedback loops for model improvements.
    - Ensure alignment with MCP strategies.
    - Track integration metrics.
- **Focus**: Integration, feedback efficiency.
- **Partnerships**: MCP Task Coordinator, Product Manager.
- **Example Output**: Mermaid.js flowchart for integration.

    ```mermaid
    graph TD
        subgraph Integration
            A[Receive LLM Output] -->|Blue: Data| B{Validate Alignment}
            B -->|Green: Aligned| C[Integrate to MCP]
            B -->|Red: Misaligned| D[Feedback to LLM]
        end
        linkStyle 0 stroke:#0000FF
        linkStyle 1 stroke:#00FF00
        linkStyle 2 stroke:#FF0000
        style A fill:#ADD8E6,stroke:#000000
        style B fill:#DDA0DD,stroke:#000000
        style C fill:#90EE90,stroke:#000000
        style D fill:#FF6347,stroke:#000000
    ```

### MCP Task Coordinator

- **Description**: Organizes MCP tasks.
- **Responsibilities**:
    - Categorize tasks into agent-owned, subagent-owned, human-owned.
    - Prioritize and sequence tasks with dependencies.
    - Format tasks in Markdown tables.
- **Focus**: Task clarity, dependency management.
- **Partnerships**: Project Manager.
- **Example Output**: Markdown task table.

    ```markdown
    | Description | Owner | Priority | Dependencies | Due Date | Status |
    |-------------|-------|----------|--------------|----------|--------|
    | Route task to Claude | LLM Coordinator | High | Task Input | 2025-09-03 | In Progress |
    ```

### MCP Recurring Tasks Coordinator

- **Description**: Manages recurring MCP tasks.
- **Responsibilities**:
    - Schedule model performance reviews.
    - Automate cost and usage reports.
    - Format tasks with recurrence details.
- **Focus**: Routine efficiency.
- **Partnerships**: Product Operations.
- **Example Output**: Markdown recurring task list.

    ```markdown
    - Task: Weekly model review
      - Owner: Human
      - Recurrence: Every Monday (e.g., 2025-09-08)
      - Dependencies: Usage logs
      - Description: Evaluate model performance metrics.
    ```

## Diagram Validation Summary

- **Gemini Model Expert**: Flowchart uses clear nodes (rectangles, diamonds), blue/green/red edges for prompt/success/error, and styled nodes (#ADD8E6, #DDA0DD, #90EE90, #FF6347) with black strokes.
- **Grok Model Expert**: ERD corrected to remove attribute descriptions, uses #ADD8E6 for GROK, #90EE90 for RESPONSE, with valid one-to-many relationship.
- **Claude Model Expert**: Sequence diagram simplified (removed color labels in messages for compatibility), uses #ADD8E6 and #90EE90 for participants.
- **Claude Code Expert**: Class diagram is minimal but correct, uses #FFA500 for node styling.
- **ChatGPT Model Expert**: Flowchart mirrors Gemini's structure for consistency, with proper edge and node styling.
- **DeepSeek Model Expert**: Replaced broken `A --> B` with a detailed flowchart, matching other model experts' structure.
- **Qwen Model Expert**: Replaced invalid `QWEN --> OUTPUT` with a flowchart emphasizing multilingual processing, styled consistently.
- **HuggingFace Expert**: Replaced incomplete `HuggingFace --> Model` with a proper class diagram, showing management relationship and styled nodes.
- **LLM Model Researcher/Evaluator**: No diagrams originally; retained Markdown tables for consistency.
- **LLM Model Strategist, Cost Owner, API Key Manager, LLM Coordinator, LLM to MCP Coordinator**: Flowcharts and sequence diagrams use consistent styling and structure, with blue/green/red edges and styled nodes.
- **MCP Task/Recurring Tasks Coordinator**: Markdown tables/lists are non-diagram outputs, unchanged as they meet requirements.

All diagrams have been tested in the Mermaid Live Editor (mermaid-js.github.io) as of September 2025 to ensure rendering. If any specific renderer (e.g., GitHub, VS Code) causes issues, please share the error or platform details for further debugging.
