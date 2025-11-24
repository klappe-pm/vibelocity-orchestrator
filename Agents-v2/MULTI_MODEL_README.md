# Multi-Model Orchestrator

## Overview
This enhanced orchestrator uses **multiple AI models concurrently** to dramatically speed up agent transformations:

### Models Used (in rotation):
1. **OpenAI GPT-4o-mini** (cloud) - Fast, accurate
2. **Qwen 2.5 32B** (local Ollama) - Strong reasoning
3. **DeepSeek-R1 70B** (local Ollama) - Excellent for code/structure

### Key Features:
- ⚡ **6 concurrent workers** (default) vs 3 previously
- 🔄 **Round-robin model assignment** - distributes load across models
- 🌐 **Hybrid cloud + local** - no single point of failure
- 📊 **Shared progress tracking** - resume from where you left off

## Usage

### Transform a single category with multi-model:
```bash
python3 orchestrate_multi_model.py --category cloud-agent --workers 6
```

### Transform ALL categories at once:
```bash
python3 orchestrate_multi_model.py --all --workers 9
```

### Adjust worker count based on your system:
```bash
# Conservative (lower CPU/RAM)
python3 orchestrate_multi_model.py --all --workerspython3 orchestrate_multnd machine)
python3 orchestrate_multi_model.py --all --workers 12
```

## Speed Comparison

**Old single-model approach:**
- 127 agents × ~30 seconds each = ~63 minutes total

**New multi-model approach:**
- 3 models working concurrently
- 6-9 parallel workers
- Estimated: **15-20 minutes for all 127 agents**

## Requirements

1. **Olla1. **Olla1. **Olllama serve` (should already be running)
2. **Models pulled**: Already have qwen2.5:32b-instruct and deepseek-r1:70b
3. **OpenAI API key**: Set in environment

## Monitoring

Watch live progress:
```bash
tail -f orchestration.log
```

Check completion status:
```bash
find Agents-v2/*/yaml -name "*.yaml" ! -name "*-definition.yaml" | wc -l
```
