### Quick Start with Local Models
```bash
# Complete local setup in 3 commands
curl -fsSL https://ollama.com/install.sh | sh
./start-ollama.sh
ollama pull llama3.2:8b && ./warmup-models.sh

# Test local model integration
./orchestrator-cli.py route "Hello world" --strategy cost_optimize
# Should select a local Llama model with $0.00 cost
```