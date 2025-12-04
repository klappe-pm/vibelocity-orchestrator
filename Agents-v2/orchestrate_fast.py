#!/usr/bin/env python3
"""
Fast Multi-Model Agent Transformation Orchestrator
Speed-optimized with local model fallback for cost efficiency
"""

import os
import sys
import json
import yaml
import time
import asyncio
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configuration
BASE_DIR = Path(__file__).parent.parent
V1_AGENTS_DIR = BASE_DIR / "Agents"
V2_AGENTS_DIR = BASE_DIR / "Agents-v2"
RESEARCH_DIR = V2_AGENTS_DIR / "research"
PROGRESS_FILE = RESEARCH_DIR / "transformation-progress.json"
LOG_FILE = V2_AGENTS_DIR / "orchestration.log"

# Model pool configuration - Speed optimized
MODEL_POOL = [
    {"name": "gpt-4o-mini", "type": "openai", "priority": 1, "speed": 0.9, "cost": 0.15},
    {"name": "qwen2.5:32b-instruct", "type": "ollama", "priority": 2, "speed": 0.7, "cost": 0.0},
    {"name": "deepseek-r1:70b", "type": "ollama", "priority": 3, "speed": 0.6, "cost": 0.0},
]

TEMPLATE_FILE = RESEARCH_DIR / "aws-agent-transformation-template.yaml"

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FastOrchestrator:
    """Speed-optimized orchestrator with local/cloud hybrid"""
    
    def __init__(self):
        self.logger = logger
        self.progress = self.load_progress()
        self.stats = {
            'local_used': 0,
            'cloud_used': 0,
            'total_cost': 0.0,
            'start_time': time.time()
        }
        
        # Initialize OpenAI
        self.openai_client = None
        if os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.logger.info("✓ OpenAI initialized")
        
        # Check Ollama availability
        self.ollama_available = self.check_ollama()
        self.ollama_models = self.get_available_ollama_models() if self.ollama_available else []
        
        self.logger.info(f"✓ Initialized: OpenAI={self.openai_client is not None}, Ollama={self.ollama_available}")
        if self.ollama_models:
            self.logger.info(f"  Available local models: {', '.join(self.ollama_models)}")
    
    def check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_available_ollama_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return [m['name'] for m in data.get('models', [])]
        except:
            pass
        return []
    
    def load_progress(self) -> Dict:
        """Load transformation progress"""
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {"completed": [], "failed": [], "skipped": []}
    
    def save_progress(self):
        """Save transformation progress"""
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def analyze_complexity(self, v1_content: str) -> float:
        """Quick complexity analysis (0-1 scale)"""
        size = len(v1_content)
        
        # Simple heuristics for speed
        if size < 2000:
            return 0.2  # Simple - prefer local
        elif size < 5000:
            return 0.5  # Medium - local if available
        else:
            return 0.8  # Complex - cloud preferred
    
    def select_model(self, complexity: float) -> Tuple[str, str]:
        """Select best model based on complexity and availability
        Returns: (model_name, model_type)
        """
        # Strategy: Use local for simple/medium, cloud for complex or if local unavailable
        
        if complexity < 0.7 and self.ollama_available and self.ollama_models:
            # Try local models
            for model_name in ["qwen2.5:32b-instruct", "deepseek-r1:70b", "mistral:latest"]:
                if model_name in self.ollama_models:
                    return model_name, "ollama"
        
        # Fallback to cloud
        return "gpt-4o-mini", "openai"
    
    def call_openai(self, model: str, prompt: str, max_retries: int = 2) -> Optional[str]:
        """Call OpenAI API"""
        if not self.openai_client:
            return None
        
        for attempt in range(max_retries):
            try:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert assistant that generates valid YAML configurations. Always output pure YAML without markdown code blocks."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=16000
                )
                self.stats['cloud_used'] += 1
                self.stats['total_cost'] += 0.02  # Rough estimate
                return response.choices[0].message.content
            except Exception as e:
                self.logger.error(f"OpenAI attempt {attempt + 1} failed: {str(e)[:100]}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        return None
    
    def call_ollama(self, model: str, prompt: str, max_retries: int = 2) -> Optional[str]:
        """Call Ollama local model"""
        url = "http://localhost:11434/api/generate"
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 16000
                        }
                    },
                    timeout=120  # 2 minute timeout for speed
                )
                
                if response.status_code == 200:
                    self.stats['local_used'] += 1
                    return response.json().get("response")
            except Exception as e:
                self.logger.error(f"Ollama attempt {attempt + 1} failed: {str(e)[:100]}")
                if attempt < max_retries - 1:
                    time.sleep(1)
        return None
    
    def generate_prompt(self, agent_name: str, category: str, 
                       v1_content: str, template_content: str, research_content: str) -> str:
        """Generate transformation prompt"""
        research_excerpt = '\n'.join(research_content.split('\n')[:80])  # Reduced for speed
        
        return f"""Transform this agent from v1 to v2 format.

CRITICAL: Output ONLY valid YAML. No markdown, no explanations, no code blocks.

V1 AGENT ({agent_name}):
---
{v1_content}
---

V2 TEMPLATE:
---
{template_content}
---

RESEARCH (excerpt):
---
{research_excerpt}
---

REQUIREMENTS:
- Extract responsibilities from v1
- Include ALL 15 v2 sections
- Replace ALL placeholders
- Generate 2 realistic examples
- Category: {category}

OUTPUT COMPLETE V2 YAML NOW:"""
    
    def validate_yaml(self, content: str) -> Tuple[bool, str]:
        """Validate YAML syntax"""
        try:
            yaml.safe_load(content)
            return True, "Valid"
        except yaml.YAMLError as e:
            return False, f"Invalid: {str(e)[:200]}"
    
    def transform_agent(self, agent_name: str, category: str) -> bool:
        """Transform a single agent"""
        
        agent_id = f"{category}/{agent_name}"
        
        # Skip if already completed
        if agent_id in self.progress['completed']:
            self.logger.info(f"⊘ Skipping {agent_name} (already done)")
            return True
        
        # File paths
        v1_file = V1_AGENTS_DIR / category / "yaml" / f"{agent_name}-definition.yaml"
        v2_file = V2_AGENTS_DIR / category / "yaml" / f"{agent_name}.yaml"
        research_file = RESEARCH_DIR / f"{category}-research.md"
        
        if category == "cloud-agent":
            research_file = RESEARCH_DIR / "cloud-platform-research.md"
        
        # Read files
        try:
            with open(v1_file, 'r') as f:
                v1_content = f.read()
        except Exception as e:
            self.logger.error(f"✗ {agent_name}: Failed to read v1 file: {e}")
            self.progress['failed'].append({"agent": agent_id, "reason": "read error"})
            return False
        
        try:
            with open(TEMPLATE_FILE, 'r') as f:
                template_content = f.read()
        except Exception as e:
            self.logger.error(f"✗ Failed to read template: {e}")
            return False
        
        try:
            with open(research_file, 'r') as f:
                research_content = f.read()
        except:
            research_content = "No research available."
        
        # Analyze and select model
        complexity = self.analyze_complexity(v1_content)
        model_name, model_type = self.select_model(complexity)
        
        self.logger.info(f"🤖 {agent_name}: Using {model_type}:{model_name} (complexity={complexity:.2f})")
        
        # Generate prompt
        prompt = self.generate_prompt(agent_name, category, v1_content, template_content, research_content)
        
        # Call model with fallback
        transformed_content = None
        
        if model_type == "ollama":
            transformed_content = self.call_ollama(model_name, prompt)
            if not transformed_content and self.openai_client:
                self.logger.warning(f"⚠ {agent_name}: Local failed, falling back to cloud")
                transformed_content = self.call_openai("gpt-4o-mini", prompt)
        else:
            transformed_content = self.call_openai(model_name, prompt)
        
        if not transformed_content:
            self.logger.error(f"✗ {agent_name}: All models failed")
            self.progress['failed'].append({"agent": agent_id, "reason": "all models failed"})
            return False
        
        # Clean output
        if transformed_content.startswith("```"):
            lines = transformed_content.split('\n')
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            transformed_content = '\n'.join(lines)
        
        # Validate
        is_valid, msg = self.validate_yaml(transformed_content)
        if not is_valid:
            self.logger.error(f"✗ {agent_name}: {msg}")
            self.progress['failed'].append({"agent": agent_id, "reason": msg})
            # Save anyway for manual review
            try:
                v2_file.parent.mkdir(parents=True, exist_ok=True)
                with open(str(v2_file) + ".invalid", 'w') as f:
                    f.write(transformed_content)
            except:
                pass
            return False
        
        # Save
        try:
            v2_file.parent.mkdir(parents=True, exist_ok=True)
            with open(v2_file, 'w') as f:
                f.write(transformed_content)
            
            self.progress['completed'].append(agent_id)
            self.save_progress()
            
            self.logger.info(f"✅ {agent_name} ({model_type})")
            return True
        except Exception as e:
            self.logger.error(f"✗ {agent_name}: Write failed: {e}")
            self.progress['failed'].append({"agent": agent_id, "reason": str(e)})
            return False
    
    def transform_category(self, category: str, max_workers: int = 8) -> Dict:
        """Transform all agents in category with parallel processing"""
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"🚀 CATEGORY: {category}")
        self.logger.info(f"⚡ Workers: {max_workers}")
        self.logger.info(f"{'='*60}")
        
        # Get agent list
        v1_category_dir = V1_AGENTS_DIR / category / "yaml"
        if not v1_category_dir.exists():
            self.logger.error(f"✗ Category not found: {v1_category_dir}")
            return {"success": 0, "failed": 0, "skipped": 0}
        
        agent_files = list(v1_category_dir.glob("*-definition.yaml"))
        agent_names = [f.stem.replace('-definition', '') for f in agent_files]
        
        self.logger.info(f"📋 Found {len(agent_names)} agents")
        
        results = {"success": 0, "failed": 0, "skipped": 0}
        
        # Process with thread pool
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_agent = {
                executor.submit(self.transform_agent, agent_name, category): agent_name
                for agent_name in agent_names
            }
            
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    success = future.result()
                    agent_id = f"{category}/{agent_name}"
                    if success:
                        if agent_id in [item['agent'] if isinstance(item, dict) else item 
                                       for item in self.progress.get('skipped', [])]:
                            results['skipped'] += 1
                        else:
                            results['success'] += 1
                    else:
                        results['failed'] += 1
                except Exception as e:
                    results['failed'] += 1
                    self.logger.error(f"✗ Exception: {agent_name}: {e}")
        
        # Print summary
        elapsed = time.time() - self.stats['start_time']
        rate = results['success'] / (elapsed / 60) if elapsed > 0 else 0
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"✓ Success: {results['success']} | ✗ Failed: {results['failed']} | ⊘ Skipped: {results['skipped']}")
        self.logger.info(f"📊 Local: {self.stats['local_used']} | Cloud: {self.stats['cloud_used']}")
        self.logger.info(f"💰 Est. Cost: ${self.stats['total_cost']:.2f}")
        self.logger.info(f"⚡ Rate: {rate:.1f} agents/min")
        self.logger.info(f"{'='*60}\n")
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Fast multi-model agent transformation")
    parser.add_argument("--category", help="Category to transform")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent workers (default: 8)")
    parser.add_argument("--all", action="store_true", help="Transform all categories")
    
    args = parser.parse_args()
    
    orchestrator = FastOrchestrator()
    
    if args.all:
        categories = [
            "cloud-agent", "business-review-agent", "content-agent",
            "context-agent", "engineering-agent", "google-apps-script-agent",
            "product-agents", "project-agent", "public-relations-agent", "ux-agent"
        ]
        
        total_results = {"success": 0, "failed": 0, "skipped": 0}
        
        for category in categories:
            results = orchestrator.transform_category(category, max_workers=args.workers)
            for key in total_results:
                total_results[key] += results[key]
        
        logger.info("\n" + "="*60)
        logger.info("🎉 ALL CATEGORIES COMPLETE")
        logger.info(f"Total: ✓ {total_results['success']} | ✗ {total_results['failed']} | ⊘ {total_results['skipped']}")
        logger.info(f"Local: {orchestrator.stats['local_used']} | Cloud: {orchestrator.stats['cloud_used']}")
        logger.info(f"Cost: ${orchestrator.stats['total_cost']:.2f}")
        logger.info("="*60)
        
        sys.exit(0 if total_results['failed'] == 0 else 1)
    
    elif args.category:
        results = orchestrator.transform_category(args.category, max_workers=args.workers)
        sys.exit(0 if results['failed'] == 0 else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
