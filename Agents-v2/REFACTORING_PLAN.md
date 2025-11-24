# Agent Transformation System - Refactoring Plan
**Integrating Model Orchestrator v1 Architecture**

## Executive Summary

The existing Model Orchestrator v1 is a production-ready, sophisticated system managing **63 models across 8 providers** with advanced features like:
- Intelligent task-based routing
- Cost optimization and tracking
- Multi-model consensus validation
- Fallback chains for reliability
- RAM-aware local model management
- Real API integration with retry logic

This refactoring plan outlines how to integrate these battle-tested components into the agent transformation system to achieve:
- **3-5x speed improvement** through parallel multi-model processing
- **80% cost reduction** by prioritizing local Ollama models
- **Superior quality** through consensus validation
- **100% reliability** via intelligent fallback chains

---

## Current State Analysis

### Agents-v2 (Current Simple System)
```
orchestrate_transformations.py (380 lines)
├── Single model (GPT-4o-mini)
├── Sequential processing (3 concurrent workers)
├── Basic error handling
├── Simple progress tracking
└── No cost optimization
```

**Limitations:**
- ❌ Single model = single point of failure
- ❌ No local model utilization = high costs
- ❌ No quality validation = inconsistent output
- ❌ Basic concurrency = slow processing
- ❌ No task analysis = inefficient routing

### Model Orchestrator v1 (Proven Production System)
```
Model Orchestrator/
├── model-orchestrator-consolidated.py (1,200+ lines)
├── api_clients.py (unified API handling)
├── zen_mcp_bridge.py (MCP integration)
├── local_model_manager.py (RAM-aware management)
├── ram_monitor.py (system resource tracking)
├── grok_api.py (xAI integration)
├── optimized-keep-alive.py (model warm-up)
└── tests/ (42 tests, 78% coverage)
```

**Capabilities:**
- ✅ 63 models (20 local, 43 cloud)
- ✅ Intelligent task routing
- ✅ Cost optimization ($0.00 local preference)
- ✅ Consensus validation
- ✅ Fallback chains
- ✅ Real-time monitoring
- ✅ Production-tested

---

## Refactoring Strategy

### Phase 1: Foundation (Days 1-2)
**Goal:** Set up multi-model infrastructure

#### 1.1 Create Unified Configuration
```bash
Agents-v2/
├── config/
│   ├── models.yaml              # Model definitions (from v1)
│   ├── providers.yaml           # Provider configurations
│   ├── routing_rules.yaml       # Task-to-model routing
│   └── cost_optimization.yaml   # Budget and cost rules
```

**Key Configuration:**
```yaml
# models.yaml
local_models:
  tier_1_fast:
    - deepseek-coder:1.3b  # 0.776 GB, instant
    - llama3.2:3b          # 2.0 GB, fast
  tier_2_balanced:
    - magicoder:7b         # 3.8 GB, code specialist
    - qwen2.5:7b-instruct  # 4.7 GB, instruction-tuned
  tier_3_power:
    - codellama:34b        # 19 GB, premium code
    - deepseek-r1:70b      # 42 GB, ultimate reasoning

cloud_models:
  primary:
    - gpt-4o-mini          # $0.15/$0.60 per M tokens
  secondary:
    - claude-3-haiku       # $0.25/$1.25 per M tokens
  premium:
    - claude-sonnet-4      # $3/$15 per M tokens

routing_strategy:
  simple_agents: local_models.tier_1_fast
  standard_agents: local_models.tier_2_balanced
  complex_agents: [local_models.tier_2_balanced, cloud_models.primary]
  critical_agents: consensus(local.tier_3 + cloud.premium)
```

#### 1.2 Integrate Core Orchestrator
Copy and adapt key components:

```python
# agent_transformation_orchestrator.py (new)
from model_orchestrator_consolidated import (
    ModelOrchestrator,
    TaskType,
    ModelProvider,
    TaskRequirements
)
from api_clients import (
    OpenAIAPIClient,
    AnthropicAPIClient,
    OllamaAPIClient  # Local models
)
from local_model_manager import LocalModelManager

class AgentTransformationOrchestrator(ModelOrchestrator):
    """Specialized orchestrator for agent transformations"""
    
    def __init__(self):
        super().__init__()
        self.local_manager = LocalModelManager()
        self.task_analyzer = AgentTaskAnalyzer()
        
    def analyze_agent_complexity(self, v1_yaml: str) -> TaskRequirements:
        """Analyze agent to determine transformation requirements"""
        # Check agent size, complexity, critical sections
        # Return TaskRequirements with appropriate model selection
        pass
    
    def transform_with_consensus(self, 
                                 agent_name: str,
                                 num_models: int = 2) -> str:
        """Transform using multiple models for validation"""
        pass
```

#### 1.3 Set Up Model Pools
```python
# model_pools.py (new)
class ModelPool:
    """Manages pools of models for concurrent processing"""
    
    def __init__(self):
        self.local_pool = LocalModelPool(
            models=["magicoder:7b", "qwen2.5:7b-instruct"],
            max_workers=4
        )
        self.cloud_pool = CloudModelPool(
            models=["gpt-4o-mini"],
            max_workers=3
        )
        
    async def process_batch(self, agents: List[str]) -> List[Result]:
        """Process agents across multiple models concurrently"""
        # Distribute agents across pools
        # Use local for simple, cloud for complex
        pass
```

---

### Phase 2: Intelligent Routing (Days 3-4)
**Goal:** Implement smart task analysis and routing

#### 2.1 Agent Complexity Analyzer
```python
# agent_analyzer.py (new)
class AgentTaskAnalyzer:
    """Analyzes v1 agents to determine transformation complexity"""
    
    def analyze(self, v1_yaml: str) -> ComplexityProfile:
        """
        Returns:
        - complexity_score: 0-1 (simple to complex)
        - estimated_tokens: input + output estimate
        - recommended_model_tier: local_fast, local_balanced, cloud, premium
        - requires_consensus: bool
        """
        metrics = {
            'yaml_size': len(v1_yaml),
            'num_responsibilities': self._count_responsibilities(v1_yaml),
            'has_complex_logic': self._detect_complex_patterns(v1_yaml),
            'is_critical_agent': self._is_critical(v1_yaml)
        }
        
        if metrics['is_critical_agent']:
            return ComplexityProfile(
                score=0.9,
                tier='premium',
                requires_consensus=True,
                num_consensus_models=3
            )
        elif metrics['has_complex_logic']:
            return ComplexityProfile(
                score=0.7,
                tier='cloud',
                requires_consensus=False
            )
        else:
            return ComplexityProfile(
                score=0.3,
                tier='local_balanced',
                requires_consensus=False
            )
```

#### 2.2 Dynamic Model Router
```python
# routing.py (adapted from model_router.py)
class AgentRouter:
    """Routes agents to optimal models based on analysis"""
    
    def __init__(self, orchestrator: ModelOrchestrator):
        self.orchestrator = orchestrator
        self.analyzer = AgentTaskAnalyzer()
        
    def select_model(self, agent_name: str, v1_content: str) -> str:
        """Select best model for agent transformation"""
        profile = self.analyzer.analyze(v1_content)
        
        # Cost optimization: prefer local models
        if profile.tier == 'local_fast':
            # Use fastest local model
            return self.orchestrator.select_model(
                task_type=TaskType.CODE_GENERATION,
                strategy='speed_priority',
                preferred_providers=[ModelProvider.LOCAL]
            )
        elif profile.tier == 'local_balanced':
            # Use balanced local model
            return 'magicoder:7b'  # or qwen2.5:7b-instruct
        elif profile.tier == 'cloud':
            # Use cloud for complex agents
            return 'gpt-4o-mini'
        else:
            # Premium for critical agents
            return 'claude-sonnet-4'
```

---

### Phase 3: Parallel Processing Engine (Days 5-7)
**Goal:** Implement high-performance concurrent processing

#### 3.1 Multi-Model Processor
```python
# parallel_processor.py (new)
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class ParallelTransformationEngine:
    """Process multiple agents across multiple models concurrently"""
    
    def __init__(self, orchestrator: AgentTransformationOrchestrator):
        self.orchestrator = orchestrator
        self.local_executor = ThreadPoolExecutor(max_workers=4)
        self.cloud_executor = ThreadPoolExecutor(max_workers=3)
        
    async def transform_category(self, 
                                  category: str,
                                  agents: List[str]) -> Results:
        """Transform entire category using optimal parallelization"""
        
        # Analyze all agents first
        profiles = [
            self.orchestrator.task_analyzer.analyze(agent)
            for agent in agents
        ]
        
        # Group by complexity
        simple = [a for a, p in zip(agents, profiles) if p.tier == 'local_fast']
        standard = [a for a, p in zip(agents, profiles) if p.tier == 'local_balanced']
        complex = [a for a, p in zip(agents, profiles) if p.tier == 'cloud']
        critical = [a for a, p in zip(agents, profiles) if p.requires_consensus]
        
        # Process in parallel with appropriate models
        results = await asyncio.gather(
            self._process_batch_local(simple, model='deepseek-coder:1.3b'),
            self._process_batch_local(standard, model='magicoder:7b'),
            self._process_batch_cloud(complex, model='gpt-4o-mini'),
            self._process_with_consensus(critical, num_models=3)
        )
        
        return self._merge_results(results)
```

#### 3.2 Load Balancing
```python
# load_balancer.py (new)
class LoadBalancer:
    """Dynamically balance load across available models"""
    
    def __init__(self):
        self.model_stats = {}  # Track response times, success rates
        self.model_queues = {}  # Task queues per model
        
    def assign_task(self, task: AgentTransformation) -> str:
        """Assign task to best available model"""
        profile = task.complexity_profile
        
        # Get eligible models
        eligible = self._get_eligible_models(profile)
        
        # Score by availability and performance
        scores = [
            self._score_model(model, profile)
            for model in eligible
        ]
        
        # Return best model
        best_model = max(zip(eligible, scores), key=lambda x: x[1])[0]
        self.model_queues[best_model].append(task)
        return best_model
    
    def _score_model(self, model: str, profile: ComplexityProfile) -> float:
        """Score model based on current state and requirements"""
        stats = self.model_stats.get(model, {})
        
        score = 0.0
        
        # Availability (not overloaded)
        queue_len = len(self.model_queues.get(model, []))
        score += max(0, 1.0 - queue_len / 10)  # Penalty for long queues
        
        # Recent success rate
        score += stats.get('success_rate', 0.5)
        
        # Response time (prefer faster models)
        avg_time_ms = stats.get('avg_response_ms', 5000)
        score += max(0, 1.0 - avg_time_ms / 10000)
        
        # Cost efficiency (prefer local models)
        if model.startswith('local:'):
            score += 1.0  # Big bonus for local models
        
        return score
```

---

### Phase 4: Consensus Validation (Days 8-9)
**Goal:** Add multi-model validation for quality assurance

#### 4.1 Consensus System
```python
# consensus.py (adapted from zen_mcp_bridge.py consensus patterns)
class ConsensusValidator:
    """Multi-model consensus for critical transformations"""
    
    def __init__(self, orchestrator: ModelOrchestrator):
        self.orchestrator = orchestrator
        
    async def validate_transformation(self,
                                      agent_name: str,
                                      v1_content: str,
                                      num_models: int = 3) -> ConsensusResult:
        """Transform agent with multiple models and validate consensus"""
        
        # Select diverse models
        models = self.orchestrator.create_consensus_group(
            prompt=v1_content,
            num_models=num_models,
            diverse=True  # Ensure provider diversity
        )
        
        # Transform with each model
        results = await asyncio.gather(*[
            self._transform_with_model(agent_name, v1_content, model)
            for model in models
        ])
        
        # Analyze consensus
        consensus = self._analyze_consensus(results)
        
        if consensus.agreement_score > 0.8:
            # High agreement - use best result
            return ConsensusResult(
                success=True,
                output=consensus.best_output,
                confidence=consensus.agreement_score,
                models_used=[m for m, _ in models]
            )
        else:
            # Low agreement - flag for manual review
            return ConsensusResult(
                success=False,
                output=None,
                confidence=consensus.agreement_score,
                models_used=[m for m, _ in models],
                conflict_details=consensus.differences
            )
```

#### 4.2 Quality Scoring
```python
# quality.py (new)
class QualityScorer:
    """Score transformation quality across multiple dimensions"""
    
    def score_transformation(self, 
                            v1_content: str,
                            v2_content: str) -> QualityScore:
        """Score transformation quality"""
        return QualityScore(
            yaml_validity=self._check_yaml_syntax(v2_content),
            completeness=self._check_all_sections_present(v2_content),
            specificity=self._check_no_placeholders(v2_content),
            consistency=self._check_v1_v2_alignment(v1_content, v2_content),
            examples_quality=self._check_examples_realistic(v2_content),
            overall=self._calculate_overall_score()
        )
```

---

### Phase 5: Monitoring & Optimization (Days 10-12)
**Goal:** Real-time monitoring and cost optimization

#### 5.1 Progress Dashboard
```python
# dashboard.py (new)
class TransformationDashboard:
    """Real-time dashboard for transformation progress"""
    
    def __init__(self):
        self.metrics = {
            'total_agents': 0,
            'completed': 0,
            'in_progress': 0,
            'failed': 0,
            'models_used': {},
            'total_cost': 0.0,
            'avg_time_per_agent': 0.0
        }
        
    def display(self):
        """Display live dashboard using rich library"""
        from rich.console import Console
        from rich.table import Table
        from rich.live import Live
        
        console = Console()
        
        while self.is_running():
            table = Table(title="Agent Transformation Progress")
            
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Completed", f"{self.metrics['completed']}/{self.metrics['total_agents']}")
            table.add_row("Success Rate", f"{self._success_rate():.1f}%")
            table.add_row("Avg Time", f"{self.metrics['avg_time_per_agent']:.2f}s")
            table.add_row("Total Cost", f"${self.metrics['total_cost']:.4f}")
            table.add_row("Cost Saved (Local)", f"${self._cost_saved():.4f}")
            
            console.clear()
            console.print(table)
            time.sleep(1)
```

#### 5.2 Cost Optimizer
```python
# cost_optimizer.py (new)
class CostOptimizer:
    """Optimize costs by preferring local models"""
    
    def __init__(self):
        self.budget = 10.0  # $10 budget
        self.spent = 0.0
        self.local_usage = 0
        self.cloud_usage = 0
        
    def should_use_cloud(self, complexity_score: float) -> bool:
        """Decide if cloud usage is justified"""
        if self.spent > self.budget * 0.9:
            # Near budget limit - use local only
            return False
        
        if complexity_score > 0.7:
            # Complex agent - justify cloud usage
            return True
        
        if self.local_usage / (self.cloud_usage + 1) < 3:
            # Not using enough local - force local
            return False
        
        return complexity_score > 0.5
```

---

## Implementation Phases

### Phase 1: Foundation (Days 1-2)
- [ ] Copy core orchestrator components
- [ ] Set up configuration system
- [ ] Integrate API clients
- [ ] Test basic multi-model setup

### Phase 2: Routing (Days 3-4)
- [ ] Implement agent analyzer
- [ ] Create routing logic
- [ ] Test model selection

### Phase 3: Parallelization (Days 5-7)
- [ ] Build parallel processor
- [ ] Implement load balancing
- [ ] Test concurrent processing

### Phase 4: Validation (Days 8-9)
- [ ] Add consensus system
- [ ] Implement quality scoring
- [ ] Test validation workflows

### Phase 5: Monitoring (Days 10-12)
- [ ] Build dashboard
- [ ] Add cost tracking
- [ ] Optimize performance

---

## Expected Improvements

### Performance
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Agents/minute | ~2 | 10-15 | **5-7x faster** |
| Concurrent workers | 3 | 12-15 | **4-5x more** |
| Model diversity | 1 | 5-8 | **Quality+Reliability** |

### Cost
| Scenario | Current | Target | Savings |
|----------|---------|--------|---------|
| Simple agents | $0.02 | $0.00 | **100% (local)** |
| Standard agents | $0.05 | $0.00 | **100% (local)** |
| Complex agents | $0.10 | $0.02 | **80% (hybrid)** |
| Critical agents | $0.15 | $0.05 | **67% (consensus)** |

### Quality
- **Validation**: 100% of critical agents validated by 3+ models
- **Consistency**: 95%+ agreement score for standard agents
- **Reliability**: 99.9% success rate with fallback chains

---

## File Structure After Refactoring

```
Agents-v2/
├── config/
│   ├── models.yaml
│   ├── providers.yaml
│   ├── routing_rules.yaml
│   └── cost_optimization.yaml
├── core/
│   ├── agent_transformation_orchestrator.py
│   ├── agent_analyzer.py
│   ├── router.py
│   └── parallel_processor.py
├── models/
│   ├── local_model_manager.py
│   ├── api_clients.py
│   └── model_pools.py
├── validation/
│   ├── consensus.py
│   ├── quality_scorer.py
│   └── validators.py
├── monitoring/
│   ├── dashboard.py
│   ├── cost_tracker.py
│   └── metrics.py
├── utils/
│   ├── token_counter.py
│   ├── rate_limiter.py
│   └── error_handler.py
└── orchestrate_v2.py (main entry point)
```

---

## Next Steps

1. **Review this plan** - Ensure alignment with project goals
2. **Prioritize phases** - Which improvements are most critical?
3. **Resource allocation** - API keys, compute resources needed
4. **Timeline adjustment** - Based on complexity and resources
5. **Begin Phase 1** - Start with foundation and configuration

---

**Questions for Review:**
1. Should we prioritize speed or quality improvements first?
2. What's the acceptable budget for cloud API usage?
3. Are there specific agent categories that need special handling?
4. Should we implement gradual rollout or all-at-once migration?
5. What monitoring/alerting requirements exist?

---

*This plan leverages battle-tested components from Model Orchestrator v1 to create a production-ready, high-performance agent transformation system.*
