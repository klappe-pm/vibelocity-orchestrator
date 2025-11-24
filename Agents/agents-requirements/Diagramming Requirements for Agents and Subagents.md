---
categories: LLM  
subCategories:
  - agent definitions
  - agent diagrams
  - agents
  - diagrams
  - subagent defintions
topics:
subTopics:
dateCreated: 2025-09-02  
dateRevised: 2025-09-02
aliases: []
tags: []
---

# Diagramming Requirements for Agents and Subagents

Each agent and subagent must produce a set of diagrams to visualize their processes, data flows, interactions, and work breakdowns. All diagrams use Mermaid.js syntax, formatted in code blocks within Markdown files. Diagrams must incorporate subgraphs to group related components and use color to differentiate data flows, decisions, workstreams, work breakdowns, and other elements. Colors are applied via style directives in Mermaid.js (e.g., `style id fill:#color,stroke:#color`), as Mermaid.js supports CSS-like styling for nodes and edges where applicable. Subgraphs are defined using `subgraph name` and `end` keywords to cluster elements logically.

The following diagram types are required for each agent and subagent, tailored to their responsibilities. For each type, details on how Mermaid.js works are provided, including key syntax, supported features, and best practices for implementation.

## Diagram Types

1. **Flow Chart**:
    
    - **Purpose**: Illustrates process steps, decision branches, and outcomes (e.g., task execution, approvals, iterations).
    - **Elements**: Nodes for tasks or steps (rectangles), diamond nodes for decisions, arrows for flow direction (use colors: blue for data flow, green for successful paths, red for error/rejection paths). Subgraphs to group related steps (e.g., by phase like "Planning" or "Execution").
    - **Use Case**: Show how an agent processes inputs (e.g., PRD for Product Manager) to outputs (e.g., roadmap).
    - **How Mermaid.js Works**: Mermaid.js flowcharts use graph syntax like `graph TD` (top-down) or `graph LR` (left-right). Nodes are defined as `id[Label]` for rectangles or `id{Label}` for diamonds. Edges are `A --> B` for connections, with labels via `A -->|Label| B`. Subgraphs are created with `subgraph Name … end`. Styling for colors is added at the end, e.g., `linkStyle 0 stroke:#0000FF` for blue edges or `style A fill:#lightgreen` for nodes. Mermaid.js renders these as SVG diagrams in supported viewers, automatically laying out elements based on direction. Best practices: Keep graphs acyclic where possible; use IDs for styling references; limit complexity to avoid rendering issues in browsers.
    - **Example**:

	   ```mermaid
        graph TD
            subgraph Planning
                A[Receive Inputs] -->|Data Flow| B{Validate Inputs}
                B -->|Valid| C[Generate Plan]
                B -->|Invalid| D[Request Clarification]
            end
            subgraph Execution
                C --> E[Execute Tasks]
                D --> F[Update Inputs]
            end
            E --> G[Output Results]
            F --> A
            linkStyle 0 stroke:#0000FF  // Blue for data flow
            linkStyle 1 stroke:#00FF00  // Green for valid
            linkStyle 2 stroke:#FF0000  // Red for invalid
        ```

2. **Entity-Relationship Diagram (ERD)**:
    
    - **Purpose**: Maps data entities, attributes, and relationships (e.g., user data for UX Design, metrics for Product Manager).
    - **Elements**: Rectangles for entities, ovals for attributes, lines for relationships (use colors: blue for primary data flow, purple for dependencies). Subgraphs to group related entities (e.g., by data source like "Internal DB" or "External API").
    - **Use Case**: Show how Research Agent handles survey data linked to user personas.
    - **How Mermaid.js Works**: ERDs use `erDiagram` syntax. Entities are `ENTITY { attribute type "description" }`, relationships like `ENTITY1 ||--o{ ENTITY2: "label"`. Cardinality is shown with `|o`, `||`, `}o`, `}|` for one/many. Subgraphs are supported to group entities. Styling is limited but can include `style ENTITY fill:#color` for nodes; edge colors via `linkStyle` are not directly supported in ERDs, so use labels or node styles for differentiation. Mermaid.js generates crow's foot notation by default and renders as a relational diagram. Best practices: Define all entities first, then relationships; use quotes for multi-word labels; avoid overly nested attributes for readability.
    - **Example**:

	   ```mermaid
        erDiagram
            subgraph UserData
                USER ||--o{ SURVEY : completes
                USER {
                    string user_id "Primary Key"
                    string name
                }
            end
            subgraph SurveyData
                SURVEY {
                    string survey_id "Primary Key"
                    string response "Data Flow"
                }
            end
            SURVEY ||--o{ ANALYSIS : feeds
            ANALYSIS {
                string analysis_id
                string insights "Dependency"
            }
            style USER fill:#ADD8E6  // Light blue for user data
            style SURVEY fill:#DDA0DD  // Plum for survey
        ```

3. **Class Diagram**:
    
    - **Purpose**: Represents the agent/subagent as a system with classes (e.g., modules, services) and their interactions.
    - **Elements**: Rectangles for classes, attributes and methods listed within, arrows for relationships (associations, inheritance; use colors: blue for data interactions, orange for control flow). Subgraphs to group related classes (e.g., by functionality like "Task Management" or "Data Processing").
    - **Use Case**: Illustrate Engineering Agent's code modules and their dependencies.
    - **How Mermaid.js Works**: Class diagrams use `classDiagram` syntax. Classes are `class Name { +method() -attribute:type }`. Relationships include `-->` for association, `<|--` for inheritance, `*--` for composition. Labels on relationships via `: label`. Subgraphs group classes. Styling with `style ClassName fill:#color,stroke:#color`. Mermaid.js follows UML-like notation and auto-arranges classes. Best practices: List public (+) and private (-) members; use namespaces if needed; reference classes by name for styling; test rendering as complex diagrams may overlap.
    - **Example**:

	   ```mermaid
        classDiagram
            subgraph TaskManagement
                class TaskManager{
                    +createTask()
                    +assignOwner()
                    -tasks: List
                }
            end
            subgraph Processing
                class DataProcessor{
                    +processInput()
                    -data: Map
                }
            end
            TaskManager --> DataProcessor : DataInteraction
            TaskManager : ControlFlow
            style TaskManager fill:#ADD8E6  // Light blue for data
            style DataProcessor fill:#FFA500  // Orange for control
        ```

4. **Sequence Diagram**:
    
    - **Purpose**: Shows the order of messages, calls, or tasks exchanged during a process (e.g., Product Manager requesting data from Research).
    - **Elements**: Actors or objects, arrows for messages (use colors: blue for requests, green for responses, red for errors). Subgraphs (or boxes) to group phases (e.g., "Initialization" or "Processing").
    - **Use Case**: Depict inter-agent communication, like UX Design Agent collaborating with Engineering.
    - **How Mermaid.js Works**: Sequence diagrams use `sequenceDiagram` syntax. Participants as `participant Actor`, messages as `Actor1->>Actor2: Message`. Activations with `activate Actor`, loops with `loop Label … end`, alternatives with `alt Label … else … end`. Subgraphs via `box Name … end`. Styling: `Note over Actor: Text`, edge colors not directly supported but nodes via `style Actor fill:#color`. Mermaid.js renders timelines vertically, with auto-spacing. Best practices: Order participants left-to-right by initiation; use `->>` for async, `->` for sync; limit to 10-15 interactions for clarity; add notes for explanations.
    - **Example**:

	   ```mermaid
        sequenceDiagram
            participant PM as ProductManager
            participant RS as Research
            box Initialization
                PM->>RS: Request Data (blue)
                activate RS
                RS-->>PM: Acknowledge
            end
            box Processing
                RS->>RS: Analyze
                RS->>PM: Send Results (green)
                deactivate RS
            end
            Note over PM,RS: Error Path (red)
            style PM fill:#ADD8E6
            style RS fill:#90EE90
        ```
