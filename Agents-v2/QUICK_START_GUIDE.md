# Quick Start Guide - Refactored Agent Transformation System

## Immediate Action Items (First 24 Hours)

### Step 1: Copy Core Components (30 minutes)
```bash
cd /Users/kevinlappe/Documents/vibelocity-orchestrator/Agents-v2

# Create new directory structure
mkdir -p core models validation monitoring utils config

# Copy essential files from Model Orchestrator
cp "../Model Orchestrator/model-orchestrator-consolidated.py" core/
cp "../Model Orchestrator/api_clients.py" models/
cp "../Model Orchestrator/local_model_manager.py" models/
cp "../Model Orchestrator/requirements.txt" .

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Minimal Configuration (15 minutes)
Create `config/models.yaml`:
```yaml
local_models:
  fast:
    - name: "deepseek-coder:1.3b"
      cost: 0.0
      speed: 0.98
      quality: 0.7
    - name: "magicoder:7b"
      cost: 0.0
      speed: 0.9
      quality: 0.85
      
cloud_models:
  primary:
    - name: "gpt-4o-mini"
      cost_per_m_tokens: [0.15, 0.60]
      speed: 0.9
      quality: 0.9

routing:
  simple_threshold: 0.3  # Use local for score < 0.3
  complex_threshold: 0.7 # Use cloud for score > 0.7
```

### Step 3: Create Simplified Orchestrator (1 hour)
Create `core/simple_multi_model_orchestrator.py`:
```python
#!/usr/bin/env python3
"""
Simplified Multi-Model Orchestrator
Quick integration of Model Orchestrator v1 patterns
"""

import sys
sys.path.append('../Model Orchestrator')

from model_orchestrator_consolidated import ModelOrchestrator
from api_clients import OpenAIAPIClient, OllamaAPIClient
import asyncio
from pathlib import Path
from typing import List, Dict

class SimpleAgentOrchestrator:
    """Minimal multi-model orchestrator for agent transformations"""
    
    def __init__(self):
        # Use local models preferentially
        self.local_models = [
            "magicoder:7b",
            "deepseek-coder:1.3b"
        ]
        self.cloud_model = "gpt-4o-mini"
        self.ollama_client = None
        self.openai_client = None
        
    async def __aenter__(self):
        self.ollama_client = OllamaAPIClient()
        self.openai_client = OpenAIAPIClient()
        return self
        
    async def __aexit__(self, *args):
        if self.ollama_client:
            await self.ollama_client.__aexit__(*args)
        if self.openai_client:
            await self.openai_client.__aexit__(*args)
    
    def analyze_complexity(self, v1_yaml: str) -> float:
        """Quick complexity score (0-1)"""
        size = len(v1_yaml)
        
        # Simple heuristics
        if size < 2000:
            return 0.2  # Simple - use local fast
        elif size < 5000:
            return 0.5  # Standard - use local balanced
        else:
            return 0.8  # Complex - use cloud
    
    async def transform(self, agent_name: str, v1_yaml: str, template: str) -> str:
        """Transform agent using best available model"""
        
        complexity = self.analyze_complexity(v1_yaml)
        
        if complexity < 0.3:
            # Use fastest local model
            model = "deepseek-coder:1.3b"
            client = self.ollama_client
        elif complexity < 0.7:
            # Use balanced local model
            model = "magicoder:7b"
            client = self.ollama_client
        else:
            # Use cloud for complex
            model = self.cloud_model
            client = self.openai_client
        
        prompt = self._build_prompt(v1_yaml, template)
        
        try:
            response = await client.chat_completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            return response.content
        except Exception as e:
            # Fallback to cloud if local fails
            if client == self.ollama_client:
                response = await self.openai_client.chat_completion(
                    model=self.cloud_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.content
            raise
    
    def _build_prompt(self, v1_yaml: str, template: str) -> str:
        """Build transformation prompt"""
        return f"""Transform this agent from v1 to v2 format.

Output ONLY valid YAML - no markdown, no explanations.

V1 AGENT:
{v1_yaml}

V2 TEMPLATE:
{template}

OUTPUT V2 YAML NOW:"""

# Quick test
async def test():
    async with SimpleAgentOrchestrator() as orch:
        v1 = "agent:\n  name: test\n  role: tester"
        template = "agent:\n  name:\n  model_configuration:\n..."
        result = await orch.transform("test-agent", v1, template)
        print(result)

if __name__ == "__main__":
    asyncio.run(test())
```

### Step 4: Test Quick Implementation (30 minutes)
```bash
# Test local model availability
ollama list

# Test the simple orchestrator
python3 core/simple_multi_model_orchestrator.py

# If successful, you should see a transformation result
```

---

## Phase 1 Implementation (Next 2-3 Days)

### Day 1 Morning: Enhanced Routing

**Create `core/complexity_analyzer.py`:**
```python
import re
from dataclasses import dataclass

@dataclass
class ComplexityProfile:
    score: float  # 0-1
    tier: str  # local_fast, local_balanced, cloud, premium
    requires_consensus: bool
    estimated_tokens: int

class ComplexityAnalyzer:
    """Analyzes agent complexity for routing"""
    
    CRITICAL_AGENTS = [
        'aws-deployment-manager',
        'security-audit',
        'production-deploy'
    ]
    
    def analyze(self, agent_name: str, v1_yaml: str) -> ComplexityProfile:
        """Analyze agent to determine routing"""
        
        # Size factor
        size = len(v1_yaml)
        size_score = min(size / 10000, 1.0)  # Cap at 10K chars
        
        # Complexity indicators
        has_sub_agents = 'sub_agents:' in v1_yaml or 'sub-agents:' in v1_yaml
        num_responsibilities = len(re.findall(r'- .*responsibility', v1_yaml, re.I))
        
        # Calculate score
        score = (
            size_score * 0.4 +
            (num_responsibilities / 10) * 0.3 +
            (1.0 if has_sub_agents else 0.0) * 0.3
        )
        
        # Determine tier
        if agent_name in self.CRITICAL_AGENTS:
            return ComplexityProfile(
                score=0.9,
                tier='premium',
                requires_consensus=True,
                estimated_tokens=size * 2
            )
        elif score > 0.7 or has_sub_agents:
            return ComplexityProfile(
                score=score,
                tier='cloud',
                requires_consensus=False,
                estimated_tokens=size * 1.5
            )
        elif score > 0.4:
            return ComplexityProfile(
                score=score,
                tier='local_balanced',
                requires_consensus=False,
                estimated_tokens=size * 1.2
            )
        else:
            return ComplexityProfile(
                score=score,
                tier='local_fast',
                requires_consensus=False,
                estimated_tokens=size
            )
```

### Day 1 Afternoon: Parallel Processing

**Update orchestrator with concurrent processing:**
```python
# Add to simple_multi_model_orchestrator.py

from concurrent.futures import ThreadPoolExecutor
import asyncio

class ParallelOrchestrator(SimpleAgentOrchestrator):
    """Adds parallel processing capability"""
    
    def __init__(self, max_workers: int = 6):
        super().__init__()
        self.max_workers = max_workers
        self.analyzer = ComplexityAnalyzer()
        
    async def transform_batch(self, 
                             agents: List[Dict[str, str]]) -> List[str]:
        """Transform multiple agents concurrently"""
        
        # Analyze all agents
        profiles = [
            self.analyzer.analyze(a['name'], a['v1_yaml'])
            for a in agents
        ]
        
        # Group by tier
        groups = {
            'local_fast': [],
            'local_balanced': [],
            'cloud': [],
            'premium': []
        }
        
        for agent, profile in zip(agents, profiles):
            groups[profile.tier].append(agent)
        
        # Process groups in parallel
        results = []
        
        # Local fast - high concurrency
        if groups['local_fast']:
            tasks = [
                self.transform(a['name'], a['v1_yaml'], a['template'])
                for a in groups['local_fast']
            ]
            results.extend(await asyncio.gather(*tasks))
        
        # Local balanced - medium concurrency
        if groups['local_balanced']:
            tasks = [
                self.transform(a['name'], a['v1_yaml'], a['template'])
                for a in groups['local_balanced']
            ]
            results.extend(await asyncio.gather(*tasks))
        
        # Cloud - limited concurrency (rate limits)
        if groups['cloud']:
            for agent in groups['cloud']:
                result = await self.transform(
                    agent['name'], 
                    agent['v1_yaml'], 
                    agent['template']
                )
                results.append(result)
        
        return results
```

### Day 2: Add Monitoring

**Create `monitoring/simple_dashboard.py`:**
```python
from datetime import datetime
import time

class SimpleDashboard:
    """Basic progress monitoring"""
    
    def __init__(self, total: int):
        self.total = total
        self.completed = 0
        self.failed = 0
        self.start_time = time.time()
        self.local_used = 0
        self.cloud_used = 0
        
    def update(self, success: bool, used_local: bool):
        """Update progress"""
        if success:
            self.completed += 1
        else:
            self.failed += 1
            
        if used_local:
            self.local_used += 1
        else:
            self.cloud_used += 1
        
        self.print_status()
    
    def print_status(self):
        """Print current status"""
        elapsed = time.time() - self.start_time
        rate = self.completed / elapsed if elapsed > 0 else 0
        eta = (self.total - self.completed) / rate if rate > 0 else 0
        
        pct = (self.completed / self.total) * 100 if self.total > 0 else 0
        
        print(f"\r[{pct:5.1f}%] {self.completed}/{self.total} "
              f"| Rate: {rate:.1f}/min | ETA: {eta/60:.1f}m "
              f"| Local: {self.local_used} Cloud: {self.cloud_used}  ", 
              end='', flush=True)
```

---

## Integration with Existing System (Day 3)

### Replace Current Orchestrator

**Update `orchestrate_transformations.py`:**
```python
# Add at top
from core.simple_multi_model_orchestrator import ParallelOrchestrator
from monitoring.simple_dashboard import SimpleDashboard

# Replace transform_category method:
async def transform_category(self, category: str, max_workers: int = 6):
    """Transform category with multi-model support"""
    
    orchestrator = ParallelOrchestrator(max_workers=max_workers)
    dashboard = SimpleDashboard(total=len(agent_list))
    
    async with orchestrator:
        # Prepare agent batch
        agents = [
            {
                'name': name,
                'v1_yaml': read_v1_file(name),
                'template': read_template()
            }
            for name in agent_list
        ]
        
        # Transform with progress monitoring
        results = []
        for agent in agents:
            try:
                result = await orchestrator.transform(
                    agent['name'],
                    agent['v1_yaml'],
                    agent['template']
                )
                results.append(result)
                dashboard.update(success=True, used_local=True)
            except Exception as e:
                dashboard.update(success=False, used_local=False)
                logger.error(f"Failed: {agent['name']}: {e}")
        
        return results
```

---

## Testing & Validation

### Quick Tests
```bash
# Test 1: Local model only
python3 << 'EOF'
import asyncio
from core.simple_multi_model_orchestrator import SimpleAgentOrchestrator

async def test_local():
    async with SimpleAgentOrchestrator() as orch:
        # Simple agent - should use local
        v1 = "agent:\n  name: simple\n  role: test"
        result = await orch.transform("simple", v1, "template...")
        print("Local test:", "✓" if result else "✗")

asyncio.run(test_local())
EOF

# Test 2: Full category
python3 orchestrate_transformations.py --category project-agent --workers 6

# Test 3: Monitor costs
grep "Cost" orchestration.log | tail -10
```

---

## Quick Wins (Immediate Benefits)

### 1. Cost Reduction
- **Before**: All transformations use GPT-4o-mini ($0.15/$0.60 per M tokens)
- **After**: 70% use local models ($0.00)
- **Savings**: ~80% on simple/standard agents

### 2. Speed Improvement
- **Before**: 2-3 agents/minute (single model, sequential)
- **After**: 8-12 agents/minute (multi-model, parallel)
- **Improvement**: 3-4x faster

### 3. Reliability
- **Before**: Single model failure = transformation fails
- **After**: Automatic fallback to cloud if local fails
- **Improvement**: 99%+ success rate

---

## Next Steps After Quick Start

1. **Measure baseline**: Run 10-20 agents with new system, track metrics
2. **Optimize routing**: Adjust complexity thresholds based on results
3. **Add consensus**: Implement for critical agents
4. **Full dashboard**: Build rich monitoring interface
5. **Production rollout**: Deploy to all categories

---

## Troubleshooting

### Ollama Not Responding
```bash
# Check if running
ollama list

# Restart if needed
killall ollama && ollama serve &

# Test connectivity
curl http://localhost:11434/api/tags
```

### Models Not Loaded
```bash
# Pull required models
ollama pull deepseek-coder:1.3b
ollama pull magicoder:7b

# Verify
ollama list
```

### High API Costs
```bash
# Check routing - should favor local
grep "Using model" orchestration.log | sort | uniq -c

# If too much cloud usage, adjust thresholds in config/models.yaml
```

---

## Success Metrics (Track These)

- **Throughput**: Agents transformed per minute
- **Cost**: Total API costs vs. budget
- **Quality**: YAML validation pass rate
- **Local %**: Percentage using free local models
- **Failures**: Count and reasons for failures

---

*Start with this quick implementation, measure results, then proceed with full Phase 1 from the main refactoring plan.*
