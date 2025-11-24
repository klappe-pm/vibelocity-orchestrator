# Local Ollama LLM Models

This document lists all locally installed LLM models available via Ollama on this system.

**Last Updated:** Generated on-demand  
**Total Models:** 18  
**Total Storage:** ~200+ GB (approximate)

---

## Model Inventory

### Mistral Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `mistral:latest` | 6577803aa9a0 | 4.4 GB | 4 days ago | Mistral AI's latest general-purpose model |
| `mistral:7b` | 6577803aa9a0 | 4.4 GB | 7 days ago | Mistral 7B base model |

**Notes:**
- Both models share the same ID, indicating `mistral:latest` points to the 7B variant
- Mistral models support tool calling and structured outputs
- Good for general conversation and reasoning tasks

---

### Qwen Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `qwen2.5:32b-instruct` | 9f13ba1299af | 19 GB | 6 days ago | Qwen 2.5 32B instruction-tuned model |
| `qwen2.5:32b-instruct-q4_K_M` | 9f13ba1299af | 19 GB | 7 days ago | Quantized version (Q4_K_M) of 32B instruct |
| `qwen2.5:32b` | 9f13ba1299af | 19 GB | 7 days ago | Qwen 2.5 32B base model |
| `qwen2.5:7b-instruct` | 845dbda0ea48 | 4.7 GB | 7 days ago | Qwen 2.5 7B instruction-tuned model |
| `qwen3:8b` | 500a1f067a9f | 5.2 GB | 7 days ago | Qwen 3 8B model |

**Notes:**
- Qwen models are multilingual and strong in Chinese, English, and other languages
- The 32B models share the same ID, indicating they're variations of the same base
- Qwen 2.5 instruct models are optimized for following instructions and tool use
- Good for complex reasoning and multilingual tasks

---

### DeepSeek Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `deepseek-r1:70b` | d37b54d01a76 | 42 GB | 7 days ago | DeepSeek R1 70B reasoning model |
| `deepseek-coder:1.3b` | 3ddd2d3fc8d2 | 776 MB | 7 days ago | DeepSeek Coder 1.3B specialized for code |

**Notes:**
- DeepSeek R1 features advanced reasoning capabilities with chain-of-thought
- DeepSeek Coder is optimized specifically for programming tasks
- R1 model includes thinking/reasoning tokens that can be extracted
- Good for mathematical reasoning, complex problem-solving, and code generation

---

### Code Llama Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `codellama:34b` | 685be00e1532 | 19 GB | 7 days ago | Code Llama 34B general code model |
| `codellama:13b` | 9f438cb9cd58 | 7.4 GB | 7 days ago | Code Llama 13B general code model |
| `codellama:13b-code` | 61b6aa1b3d0f | 7.4 GB | 7 days ago | Code Llama 13B code-focused variant |

**Notes:**
- Meta's Code Llama models are specialized for programming tasks
- Trained on code datasets and supports multiple programming languages
- Includes infilling capabilities for code completion
- Good for code generation, explanation, and debugging

---

### Llama Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `llama3.1:70b` | 711a9e8463af | 42 GB | 7 days ago | Llama 3.1 70B general-purpose model |
| `llama3.1:8b` | 46e0c10c039e | 4.9 GB | 7 days ago | Llama 3.1 8B general-purpose model |
| `llama3:8b` | 365c0bd3c000 | 4.7 GB | 7 days ago | Llama 3 8B general-purpose model |
| `llama3.2:3b` | a80c4f17acd5 | 2.0 GB | 7 days ago | Llama 3.2 3B lightweight model |

**Notes:**
- Meta's Llama series are strong general-purpose models
- Llama 3.1/3.2 include improved instruction following
- 70B model provides best performance but requires significant resources
- 3B model is optimized for speed and lower resource usage
- Good for general conversation, reasoning, and instruction following

---

### Specialized Coding Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `magicoder:7b` | 8007de06f5d9 | 3.8 GB | 7 days ago | Magicoder 7B code generation model |

**Notes:**
- Magicoder is designed for high-quality code generation
- Trained on curated code datasets
- Good for generating production-quality code

---

### Google Models
| Model Name | Model ID | Size | Modified | Description |
|------------|----------|------|----------|-------------|
| `gemma:7b` | a72c7f4d0a15 | 5.0 GB | 7 days ago | Google Gemma 7B model |

**Notes:**
- Google's Gemma models are derived from Gemini research
- Good for general-purpose tasks and instruction following
- Supports multi-turn conversations

---

## Model Categories

### By Size
- **Large Models (30GB+):** 
  - `deepseek-r1:70b` (42 GB)
  - `llama3.1:70b` (42 GB)
  
- **Medium Models (10-30GB):**
  - `qwen2.5:32b-instruct` (19 GB)
  - `qwen2.5:32b-instruct-q4_K_M` (19 GB)
  - `qwen2.5:32b` (19 GB)
  - `codellama:34b` (19 GB)

- **Standard Models (4-10GB):**
  - `mistral:latest` (4.4 GB)
  - `mistral:7b` (4.4 GB)
  - `qwen2.5:7b-instruct` (4.7 GB)
  - `llama3:8b` (4.7 GB)
  - `llama3.1:8b` (4.9 GB)
  - `gemma:7b` (5.0 GB)
  - `qwen3:8b` (5.2 GB)
  - `codellama:13b` (7.4 GB)
  - `codellama:13b-code` (7.4 GB)

- **Small Models (<4GB):**
  - `llama3.2:3b` (2.0 GB)
  - `magicoder:7b` (3.8 GB)
  - `deepseek-coder:1.3b` (776 MB)

### By Use Case

**General Purpose & Reasoning:**
- `llama3.1:70b` - Best overall performance
- `deepseek-r1:70b` - Advanced reasoning
- `qwen2.5:32b-instruct` - Multilingual reasoning
- `mistral:latest` - Fast general purpose

**Code Generation:**
- `deepseek-coder:1.3b` - Fast, lightweight coding
- `codellama:34b` - Best code quality (large)
- `codellama:13b` - Balanced code generation
- `magicoder:7b` - Production-quality code
- `codellama:13b-code` - Code-focused variant

**Instruction Following:**
- `qwen2.5:32b-instruct` - Complex instructions
- `llama3.1:8b` - Fast instruction following
- `mistral:latest` - Tool calling support

**Multilingual Tasks:**
- `qwen2.5:32b-instruct` - Strong multilingual support
- `qwen3:8b` - Multilingual capabilities
- `qwen2.5:7b-instruct` - Fast multilingual

**Resource-Constrained:**
- `llama3.2:3b` - Lowest resource usage
- `deepseek-coder:1.3b` - Minimal code model
- `llama3.1:8b` - Balanced performance/size

---

## Usage Recommendations

### For Agent Configuration (Model Orchestrator)

**Primary Models (High Autonomy, Complex Tasks):**
- `deepseek-r1:70b` - For complex reasoning tasks requiring step-by-step thinking
- `llama3.1:70b` - For general high-quality responses
- `qwen2.5:32b-instruct` - For multilingual and complex instruction following

**Fallback Models (Cost/Performance Balance):**
- `mistral:latest` - Fast, efficient, supports tool calling
- `llama3.1:8b` - Good performance-to-cost ratio
- `qwen2.5:7b-instruct` - Fast multilingual option

**Specialized Models:**
- **Code Tasks:** `codellama:34b`, `deepseek-coder:1.3b`, `magicoder:7b`
- **Quick Responses:** `llama3.2:3b`, `mistral:7b`
- **Reasoning Tasks:** `deepseek-r1:70b`, `qwen2.5:32b-instruct`

### Model Selection Guidelines

1. **Task Complexity:**
   - Simple tasks: Use 7B-8B models (mistral, llama3.1:8b, qwen2.5:7b)
   - Complex reasoning: Use 32B+ models (qwen2.5:32b, llama3.1:70b, deepseek-r1:70b)
   - Code generation: Use specialized code models

2. **Response Time Requirements:**
   - Fast responses: Use smaller models (3B-8B)
   - Quality over speed: Use larger models (32B-70B)

3. **Context Window Needs:**
   - All models support substantial context windows
   - Larger models generally handle longer contexts better

4. **Multilingual Requirements:**
   - Use Qwen models for best multilingual support
   - Llama and Mistral models are primarily English-optimized

5. **Tool Calling:**
   - Mistral and Qwen models have strong tool calling support
   - Consider for agent workflows requiring function execution

---

## Storage Summary

| Category | Count | Total Size (Approx) |
|----------|-------|---------------------|
| Large (30GB+) | 2 | 84 GB |
| Medium (10-30GB) | 4 | 76 GB |
| Standard (4-10GB) | 9 | ~50 GB |
| Small (<4GB) | 3 | ~7 GB |
| **Total** | **18** | **~217 GB** |

---

## Model Details Reference

For detailed model information, run:
```bash
ollama show <model-name>
```

To test a model:
```bash
ollama run <model-name>
```

To pull additional models:
```bash
ollama pull <model-name>
```

To remove a model:
```bash
ollama rm <model-name>
```

---

## Notes

- Model IDs that match indicate they share the same underlying model files
- Sizes shown are approximate and may vary based on quantization
- Modified dates reflect when the model was last accessed/downloaded
- All models are available locally and do not require internet connection for inference
- Models can be used concurrently depending on available system resources

---

## Integration with Agent Definitions

When configuring agents in `Agents-v2/`, use these model names in the `model_configuration.primary.model` and `model_configuration.fallback.model` fields.

Example:
```yaml
model_configuration:
  primary:
    model: 'deepseek-r1:70b'
    temperature: 0.7
    max_tokens: 4096
    reasoning_mode: 'chain-of-thought'
  fallback:
    model: 'mistral:latest'
    trigger_conditions: 'error conditions, latency thresholds'
```

