# Model Selection Guide

**63 Models Across 8 Providers** - Intelligent Task-to-Model Routing

## Task-to-Model Mapping Rules

### Code Tasks
- **Code Generation**: 
  - **Premium**: codellama:34b (local, free) > grok-code-fast-1 > claude-sonnet-4.5 > o3 > magicoder:7b (local, free)
  - **Balanced**: magicoder:7b (local, free) > codellama:13b (local, free) > gemma:7b (local, free) > claude-sonnet-4 > gpt-4o > qwen2.5:32b (local, free)
  - **Fast**: deepseek-coder:1.3b (local, free) > gpt-4o-mini > claude-3-haiku
- **Code Review**: 
  - **Ultimate**: deepseek-r1:70b (local, free) > claude-opus-4.1 > o1-pro > codellama:34b (local, free)
  - **Balanced**: claude-opus-4 > grok-3 > codellama:13b (local, free) > claude-sonnet-4.5
- **Debugging**: 
  - **Best**: deepseek-r1:70b (local, free) > o1-pro > grok-code-fast-1 > codellama:34b (local, free)
  - **Fast**: magicoder:7b (local, free) > gpt-4o > o3-mini > deepseek-coder:1.3b (local, free)

### Reasoning & Analysis
- **Complex Reasoning**: 
  - **Ultimate**: deepseek-r1:70b (local, free) > claude-opus-4.1 > o1-pro > grok-4-fast-reasoning
  - **Balanced**: qwen2.5:32b (local, free) > qwen2.5:7b-instruct (local, free) > claude-opus-4 > o1 > gemini-2.0-pro
- **System Design**: 
  - **Best**: deepseek-r1:70b (local, free) > claude-opus-4.1 > llama-3.1-405b (local, free) > o1-pro
  - **Practical**: qwen2.5:32b (local, free) > claude-sonnet-4.5 > gemini-2.0-pro > grok-3
- **Data Analysis**: 
  - **Advanced**: deepseek-r1:70b (local, free) > gemini-2.0-pro > claude-opus-4 > qwen2.5:32b (local, free)
  - **Quick**: qwen3:8b (local, free) > gemini-2.0-flash > gpt-4o-mini
- **Research**: 
  - **Deep**: deepseek-r1:70b (local, free) > gemini-2.0-pro > claude-opus-4.1 > grok-4-fast-reasoning
  - **Fast**: qwen2.5:32b (local, free) > gemini-2.0-flash > claude-3.5-sonnet

### Creative Tasks
- **Creative Writing**: 
  - **Premium**: claude-opus-4.1 > gpt-4.1-2025 > qwen2.5:32b (local, free) > claude-opus-4
  - **Balanced**: claude-sonnet-4.5 > qwen3:8b (local, free) > gemma:7b (local, free) > gpt-4o > gemini-2.0-pro
- **Storytelling**: 
  - **Best**: gpt-4.1-2025 > claude-opus-4.1 > qwen2.5:32b (local, free) > claude-sonnet-4.5
  - **Quick**: qwen3:8b (local, free) > llama3.1:8b (local, free) > gpt-4o-mini
- **Poetry**: 
  - **Artistic**: claude-opus-4.1 > gpt-4.1-2025 > qwen2.5:32b (local, free) > claude-3.5-sonnet

### Vision & Images
- **Image Analysis**: 
  - **Best**: llama-3.2-90b (local, free, vision) > gpt-4o > grok-2-vision-1212 > llama-3.2-11b (local, free, vision)
  - **Cloud**: gpt-4-turbo > grok-2-vision-1212 > gemini-2.0-pro
- **Screenshot Analysis**: 
  - **Local**: llama-3.2-90b (local, free, vision) > llama-3.2-11b (local, free, vision)
  - **Cloud**: gpt-4o > grok-2-vision-1212 > gemini-2.0-flash

### Fast Tasks
- **Quick Answers**: 
  - **Instant**: deepseek-coder:1.3b (local, free) > llama3.2:3b (local, free) > gemma:7b (local, free) > llama3.1:8b (local, free)
  - **Cloud**: gemini-2.0-flash > claude-3-haiku > gpt-4o-mini
- **Translation**: 
  - **Best**: qwen2.5:32b (local, free) > qwen2.5:7b-instruct (local, free) > qwen3:8b (local, free) > gemini-2.0-flash > claude-3.5-sonnet
  - **Quick**: qwen2.5:7b-instruct (local, free) > qwen3:8b (local, free) > llama3.1:8b (local, free) > gemini-2.0-flash
- **Summarization**: 
  - **Fast**: llama3.2:3b (local, free) > llama3.1:8b (local, free) > claude-3-haiku
  - **Quality**: qwen2.5:32b (local, free) > grok-4-fast-non-reasoning > gemini-2.0-flash

### Large Context Tasks (>500K tokens)
**2M Token Models:**
1. grok-4-fast-reasoning (2M) - Best for complex reasoning
2. grok-4-fast-non-reasoning (2M) - Fast processing
3. gemini-2.0-pro (2M) - Research and analysis
4. gemini-1.5-pro (2M) - Previous generation

**1M Token Models:**
5. gpt-4.1-2025 (1M) - Premium OpenAI
6. gemini-2.0-flash (1M) - Fast responses
7. gemini-1.5-flash (1M) - Cost-effective

**Large Context Local Models:**
8. llama-3.2-90b (128K, local, free) - Best local large context
9. llama-3.1-405b (128K, local, free) - Ultimate local model
10. llama-3.1-70b (128K, local, free) - Balanced local option

## Cost Optimization Rules

### Budget Tiers
- **FREE ($0.00)**: All 20 local models - **ALWAYS PREFERRED**
  - deepseek-r1:70b, codellama:34b, qwen2.5:32b, magicoder:7b, gemma:7b, qwen2.5:7b-instruct, etc.
- **Ultra-Low (<$0.001/1K)**: gemini-2.0-flash ($0.1/$0.4), gemini-1.5-flash ($0.075/$0.3)
- **Low (<$0.01/1K)**: claude-3-haiku ($0.25/$1.25), gpt-4o-mini ($0.15/$0.6), grok-3 ($1/$3)
- **Medium (<$0.1/1K)**: claude-3.5-sonnet ($3/$15), gpt-4o ($5/$15), claude-sonnet-4 ($3/$15)
- **High (<$1/1K)**: o1 ($15/$60), o3 ($10/$30), grok-4 variants ($1-2/$3-6)
- **Premium (>$1/1K)**: claude-opus-4.1 ($20/$100), o1-pro ($60/$240)

### Cost Strategy Overrides
- **Always prefer local models first**: All local models are $0.00 and should be prioritized
- If budget < $0.01: Use local models OR gemini-2.0-flash, claude-3-haiku
- If budget < $0.1: Exclude premium models (opus-4.1, o1-pro, high-cost Grok variants)
- **Local model validation**: Use consensus with cloud models for critical tasks
- **Zero-cost strategy**: `cost_optimize` should always prefer suitable local models

## Performance Rules

### Speed Priority
**Local Models (Instant Response):**
1. deepseek-coder:1.3b (local, instant, 0.98 speed)
2. llama3.2:3b (local, instant, 0.95 speed)
3. llama3.1:8b (local, instant, 0.9 speed)
4. magicoder:7b (local, instant, 0.9 speed)
5. qwen3:8b (local, instant, 0.85 speed)

**Cloud Models:**
6. gemini-2.0-flash (0.95 speed)
7. claude-3-haiku (0.9 speed)
8. gpt-4o-mini (0.9 speed)
9. grok-4-fast-non-reasoning (0.9 speed)

### Accuracy Priority  
**Ultimate Accuracy:**
1. claude-opus-4.1 (0.95 accuracy) - Premium cloud
2. deepseek-r1:70b (0.92 accuracy) - **FREE local**
3. o1-pro (0.98 accuracy) - Premium cloud
4. codellama:34b (0.9 accuracy) - **FREE local**
5. qwen2.5:32b (0.88 accuracy) - **FREE local**

**High Accuracy Cloud:**
6. claude-opus-4 (0.95 accuracy)
7. o1 (0.95 accuracy)
8. gpt-4o (0.9 accuracy)
9. grok-4-fast-reasoning (0.9 accuracy)

### Balanced Selection
**Local Models (Free + Balanced):**
1. magicoder:7b (excellent code balance, **FREE**)
2. qwen2.5:32b (premium intelligence, **FREE**) 
3. codellama:13b (solid code quality, **FREE**)
4. gemma:7b (Google's balanced model, **FREE**)
5. qwen2.5:7b-instruct (instruction-tuned, **FREE**)
6. qwen3:8b (multilingual reasoning, **FREE**)

**Cloud Models:**
5. claude-3.5-sonnet (excellent balance)
6. gpt-4o (strong all-around)
7. gemini-2.0-pro (good balance)
8. claude-sonnet-4 (reliable choice)

## Special Cases

### Multi-Model Consensus
For critical decisions, use 3+ diverse models:
- **Provider diversity**: Mix local + cloud (e.g., deepseek-r1:70b + claude-opus-4.1 + grok-4-fast-reasoning)
- **Capability diversity**: Mix reasoning + speed + accuracy leaders
- **Cost awareness**: Always include at least one FREE local model
- **Local + Cloud**: Best practice is 1-2 local models + 1-2 premium cloud models

### Fallback Chains
Primary → Secondary → Fallback (Local models prioritized):

**Code Generation:**
codellama:34b (local) → magicoder:7b (local) → gemma:7b (local) → grok-code-fast-1 → claude-sonnet-4.5 → deepseek-coder:1.3b (local)

**Reasoning:**
deepseek-r1:70b (local) → qwen2.5:32b (local) → qwen2.5:7b-instruct (local) → claude-opus-4.1 → grok-4-fast-reasoning → o1

**Creative Writing:**
qwen2.5:32b (local) → gemma:7b (local) → qwen3:8b (local) → claude-opus-4.1 → gpt-4.1-2025 → claude-sonnet-4.5

**Quick Tasks:**
deepseek-coder:1.3b (local) → llama3.2:3b (local) → gemma:7b (local) → llama3.1:8b (local) → gemini-2.0-flash → claude-3-haiku

**Vision:**
llama-3.2-90b (local, vision) → llama-3.2-11b (local, vision) → gpt-4o → grok-2-vision-1212

### Model Usage Guidelines

**Local Models - Production Ready:**
- deepseek-r1:70b: ✅ Production reasoning and analysis
- codellama:34b: ✅ Production code generation
- qwen2.5:32b: ✅ Production multilingual tasks
- magicoder:7b: ✅ Production code with validation
- gemma:7b: ✅ Production balanced tasks and conversations
- qwen2.5:7b-instruct: ✅ Production instruction-following tasks

**Local Models - Development/Testing:**
- llama3.2:3b: ⚠️ Quick prototyping only, validate for production
- deepseek-coder:1.3b: ⚠️ Rapid iteration, not final production code
- llama3.1:8b: ⚠️ General tasks, validate critical outputs

**Specialized Usage:**
- grok-2-vision-1212: Only for explicit image analysis tasks
- All vision models: Require explicit vision capability requests

## Context Window Requirements

### Minimum Context by Task
- Simple queries: 4K minimum
- Code files: 32K minimum
- Project analysis: 128K minimum
- Codebase review: 256K minimum
- Large documents: 1M+ required

### Auto-Upgrade Rules
If context_needed > model.context_window:
- Upgrade to next tier model
- Split task if possible
- Warn user about limitations

## Quality Gates

### Minimum Scores by Task Type
- Production Code: accuracy >= 0.85
- Financial Analysis: accuracy >= 0.9
- Creative Writing: creativity >= 0.8
- Customer Support: speed >= 0.7
- Research: reasoning_depth >= 0.8

### Validation Requirements

**Critical Tasks Requiring Multi-Model Consensus:**
- **Code deployment**: deepseek-r1:70b (local) + codellama:34b (local) + claude-opus-4.1 (cloud)
- **Financial decisions**: deepseek-r1:70b (local) + o1-pro (cloud) + claude-opus-4.1 (cloud)
- **Legal text**: claude-opus-4.1 + o1-pro + qwen2.5:32b (local validation)
- **Medical content**: Highest accuracy models + mandatory disclaimer

**Production Code Validation:**
- Use local models for initial development (codellama:34b, magicoder:7b)
- Validate with cloud models for critical systems (claude-sonnet-4.5, gpt-4o)
- Always test locally before cloud API costs

**Cost-Effective Validation:**
- Start with free local models
- Use cloud models only for final validation or complex edge cases
- Leverage local model speed for iterative development
