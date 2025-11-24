## Common Development Commands
### Environment Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run automated setup (installs deps, checks API keys, creates aliases)
./setup_orchestrator.sh

# Set required API keys (set only those you plan to use)
export XAI_API_KEY="your-grok-key"
export OPENAI_API_KEY="your-openai-key" 
export GOOGLE_API_KEY="your-google-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DIAL_API_KEY="your-dial-key"
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="your-azure-endpoint"
# AWS credentials for Bedrock (configure via AWS CLI or environment)
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
export AWS_REGION="us-east-1"
```

### Development Operations
```bash
# Make scripts executable (if needed)
chmod +x orchestrator-cli.py grok.sh grok_api.py model-orchestrator.py

# List all available models
./orchestrator-cli.py list --verbose

# Analyze a prompt to see model selection logic
./orchestrator-cli.py analyze "Write a Python web server"

# Route a request with specific strategy
./orchestrator-cli.py route "Explain quantum computing" --strategy quality_first

# Test system functionality
./orchestrator-cli.py test

# Show cost tracking report
./orchestrator-cli.py cost
```

## Common Development Commands
### Environment Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run automated setup (installs deps, checks API keys, creates aliases)
./setup_orchestrator.sh

# Set required API keys (set only those you plan to use)
export XAI_API_KEY="your-grok-key"
export OPENAI_API_KEY="your-openai-key" 
export GOOGLE_API_KEY="your-google-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DIAL_API_KEY="your-dial-key"
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="your-azure-endpoint"
# AWS credentials for Bedrock (configure via AWS CLI or environment)
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
export AWS_REGION="us-east-1"
```

### Development Operations
```bash
# Make scripts executable (if needed)
chmod +x orchestrator-cli.py grok.sh grok_api.py model-orchestrator.py

# List all available models
./orchestrator-cli.py list --verbose

# Analyze a prompt to see model selection logic
./orchestrator-cli.py analyze "Write a Python web server"

# Route a request with specific strategy
./orchestrator-cli.py route "Explain quantum computing" --strategy quality_first

# Test system functionality
./orchestrator-cli.py test

# Show cost tracking report
./orchestrator-cli.py cost
```

### Testing Commands
```bash
# Run comprehensive integration tests
python3 test_integration.py

# Run real-world API tests (requires API keys)
python3 test_real_world.py

# Test specific orchestrator functionality
./orchestrator-cli.py test

# Test Grok models specifically
./grok.sh list
./grok.sh quick "Hello world test"
```
