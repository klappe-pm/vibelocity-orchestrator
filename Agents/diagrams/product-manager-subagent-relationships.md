# Product Manager Agent - SubAgent Relationships

## 1. Entity Relationship Diagram (ERD) - PM Agent to SubAgents

```mermaid
erDiagram
    PRODUCT_MANAGER_AGENT ||--o{ STRATEGIST : "delegates-strategy"
    PRODUCT_MANAGER_AGENT ||--o{ BUSINESS_ANALYST : "delegates-analysis"
    PRODUCT_MANAGER_AGENT ||--o{ METRICS_ANALYST : "delegates-metrics"
    PRODUCT_MANAGER_AGENT ||--o{ DASHBOARD_DESIGNER : "delegates-visualization"
    PRODUCT_MANAGER_AGENT ||--o{ REQUIREMENTS_WRITER : "delegates-documentation"
    PRODUCT_MANAGER_AGENT ||--o{ BUSINESS_CASE_OWNER : "delegates-justification"
    PRODUCT_MANAGER_AGENT ||--o{ METRICS_RESEARCHER : "delegates-research"
    PRODUCT_MANAGER_AGENT ||--o{ INTERNAL_DOC_RESEARCHER : "delegates-knowledge"
    PRODUCT_MANAGER_AGENT ||--o{ FRAMEWORKS_DESIGNER : "delegates-frameworks"
    PRODUCT_MANAGER_AGENT ||--o{ OPP_SOLUTIONS_DESIGNER : "delegates-opportunities"
    PRODUCT_MANAGER_AGENT ||--o{ OPERATIONS : "delegates-operations"
    PRODUCT_MANAGER_AGENT ||--o{ TASK_COORDINATOR : "manages-tasks"
    PRODUCT_MANAGER_AGENT ||--o{ RECURRING_COORDINATOR : "manages-recurring"
    
    STRATEGIST ||--o{ BUSINESS_ANALYST : "informs-analysis"
    STRATEGIST ||--o{ METRICS_ANALYST : "defines-kpis"
    STRATEGIST ||--o{ FRAMEWORKS_DESIGNER : "guides-frameworks"
    
    BUSINESS_ANALYST ||--o{ REQUIREMENTS_WRITER : "provides-data"
    BUSINESS_ANALYST ||--o{ BUSINESS_CASE_OWNER : "supports-case"
    BUSINESS_ANALYST ||--o{ METRICS_RESEARCHER : "requests-metrics"
    
    METRICS_ANALYST ||--o{ DASHBOARD_DESIGNER : "feeds-data"
    METRICS_ANALYST ||--o{ METRICS_RESEARCHER : "validates-research"
    
    REQUIREMENTS_WRITER ||--o{ INTERNAL_DOC_RESEARCHER : "references-docs"
    
    TASK_COORDINATOR ||--o{ ALL_SUBAGENTS : "assigns-work"
    RECURRING_COORDINATOR ||--o{ ALL_SUBAGENTS : "schedules-tasks"
    
    PRODUCT_MANAGER_AGENT {
        string agent_id PK
        string current_priority
        json active_initiatives
        json subagent_status
        timestamp last_sync
    }
    
    STRATEGIST {
        string subagent_id PK
        string parent_agent_id FK
        json strategies
        json roadmaps
        string vision_alignment
    }
    
    BUSINESS_ANALYST {
        string subagent_id PK
        string parent_agent_id FK
        json analyses
        json market_data
        json competitor_insights
    }
    
    METRICS_ANALYST {
        string subagent_id PK
        string parent_agent_id FK
        json kpis
        json metrics_definitions
        json tracking_setup
    }
    
    DASHBOARD_DESIGNER {
        string subagent_id PK
        string parent_agent_id FK
        json dashboard_configs
        json visualizations
        string tool_integrations
    }
    
    REQUIREMENTS_WRITER {
        string subagent_id PK
        string parent_agent_id FK
        json prds
        json user_stories
        json acceptance_criteria
    }
    
    TASK_COORDINATOR {
        string subagent_id PK
        string parent_agent_id FK
        json task_queue
        json assignments
        timestamp next_review
    }
```

## 2. Class Diagram - PM Agent to SubAgent Architecture

```mermaid
classDiagram
    class ProductManagerAgent {
        -String agentId
        -Map~String-SubAgent~ subAgents
        -PriorityQueue~Task~ taskQueue
        -StateManager state
        +delegateTask(task, subAgent)
        +aggregateResults()
        +coordinateSubAgents()
        +getPriorities()
    }
    
    class PMSubAgent {
        <<abstract>>
        #String subAgentId
        #String parentAgentId
        #String specialization
        #Status status
        +executeTask(task)
        +reportToParent(result)
        +collaborateWith(subAgent)
    }
    
    class StrategistSubAgent {
        -StrategyEngine engine
        -RoadmapBuilder roadmap
        -VisionAligner aligner
        +developStrategy()
        +createRoadmap()
        +alignWithVision()
        +prioritizeInitiatives()
    }
    
    class BusinessAnalystSubAgent {
        -MarketAnalyzer market
        -CompetitorTracker competitor
        -DataProcessor processor
        +analyzeMarket()
        +trackCompetitors()
        +generateInsights()
        +createBusinessCase()
    }
    
    class MetricsAnalystSubAgent {
        -KPIDefiner kpis
        -MetricsTracker tracker
        -AnalyticsEngine analytics
        +defineKPIs()
        +setupTracking()
        +analyzeMetrics()
        +reportPerformance()
    }
    
    class DashboardDesignerSubAgent {
        -VisualizationBuilder viz
        -DashboardComposer composer
        -IntegrationManager integrations
        +designDashboard()
        +createVisualizations()
        +integrateDataSources()
        +publishDashboard()
    }
    
    class RequirementsWriterSubAgent {
        -PRDGenerator prd
        -UserStoryWriter stories
        -CriteriaBuilder criteria
        +writePRD()
        +createUserStories()
        +defineAcceptanceCriteria()
        +documentRequirements()
    }
    
    class BusinessCaseOwnerSubAgent {
        -ROICalculator roi
        -RiskAssessor risk
        -JustificationBuilder justification
        +buildBusinessCase()
        +calculateROI()
        +assessRisks()
        +presentJustification()
    }
    
    class MetricsResearcherSubAgent {
        -DataCollector collector
        -BenchmarkAnalyzer benchmark
        -TrendIdentifier trends
        +researchMetrics()
        +analyzeBenchmarks()
        +identifyTrends()
        +provideRecommendations()
    }
    
    class TaskCoordinatorSubAgent {
        -TaskScheduler scheduler
        -AssignmentEngine assigner
        -ProgressTracker tracker
        +scheduleTask()
        +assignToSubAgent()
        +trackProgress()
        +reportStatus()
    }
    
    PMSubAgent <|-- StrategistSubAgent
    PMSubAgent <|-- BusinessAnalystSubAgent
    PMSubAgent <|-- MetricsAnalystSubAgent
    PMSubAgent <|-- DashboardDesignerSubAgent
    PMSubAgent <|-- RequirementsWriterSubAgent
    PMSubAgent <|-- BusinessCaseOwnerSubAgent
    PMSubAgent <|-- MetricsResearcherSubAgent
    PMSubAgent <|-- TaskCoordinatorSubAgent
    
    ProductManagerAgent "1" o-- "*" PMSubAgent : manages
    StrategistSubAgent "1" --> "*" BusinessAnalystSubAgent : guides
    BusinessAnalystSubAgent "1" --> "1" RequirementsWriterSubAgent : informs
    MetricsAnalystSubAgent "1" --> "1" DashboardDesignerSubAgent : provides-data
    TaskCoordinatorSubAgent "1" --> "*" PMSubAgent : coordinates
```

## 3. Sequence Diagram - PM Agent to SubAgent Workflow

```mermaid
sequenceDiagram
    participant PM as PM_Agent
    participant TC as TaskCoordinator
    participant S as Strategist
    participant BA as BusinessAnalyst
    participant MA as MetricsAnalyst
    participant RW as RequirementsWriter
    participant DD as DashboardDesigner
    participant BC as BusinessCaseOwner
    participant MR as MetricsResearcher
    
    Note over PM,MR: Product Feature Development Flow
    
    rect rgb(240, 240, 255)
        Note right of PM: Initialization
        PM->>TC: New feature request
        TC->>TC: Analyze task complexity
        TC->>PM: Task breakdown plan
        PM->>TC: Approve execution
    end
    
    rect rgb(255, 240, 240)
        Note right of S: Strategy Phase
        TC->>S: Initiate strategy development
        activate S
        S->>S: Analyze market position
        S->>BA: Request market analysis
        activate BA
        BA->>MR: Request benchmark data
        activate MR
        MR->>MR: Research metrics
        MR-->>BA: Benchmark insights
        deactivate MR
        BA->>BA: Competitive analysis
        BA-->>S: Market insights
        deactivate BA
        S->>S: Develop strategy
        S-->>PM: Strategy proposal
        deactivate S
    end
    
    rect rgb(240, 255, 240)
        Note right of BC: Business Case Phase
        PM->>BC: Build business case
        activate BC
        BC->>BA: Request analysis data
        BA-->>BC: Business data
        BC->>MA: Request metrics projections
        activate MA
        MA->>MR: Historical metrics needed
        MR-->>MA: Historical data
        MA->>MA: Calculate projections
        MA-->>BC: Metrics projections
        deactivate MA
        BC->>BC: ROI calculation
        BC-->>PM: Business case document
        deactivate BC
    end
    
    rect rgb(255, 255, 240)
        Note right of RW: Requirements Phase
        PM->>RW: Document requirements
        activate RW
        RW->>S: Get strategic context
        S-->>RW: Strategy alignment
        RW->>BA: Get business context
        BA-->>RW: Business requirements
        RW->>MA: Get success metrics
        MA-->>RW: KPIs and criteria
        RW->>RW: Write PRD
        RW-->>PM: PRD document
        deactivate RW
    end
    
    rect rgb(240, 255, 255)
        Note right of DD: Visualization Phase
        PM->>DD: Create dashboard
        activate DD
        DD->>MA: Request metrics design
        activate MA
        MA->>MA: Define tracking
        MA-->>DD: Metrics specifications
        deactivate MA
        DD->>DD: Design visualizations
        DD->>DD: Build dashboard
        DD-->>PM: Dashboard ready
        deactivate DD
        
        PM->>TC: Update task status
        TC->>TC: Archive workflow
        TC-->>PM: Completion report
    end
```

---

# Color Coding Applied
- **Blue backgrounds** (rgb(240, 240, 255)): Initialization/Setup phases
- **Red backgrounds** (rgb(255, 240, 240)): Critical decision phases
- **Green backgrounds** (rgb(240, 255, 240)): Execution phases
- **Yellow backgrounds** (rgb(255, 255, 240)): Documentation phases
- **Cyan backgrounds** (rgb(240, 255, 255)): Finalization phases
