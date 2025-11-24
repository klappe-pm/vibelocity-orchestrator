# Troubleshooting Guide

## Table of Contents

1. [Quick Diagnostic](#quick-diagnostic)
2. [API Key Issues](#api-key-issues)
3. [Model Selection Problems](#model-selection-problems)
4. [Local Model Issues](#local-model-issues)
5. [Performance Issues](#performance-issues)
6. [Agent Issues](#agent-issues)
7. [Cost and Usage Issues](#cost-and-usage-issues)
8. [Testing Issues](#testing-issues)
9. [Integration Issues](#integration-issues)
10. [File and Permission Issues](#file-and-permission-issues)
11. [Configuration Issues](#configuration-issues)
12. [Getting Help](#getting-help)

---

## Quick Diagnostic

### System Health Check

Run this quick diagnostic to identify common issues:

```bash
# 1. Check Ollama service (for local models)
curl http://localhost:11434/api/version
ollama list

# 2. Verify installed models
ls -la ~/.ollama/models/

# 3. Check system resources
vm_stat | head -4              # macOS
free -h                        # Linux

# 4. Verify API keys configured
./setup_orchestrator.sh        # Shows missing keys

# 5. Test API connectivity
./orchestrator-cli.py test

# 6. Check agent definitions exist
ls -l gitignore/Claude\ Agents/*.md

# 7. Verify project context file
cat gitignore/Claude\ Context/CLAUDE.context.md | head -20
```

### Common Symptom Quick Reference

| Symptom | Likely Issue | Quick Fix |
|---------|-------------|-----------|
| "Model not found" | Local model not installed | `ollama pull [model-name]` |
| "Out of memory" | RAM exceeded | Close apps or use smaller model |
| "API key invalid" | Missing/wrong API key | Run `./setup_orchestrator.sh` |
| "Agent scope violation" | Wrong agent activated | Check task description matches agent scope |
| "File permission denied" | Permission issue | `chmod 644 [file]` |
| "High costs" | Cloud model overuse | Switch to `cost_optimize` strategy |
| "Connection timeout" | Ollama not running | `./start-ollama.sh` |

---

## API Key Issues

### Issue: Missing or Invalid API Keys

**Symptoms**:
- Error: "API key invalid"
- "API client connection failed"
- Authentication errors

**Solutions**:

**Solution 1: Check and Configure API Keys**
```bash
# Check which API keys are set
./setup_orchestrator.sh  # Shows missing keys

# Set API keys for current session
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
export XAI_API_KEY="..."

# Test API connectivity
./orchestrator-cli.py test
```

**Solution 2: Persist API Keys**
```bash
# Determine your shell
echo $SHELL

# For zsh (default macOS Catalina+)
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

**Solution 3: Use .env File** (Alternative)
```bash
# Create .env file in project root
cat > .env << EOF
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
XAI_API_KEY=...
EOF

# Load with:
source .env
```

**Solution 4: Test Network Connectivity**
```bash
# Test API endpoint accessibility
curl -I https://api.openai.com/v1/models
curl -I https://api.anthropic.com/v1/messages

# If blocked, check firewall/proxy settings
```

---

## Model Selection Problems

### Issue: Model Selection Not Optimal

**Symptoms**:
- Expensive cloud model selected for simple task
- Low-quality model selected for critical task
- Local models not preferred despite availability

**Solutions**:

**Solution 1: Debug Model Selection**
```bash
# Debug model selection for a specific prompt
./orchestrator-cli.py analyze "your problematic prompt"

# List available models to verify configuration
./orchestrator-cli.py list --verbose
```

**Solution 2: Use Correct Strategy**
```python
# For development/testing - prefer local models
model_id, model = orchestrator.select_model(
    "Task description",
    strategy="cost_optimize"  # Prefers local models
)

# For critical decisions - prefer quality
model_id, model = orchestrator.select_model(
    "Important task",
    strategy="quality_first"  # Best accuracy/reasoning
)

# For quick queries - prefer speed
model_id, model = orchestrator.select_model(
    "Quick question",
    strategy="speed_priority"  # Fastest models
)
```

**Solution 3: Specify Requirements Explicitly**
```python
from model_orchestrator import TaskRequirements, TaskType

requirements = TaskRequirements(
    task_type=TaskType.CODE_GENERATION,
    max_cost=0.0,  # Force local models only
    quality_threshold=0.85
)

model_id, model = orchestrator.select_model_with_requirements(requirements)
```

### Issue: Model Configuration Not Loading

**Symptoms**:
- Orchestrator shows 0 models available
- Model list empty
- Selection always fails

**Solutions**:

**Solution 1: Check Model Loading**
```python
# Test model loading
from model_orchestrator import ModelOrchestrator

orchestrator = ModelOrchestrator()
print(f"Models loaded: {len(orchestrator.models)}")

# Should show 63+ models
# If 0, check _load_models() method
```

**Solution 2: Verify Configuration Files**
```bash
# Check for orchestrator configuration
ls -l orchestrator_config.yaml grok-models-config.yaml

# Verify rate limits and model definitions
cat grok-models-config.yaml
```

---

## Local Model Issues

### Issue: Ollama Service Not Running

**Symptoms**:
- Error: "Model not found"
- Connection refused to localhost:11434
- Local models unavailable

**Solutions**:

**Solution 1: Start Ollama Service**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version
ps aux | grep ollama

# Start Ollama service
./start-ollama.sh

# Or manually
ollama serve &

# Or use system service
brew services start ollama  # macOS
systemctl start ollama      # Linux
```

**Solution 2: Verify Ollama Installation**
```bash
# Check Ollama version
ollama --version

# If not installed, install from https://ollama.ai
```

### Issue: Model Not Available Locally

**Symptoms**:
- Error: "Model not found: [model-name]"
- Orchestrator falls back to cloud models unexpectedly
- `ollama list` does not show expected model

**Solutions**:

**Solution 1: Install Missing Models**
```bash
# Check installed models
ollama list

# Install missing models
ollama pull llama3.2:8b       # Example
ollama pull codellama:34b      # Example
ollama pull magicoder:7b       # Example
ollama pull deepseek-r1:70b    # Example

# Verify installation
ollama list | grep [model-name]
```

**Solution 2: Test Specific Model**
```bash
# Test if model works
ollama run llama3.2:8b "Hello world"

# Check model status
ollama ps
```

**Solution 3: Verify Model Name Match**
```bash
# List exact model names
ollama list

# Ensure orchestrator model IDs match
# Example: "codellama:34b" not "CodeLlama 34B"
```

### Issue: Out of Memory Error

**Symptoms**:
- Error: "Out of memory" or system slowdown
- Model load fails
- System becomes unresponsive

**Solutions**:

**Solution 1: Check RAM Requirements and Usage**
```bash
# Check memory usage
vm_stat | head -4              # macOS
free -h                        # Linux
htop                          # Linux (detailed)

# Model RAM requirements:
# - Llama 3.2 8B: ~8GB
# - CodeLlama 34B: ~30GB
# - DeepSeek R1 70B: ~42GB
# - Qwen 2.5 32B: ~25GB
# - Magicoder 7B: ~8GB
# - DeepSeek Coder 1.3B: ~2GB
```

**Solution 2: Use Smaller Model Variants**
```bash
# If RAM limited, use smaller variants
ollama pull codellama:13b      # Instead of 34B
ollama pull qwen2.5:7b-instruct # Instead of 32B
ollama pull llama3.2:3b        # Instead of 8B
```

**Solution 3: Free Up Memory**
```bash
# Stop Ollama to unload all models
ollama stop

# Restart and load only needed models
ollama serve &

# Close memory-intensive applications
```

### Issue: Slow Model Response Time

**Symptoms**:
- Local models respond slowly (>30 seconds)
- First request very slow
- System resource saturation

**Solutions**:

**Solution 1: Pre-warm Models**
```bash
# Run warmup script to load models into memory
./Model\ Orchestrator/warmup-models.sh

# Or aggressive parallel warmup
./Model\ Orchestrator/warmup-aggressive-parallel.sh

# Keep frequently-used models loaded
./Model\ Orchestrator/optimized-keep-alive.py
```

**Solution 2: Use Appropriate Model Size**
```bash
# For fast responses, use smaller models
ollama pull llama3.2:3b        # Very fast
ollama pull deepseek-coder:1.3b # Quick code

# Use speed_priority strategy
```

---

## Performance Issues

### Issue: High Latency for Simple Tasks

**Symptoms**:
- Simple queries take >5 seconds
- Model selection takes excessive time
- System feels sluggish

**Solutions**:

**Solution 1: Use Speed-Priority Strategy**
```python
# For simple queries
model_id, model = orchestrator.select_model(
    "What is Python?",
    strategy="speed_priority"
)
```

**Solution 2: Pre-load Frequently-Used Models**
```bash
# Keep core models loaded in memory
./Model\ Orchestrator/optimized-keep-alive.py

# Use warmup script
./Model\ Orchestrator/warmup-models.sh
```

**Solution 3: Check System Resources**
```bash
# Check CPU usage
top -o cpu  # macOS
htop        # Linux

# Ensure adequate cooling (check for thermal throttling)
# Close resource-intensive applications
```

### Issue: Large Context Models Slow

**Symptoms**:
- Models with 2M+ context (Grok-4 variants) respond slowly
- Timeout errors with large inputs

**Solutions**:

**Solution 1: Check Rate Limits**
```bash
# Review rate limits in configuration
cat grok-models-config.yaml

# Adjust if needed for your use case
```

**Solution 2: Use Appropriate Model**
- Models with 2M+ context handle larger inputs but may be slower
- For quick responses, use models with standard context windows
- Reserve large-context models for tasks that require them

---

## Agent Issues

### Issue: Agent Scope Violation

**Symptoms**:
- Error: "Agent scope violation: attempted to access forbidden resource"
- Task fails to complete
- Handoff loop between agents

**Solutions**:

**Solution 1: Verify Correct Agent**
```bash
# Review agent definition
cat gitignore/Claude\ Agents/[Agent-Name].md

# Ensure task matches agent scope
```

**Solution 2: Rephrase Request**
```
Instead of: "Fix the orchestrator code and update README"
(Requires 2 agents)

Use: "Fix the orchestrator code"
Then: "Update README with orchestrator changes"
(Sequential)
```

### Issue: Agent Not Activating

**Symptoms**:
- Expected agent does not activate
- Wrong agent handles request

**Solutions**:

**Solution 1: Include Agent-Specific Keywords**
```
Generic: "Check the code"
Specific: "Perform a security audit of the code"
```

**Solution 2: Verify Agent File Exists**
```bash
# Check agent definition exists
ls -l gitignore/Claude\ Agents/[Agent-Name].md

# Verify status is "Active"
head -10 gitignore/Claude\ Agents/[Agent-Name].md
```

---

## Cost and Usage Issues

### Issue: Unexpected High Costs

**Symptoms**:
- Cost report shows higher than expected expenses
- Budget exceeded

**Solutions**:

**Solution 1: Audit Model Usage**
```bash
# View cost report
./orchestrator-cli.py cost

# Identify expensive models
```

**Solution 2: Switch to Cost-Optimize Strategy**
```python
# Prefer local models
model_id, model = orchestrator.select_model(
    prompt,
    strategy="cost_optimize"
)
```

**Solution 3: Set Cost Thresholds**
```python
requirements = TaskRequirements(
    task_type=TaskType.CODE_GENERATION,
    max_cost=0.05,  # $0.05 max per request
    quality_threshold=0.75
)
```

---

## Testing Issues

### Issue: Async Tests Not Running

**Symptoms**:
- Tests skipped or not executed
- Async test errors

**Solution**:
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Run tests
python -m pytest tests/test_integration_comprehensive.py
```

### Issue: Import Errors in Tests

**Symptoms**:
- ModuleNotFoundError
- Import fails

**Solution**:
```bash
# Set PYTHONPATH
export PYTHONPATH="/Users/kevinlappe/Obsidian/Power Prompts/Model Orchestrator:$PYTHONPATH"

# Run tests
python -m pytest tests/
```

### Issue: Mock Not Working

**Symptoms**:
- Mock objects not functioning
- Real API calls during tests

**Solution**:
```bash
# Verify mock setup
python -c "from unittest.mock import AsyncMock; print('OK')"

# If error, update Python or unittest
```

### Issue: Tests Timing Out

**Symptoms**:
- Tests exceed time limit
- Hung tests

**Solution**:
```bash
# Increase timeout
python -m pytest tests/test_integration_comprehensive.py --timeout=60

# Run with debug output
python -m pytest tests/test_integration_comprehensive.py -vv --tb=long --log-cli-level=DEBUG
```

---

## Integration Issues

### Issue: Claude Code Not Activating Agents

**Symptoms**:
- Agents not responding to requests
- No agent coordination

**Solutions**:

**Solution 1: Verify Agent Files Location**
```bash
# Check agent definitions exist
ls -l gitignore/Claude\ Agents/*.md
```

**Solution 2: Check Configuration**
```bash
# Verify CLAUDE.md exists
cat CLAUDE.md | head -20

# Verify context file
cat gitignore/Claude\ Context/CLAUDE.context.md | head -30
```

---

## File and Permission Issues

### Issue: Permission Denied Errors

**Symptoms**:
- Error: "Permission denied"
- File operations fail

**Solutions**:

**Solution 1: Fix File Permissions**
```bash
# Check permissions
ls -la gitignore/Claude\ Agents/

# Fix file permissions
chmod 644 gitignore/Claude\ Agents/*.md

# Fix directory permissions
chmod 755 gitignore/Claude\ Agents/
```

**Solution 2: Check Ownership**
```bash
# Check file owner
ls -l gitignore/Claude\ Agents/*.md

# Fix if needed
sudo chown $USER:$USER gitignore/Claude\ Agents/*.md
```

---

## Configuration Issues

### Issue: Environment Variables Not Persisting

**Symptoms**:
- API keys not available in new sessions
- Must re-export keys each time

**Solutions**:

See [API Key Issues](#api-key-issues) section for detailed solutions.

---

## Getting Help

### Self-Service Resources

1. **Documentation**:
   - Multi-Agent System User Guide
   - Model Orchestrator API Documentation
   - Agent Creation Tutorial

2. **Context Files**:
   - `gitignore/Claude Context/CLAUDE.context.md`
   - `CLAUDE.md`
   - `README.md`

3. **Model Guide**:
   - `gitignore/Claude Context/MODELS.md`

### Debug Mode

Enable verbose logging:

```bash
# Set debug environment variable
export ORCHESTRATOR_LOG_LEVEL=DEBUG

# Run with verbose output
./orchestrator-cli.py --verbose list
./orchestrator-cli.py --verbose analyze "Test task"

# For tests
python -m pytest -vv --tb=long --log-cli-level=DEBUG
```

### Quick Reference Commands

```bash
# System Health
ollama list                                          # List models
curl http://localhost:11434/api/version             # Check Ollama
vm_stat | head -4                                   # Memory (macOS)
free -h                                             # Memory (Linux)

# Setup and Testing
./setup_orchestrator.sh                             # Check API keys
./orchestrator-cli.py test                          # Test connectivity
./start-ollama.sh                                   # Start Ollama

# Model Management
ollama pull [model]                                 # Install model
ollama ps                                           # Check running models
./Model\ Orchestrator/warmup-models.sh              # Pre-warm models

# Orchestrator
./orchestrator-cli.py list --verbose                # List models
./orchestrator-cli.py analyze "Task"                # Analyze task
./orchestrator-cli.py cost                          # View costs

# Debugging
./orchestrator-cli.py --verbose analyze "Task"      # Debug selection
cat gitignore/Claude\ Context/CLAUDE.context.md     # Check context
ls -l gitignore/Claude\ Agents/*.md                 # List agents
```

---

**Guide Version**: 2.0  
**Last Updated**: 2025-11-09  
**Maintained By**: Documentation & Knowledge Agent