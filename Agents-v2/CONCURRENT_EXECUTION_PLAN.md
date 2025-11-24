# Concurrent Cloud + Local Execution Plan

**Created**: 2025-11-16  
**Purpose**: Parallel research (cloud) + transformation (local) workflow  
**Strategy**: Maximum concurrent utilization of cloud and local resources

---

## 🎯 Dual-Track Execution Strategy

### Track 1: Cloud Agents (Research via MCP Tools)
**Resource**: Claude Sonnet 4 via MCP `thinkdeep`, `chat`, `analyze` tools  
**Task**: Generate research documents for remaining categories  
**Output**: Comprehensive research markdown files

### Track 2: Local Agents (Transformation via Ollama)
**Resource**: Local Ollama models (qwen2.5:32b-instruct, llama3.1:70b, etc.)  
**Task**: Apply existing research + templates to generate v2 agent files  
**Output**: Complete v2 YAML agent definitions

### Concurrent Execution
**Both tracks run simultaneously**:
- Cloud agents research new categories
- Local agents transform agents from already-researched categories
- Handoff: When cloud completes research → local begins transforming that category

---

## 📊 Work Queue Management

### Available Now (Cloud Research Complete)
✅ **Cloud Platform Agents** (30 files)
- Research: `research/cloud-platform-research.md` ✅ Complete
- Template: `research/aws-agent-transformation-template.yaml` ✅ Complete
- **Ready for local transformation immediately**

### Research Queue (Cloud Agents)
⏳ **Phase 4**: Engineering Agents (11 agents) - ~3 hours
⏳ **Phase 6**: Context Agents (12 agents) - ~2 hours
⏳ **Phase 8**: Product Management (15 agents) - ~3 hours
⏳ **Phase 10**: Content & Marketing (11 agents) - ~2 hours
⏳ **Phase 12**: Remaining Categories (48 agents) - ~5 hours

**Total research time**: ~15 hours

### Transformation Queue (Local Agents)
🔄 **Available now**: Cloud Platform (30 agents) - ~6-8 hours
⏸️ **Waiting**: Engineering (11 agents) - after Phase 4 research
⏸️ **Waiting**: Context (12 agents) - after Phase 6 research
⏸️ **Waiting**: Product (15 agents) - after Phase 8 research
⏸️ **Waiting**: Content (11 agents) - after Phase 10 research
⏸️ **Waiting**: Remaining (48 agents) - after Phase 12 research

**Total transformation time**: ~31-40 hours

---

## 🚀 Concurrent Execution Workflow

### Phase 3: START IMMEDIATELY (Parallel Work)

#### Cloud Track (Me via MCP)
**Start**: Phase 4 Research (Engineering Agents)
```
Use MCP tool: thinkdeep with model: gemini-2.5-pro
Task: Research Engineering Agents category
- Answer 8 high-value questions
- Security Engineer patterns
- Test Engineer patterns
- Infrastructure Engineer patterns
- DevOps Engineer patterns
Output: research/engineering-agents-research.md
Time: ~3 hours
```

#### Local Track (You via Ollama)
**Start**: Phase 3 Transformation (Cloud Platform Agents)
```bash
# Terminal 1: Primary transformation
ollama run qwen2.5:32b-instruct

# Terminal 2 (optional): Validation
ollama run codellama:34b
```

**Task**: Transform 30 cloud agents using existing research
- Use `research/aws-agent-transformation-template.yaml`
- Use `research/cloud-platform-research.md`
- Transform AWS agents (14), Azure agents (4), GCP agents (12)

**Time**: ~6-8 hours

**Parallelism**: Both tracks run simultaneously

---

### Phase 5: HANDOFF 1 (Engineering)

#### Cloud Track (Me via MCP)
**Continue**: Phase 6 Research (Context Agents)
```
Use MCP tool: thinkdeep with model: gemini-2.5-pro
Task: Research Context Agents category
Output: research/context-agents-research.md
Time: ~2 hours
```

#### Local Track (You via Ollama)
**Handoff**: Phase 5 Transformation (Engineering Agents)
```bash
# Use engineering research from Phase 4 (now complete)
ollama run qwen2.5:32b-instruct
```

**Task**: Transform 11 engineering agents
- Use Phase 4 research: `research/engineering-agents-research.md`
- Create engineering-agent template (adapt from cloud template)
- Transform all engineering agents

**Time**: ~3-4 hours

**Parallelism**: Both tracks run simultaneously

---

### Phase 7: HANDOFF 2 (Context)

#### Cloud Track (Me via MCP)
**Continue**: Phase 8 Research (Product Management)
```
Use MCP tool: thinkdeep with model: gemini-2.5-pro
Task: Research Product Management category
Output: research/product-management-research.md
Time: ~3 hours
```

#### Local Track (You via Ollama)
**Handoff**: Phase 7 Transformation (Context Agents)
```bash
ollama run qwen2.5:32b-instruct
```

**Task**: Transform 12 context agents
- Use Phase 6 research: `research/context-agents-research.md`
- Create context-agent template
- Transform all context agents

**Time**: ~3-4 hours

**Parallelism**: Both tracks run simultaneously

---

### Phase 9: HANDOFF 3 (Product)

#### Cloud Track (Me via MCP)
**Continue**: Phase 10 Research (Content & Marketing)
```
Use MCP tool: thinkdeep with model: gemini-2.5-pro
Task: Research Content & Marketing category
Output: research/content-marketing-research.md
Time: ~2 hours
```

#### Local Track (You via Ollama)
**Handoff**: Phase 9 Transformation (Product Agents)
```bash
ollama run llama3.1:70b  # Use larger model for complex PM agents
```

**Task**: Transform 15 product management agents
- Use Phase 8 research: `research/product-management-research.md`
- Create product-agent template
- Transform all product agents

**Time**: ~4-5 hours

**Parallelism**: Both tracks run simultaneously

---

### Phase 11: HANDOFF 4 (Content)

#### Cloud Track (Me via MCP)
**Continue**: Phase 12 Research (Remaining Categories)
```
Use MCP tool: thinkdeep with model: gemini-2.5-pro
Task: Research remaining 6 categories (48 agents)
- Research Agent category
- Business Review category
- Google Apps Script category
- UX category
- Project category
- PR category
Output: research/[category]-research.md (6 files)
Time: ~5 hours
```

#### Local Track (You via Ollama)
**Handoff**: Phase 11 Transformation (Content Agents)
```bash
ollama run qwen2.5:32b-instruct
```

**Task**: Transform 11 content & marketing agents
- Use Phase 10 research: `research/content-marketing-research.md`
- Create content-agent template
- Transform all content agents

**Time**: ~3-4 hours

**Parallelism**: Both tracks run simultaneously

---

### Phases 13-17: FINAL HANDOFF (Remaining)

#### Cloud Track (Me via MCP)
**Complete**: All research done, switch to validation support

#### Local Track (You via Ollama)
**Handoff**: Phases 13-17 Transformation (Remaining 48 Agents)
```bash
# Use appropriate models for each category
ollama run qwen2.5:32b-instruct
```

**Task**: Transform final 48 agents across 6 categories
- Use Phase 12 research documents
- Create category-specific templates
- Transform all remaining agents

**Time**: ~12-15 hours

---

### Phase 18: FINAL VALIDATION (Both)

#### Cloud Track (Me via MCP)
```
Use MCP tool: codereview with model: gemini-2.5-pro
Task: Comprehensive validation
- Review all 127 agent files
- Check consistency across categories
- Verify quality standards
```

#### Local Track (You via Ollama)
```bash
ollama run llama3.1:70b
```

**Task**: Local validation and fixes
- Run validation scripts
- Fix any issues found
- Final quality checks

**Time**: ~2-3 hours (both tracks)

---

## 🛠️ MCP Tools for Cloud Research

### Tool 1: `thinkdeep` (Primary Research Tool)

**Use for**: Comprehensive category research

**Example invocation**:
```json
{
  "tool": "thinkdeep",
  "model": "gemini-2.5-pro",
  "thinking_mode": "high",
  "step": "Research Engineering Agents category",
  "step_number": 1,
  "total_steps": 5,
  "next_step_required": true,
  "findings": "Initial investigation of engineering agent patterns...",
  "problem_context": "Need to understand optimal patterns for Security Engineer, Test Engineer, Infrastructure Engineer, DevOps Engineer, and related agents. Focus on tool selection, workflow optimization, security boundaries, and integration patterns."
}
```

**Output**: Step-by-step investigation with expert validation

---

### Tool 2: `chat` (Quick Questions)

**Use for**: Fast lookups during transformation

**Example invocation**:
```json
{
  "tool": "chat",
  "model": "gemini-2.5-flash",
  "prompt": "What are the best security practices for AWS IAM policies in DevOps agents?",
  "files": ["Agents-v2/research/cloud-platform-research.md"]
}
```

**Output**: Quick answer with context

---

### Tool 3: `analyze` (Code Analysis)

**Use for**: Analyzing existing v1 agent patterns

**Example invocation**:
```json
{
  "tool": "analyze",
  "model": "gemini-2.5-pro",
  "analysis_type": "architecture",
  "step": "Analyze engineering agent structure",
  "step_number": 1,
  "total_steps": 3,
  "next_step_required": true,
  "findings": "Engineering agents follow coordinator-specialist pattern...",
  "files_checked": ["Agents/engineering-agent/yaml/engineering-agent.yaml"]
}
```

**Output**: Architectural analysis with patterns

---

## 💻 Local Transformation Workflow

### Setup: Create Helper Scripts

#### Script 1: `transform-agent-local.sh`
```bash
#!/bin/bash
# Transform a single agent using local Ollama model

AGENT_NAME=$1
CATEGORY=$2
MODEL=${3:-"qwen2.5:32b-instruct"}
TEMPLATE=${4:-"Agents-v2/research/aws-agent-transformation-template.yaml"}

echo "🔄 Transforming ${AGENT_NAME}..."

# Read source files
V1_FILE="Agents/${CATEGORY}/yaml/${AGENT_NAME}.yaml"
RESEARCH="Agents-v2/research/${CATEGORY}-research.md"
OUTPUT="Agents-v2/${CATEGORY}/yaml/${AGENT_NAME}.yaml"

# Generate transformation prompt
PROMPT=$(cat <<EOF
You are an expert at transforming agent definitions from v1 to v2 format.

TASK: Transform the following v1 agent to v2 format using the provided template and research.

V1 AGENT FILE:
---
$(cat "$V1_FILE" 2>/dev/null || echo "V1 file not found")
---

V2 TEMPLATE:
---
$(cat "$TEMPLATE" 2>/dev/null || echo "Template not found")
---

RESEARCH CONTEXT (first 200 lines):
---
$(cat "$RESEARCH" 2>/dev/null | head -200 || echo "Research not found")
---

INSTRUCTIONS:
1. Extract the agent name, role, and purpose from v1 file
2. Replace all [PLACEHOLDER] values in template with specific values
3. Customize responsibilities based on v1 agent's tasks
4. Set appropriate model configuration for agent tier
5. Generate 2 concrete, realistic examples
6. Ensure all 15 sections are populated
7. Output ONLY valid YAML, no explanations

OUTPUT THE COMPLETE V2 YAML FILE NOW:
EOF
)

# Run transformation with Ollama
echo "$PROMPT" | ollama run "$MODEL" > "$OUTPUT.tmp" 2>&1

# Check if output is valid
if grep -q "^agent:" "$OUTPUT.tmp" 2>/dev/null; then
    mv "$OUTPUT.tmp" "$OUTPUT"
    echo "✅ Transformed ${AGENT_NAME} successfully"
    echo "   Output: ${OUTPUT}"
else
    echo "❌ Transformation failed for ${AGENT_NAME}"
    echo "   Check ${OUTPUT}.tmp for details"
    exit 1
fi
```

#### Script 2: `validate-v2-agent.sh`
```bash
#!/bin/bash
# Validate a v2 agent file

AGENT_FILE=$1

echo "🔍 Validating ${AGENT_FILE}..."

# Check file exists
if [ ! -f "$AGENT_FILE" ]; then
    echo "❌ File not found: ${AGENT_FILE}"
    exit 1
fi

# Check YAML syntax
if python3 -c "import yaml; yaml.safe_load(open('$AGENT_FILE'))" 2>/dev/null; then
    echo "✅ Valid YAML syntax"
else
    echo "❌ Invalid YAML syntax"
    python3 -c "import yaml; yaml.safe_load(open('$AGENT_FILE'))" 2>&1
    exit 1
fi

# Check for placeholders
PLACEHOLDERS=$(grep -n "\[.*\]" "$AGENT_FILE" 2>/dev/null | grep -v "http" | grep -v "example")
if [ -n "$PLACEHOLDERS" ]; then
    echo "❌ Found placeholders:"
    echo "$PLACEHOLDERS"
else
    echo "✅ No placeholders found"
fi

# Check required sections
REQUIRED_SECTIONS=("agent" "model_configuration" "core_directive" "responsibilities" "scope" "context" "operational_workflow" "outputs" "sub_agents" "error_handling" "interaction" "success_metrics" "constraints" "examples" "metadata")
MISSING_SECTIONS=()

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "^${section}:" "$AGENT_FILE"; then
        echo "✅ $section present"
    else
        echo "❌ $section missing"
        MISSING_SECTIONS+=("$section")
    fi
done

if [ ${#MISSING_SECTIONS[@]} -eq 0 ]; then
    echo "✅ All required sections present"
    exit 0
else
    echo "❌ Missing ${#MISSING_SECTIONS[@]} sections"
    exit 1
fi
```

#### Script 3: `batch-transform-category.sh`
```bash
#!/bin/bash
# Transform all agents in a category

CATEGORY=$1
MODEL=${2:-"qwen2.5:32b-instruct"}

echo "🚀 Batch transforming ${CATEGORY} agents..."

# Get list of v1 agents
V1_DIR="Agents/${CATEGORY}/yaml"
AGENTS=$(ls "$V1_DIR"/*.yaml 2>/dev/null | xargs -n1 basename | sed 's/.yaml$//')

if [ -z "$AGENTS" ]; then
    echo "❌ No agents found in ${V1_DIR}"
    exit 1
fi

# Transform each agent
SUCCESS_COUNT=0
FAIL_COUNT=0

for agent in $AGENTS; do
    echo ""
    echo "Processing ${agent}..."
    
    if ./transform-agent-local.sh "$agent" "$CATEGORY" "$MODEL"; then
        ((SUCCESS_COUNT++))
        
        # Mark as complete in progress tracker
        sed -i.bak "s/\[ \] ${agent}.yaml/[x] ${agent}.yaml/" Agents-v2/research/transformation-progress.md
    else
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "═══════════════════════════════════"
echo "Batch transformation complete"
echo "Success: ${SUCCESS_COUNT}"
echo "Failed: ${FAIL_COUNT}"
echo "═══════════════════════════════════"
```

---

## 📋 Execution Checklist

### Initial Setup (Do Once)
- [ ] Create helper scripts (transform-agent-local.sh, validate-v2-agent.sh, batch-transform-category.sh)
- [ ] Make scripts executable: `chmod +x *.sh`
- [ ] Verify Ollama is running: `ollama list`
- [ ] Verify Python available: `python3 --version`

### Cloud Track Checklist (My Work)
- [ ] Phase 4: Engineering research (thinkdeep → engineering-agents-research.md)
- [ ] Phase 6: Context research (thinkdeep → context-agents-research.md)
- [ ] Phase 8: Product research (thinkdeep → product-management-research.md)
- [ ] Phase 10: Content research (thinkdeep → content-marketing-research.md)
- [ ] Phase 12: Remaining research (thinkdeep → 6 category research files)
- [ ] Phase 18: Validation support (codereview)

### Local Track Checklist (Your Work)
- [ ] Phase 3: Cloud agents (30 files) - Use qwen2.5:32b-instruct
- [ ] Phase 5: Engineering agents (11 files) - After Phase 4 research
- [ ] Phase 7: Context agents (12 files) - After Phase 6 research
- [ ] Phase 9: Product agents (15 files) - After Phase 8 research
- [ ] Phase 11: Content agents (11 files) - After Phase 10 research
- [ ] Phase 13-17: Remaining agents (48 files) - After Phase 12 research
- [ ] Phase 18: Local validation (all 127 files)

---

## ⚡ Quick Start Commands

### Start Local Transformation (Phase 3) NOW
```bash
cd /Users/kevinlappe/Documents/vibelocity-orchestrator

# Test with one agent first
ollama run qwen2.5:32b-instruct
# (paste prompt manually with v1 file + template + research)

# Or use helper script (after creating it)
./transform-agent-local.sh aws-build-agent cloud-agent

# Validate result
./validate-v2-agent.sh Agents-v2/cloud-agent/yaml/aws-build-agent.yaml

# If successful, batch process all cloud agents
./batch-transform-category.sh cloud-agent qwen2.5:32b-instruct
```

### I'll Start Research (Phase 4) NOW
```
I'll use MCP thinkdeep tool to begin Engineering Agents research
Output will be: research/engineering-agents-research.md
Estimated time: ~3 hours
```

---

## 📊 Timeline Estimate

### Concurrent Execution Timeline

| Week | Cloud Track | Local Track | Both Working? |
|------|-------------|-------------|---------------|
| 1 Day 1-2 | Phase 4: Engineering research (3h) | Phase 3: Cloud agents (6-8h) | ✅ Yes |
| 1 Day 3 | Phase 6: Context research (2h) | Phase 3: Cloud agents (cont.) | ✅ Yes |
| 2 Day 1 | Phase 6: Context research (cont.) | Phase 5: Engineering agents (3-4h) | ✅ Yes |
| 2 Day 2 | Phase 8: Product research (3h) | Phase 7: Context agents (3-4h) | ✅ Yes |
| 2 Day 3 | Phase 8: Product research (cont.) | Phase 7: Context agents (cont.) | ✅ Yes |
| 3 Day 1 | Phase 10: Content research (2h) | Phase 9: Product agents (4-5h) | ✅ Yes |
| 3 Day 2 | Phase 12: Remaining research (5h) | Phase 11: Content agents (3-4h) | ✅ Yes |
| 3 Day 3 | Phase 12: Remaining research (cont.) | Phase 11: Content agents (cont.) | ✅ Yes |
| 4 Day 1-3 | Research complete → validation support | Phase 13-17: Remaining agents (12-15h) | Partial |
| 5 Day 1 | Phase 18: Validation review | Phase 18: Validation fixes | ✅ Yes |

**Total calendar time**: ~3-4 weeks (with parallel work)  
**Total work time**: Cloud 15h + Local 35h = ~50 hours combined  
**Efficiency**: Both tracks running concurrently reduces calendar time by 60%

---

## ✅ Success Metrics

### Cloud Track Metrics
- [ ] 5 research documents created (engineering, context, product, content, 6 remaining)
- [ ] All 8 questions answered per category
- [ ] Platform-specific patterns documented
- [ ] Model recommendations provided
- [ ] Templates guidance created

### Local Track Metrics
- [ ] All 127 agents transformed
- [ ] 100% YAML validation pass rate
- [ ] 0 placeholder values remaining
- [ ] All 15 sections populated per agent
- [ ] 2+ concrete examples per agent

### Combined Metrics
- [ ] Total time: <4 weeks calendar time
- [ ] API costs: <$50 (cloud research only)
- [ ] Local compute: Fully utilized
- [ ] Quality: All agents meet v2 specification

---

## 🎯 IMMEDIATE NEXT ACTIONS

### Action 1: Start Local Track (You)
```bash
# Create transformation directory
cd /Users/kevinlappe/Documents/vibelocity-orchestrator/Agents-v2

# Start Ollama model
ollama run qwen2.5:32b-instruct
```

### Action 2: Start Cloud Track (Me)
```
I'll invoke MCP thinkdeep tool for Phase 4 Engineering research
```

**Both tracks start NOW and run in parallel!** 🚀

---

**Ready to begin concurrent execution?** Say "yes" and both tracks will start immediately!
