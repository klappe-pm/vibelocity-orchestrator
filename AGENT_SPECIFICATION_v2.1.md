# Agent Instructions File Format v2.1
## LLM-Optimized Agent Definition Specification with Orchestration Protocol

---

# SECTION 0: INSTRUCTIONS FOR LLM USING THIS SPECIFICATION

## 0.1 Purpose of This Document
You are an LLM tasked with creating or transforming agent definition files. This specification defines the standard format for autonomous agent configuration. Follow these instructions to produce compliant agent files.

## 0.2 When to Use This Specification

### Creating a NEW Agent File:
```
IF user provides: requirements, role description, or task definition
THEN:
  1. Read entire specification (Sections 1-18)
  2. Follow "Agent Creation Workflow" (Section 0.3)
  3. Populate all required sections
  4. Generate examples and test cases
  5. Validate against specification schema
  6. Output complete agent file
```

### Transforming an EXISTING Agent File:
```
IF user provides: existing agent file in any format
THEN:
  1. Parse existing file and extract components
  2. Map components to this specification structure
  3. Fill gaps with reasonable defaults
  4. Preserve original intent and constraints
  5. Add missing required sections
  6. Enhance with planning/estimation/delegation protocols
  7. Validate against specification schema
  8. Output transformed agent file with changelog
```

## 0.3 Agent Creation Workflow

```yaml
workflow:
  step_1_requirements_analysis:
    task: "Extract and structure requirements"
    questions_to_answer:
      - "What is the agent's primary objective?"
      - "What resources does it need access to?"
      - "What are the success criteria?"
      - "What are the failure modes?"
      - "Who/what does it interact with?"
    output: "requirements_summary.yaml"
    
  step_2_scope_definition:
    task: "Define boundaries and constraints"
    questions_to_answer:
      - "What can this agent modify/access?"
      - "What must it never touch?"
      - "When should it ask for help?"
      - "What are the resource limits?"
    output: "scope_contract.yaml"
    
  step_3_decomposition_analysis:
    task: "Identify if sub-agents are needed"
    decision_criteria:
      requires_subagents_if:
        - "Task has >3 distinct phases requiring different expertise"
        - "Subtasks can run in parallel"
        - "Different subtasks need different model capabilities"
        - "Task complexity exceeds single agent context window"
        - "Specialized domain knowledge needed for subtasks"
      remains_single_agent_if:
        - "Task is linear and simple"
        - "All operations require same context"
        - "Total complexity < 5 steps"
        - "No parallel processing opportunities"
    output: "agent_architecture.yaml"
    
  step_4_model_selection_strategy:
    task: "Define model selection criteria"
    use_framework: "See Section 0.5 - Model Selection Framework"
    consider:
      - "Task complexity and reasoning requirements"
      - "Context window needs"
      - "Cost constraints and optimization strategy"
      - "Speed vs quality tradeoffs"
      - "Special capabilities (vision, code, reasoning)"
    output: "model_strategy.yaml"
    
  step_5_planning_framework:
    task: "Define how agent creates execution plans"
    use_framework: "See Section 0.6 - Planning Protocol"
    output: "planning_protocol.yaml"
    
  step_6_estimation_framework:
    task: "Define cost and complexity estimation"
    use_framework: "See Section 0.7 - Estimation Protocol"
    output: "estimation_protocol.yaml"
    
  step_7_delegation_protocol:
    task: "Define subagent delegation rules"
    use_framework: "See Section 0.8 - Delegation Protocol"
    output: "delegation_protocol.yaml"
    
  step_8_complete_specification:
    task: "Generate complete agent file"
    actions:
      - "Populate all sections 1-18"
      - "Include concrete examples"
      - "Add validation criteria"
      - "Generate test cases"
    output: "agent_specification_v2.1.yaml"
```

## 0.4 Agent vs Sub-Agent Relationship Model

```yaml
relationship_model:
  
  parent_agent:
    role: "Coordinator and decision maker"
    responsibilities:
      - "Receive top-level task from user"
      - "Create execution plan (see Section 0.6)"
      - "Estimate complexity and costs (see Section 0.7)"
      - "Decide when to delegate (see Section 0.8)"
      - "Select appropriate sub-agents"
      - "Aggregate sub-agent outputs"
      - "Validate final results"
      - "Report to user"
    
    file_location: "/agents/[agent-name].agent.yaml"
    naming_convention: "[domain]-[role]-agent.yaml"
    example: "model-orchestrator-agent.yaml"
    
  sub_agent:
    role: "Specialist executor"
    responsibilities:
      - "Receive scoped task from parent agent"
      - "Create sub-plan if needed"
      - "Estimate own costs and complexity"
      - "Execute specialized task"
      - "Return structured results to parent"
      - "Report errors with recovery suggestions"
    
    file_location: "/agents/subagents/[parent-agent]/[subagent-name].subagent.yaml"
    naming_convention: "[parent-name]-[specialty]-subagent.yaml"
    example: "model-orchestrator-task-analysis-subagent.yaml"
    
  key_differences:
    scope:
      parent: "Broad, multi-phase tasks"
      sub: "Narrow, specialized tasks"
    
    delegation_authority:
      parent: "Can delegate to multiple sub-agents"
      sub: "Can only escalate back to parent or delegate to sibling if authorized"
    
    model_selection:
      parent: "Selects model for coordination and aggregation"
      sub: "Selects model optimized for specialized task"
    
    planning_depth:
      parent: "High-level multi-phase planning"
      sub: "Detailed single-phase execution planning"
    
    estimation_scope:
      parent: "Estimates total cost including all sub-agents"
      sub: "Estimates only own execution cost"
```

---

## Key Usage Reminders for LLMs

### When Creating New Agent Files:
1. **Always** include planning, estimation, delegation, and model selection sections
2. **Define** clear parent/sub-agent relationships if applicable
3. **Specify** model selection criteria and strategy
4. **Provide** concrete examples throughout
5. **Validate** against all required sections

### When Transforming Existing Files:
1. **Preserve** original intent and functionality
2. **Enhance** with missing protocols (planning, estimation, delegation)
3. **Clarify** agent relationships and communication
4. **Add** model selection framework if not present
5. **Document** transformation decisions in changelog

### Critical Success Factors:
- ✅ Clear delegation triggers and handoff protocols
- ✅ Explicit cost estimation methodology
- ✅ Well-defined model selection criteria
- ✅ Concrete examples for all major workflows
- ✅ Sub-agent files reference parent agent
- ✅ All agents follow consistent communication formats

---

**NOTE**: Due to file size limitations, this is a condensed version. For the complete specification with all 18 sections including detailed model selection frameworks, planning protocols, estimation protocols, delegation protocols, and comprehensive examples, please refer to the full documentation or request specific sections.

The complete specification includes:
- Section 0.5: Model Selection Framework (63 models, 8 providers)
- Section 0.6: Planning Protocol (6-phase planning process)
- Section 0.7: Estimation Protocol (cost, time, complexity calculations)
- Section 0.8: Delegation Protocol (when/how to delegate)
- Section 0.9: Complete transformation example for Model Orchestration Agent
- Sections 1-18: Full YAML specification template

To generate complete agent files, follow the workflow in Section 0.3 and reference the appropriate protocol sections for each step.
