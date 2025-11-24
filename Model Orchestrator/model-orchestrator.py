#!/usr/bin/env python3
"""
Model Orchestration Agent
Intelligent multi-model routing system with cost optimization and capability matching
"""

import os
import json
import yaml
import asyncio
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import numpy as np

# API integration
from api_clients import get_api_client, APIResponse, BaseAPIClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskType(Enum):
    """Task categorization for model selection"""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    REASONING = "reasoning"
    CREATIVE_WRITING = "creative_writing"
    ANALYSIS = "analysis"
    VISION = "vision"
    IMAGE_GENERATION = "image_generation"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    QA = "question_answering"
    CONVERSATION = "conversation"
    RESEARCH = "research"
    DEBUGGING = "debugging"
    SYSTEM_DESIGN = "system_design"
    DATA_ANALYSIS = "data_analysis"

class ModelProvider(Enum):
    """Available model providers"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    XAI = "xai"
    LOCAL = "local"
    DIAL = "dial"
    ZEN_MCP = "zen_mcp"
    AZURE = "azure"
    BEDROCK = "bedrock"
    META = "meta"

@dataclass
class ModelCapabilities:
    """Model capability profile"""
    provider: ModelProvider
    model_id: str
    context_window: int
    supports_vision: bool = False
    supports_function_calling: bool = False
    supports_streaming: bool = True
    supports_reasoning: bool = False
    code_specialized: bool = False
    
    # Performance metrics (0-1 scale)
    speed: float = 0.5
    accuracy: float = 0.5
    creativity: float = 0.5
    reasoning_depth: float = 0.5
    
    # Cost per million tokens
    input_cost: float = 0.0
    output_cost: float = 0.0
    
    # Task affinity scores (0-1 scale)
    task_scores: Dict[TaskType, float] = field(default_factory=dict)
    
    # Availability
    rate_limit: Optional[str] = None
    available: bool = True
    
@dataclass
class TaskRequirements:
    """Requirements for a specific task"""
    task_type: TaskType
    min_context_window: int = 4096
    requires_vision: bool = False
    requires_function_calling: bool = False
    requires_reasoning: bool = False
    max_latency_ms: Optional[int] = None
    max_cost: Optional[float] = None
    preferred_providers: List[ModelProvider] = field(default_factory=list)
    quality_threshold: float = 0.7
    
class ModelGuideParser:
    """Parse MODELS.md for model selection guidance"""

    def __init__(self, guide_path: str = None):
        self.guide_path = guide_path or str(Path.home() / "Obsidian/Power Prompts/gitignore/Claude Context/MODELS.md")
        self.rules = self._parse_guide()

    def _parse_guide(self) -> Dict[str, Any]:
        """Parse the MODELS.md file for rules"""
        if not os.path.exists(self.guide_path):
            return {}

        with open(self.guide_path, 'r') as f:
            content = f.read()

        rules = {
            "task_mappings": {},
            "fallback_chains": {},
            "cost_tiers": {},
            "blocked_models": [],
            "consensus_rules": {},
            "quality_gates": {}
        }

        # Parse task-to-model mappings
        task_section = re.search(r'### Code Tasks(.*?)###', content, re.DOTALL)
        if task_section:
            lines = task_section.group(1).strip().split('\n')
            for line in lines:
                if '**' in line and ':' in line:
                    match = re.match(r'- \*\*(.+?)\*\*: (.+)', line)
                    if match:
                        task = match.group(1).lower().replace(' ', '_')
                        models = [m.strip() for m in match.group(2).split('>')]
                        rules["task_mappings"][task] = models

        # Parse blocked models
        blocked_section = re.search(r'### Blocked Models(.*?)##', content, re.DOTALL)
        if blocked_section:
            lines = blocked_section.group(1).strip().split('\n')
            for line in lines:
                if line.startswith('- '):
                    model = line.split(':')[0].replace('- ', '').strip()
                    rules["blocked_models"].append(model)

        # Parse fallback chains
        fallback_section = re.search(r'### Fallback Chains(.*?)###', content, re.DOTALL)
        if fallback_section:
            lines = fallback_section.group(1).strip().split('\n')
            for line in lines:
                if '→' in line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        task = parts[0].replace('- ', '').strip().lower()
                        chain = [m.strip() for m in parts[1].split('→')]
                        rules["fallback_chains"][task] = chain

        return rules

    def get_recommended_models(self, task_type: str) -> List[str]:
        """Get recommended models for a task type"""
        task_key = task_type.lower().replace(' ', '_')
        return self.rules.get("task_mappings", {}).get(task_key, [])

    def get_fallback_chain(self, task_type: str) -> List[str]:
        """Get fallback chain for a task"""
        return self.rules.get("fallback_chains", {}).get(task_type.lower(), [])

    def is_model_blocked(self, model_id: str, task_type: str = None) -> bool:
        """Check if model is blocked for sensitive tasks"""
        return model_id in self.rules.get("blocked_models", [])


class ModelOrchestrator:
    """Intelligent model orchestration system with MODELS.md guidance and API integration"""

    def __init__(self, config_path: Optional[str] = None, guide_path: Optional[str] = None):
        self.config_path = config_path or Path(".") / "orchestrator_config.yaml"
        self.guide_path = guide_path
        self.models: Dict[str, ModelCapabilities] = {}
        self.api_clients: Dict[str, BaseAPIClient] = {}
        self.cost_tracker: Dict[str, float] = {}
        self.performance_history: List[Dict] = []
        self.guide: Optional[ModelGuideParser] = None

        # Load models and configuration
        self._load_models()

        # Load MODELS.md guidance if path provided
        if self.guide_path:
            try:
                self.guide = ModelGuideParser(self.guide_path)
                logger.info("✓ MODELS.md guidance loaded")
            except Exception as e:
                logger.warning(f"Failed to load MODELS.md guidance: {e}")

        # Initialize API clients
        self._initialize_clients()
        
    def _load_models(self):
        """Load all available models with capabilities"""
        
        # Grok models
        self.models.update({
            "grok-4-fast-reasoning": ModelCapabilities(
                provider=ModelProvider.XAI,
                model_id="grok-4-fast-reasoning",
                context_window=2000000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.7,
                accuracy=0.9,
                reasoning_depth=0.95,
                input_cost=2.0,
                output_cost=6.0,
                task_scores={
                    TaskType.REASONING: 0.95,
                    TaskType.ANALYSIS: 0.9,
                    TaskType.SYSTEM_DESIGN: 0.9,
                    TaskType.CODE_REVIEW: 0.85,
                }
            ),
            "grok-4-fast-non-reasoning": ModelCapabilities(
                provider=ModelProvider.XAI,
                model_id="grok-4-fast-non-reasoning",
                context_window=2000000,
                speed=0.9,
                accuracy=0.8,
                input_cost=1.0,
                output_cost=3.0,
                task_scores={
                    TaskType.SUMMARIZATION: 0.8,
                    TaskType.TRANSLATION: 0.8,
                    TaskType.QA: 0.7,
                }
            ),
            "grok-code-fast-1": ModelCapabilities(
                provider=ModelProvider.XAI,
                model_id="grok-code-fast-1",
                context_window=256000,
                code_specialized=True,
                speed=0.8,
                accuracy=0.85,
                input_cost=1.5,
                output_cost=4.5,
                task_scores={
                    TaskType.CODE_GENERATION: 0.9,
                    TaskType.CODE_REVIEW: 0.85,
                    TaskType.DEBUGGING: 0.9,
                }
            ),
            "grok-3": ModelCapabilities(
                provider=ModelProvider.XAI,
                model_id="grok-3",
                context_window=131072,
                speed=0.6,
                accuracy=0.85,
                input_cost=1.0,
                output_cost=3.0,
                task_scores={
                    TaskType.ANALYSIS: 0.8,
                    TaskType.CODE_GENERATION: 0.75,
                    TaskType.CONVERSATION: 0.8,
                }
            ),
            "grok-2-vision-1212": ModelCapabilities(
                provider=ModelProvider.XAI,
                model_id="grok-2-vision-1212",
                context_window=32768,
                supports_vision=True,
                speed=0.5,
                accuracy=0.8,
                input_cost=2.0,
                output_cost=6.0,
                task_scores={
                    TaskType.VISION: 0.9,
                    TaskType.ANALYSIS: 0.7,
                }
            ),
        })
        
        # OpenAI models - Complete family coverage
        self.models.update({
            # GPT-4 Family
            "gpt-4": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4",
                context_window=8192,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.5,
                accuracy=0.92,
                reasoning_depth=0.88,
                creativity=0.85,
                input_cost=30.0,
                output_cost=60.0,
                task_scores={
                    TaskType.REASONING: 0.92,
                    TaskType.CREATIVE_WRITING: 0.88,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.9,
                }
            ),
            "gpt-4-turbo": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4-turbo",
                context_window=128000,
                supports_function_calling=True,
                supports_reasoning=True,
                supports_vision=True,
                speed=0.7,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.85,
                input_cost=10.0,
                output_cost=30.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.88,
                    TaskType.CODE_GENERATION: 0.88,
                    TaskType.VISION: 0.85,
                }
            ),
            "gpt-4o": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4o",
                context_window=128000,
                supports_function_calling=True,
                supports_reasoning=True,
                supports_vision=True,
                speed=0.8,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.85,
                input_cost=5.0,
                output_cost=15.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.9,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.VISION: 0.88,
                    TaskType.ANALYSIS: 0.85,
                }
            ),
            "gpt-4o-mini": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4o-mini",
                context_window=128000,
                supports_function_calling=True,
                supports_vision=True,
                speed=0.9,
                accuracy=0.82,
                reasoning_depth=0.75,
                creativity=0.8,
                input_cost=0.15,
                output_cost=0.6,
                task_scores={
                    TaskType.CONVERSATION: 0.8,
                    TaskType.QA: 0.82,
                    TaskType.SUMMARIZATION: 0.8,
                    TaskType.VISION: 0.78,
                }
            ),
            
            # GPT-3.5 Family
            "gpt-3.5-turbo": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="gpt-3.5-turbo",
                context_window=16385,
                supports_function_calling=True,
                speed=0.95,
                accuracy=0.8,
                reasoning_depth=0.7,
                creativity=0.75,
                input_cost=0.5,
                output_cost=1.5,
                task_scores={
                    TaskType.CONVERSATION: 0.8,
                    TaskType.QA: 0.78,
                    TaskType.SUMMARIZATION: 0.8,
                    TaskType.CODE_GENERATION: 0.75,
                }
            ),
            
            # O1 Family - Extended reasoning models
            "o1": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="o1",
                context_window=200000,
                supports_reasoning=True,
                speed=0.4,
                accuracy=0.95,
                reasoning_depth=0.95,
                input_cost=15.0,
                output_cost=60.0,
                task_scores={
                    TaskType.REASONING: 0.98,
                    TaskType.DEBUGGING: 0.95,
                    TaskType.SYSTEM_DESIGN: 0.92,
                    TaskType.ANALYSIS: 0.95,
                }
            ),
            "o1-mini": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="o1-mini",
                context_window=200000,
                supports_reasoning=True,
                speed=0.7,
                accuracy=0.85,
                reasoning_depth=0.8,
                input_cost=3.0,
                output_cost=12.0,
                task_scores={
                    TaskType.REASONING: 0.85,
                    TaskType.CODE_GENERATION: 0.8,
                    TaskType.QA: 0.8,
                }
            ),
            "o1-pro": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="o1-pro",
                context_window=200000,
                supports_reasoning=True,
                speed=0.3,
                accuracy=0.98,
                reasoning_depth=0.98,
                input_cost=60.0,
                output_cost=240.0,
                task_scores={
                    TaskType.REASONING: 0.99,
                    TaskType.DEBUGGING: 0.98,
                    TaskType.SYSTEM_DESIGN: 0.95,
                    TaskType.ANALYSIS: 0.98,
                }
            ),
            
            # Legacy naming for compatibility
            "gpt-4.1-2025-04-14": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4.1-2025-04-14",
                context_window=1000000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.6,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.85,
                input_cost=5.0,
                output_cost=15.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.9,
                    TaskType.ANALYSIS: 0.85,
                    TaskType.CODE_GENERATION: 0.85,
                }
            ),
            "o3": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="o3",
                context_window=200000,
                supports_reasoning=True,
                speed=0.5,
                accuracy=0.92,
                reasoning_depth=0.9,
                input_cost=10.0,
                output_cost=30.0,
                task_scores={
                    TaskType.REASONING: 0.95,
                    TaskType.DEBUGGING: 0.9,
                    TaskType.SYSTEM_DESIGN: 0.9,
                }
            ),
            "o3-mini": ModelCapabilities(
                provider=ModelProvider.OPENAI,
                model_id="o3-mini",
                context_window=200000,
                supports_reasoning=True,
                speed=0.7,
                accuracy=0.85,
                reasoning_depth=0.8,
                input_cost=3.0,
                output_cost=9.0,
                task_scores={
                    TaskType.REASONING: 0.85,
                    TaskType.CODE_GENERATION: 0.8,
                    TaskType.QA: 0.8,
                }
            ),
        })
        
        # Google Gemini models - Complete family coverage
        self.models.update({
            # Gemini 2.0 Family - Latest generation
            "gemini-2.0-pro": ModelCapabilities(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-2.0-pro",
                context_window=2000000,
                supports_function_calling=True,
                supports_reasoning=True,
                supports_vision=True,
                speed=0.75,
                accuracy=0.9,
                reasoning_depth=0.88,
                input_cost=1.5,
                output_cost=6.0,
                task_scores={
                    TaskType.REASONING: 0.88,
                    TaskType.ANALYSIS: 0.9,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.RESEARCH: 0.92,
                    TaskType.VISION: 0.85,
                }
            ),
            "gemini-2.0-flash": ModelCapabilities(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-2.0-flash",
                context_window=1000000,
                supports_function_calling=True,
                supports_vision=True,
                speed=0.95,
                accuracy=0.85,
                reasoning_depth=0.8,
                input_cost=0.1,
                output_cost=0.4,
                task_scores={
                    TaskType.SUMMARIZATION: 0.85,
                    TaskType.TRANSLATION: 0.88,
                    TaskType.QA: 0.82,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.VISION: 0.8,
                }
            ),
            
            # Gemini 1.5 Family - Previous generation
            "gemini-1.5-pro": ModelCapabilities(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-1.5-pro",
                context_window=2000000,
                supports_function_calling=True,
                supports_reasoning=True,
                supports_vision=True,
                speed=0.7,
                accuracy=0.88,
                reasoning_depth=0.85,
                input_cost=1.25,
                output_cost=5.0,
                task_scores={
                    TaskType.REASONING: 0.85,
                    TaskType.ANALYSIS: 0.85,
                    TaskType.CODE_GENERATION: 0.8,
                    TaskType.RESEARCH: 0.9,
                    TaskType.VISION: 0.82,
                }
            ),
            "gemini-1.5-flash": ModelCapabilities(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-1.5-flash",
                context_window=1000000,
                supports_function_calling=True,
                supports_vision=True,
                speed=0.9,
                accuracy=0.8,
                reasoning_depth=0.75,
                input_cost=0.075,
                output_cost=0.3,
                task_scores={
                    TaskType.SUMMARIZATION: 0.8,
                    TaskType.TRANSLATION: 0.85,
                    TaskType.QA: 0.75,
                    TaskType.CONVERSATION: 0.8,
                    TaskType.VISION: 0.75,
                }
            ),
            
            # Legacy naming for compatibility
            "gemini-2.5-pro": ModelCapabilities(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-2.5-pro",
                context_window=1000000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.7,
                accuracy=0.88,
                reasoning_depth=0.85,
                input_cost=1.25,
                output_cost=5.0,
                task_scores={
                    TaskType.REASONING: 0.85,
                    TaskType.ANALYSIS: 0.85,
                    TaskType.CODE_GENERATION: 0.8,
                    TaskType.RESEARCH: 0.9,
                }
            ),
            "gemini-2.5-flash": ModelCapabilities(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-2.5-flash",
                context_window=1000000,
                speed=0.9,
                accuracy=0.8,
                input_cost=0.075,
                output_cost=0.3,
                task_scores={
                    TaskType.SUMMARIZATION: 0.8,
                    TaskType.TRANSLATION: 0.85,
                    TaskType.QA: 0.75,
                    TaskType.CONVERSATION: 0.8,
                }
            ),
        })
        
        # Claude 4 Family models via DIAL and Anthropic
        self.models.update({
            # Claude 4 Family - Latest generation
            "claude-opus-4.1": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-opus-4.1",
                context_window=200000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.6,
                accuracy=0.95,
                reasoning_depth=0.95,
                creativity=0.95,
                input_cost=20.0,
                output_cost=100.0,
                task_scores={
                    TaskType.REASONING: 0.98,
                    TaskType.CREATIVE_WRITING: 0.95,
                    TaskType.CODE_GENERATION: 0.92,
                    TaskType.ANALYSIS: 0.94,
                    TaskType.SYSTEM_DESIGN: 0.92,
                }
            ),
            "claude-opus-4": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-opus-4",
                context_window=200000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.6,
                accuracy=0.92,
                reasoning_depth=0.9,
                creativity=0.9,
                input_cost=15.0,
                output_cost=75.0,
                task_scores={
                    TaskType.REASONING: 0.95,
                    TaskType.CREATIVE_WRITING: 0.95,
                    TaskType.CODE_GENERATION: 0.9,
                    TaskType.ANALYSIS: 0.9,
                }
            ),
            "claude-sonnet-4.5": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-sonnet-4.5",
                context_window=200000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.75,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.85,
                input_cost=4.0,
                output_cost=20.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.9,
                    TaskType.REASONING: 0.88,
                    TaskType.ANALYSIS: 0.88,
                    TaskType.CONVERSATION: 0.9,
                }
            ),
            "claude-sonnet-4": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-sonnet-4",
                context_window=200000,
                supports_function_calling=True,
                speed=0.8,
                accuracy=0.85,
                reasoning_depth=0.8,
                creativity=0.8,
                input_cost=3.0,
                output_cost=15.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.SUMMARIZATION: 0.8,
                }
            ),
            
            # Claude 3 Family - Previous generation
            "claude-3-opus": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-opus",
                context_window=200000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.6,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.9,
                input_cost=15.0,
                output_cost=75.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.92,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.88,
                }
            ),
            "claude-3.5-sonnet": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3.5-sonnet",
                context_window=200000,
                supports_function_calling=True,
                speed=0.8,
                accuracy=0.88,
                reasoning_depth=0.8,
                creativity=0.82,
                input_cost=3.0,
                output_cost=15.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.88,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.SUMMARIZATION: 0.85,
                    TaskType.ANALYSIS: 0.82,
                }
            ),
            "claude-3-haiku": ModelCapabilities(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-haiku",
                context_window=200000,
                supports_function_calling=True,
                speed=0.9,
                accuracy=0.8,
                reasoning_depth=0.7,
                creativity=0.75,
                input_cost=0.25,
                output_cost=1.25,
                task_scores={
                    TaskType.CONVERSATION: 0.8,
                    TaskType.SUMMARIZATION: 0.82,
                    TaskType.QA: 0.8,
                    TaskType.TRANSLATION: 0.78,
                }
            ),
            
            # DIAL API versions (for compatibility)
            "anthropic.claude-opus-4-20250514-v1:0": ModelCapabilities(
                provider=ModelProvider.DIAL,
                model_id="anthropic.claude-opus-4-20250514-v1:0",
                context_window=200000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.6,
                accuracy=0.92,
                reasoning_depth=0.9,
                creativity=0.9,
                input_cost=15.0,
                output_cost=75.0,
                task_scores={
                    TaskType.REASONING: 0.95,
                    TaskType.CREATIVE_WRITING: 0.95,
                    TaskType.CODE_GENERATION: 0.9,
                    TaskType.ANALYSIS: 0.9,
                }
            ),
            "anthropic.claude-sonnet-4-20250514-v1:0": ModelCapabilities(
                provider=ModelProvider.DIAL,
                model_id="anthropic.claude-sonnet-4-20250514-v1:0",
                context_window=200000,
                supports_function_calling=True,
                speed=0.8,
                accuracy=0.85,
                reasoning_depth=0.8,
                creativity=0.8,
                input_cost=3.0,
                output_cost=15.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.SUMMARIZATION: 0.8,
                }
            ),
        })
        
        # Meta Llama models - Open source family
        self.models.update({
            # Llama 3.2 Family - Latest
            "llama-3.2-90b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3.2-90b",
                context_window=128000,
                supports_function_calling=True,
                supports_vision=True,
                speed=0.7,
                accuracy=0.85,
                reasoning_depth=0.8,
                input_cost=0.0,  # Local/open source
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.82,
                    TaskType.REASONING: 0.8,
                    TaskType.CONVERSATION: 0.8,
                    TaskType.VISION: 0.75,
                }
            ),
            "llama-3.2-11b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3.2-11b",
                context_window=128000,
                supports_vision=True,
                speed=0.9,
                accuracy=0.78,
                reasoning_depth=0.75,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.78,
                    TaskType.QA: 0.75,
                    TaskType.VISION: 0.72,
                    TaskType.SUMMARIZATION: 0.75,
                }
            ),
            "llama-3.2-3b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3.2-3b",
                context_window=128000,
                speed=0.95,
                accuracy=0.72,
                reasoning_depth=0.7,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.72,
                    TaskType.QA: 0.7,
                    TaskType.SUMMARIZATION: 0.72,
                }
            ),
            
            # Llama 3.1 Family
            "llama-3.1-405b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3.1-405b",
                context_window=128000,
                supports_function_calling=True,
                speed=0.5,
                accuracy=0.9,
                reasoning_depth=0.88,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.REASONING: 0.88,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.85,
                    TaskType.SYSTEM_DESIGN: 0.82,
                }
            ),
            "llama-3.1-70b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3.1-70b",
                context_window=128000,
                supports_function_calling=True,
                speed=0.7,
                accuracy=0.82,
                reasoning_depth=0.8,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.8,
                    TaskType.REASONING: 0.78,
                    TaskType.CONVERSATION: 0.8,
                    TaskType.QA: 0.78,
                }
            ),
            "llama-3.1-8b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3.1-8b",
                context_window=128000,
                speed=0.9,
                accuracy=0.75,
                reasoning_depth=0.72,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.75,
                    TaskType.QA: 0.72,
                    TaskType.SUMMARIZATION: 0.75,
                    TaskType.CODE_GENERATION: 0.72,
                }
            ),
            
            # Llama 3 Family
            "llama-3-70b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3-70b",
                context_window=8192,
                speed=0.8,
                accuracy=0.8,
                reasoning_depth=0.75,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.8,
                    TaskType.CODE_GENERATION: 0.75,
                    TaskType.QA: 0.78,
                    TaskType.SUMMARIZATION: 0.75,
                }
            ),
            "llama-3-8b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama-3-8b",
                context_window=8192,
                speed=0.95,
                accuracy=0.72,
                reasoning_depth=0.7,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.72,
                    TaskType.QA: 0.7,
                    TaskType.SUMMARIZATION: 0.7,
                }
            ),
            
            # Qwen2.5 Family - Alibaba Cloud models
            "qwen2.5-32b-instruct": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="qwen2.5:32b-instruct-q4_K_M",
                context_window=32768,
                supports_function_calling=True,  # Supports tools
                speed=0.6,  # 32B model, reasonably fast
                accuracy=0.88,  # High quality model
                reasoning_depth=0.85,
                creativity=0.82,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.REASONING: 0.88,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.87,
                    TaskType.QA: 0.85,
                    TaskType.CONVERSATION: 0.83,
                    TaskType.SUMMARIZATION: 0.84,
                    TaskType.TRANSLATION: 0.86,  # Strong multilingual
                }
            ),
            
            # Legacy naming for compatibility
            "llama3.2": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama3.2",
                context_window=128000,
                speed=0.95,
                accuracy=0.7,
                input_cost=0.0,
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.7,
                    TaskType.QA: 0.65,
                    TaskType.SUMMARIZATION: 0.7,
                }
            ),
            
            # Code-specialized local models
            "codellama:34b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="codellama:34b",
                context_window=16384,
                code_specialized=True,
                supports_function_calling=True,
                speed=0.5,  # Large model, slower but high quality
                accuracy=0.9,  # Very high code quality
                reasoning_depth=0.85,
                creativity=0.75,  # More focused on correctness
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.95,  # Excellent for code
                    TaskType.CODE_REVIEW: 0.9,
                    TaskType.DEBUGGING: 0.92,
                    TaskType.SYSTEM_DESIGN: 0.8,
                    TaskType.ANALYSIS: 0.75,
                    TaskType.REASONING: 0.8,
                }
            ),
            "codellama:13b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="codellama:13b",
                context_window=16384,
                code_specialized=True,
                supports_function_calling=True,
                speed=0.8,  # Balanced size, good speed
                accuracy=0.85,  # High code quality
                reasoning_depth=0.8,
                creativity=0.7,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.9,  # Excellent for code
                    TaskType.CODE_REVIEW: 0.85,
                    TaskType.DEBUGGING: 0.88,
                    TaskType.SYSTEM_DESIGN: 0.75,
                    TaskType.ANALYSIS: 0.7,
                    TaskType.REASONING: 0.75,
                }
            ),
            "deepseek-coder:1.3b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="deepseek-coder:1.3b",
                context_window=16384,
                code_specialized=True,
                speed=0.98,  # Very fast, small model
                accuracy=0.75,  # Good for simple tasks
                reasoning_depth=0.6,
                creativity=0.65,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.8,  # Good for simple code
                    TaskType.CODE_REVIEW: 0.7,
                    TaskType.DEBUGGING: 0.75,
                    TaskType.QA: 0.7,
                    TaskType.CONVERSATION: 0.65,
                }
            ),
            "qwen3:8b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="qwen3:8b",
                context_window=32768,
                supports_function_calling=True,
                speed=0.85,  # Good balance
                accuracy=0.82,  # Solid general model
                reasoning_depth=0.8,
                creativity=0.8,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.82,  # Good code capabilities
                    TaskType.REASONING: 0.85,
                    TaskType.ANALYSIS: 0.83,
                    TaskType.QA: 0.8,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.SUMMARIZATION: 0.8,
                    TaskType.TRANSLATION: 0.88,  # Strong multilingual
                }
            ),
            "magicoder:7b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="magicoder:7b",
                context_window=16384,
                code_specialized=True,
                supports_function_calling=True,
                speed=0.9,  # Fast 7B model
                accuracy=0.88,  # Optimized for code quality
                reasoning_depth=0.8,
                creativity=0.75,  # Focused on code correctness
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.92,  # Excellent for code - specialized model
                    TaskType.CODE_REVIEW: 0.88,
                    TaskType.DEBUGGING: 0.9,
                    TaskType.SYSTEM_DESIGN: 0.78,
                    TaskType.ANALYSIS: 0.75,
                    TaskType.QA: 0.72,
                }
            ),
            
            # Additional installed models that were missing
            "llama3.1:8b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama3.1:8b",
                context_window=128000,
                supports_function_calling=True,
                speed=0.90,  # Fast 8B model
                accuracy=0.75,  # Good general model
                reasoning_depth=0.7,
                creativity=0.8,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.75,
                    TaskType.SUMMARIZATION: 0.75,
                    TaskType.QA: 0.72,
                    TaskType.CODE_GENERATION: 0.7,
                    TaskType.REASONING: 0.73,
                }
            ),
            "llama3.2:3b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="llama3.2:3b",
                context_window=128000,
                speed=0.95,  # Very fast, lightweight
                accuracy=0.72,  # Good for simple tasks
                reasoning_depth=0.65,
                creativity=0.7,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.CONVERSATION: 0.72,
                    TaskType.SUMMARIZATION: 0.72,
                    TaskType.QA: 0.70,
                    TaskType.CODE_GENERATION: 0.65,
                }
            ),
            "deepseek-r1:70b": ModelCapabilities(
                provider=ModelProvider.LOCAL,
                model_id="deepseek-r1:70b",
                context_window=32768,
                supports_reasoning=True,
                supports_function_calling=True,
                speed=0.4,  # Large model, slower
                accuracy=0.92,  # Very high quality
                reasoning_depth=0.95,  # Excellent reasoning
                creativity=0.85,
                input_cost=0.0,  # Local/free
                output_cost=0.0,
                task_scores={
                    TaskType.REASONING: 0.95,  # Excellent reasoning model
                    TaskType.ANALYSIS: 0.93,
                    TaskType.SYSTEM_DESIGN: 0.88,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.DEBUGGING: 0.90,
                    TaskType.RESEARCH: 0.92,
                }
            ),
        })
        
        # Azure OpenAI Service models
        self.models.update({
            # Azure GPT-4 models
            "azure-gpt-4": ModelCapabilities(
                provider=ModelProvider.AZURE,
                model_id="gpt-4",
                context_window=8192,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.5,
                accuracy=0.92,
                reasoning_depth=0.88,
                creativity=0.85,
                input_cost=30.0,  # Azure pricing may vary
                output_cost=60.0,
                task_scores={
                    TaskType.REASONING: 0.92,
                    TaskType.CREATIVE_WRITING: 0.88,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.9,
                }
            ),
            "azure-gpt-4-turbo": ModelCapabilities(
                provider=ModelProvider.AZURE,
                model_id="gpt-4-turbo",
                context_window=128000,
                supports_function_calling=True,
                supports_reasoning=True,
                supports_vision=True,
                speed=0.7,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.85,
                input_cost=10.0,
                output_cost=30.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.88,
                    TaskType.CODE_GENERATION: 0.88,
                    TaskType.VISION: 0.85,
                }
            ),
            "azure-gpt-4o": ModelCapabilities(
                provider=ModelProvider.AZURE,
                model_id="gpt-4o",
                context_window=128000,
                supports_function_calling=True,
                supports_reasoning=True,
                supports_vision=True,
                speed=0.8,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.85,
                input_cost=5.0,
                output_cost=15.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.9,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.VISION: 0.88,
                }
            ),
            
            # Azure Claude models (through partnership)
            "azure-claude-3.5-sonnet": ModelCapabilities(
                provider=ModelProvider.AZURE,
                model_id="claude-3.5-sonnet",
                context_window=200000,
                supports_function_calling=True,
                speed=0.8,
                accuracy=0.88,
                reasoning_depth=0.8,
                creativity=0.82,
                input_cost=3.0,
                output_cost=15.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.88,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.SUMMARIZATION: 0.85,
                }
            ),
        })
        
        # Amazon Bedrock models
        self.models.update({
            # Bedrock Claude models
            "bedrock-claude-3-opus": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="anthropic.claude-3-opus-20240229-v1:0",
                context_window=200000,
                supports_function_calling=True,
                supports_reasoning=True,
                speed=0.6,
                accuracy=0.9,
                reasoning_depth=0.85,
                creativity=0.9,
                input_cost=15.0,
                output_cost=75.0,
                task_scores={
                    TaskType.REASONING: 0.9,
                    TaskType.CREATIVE_WRITING: 0.92,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.88,
                }
            ),
            "bedrock-claude-3.5-sonnet": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
                context_window=200000,
                supports_function_calling=True,
                speed=0.8,
                accuracy=0.88,
                reasoning_depth=0.8,
                creativity=0.82,
                input_cost=3.0,
                output_cost=15.0,
                task_scores={
                    TaskType.CODE_GENERATION: 0.88,
                    TaskType.CONVERSATION: 0.85,
                    TaskType.SUMMARIZATION: 0.85,
                }
            ),
            "bedrock-claude-3-haiku": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                context_window=200000,
                speed=0.9,
                accuracy=0.8,
                reasoning_depth=0.7,
                creativity=0.75,
                input_cost=0.25,
                output_cost=1.25,
                task_scores={
                    TaskType.CONVERSATION: 0.8,
                    TaskType.SUMMARIZATION: 0.82,
                    TaskType.QA: 0.8,
                }
            ),
            
            # Bedrock Llama models
            "bedrock-llama-3.1-405b": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="meta.llama3-1-405b-instruct-v1:0",
                context_window=32768,
                supports_function_calling=True,
                speed=0.5,
                accuracy=0.9,
                reasoning_depth=0.88,
                input_cost=5.32,
                output_cost=16.0,
                task_scores={
                    TaskType.REASONING: 0.88,
                    TaskType.CODE_GENERATION: 0.85,
                    TaskType.ANALYSIS: 0.85,
                }
            ),
            "bedrock-llama-3.1-70b": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="meta.llama3-1-70b-instruct-v1:0",
                context_window=32768,
                supports_function_calling=True,
                speed=0.7,
                accuracy=0.82,
                reasoning_depth=0.8,
                input_cost=2.65,
                output_cost=3.5,
                task_scores={
                    TaskType.CODE_GENERATION: 0.8,
                    TaskType.REASONING: 0.78,
                    TaskType.CONVERSATION: 0.8,
                }
            ),
            "bedrock-llama-3.1-8b": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="meta.llama3-1-8b-instruct-v1:0",
                context_window=32768,
                speed=0.9,
                accuracy=0.75,
                reasoning_depth=0.72,
                input_cost=0.22,
                output_cost=0.22,
                task_scores={
                    TaskType.CONVERSATION: 0.75,
                    TaskType.QA: 0.72,
                    TaskType.SUMMARIZATION: 0.75,
                }
            ),
            
            # Amazon Titan models
            "bedrock-titan-text-express": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="amazon.titan-text-express-v1",
                context_window=8192,
                speed=0.9,
                accuracy=0.75,
                reasoning_depth=0.7,
                input_cost=0.8,
                output_cost=1.6,
                task_scores={
                    TaskType.CONVERSATION: 0.75,
                    TaskType.SUMMARIZATION: 0.78,
                    TaskType.QA: 0.72,
                }
            ),
            "bedrock-titan-text-lite": ModelCapabilities(
                provider=ModelProvider.BEDROCK,
                model_id="amazon.titan-text-lite-v1",
                context_window=4096,
                speed=0.95,
                accuracy=0.7,
                reasoning_depth=0.65,
                input_cost=0.3,
                output_cost=0.4,
                task_scores={
                    TaskType.CONVERSATION: 0.7,
                    TaskType.SUMMARIZATION: 0.72,
                    TaskType.QA: 0.68,
                }
            ),
        })

    def _initialize_clients(self):
        """Initialize API clients for available providers"""

        # xAI/Grok
        if os.getenv("XAI_API_KEY"):
            try:
                from grok_api import GrokAPI
                self.api_clients['xai'] = GrokAPI()
                logger.info("✓ Grok API client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Grok client: {e}")

        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.api_clients['openai'] = get_api_client('openai')
                logger.info("✓ OpenAI API client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")

        # Google
        if os.getenv("GOOGLE_API_KEY"):
            try:
                self.api_clients['google'] = get_api_client('google')
                logger.info("✓ Google API client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google client: {e}")

        # Anthropic/DIAL
        if os.getenv("DIAL_API_KEY"):
            try:
                self.api_clients['dial'] = get_api_client('dial')
                logger.info("✓ DIAL API client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize DIAL client: {e}")
        elif os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.api_clients['anthropic'] = get_api_client('anthropic')
                logger.info("✓ Anthropic API client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {e}")

        # Local models
        try:
            self.api_clients['local'] = get_api_client('local')
            logger.info("✓ Local model client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize local client: {e}")

    def analyze_task(self, prompt: str, context: Optional[Dict] = None) -> TaskRequirements:
        """Analyze prompt to determine task requirements"""
        
        # Keywords for task type detection
        task_keywords = {
            TaskType.CODE_GENERATION: ["write", "implement", "create", "code", "function", "class"],
            TaskType.CODE_REVIEW: ["review", "check", "analyze code", "improve code"],
            TaskType.REASONING: ["think", "reason", "analyze", "solve", "deduce"],
            TaskType.CREATIVE_WRITING: ["story", "poem", "creative", "fiction", "narrative"],
            TaskType.VISION: ["image", "picture", "screenshot", "visual", "see"],
            TaskType.DEBUGGING: ["debug", "fix", "error", "bug", "troubleshoot"],
            TaskType.SYSTEM_DESIGN: ["design", "architect", "structure", "system"],
            TaskType.RESEARCH: ["research", "find", "discover", "investigate"],
            TaskType.TRANSLATION: ["translate", "translation", "chinese", "japanese", "spanish", "french", "german", "multilingual"],
        }
        
        # Detect task type
        prompt_lower = prompt.lower()
        detected_type = TaskType.CONVERSATION  # default
        max_matches = 0
        
        for task_type, keywords in task_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in prompt_lower)
            if matches > max_matches:
                max_matches = matches
                detected_type = task_type
        
        # Estimate context requirements
        prompt_length = len(prompt)
        estimated_context = max(4096, prompt_length * 10)  # Rule of thumb
        
        # Check for specific requirements
        requires_vision = any(word in prompt_lower for word in ["image", "picture", "screenshot", "visual"])
        requires_reasoning = any(word in prompt_lower for word in ["think", "reason", "explain why", "analyze"])
        requires_function = any(word in prompt_lower for word in ["function", "api", "tool", "call"])
        
        return TaskRequirements(
            task_type=detected_type,
            min_context_window=estimated_context,
            requires_vision=requires_vision,
            requires_function_calling=requires_function,
            requires_reasoning=requires_reasoning,
        )
    
    def score_model(self, model: ModelCapabilities, requirements: TaskRequirements) -> float:
        """Score model fitness for task requirements"""
        score = 0.0
        
        # Hard requirements (disqualifying if not met)
        if requirements.min_context_window > model.context_window:
            return 0.0
        if requirements.requires_vision and not model.supports_vision:
            return 0.0
        if requirements.requires_function_calling and not model.supports_function_calling:
            return 0.0
        
        # Task affinity score (40% weight)
        task_score = model.task_scores.get(requirements.task_type, 0.5)
        score += task_score * 0.4
        
        # Performance score (30% weight)
        if requirements.requires_reasoning:
            score += model.reasoning_depth * 0.3
        else:
            score += model.speed * 0.3
        
        # Accuracy score (20% weight)
        score += model.accuracy * 0.2
        
        # Cost efficiency (10% weight)
        # Inverse cost score (lower cost = higher score)
        max_cost = 100.0  # Normalize against max expected cost
        cost_score = 1.0 - min(1.0, (model.input_cost + model.output_cost) / max_cost)
        score += cost_score * 0.1
        
        # Apply provider preference if specified
        if requirements.preferred_providers and model.provider in requirements.preferred_providers:
            score *= 1.1  # 10% bonus
        
        return min(1.0, score)  # Cap at 1.0
    
    def select_model(self, 
                    prompt: str, 
                    context: Optional[Dict] = None,
                    strategy: str = "balanced") -> Tuple[str, ModelCapabilities]:
        """Select best model for task"""
        
        requirements = self.analyze_task(prompt, context)
        
        # Score all available models
        scores = {}
        for model_id, model in self.models.items():
            if model.available:
                scores[model_id] = self.score_model(model, requirements)
        
        if not scores:
            raise ValueError("No suitable models available")
        
        # Apply strategy modifiers
        if strategy == "cost_optimize":
            # Heavily weight cost efficiency
            for model_id in scores:
                model = self.models[model_id]
                cost_factor = 1.0 - min(1.0, (model.input_cost + model.output_cost) / 50.0)
                scores[model_id] *= (0.5 + 0.5 * cost_factor)
        elif strategy == "quality_first":
            # Heavily weight accuracy and reasoning
            for model_id in scores:
                model = self.models[model_id]
                quality_factor = (model.accuracy + model.reasoning_depth) / 2
                scores[model_id] *= (0.5 + 0.5 * quality_factor)
        elif strategy == "speed_priority":
            # Heavily weight speed
            for model_id in scores:
                model = self.models[model_id]
                scores[model_id] *= (0.5 + 0.5 * model.speed)
        
        # Select best model
        best_model_id = max(scores, key=scores.get)
        
        logger.info(f"Selected model: {best_model_id} (score: {scores[best_model_id]:.2f})")
        logger.info(f"Task type: {requirements.task_type.value}")
        
        return best_model_id, self.models[best_model_id]
    
    def create_model_chain(self, 
                          tasks: List[str],
                          strategy: str = "balanced") -> List[Tuple[str, ModelCapabilities]]:
        """Create chain of models for sequential tasks"""
        chain = []
        
        for task in tasks:
            model_id, model = self.select_model(task, strategy=strategy)
            chain.append((model_id, model))
        
        return chain
    
    def create_consensus_group(self,
                             prompt: str,
                             num_models: int = 3,
                             diverse: bool = True) -> List[Tuple[str, ModelCapabilities]]:
        """Select multiple models for consensus/voting"""
        requirements = self.analyze_task(prompt)
        
        # Score all models
        scores = {}
        for model_id, model in self.models.items():
            if model.available:
                scores[model_id] = self.score_model(model, requirements)
        
        # Sort by score
        sorted_models = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if diverse:
            # Select diverse providers
            selected = []
            providers_used = set()
            
            for model_id, score in sorted_models:
                model = self.models[model_id]
                if model.provider not in providers_used or len(selected) < num_models:
                    selected.append((model_id, model))
                    providers_used.add(model.provider)
                    
                if len(selected) >= num_models:
                    break
        else:
            # Just take top N
            selected = [(m[0], self.models[m[0]]) for m in sorted_models[:num_models]]
        
        return selected
    
    def estimate_cost(self, 
                     model_id: str,
                     input_tokens: int,
                     output_tokens: int) -> float:
        """Estimate cost for model usage"""
        model = self.models[model_id]
        
        input_cost = (input_tokens / 1_000_000) * model.input_cost
        output_cost = (output_tokens / 1_000_000) * model.output_cost
        
        return input_cost + output_cost
    
    def track_usage(self,
                   model_id: str,
                   input_tokens: int,
                   output_tokens: int,
                   latency_ms: int,
                   success: bool = True):
        """Track model usage for optimization"""
        cost = self.estimate_cost(model_id, input_tokens, output_tokens)
        
        # Update cost tracker
        if model_id not in self.cost_tracker:
            self.cost_tracker[model_id] = 0.0
        self.cost_tracker[model_id] += cost
        
        # Record performance
        self.performance_history.append({
            "timestamp": datetime.now().isoformat(),
            "model_id": model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "latency_ms": latency_ms,
            "success": success
        })
    
    def get_cost_report(self) -> Dict[str, Any]:
        """Generate cost report"""
        total_cost = sum(self.cost_tracker.values())
        
        report = {
            "total_cost": total_cost,
            "by_model": self.cost_tracker.copy(),
            "by_provider": {},
            "usage_count": {}
        }
        
        # Aggregate by provider
        for model_id, cost in self.cost_tracker.items():
            provider = self.models[model_id].provider.value
            if provider not in report["by_provider"]:
                report["by_provider"][provider] = 0.0
            report["by_provider"][provider] += cost
        
        # Count usage
        for entry in self.performance_history:
            model_id = entry["model_id"]
            if model_id not in report["usage_count"]:
                report["usage_count"][model_id] = 0
            report["usage_count"][model_id] += 1
        
        return report

class InteractionPattern:
    """Multi-model interaction patterns"""
    
    @staticmethod
    async def chain_of_thought(orchestrator: ModelOrchestrator,
                              tasks: List[str]) -> List[Any]:
        """Sequential chain of thought across models"""
        results = []
        context = {}
        
        for i, task in enumerate(tasks):
            model_id, model = orchestrator.select_model(task, context)
            
            # Simulate API call (replace with actual implementation)
            result = await InteractionPattern._call_model(model_id, task, context)
            
            results.append(result)
            context[f"step_{i}"] = result
        
        return results
    
    @staticmethod
    async def parallel_consensus(orchestrator: ModelOrchestrator,
                                prompt: str,
                                num_models: int = 3) -> Dict[str, Any]:
        """Parallel execution with consensus"""
        models = orchestrator.create_consensus_group(prompt, num_models)
        
        # Parallel execution
        tasks = []
        for model_id, model in models:
            tasks.append(InteractionPattern._call_model(model_id, prompt))
        
        results = await asyncio.gather(*tasks)
        
        # Simple voting consensus (can be enhanced)
        consensus = {
            "models": [m[0] for m in models],
            "results": results,
            "consensus": InteractionPattern._determine_consensus(results)
        }
        
        return consensus
    
    @staticmethod
    async def hierarchical_refinement(orchestrator: ModelOrchestrator,
                                     initial_prompt: str,
                                     refinement_prompts: List[str]) -> Dict[str, Any]:
        """Hierarchical refinement with increasing capability"""
        results = {"initial": None, "refinements": []}
        
        # Start with fast/cheap model
        model_id, _ = orchestrator.select_model(initial_prompt, strategy="speed_priority")
        results["initial"] = await InteractionPattern._call_model(model_id, initial_prompt)
        
        # Refine with increasingly capable models
        for prompt in refinement_prompts:
            model_id, _ = orchestrator.select_model(prompt, strategy="quality_first")
            refinement = await InteractionPattern._call_model(
                model_id, 
                f"{prompt}\n\nPrevious result: {results['initial']}"
            )
            results["refinements"].append(refinement)
        
        return results
    
    @staticmethod
    async def _call_model(model_id: str, prompt: str, context: Optional[Dict] = None) -> str:
        """Make actual API calls to different providers"""
        from api_clients import get_api_client, APIResponse
        
        # Get model info from orchestrator (needs to be passed in or made accessible)
        # For now, we'll parse the provider from model_id patterns
        provider_map = {
            'grok': 'xai',
            'gpt': 'openai',
            'o3': 'openai',
            'gemini': 'google',
            'claude': 'anthropic',
            'llama': 'local'
        }
        
        provider = None
        for key, val in provider_map.items():
            if key in model_id.lower():
                provider = val
                break
        
        if not provider:
            # Try DIAL models
            if 'anthropic' in model_id:
                provider = 'dial'
            else:
                raise ValueError(f"Cannot determine provider for model: {model_id}")
        
        try:
            # Create appropriate client
            client = get_api_client(provider)
            
            # Prepare messages
            messages = []
            if context and 'system_prompt' in context:
                messages.append({"role": "system", "content": context['system_prompt']})
            
            # Add previous context if available
            if context and 'history' in context:
                messages.extend(context['history'])
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            async with client:
                response = await client.chat_completion(
                    model=model_id,
                    messages=messages,
                    temperature=context.get('temperature', 0.7) if context else 0.7
                )
            
            return response.content
            
        except Exception as e:
            logger.error(f"API call failed for {model_id}: {e}")
            # Fallback to mock response in case of error
            return f"Error calling {model_id}: {str(e)}"
    
    @staticmethod
    def _determine_consensus(results: List[str]) -> str:
        """Determine consensus from multiple results"""
        # Simplified consensus - would use more sophisticated methods
        return results[0] if results else "No consensus"

def main():
    """Demo and testing"""
    orchestrator = ModelOrchestrator()
    
    # Test scenarios
    test_prompts = [
        "Write a Python function to calculate fibonacci",
        "Analyze this image and describe what you see",
        "Reason through this complex math problem step by step",
        "Generate a creative story about space exploration",
        "Debug this code and find the error",
        "Translate this text to Spanish",
    ]
    
    print("="*80)
    print("Model Orchestrator - Intelligent Model Selection")
    print("="*80)
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt[:50]}...")
        model_id, model = orchestrator.select_model(prompt)
        
        print(f"  Selected: {model_id}")
        print(f"  Provider: {model.provider.value}")
        print(f"  Context: {model.context_window:,} tokens")
        print(f"  Est. Cost: ${model.input_cost:.2f}/$M input, ${model.output_cost:.2f}/$M output")
        
        # Simulate usage
        orchestrator.track_usage(model_id, 1000, 500, 250)
    
    print("\n" + "="*80)
    print("Cost Report")
    print("="*80)
    
    report = orchestrator.get_cost_report()
    print(f"Total Cost: ${report['total_cost']:.4f}")
    print("\nBy Provider:")
    for provider, cost in report["by_provider"].items():
        print(f"  {provider}: ${cost:.4f}")

if __name__ == "__main__":
    main()