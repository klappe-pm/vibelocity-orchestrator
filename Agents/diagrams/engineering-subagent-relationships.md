# Engineering Agent - SubAgent Relationships

## 1. Entity Relationship Diagram (ERD) - Engineering Agent to SubAgents

```mermaid
erDiagram
    ENGINEERING_AGENT ||--o{ BACKEND_DEVELOPER : "delegates-backend"
    ENGINEERING_AGENT ||--o{ FRONTEND_DEVELOPER : "delegates-frontend"
    ENGINEERING_AGENT ||--o{ DATABASE_ADMIN : "delegates-database"
    ENGINEERING_AGENT ||--o{ DEVOPS_ENGINEER : "delegates-infrastructure"
    ENGINEERING_AGENT ||--o{ SYSTEM_ARCHITECT : "delegates-architecture"
    ENGINEERING_AGENT ||--o{ API_DESIGNER : "delegates-apis"
    ENGINEERING_AGENT ||--o{ SECURITY_ENGINEER : "delegates-security"
    ENGINEERING_AGENT ||--o{ TESTING_QA : "delegates-testing"
    ENGINEERING_AGENT ||--o{ TASK_COORDINATOR : "manages-tasks"
    ENGINEERING_AGENT ||--o{ RECURRING_COORDINATOR : "manages-recurring"
    
    SYSTEM_ARCHITECT ||--o{ BACKEND_DEVELOPER : "defines-architecture"
    SYSTEM_ARCHITECT ||--o{ FRONTEND_DEVELOPER : "defines-patterns"
    SYSTEM_ARCHITECT ||--o{ DATABASE_ADMIN : "defines-schema"
    SYSTEM_ARCHITECT ||--o{ API_DESIGNER : "defines-contracts"
    
    BACKEND_DEVELOPER ||--o{ DATABASE_ADMIN : "queries-database"
    BACKEND_DEVELOPER ||--o{ API_DESIGNER : "implements-apis"
    
    FRONTEND_DEVELOPER ||--o{ API_DESIGNER : "consumes-apis"
    
    DEVOPS_ENGINEER ||--o{ BACKEND_DEVELOPER : "deploys-services"
    DEVOPS_ENGINEER ||--o{ FRONTEND_DEVELOPER : "deploys-apps"
    DEVOPS_ENGINEER ||--o{ DATABASE_ADMIN : "manages-infra"
    
    SECURITY_ENGINEER ||--o{ ALL_SUBAGENTS : "audits-security"
    TESTING_QA ||--o{ ALL_SUBAGENTS : "validates-quality"
    
    ENGINEERING_AGENT {
        string agent_id PK
        string current_sprint
        json active_features
        json tech_stack
        string deployment_status
    }
    
    BACKEND_DEVELOPER {
        string subagent_id PK
        string parent_agent_id FK
        json services
        json apis
        string language_stack
    }
    
    FRONTEND_DEVELOPER {
        string subagent_id PK
        string parent_agent_id FK
        json components
        json ui_state
        string framework
    }
    
    DATABASE_ADMIN {
        string subagent_id PK
        string parent_agent_id FK
        json schemas
        json migrations
        string db_type
    }
    
    DEVOPS_ENGINEER {
        string subagent_id PK
        string parent_agent_id FK
        json pipelines
        json environments
        string cloud_provider
    }
    
    SYSTEM_ARCHITECT {
        string subagent_id PK
        string parent_agent_id FK
        json architectures
        json design_docs
        string patterns
    }
    
    SECURITY_ENGINEER {
        string subagent_id PK
        string parent_agent_id FK
        json vulnerabilities
        json compliance
        string security_tools
    }
```

## 2. Class Diagram - Engineering Agent to SubAgent Architecture

```mermaid
classDiagram
    class EngineeringAgent {
        -String agentId
        -Map~String-SubAgent~ subAgents
        -SprintManager sprints
        -CodeRepository repository
        +delegateTask(task, subAgent)
        +coordinateDevelopment()
        +reviewCode()
        +deployRelease()
    }
    
    class EngSubAgent {
        <<abstract>>
        #String subAgentId
        #String parentAgentId
        #String expertise
        #Environment environment
        +implementTask(task)
        +runTests()
        +reportStatus()
    }
    
    class SystemArchitectSubAgent {
        -DesignPatterns patterns
        -ArchitectureRepo architectures
        -TechStackManager stack
        +designArchitecture()
        +reviewDesign()
        +defineStandards()
        +evaluateTechnologies()
    }
    
    class BackendDeveloperSubAgent {
        -ServiceBuilder services
        -APIImplementer apis
        -BusinessLogic logic
        +buildService()
        +implementAPI()
        +optimizePerformance()
        +handleIntegrations()
    }
    
    class FrontendDeveloperSubAgent {
        -ComponentLibrary components
        -UIBuilder ui
        -StateManager state
        +buildUI()
        +implementComponents()
        +manageState()
        +optimizeUX()
    }
    
    class DatabaseAdminSubAgent {
        -SchemaDesigner schema
        -MigrationManager migrations
        -QueryOptimizer optimizer
        +designSchema()
        +runMigrations()
        +optimizeQueries()
        +manageIndexes()
    }
    
    class DevOpsEngineerSubAgent {
        -PipelineBuilder pipelines
        -InfrastructureManager infra
        -DeploymentAutomation deploy
        +buildPipeline()
        +provisionInfra()
        +deployApplication()
        +monitorHealth()
    }
    
    class APIDesignerSubAgent {
        -ContractDefiner contracts
        -DocumentationGen docs
        -VersionManager versions
        +defineContract()
        +generateDocs()
        +manageVersions()
        +validateSchema()
    }
    
    class SecurityEngineerSubAgent {
        -VulnerabilityScanner scanner
        -ComplianceChecker compliance
        -SecurityAuditor auditor
        +scanVulnerabilities()
        +checkCompliance()
        +auditSecurity()
        +implementControls()
    }
    
    class TestingQASubAgent {
        -TestSuiteManager suites
        -AutomationFramework automation
        -QualityMetrics metrics
        +writeTests()
        +runAutomation()
        +measureQuality()
        +reportDefects()
    }
    
    EngSubAgent <|-- SystemArchitectSubAgent
    EngSubAgent <|-- BackendDeveloperSubAgent
    EngSubAgent <|-- FrontendDeveloperSubAgent
    EngSubAgent <|-- DatabaseAdminSubAgent
    EngSubAgent <|-- DevOpsEngineerSubAgent
    EngSubAgent <|-- APIDesignerSubAgent
    EngSubAgent <|-- SecurityEngineerSubAgent
    EngSubAgent <|-- TestingQASubAgent
    
    EngineeringAgent "1" o-- "*" EngSubAgent : manages
    SystemArchitectSubAgent "1" --> "*" BackendDeveloperSubAgent : guides
    SystemArchitectSubAgent "1" --> "*" FrontendDeveloperSubAgent : guides
    BackendDeveloperSubAgent "1" --> "1" DatabaseAdminSubAgent : uses
    BackendDeveloperSubAgent "1" --> "1" APIDesignerSubAgent : implements
    DevOpsEngineerSubAgent "1" --> "*" EngSubAgent : deploys
```

## 3. Sequence Diagram - Engineering Agent to SubAgent Workflow

```mermaid
sequenceDiagram
    participant EA as Engineering_Agent
    participant SA as SystemArchitect
    participant BE as BackendDev
    participant FE as FrontendDev
    participant DB as DatabaseAdmin
    participant API as APIDesigner
    participant DO as DevOpsEng
    participant SEC as SecurityEng
    participant QA as TestingQA
    
    Note over EA,QA: Feature Implementation Workflow
    
    rect rgb(240, 240, 255)
        Note right of EA: Planning Phase
        EA->>SA: New feature requirements
        activate SA
        SA->>SA: Analyze requirements
        SA->>API: Define API contracts
        activate API
        API->>API: Design endpoints
        API-->>SA: API specifications
        deactivate API
        SA->>DB: Define data model
        activate DB
        DB->>DB: Design schema
        DB-->>SA: Schema design
        deactivate DB
        SA->>SA: Create architecture
        SA-->>EA: Architecture approved
        deactivate SA
    end
    
    rect rgb(255, 240, 240)
        Note right of BE: Backend Development
        EA->>BE: Implement backend
        activate BE
        BE->>DB: Setup database
        activate DB
        DB->>DB: Create tables
        DB->>DB: Run migrations
        DB-->>BE: Database ready
        deactivate DB
        BE->>API: Implement endpoints
        activate API
        API->>API: Validate contracts
        API-->>BE: API validated
        deactivate API
        BE->>BE: Business logic
        BE-->>EA: Backend complete
        deactivate BE
    end
    
    rect rgb(240, 255, 240)
        Note right of FE: Frontend Development
        EA->>FE: Implement frontend
        activate FE
        FE->>API: Consume APIs
        API-->>FE: API documentation
        FE->>FE: Build components
        FE->>FE: Implement UI
        FE-->>EA: Frontend complete
        deactivate FE
    end
    
    rect rgb(255, 255, 240)
        Note right of QA: Testing Phase
        EA->>QA: Begin testing
        activate QA
        QA->>BE: Test backend
        BE-->>QA: Test results
        QA->>FE: Test frontend
        FE-->>QA: Test results
        QA->>SEC: Security review
        activate SEC
        SEC->>SEC: Security scan
        SEC->>SEC: Compliance check
        SEC-->>QA: Security report
        deactivate SEC
        QA-->>EA: Quality approved
        deactivate QA
    end
    
    rect rgb(240, 255, 255)
        Note right of DO: Deployment Phase
        EA->>DO: Deploy to production
        activate DO
        DO->>DO: Build pipeline
        DO->>BE: Package backend
        DO->>FE: Package frontend
        DO->>DB: Migrate production
        DO->>DO: Deploy services
        DO->>DO: Health checks
        DO-->>EA: Deployment complete
        deactivate DO
        
        EA->>SEC: Final security audit
        SEC-->>EA: Security certified
        EA->>EA: Feature released
    end
```

---

# Engineering SubAgent Interactions
- **Blue**: Infrastructure and setup operations
- **Green**: Development and implementation
- **Red**: Critical security and compliance checks
- **Yellow**: Testing and validation
- **Cyan**: Deployment and release
