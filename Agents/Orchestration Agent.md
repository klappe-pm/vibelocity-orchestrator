# Model Orchestration Agent

## Agent Overview

**Agent Name**: Model Orchestration Agent  
**Role**: Intelligent multi-model routing and cost optimization  
**Primary Responsibility**: Route tasks across **63 AI models** from **8 providers** with optimal cost and performance characteristics

## Agent Capabilities

### Core Functions
- **Task Analysis**: Automatically detect task type and requirements from user prompts
- **Model Selection**: Score and rank models based on task affinity, performance, accuracy, and cost
- **Cost Optimization**: Track and minimize costs across all providers while meeting quality requirements
- **Multi-Model Patterns**: Support chain of thought, parallel consensus, hierarchical refinement
- **Local Model Management**: Zero-cost model utilization with privacy and offline capabilities

### Local Models Capabilities
- **Zero Cost**: 20 models with no API fees or usage limits
- **Full Privacy**: All processing happens locally, no data sent to external APIs
- **Offline Operation**: Complete functionality without internet connectivity
- **Resource Management**: Intelligent RAM and storage optimization
- **Model Families**: 
  - **CodeLlama**: Best local code generation (34B, 13B variants)
  - **DeepSeek R1**: Ultimate local reasoning (70B model)
  - **Magicoder**: Optimal code generation balance (7B model)
  - **Qwen**: Multilingual reasoning and analysis (32B, 7B-instruct, 8B variants)
  - **Llama**: General purpose models across multiple sizes
  - **Gemma**: Google's balanced performance model (7B)

### Supported Providers (63 Total Models)
- **Local/Ollama**: 20 models (Llama, CodeLlama, DeepSeek, Qwen, Magicoder, Gemma families) - **ZERO COST**
- **OpenAI**: 11 models (GPT-4, GPT-3.5, O1, O3 families)
- **Amazon Bedrock**: 8 models (Bedrock Claude, Llama, Titan)
- **Anthropic Claude**: 7 models (Claude 4 & 3 families)
- **Google Gemini**: 6 models (Gemini 2.0 & 1.5 families)
- **xAI Grok**: 5 models (2M context variants, vision)
- **Microsoft Azure**: 4 models (Azure OpenAI & Claude)
- **DIAL Gateway**: 2 models (Enterprise API access)

## Task Type Classifications

The agent automatically detects and optimizes for these task types:

### Primary Categories
- **CODE_GENERATION**: Writing new code, functions, classes
- **CODE_REVIEW**: Analyzing and improving existing code
- **DEBUGGING**: Finding and fixing code errors
- **REASONING**: Complex logical analysis and problem-solving
- **ANALYSIS**: Data analysis, system analysis, research
- **SYSTEM_DESIGN**: Architecture planning and design
- **VISION**: Image analysis and visual understanding
- **IMAGE_GENERATION**: Creating visual content
- **CREATIVE_WRITING**: Stories, poems, creative content
- **TRANSLATION**: Language translation tasks
- **SUMMARIZATION**: Text summarization and condensation
- **QA**: Question answering tasks
- **CONVERSATION**: General conversational interactions
- **RESEARCH**: Information gathering and synthesis
- **DATA_ANALYSIS**: Processing and interpreting data

## Scoring Algorithm

The agent uses a weighted scoring system for model selection:

### Weight Distribution
- **Task Affinity (40%)**: How well the model handles the specific task type
- **Performance (30%)**: Speed vs reasoning depth trade-off based on requirements
- **Accuracy (20%)**: Model accuracy rating for the detected task type
- **Cost Efficiency (10%)**: Price/performance ratio optimization

### Selection Strategies
- **balanced**: Default strategy balancing all factors
- **cost_optimize**: Minimize costs while meeting quality requirements
- **quality_first**: Maximize accuracy and reasoning capability
- **speed_priority**: Optimize for fastest response time

## Integration Points

### Claude Configuration System
- Integrates with existing `CLAUDE.md.md` configuration
- Respects Claude context management through snapshot files
- Aligns with task planning integration workflow
- Maintains cost tracking alignment with multi-provider optimization

### Zen MCP Bridge
- Extends Zen MCP tools with intelligent model routing
- Provides multi-model consensus support
- Enables adaptive analysis depth adjustment
- Supports tool-to-model mapping

### API Client Management
- Unified interface across all **8 providers** (including local Ollama)
- Handles authentication and rate limiting for cloud providers
- Manages provider-specific formatting requirements
- Implements retry logic and error handling
- **Local Model Integration**: Direct Ollama API for zero-cost models

## Sub-Agents

### Task Analysis Sub-Agent
**Role**: Prompt analysis and requirement detection  
**Responsibilities**:
- Parse user prompts for task type indicators
- Estimate context window requirements
- Detect special capability needs (vision, reasoning, functions)
- Set quality thresholds and constraints

### Cost Optimization Sub-Agent
**Role**: Multi-provider cost tracking and optimization  
**Responsibilities**:
- Track usage and costs across all **8 providers**
- Generate cost reports and analytics (including $0 local model usage)
- Optimize provider selection for cost efficiency
- Manage rate limits and quotas
- **Local Model Prioritization**: Prefer zero-cost models when suitable
- **Resource Monitoring**: Track RAM and storage usage for local models

### Model Scoring Sub-Agent
**Role**: Model capability assessment and ranking  
**Responsibilities**:
- Score models against task requirements
- Apply strategy-specific modifiers
- Handle provider preferences
- Manage model availability status

### Consensus Management Sub-Agent
**Role**: Multi-model interaction coordination  
**Responsibilities**:
- Create diverse model consensus groups
- Coordinate parallel model execution
- Aggregate and synthesize multi-model responses
- Manage hierarchical refinement workflows

## Input Requirements

### Required Inputs
- **Prompt**: User task description or question
- **Context**: Optional additional context or constraints

### Optional Parameters
- **Strategy**: Selection strategy (balanced, cost_optimize, quality_first, speed_priority)
- **Max Cost**: Maximum acceptable cost per request
- **Preferred Providers**: List of preferred model providers
- **Quality Threshold**: Minimum acceptable quality score
- **Max Latency**: Maximum acceptable response time

## Output Specifications

### Primary Outputs
- **Selected Model**: Optimal model ID and provider
- **Rationale**: Explanation of selection logic
- **Cost Estimate**: Projected cost for the request
- **Capability Match**: How well the model fits the task

### Extended Outputs (Optional)
- **Alternative Models**: Top 5 alternative model recommendations
- **Cost Comparison**: Cost analysis across top models (including $0 local models)
- **Performance Metrics**: Expected speed, accuracy, creativity scores
- **Usage Analytics**: Historical usage and performance data
- **Local Model Availability**: Status of local models and resource usage

## Dependencies

### External Dependencies
- **API Keys**: Valid authentication for desired cloud providers (optional)
- **Network Access**: Internet connectivity for cloud providers (optional for local-only usage)
- **Local Models**: Ollama (recommended) or compatible local model server
- **Hardware**: Sufficient RAM for local models (8GB+ minimum, 64GB+ optimal for large models)
- **Storage**: 10-150GB for local model storage (20 models available)

### Local Model Requirements
- **Ollama Service**: Version 0.1.x or higher
- **Model Storage**: ~110GB total for all 20 local models
- **RAM Requirements by Model Size**:
  - Small models (1.3B-8B): 2-8GB RAM
  - Medium models (13B-32B): 12-25GB RAM  
  - Large models (34B-70B): 30-50GB RAM

### Internal Dependencies
- **Model Configuration**: Up-to-date model capability definitions
- **Cost Database**: Current pricing information
- **Performance History**: Historical model performance data

## Handoff Instructions

### To Downstream Agents
1. **Provide selected model information**: Include model ID, provider, and rationale
2. **Include cost estimates**: Pass through projected costs for budget tracking
3. **Share task analysis**: Provide detected task type and requirements for consistency
4. **Pass configuration**: Include any strategy or preference overrides

### From Upstream Agents
1. **Accept task specifications**: Receive clear task descriptions and constraints
2. **Process context data**: Incorporate any additional context or requirements
3. **Respect preferences**: Honor any provider or strategy preferences
4. **Maintain cost awareness**: Consider any budget constraints or cost targets

## Performance Metrics

### Key Performance Indicators
- **Selection Accuracy**: How often the selected model performs optimally
- **Cost Efficiency**: Actual vs. projected costs across providers
- **Response Time**: Model selection and routing latency
- **Provider Coverage**: Utilization across all available providers

### Optimization Targets
- **<10ms Model Selection**: Fast model scoring and selection
- **>90% Cost Accuracy**: Accurate cost estimation
- **>95% Availability**: High system availability across providers
- **<5% Cost Variance**: Consistent cost optimization performance

## Error Handling

### Common Error Scenarios
- **No Available Models**: All models fail requirements check
- **API Key Missing**: Required authentication not available
- **Rate Limit Exceeded**: Provider-specific rate limiting
- **Model Unavailable**: Temporary model or provider outage

### Recovery Strategies
- **Fallback Selection**: Automatic fallback to alternative models
- **Graceful Degradation**: Relax constraints to find suitable models
- **Error Reporting**: Clear error messages with suggested actions
- **Retry Logic**: Intelligent retry with exponential backoff

## Configuration Files

### Primary Configuration
- **model-orchestrator.py**: Main orchestration logic and model definitions
- **api_clients.py**: Provider-specific API client implementations
- **grok-models-config.yaml**: Grok-specific model configuration

### Supporting Configuration
- **requirements.txt**: Python dependencies
- **setup_orchestrator.sh**: Automated setup and initialization
- **orchestrator-cli.py**: Command-line interface
- **start-ollama.sh**: Local model service startup and management
- **warmup-models.sh**: Local model performance optimization
- **local-models-setup.md**: Complete local models setup guide

## Usage Examples

### Basic Model Selection
```python
orchestrator = ModelOrchestrator()
model_id, model = orchestrator.select_model("Write a Python web server")
```

### Cost-Optimized Selection
```python
model_id, model = orchestrator.select_model(
    "Analyze this data", 
    strategy="cost_optimize"
)
```

### Multi-Model Consensus
```python
consensus_group = orchestrator.create_consensus_group(
    "What's the best database for this project?", 
    num_models=3, 
    diverse=True
)
```

### Maintenance Requirements

### Regular Updates
- **Model Pricing**: Update cost information monthly
- **Model Availability**: Monitor provider model status
- **Performance Metrics**: Calibrate scoring based on usage data
- **API Changes**: Adapt to provider API updates
- **Local Models**: Update Ollama and local models as needed

### Monitoring Requirements
- **Cost Tracking**: Daily cost analysis and reporting
- **Performance Analysis**: Weekly model performance review
- **Error Monitoring**: Real-time error tracking and alerting
- **Usage Analytics**: Monthly usage pattern analysis
- **Local Model Health**: Monitor Ollama service status and model loading times
- **Resource Usage**: Monitor RAM and storage usage for local models
