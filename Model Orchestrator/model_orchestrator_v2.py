#!/usr/bin/env python3
"""
Model Orchestrator V2 - With Real API Integration
Enhanced version with actual API calls and improved error handling
"""

import os
import json
import yaml
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import time

from api_clients import get_api_client, APIResponse, BaseAPIClient
from model_orchestrator import TaskType, ModelProvider, ModelCapabilities, TaskRequirements

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelOrchestratorV2:
    """Enhanced orchestrator with real API integration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or Path(__file__).parent / "orchestrator_config.yaml"
        self.models: Dict[str, ModelCapabilities] = {}
        self.api_clients: Dict[str, BaseAPIClient] = {}
        self.cost_tracker: Dict[str, float] = {}
        self.performance_history: List[Dict] = []
        
        # Load models from base orchestrator
        from model_orchestrator import ModelOrchestrator
        base_orchestrator = ModelOrchestrator()
        self.models = base_orchestrator.models
        
        # Initialize API clients
        self._initialize_clients()
    
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
    
    async def call_model(self,
                        model_id: str,
                        messages: Union[List[Dict], str],
                        temperature: float = 0.7,
                        max_tokens: Optional[int] = None,
                        stream: bool = False,
                        **kwargs) -> APIResponse:
        """Call a specific model with proper client routing"""
        
        if model_id not in self.models:
            raise ValueError(f"Unknown model: {model_id}")
        
        model = self.models[model_id]
        provider = model.provider.value
        
        # Convert string prompt to messages format
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        # Check if we have client for this provider
        if provider not in self.api_clients:
            raise ValueError(f"No API client available for provider: {provider}")
        
        client = self.api_clients[provider]
        
        # Special handling for Grok models
        if provider == 'xai' and isinstance(client, type(client).__class__.__name__ == 'GrokAPI'):
            # Use GrokAPI's native method
            start_time = time.time()
            
            if stream:
                # Handle streaming for Grok
                response = client.stream_completion(
                    model_id=model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                # For streaming, return generator
                return response
            else:
                response_data = client.chat_completion(
                    model_id=model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                
                latency_ms = int((time.time() - start_time) * 1000)
                
                # Convert to standardized format
                return APIResponse(
                    content=response_data['choices'][0]['message']['content'],
                    model=model_id,
                    provider=provider,
                    usage={
                        'input_tokens': response_data['usage']['prompt_tokens'],
                        'output_tokens': response_data['usage']['completion_tokens']
                    },
                    latency_ms=latency_ms,
                    raw_response=response_data
                )
        else:
            # Use unified API client
            async with client:
                response = await client.chat_completion(
                    model=model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    **kwargs
                )
            
            # Track usage
            if not stream:
                self.track_usage(
                    model_id=model_id,
                    input_tokens=response.usage['input_tokens'],
                    output_tokens=response.usage['output_tokens'],
                    latency_ms=response.latency_ms,
                    success=response.error is None
                )
            
            return response
    
    async def route_request(self,
                           prompt: str,
                           strategy: str = "balanced",
                           context: Optional[Dict] = None,
                           stream: bool = False) -> APIResponse:
        """Route request to best model and make actual API call"""
        
        # Analyze task
        from model_orchestrator import ModelOrchestrator
        base_orchestrator = ModelOrchestrator()
        requirements = base_orchestrator.analyze_task(prompt, context)
        
        # Select best model
        model_id, model = base_orchestrator.select_model(prompt, context, strategy)
        
        logger.info(f"Selected model: {model_id} (provider: {model.provider.value})")
        
        # Make actual API call
        try:
            response = await self.call_model(
                model_id=model_id,
                messages=prompt,
                temperature=context.get('temperature', 0.7) if context else 0.7,
                max_tokens=context.get('max_tokens') if context else None,
                stream=stream
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to call {model_id}: {e}")
            
            # Try fallback model
            fallback_models = self._get_fallback_models(model_id, requirements)
            
            for fallback_id in fallback_models:
                try:
                    logger.info(f"Trying fallback model: {fallback_id}")
                    response = await self.call_model(
                        model_id=fallback_id,
                        messages=prompt,
                        temperature=context.get('temperature', 0.7) if context else 0.7,
                        max_tokens=context.get('max_tokens') if context else None,
                        stream=stream
                    )
                    return response
                except Exception as e2:
                    logger.error(f"Fallback {fallback_id} also failed: {e2}")
                    continue
            
            # All models failed
            raise Exception(f"All models failed for this request. Original error: {e}")
    
    def _get_fallback_models(self, 
                            failed_model_id: str,
                            requirements: TaskRequirements) -> List[str]:
        """Get fallback models for a failed request"""
        
        from model_orchestrator import ModelOrchestrator
        base_orchestrator = ModelOrchestrator()
        
        # Score all models except the failed one
        scores = {}
        for model_id, model in self.models.items():
            if model_id != failed_model_id and model.available:
                # Check if provider client is available
                if model.provider.value in self.api_clients:
                    scores[model_id] = base_orchestrator.score_model(model, requirements)
        
        # Sort by score and return top 3
        sorted_models = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [m[0] for m in sorted_models[:3]]
    
    async def consensus_call(self,
                            prompt: str,
                            num_models: int = 3,
                            diverse: bool = True) -> Dict[str, Any]:
        """Call multiple models for consensus"""
        
        from model_orchestrator import ModelOrchestrator
        base_orchestrator = ModelOrchestrator()
        
        # Get consensus group
        models = base_orchestrator.create_consensus_group(prompt, num_models, diverse)
        
        # Filter to only available providers
        available_models = [
            (m_id, m) for m_id, m in models 
            if m.provider.value in self.api_clients
        ]
        
        if not available_models:
            raise ValueError("No available models for consensus")
        
        # Make parallel calls
        tasks = []
        for model_id, model in available_models:
            tasks.append(self.call_model(model_id, prompt))
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process responses
        results = []
        errors = []
        
        for i, response in enumerate(responses):
            model_id = available_models[i][0]
            
            if isinstance(response, Exception):
                errors.append({"model": model_id, "error": str(response)})
            else:
                results.append({
                    "model": model_id,
                    "content": response.content,
                    "latency_ms": response.latency_ms,
                    "tokens": response.usage
                })
        
        # Determine consensus (simple voting for now)
        consensus_content = None
        if results:
            # For now, just take the most common response or first one
            # Could implement more sophisticated consensus logic
            consensus_content = results[0]["content"]
        
        return {
            "consensus": consensus_content,
            "individual_results": results,
            "errors": errors,
            "models_used": [m[0] for m in available_models],
            "timestamp": datetime.now().isoformat()
        }
    
    async def stream_response(self,
                            model_id: str,
                            prompt: str,
                            **kwargs):
        """Stream response from a model"""
        
        if model_id not in self.models:
            raise ValueError(f"Unknown model: {model_id}")
        
        model = self.models[model_id]
        provider = model.provider.value
        
        if provider not in self.api_clients:
            raise ValueError(f"No API client for provider: {provider}")
        
        client = self.api_clients[provider]
        
        # Special handling for different providers
        if provider == 'xai':
            # Grok streaming
            async for chunk in client.stream_completion(
                model_id=model_id,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            ):
                yield chunk
        else:
            # Generic streaming
            async with client:
                if hasattr(client, '_stream_completion'):
                    async for chunk in client._stream_completion(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt}],
                        **kwargs
                    ):
                        yield chunk
                else:
                    # Fallback to non-streaming
                    response = await client.chat_completion(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt}],
                        **kwargs
                    )
                    yield response.content
    
    def track_usage(self,
                   model_id: str,
                   input_tokens: int,
                   output_tokens: int,
                   latency_ms: int,
                   success: bool = True):
        """Track model usage for optimization"""
        
        from model_orchestrator import ModelOrchestrator
        base_orchestrator = ModelOrchestrator()
        
        # Calculate cost
        cost = base_orchestrator.estimate_cost(model_id, input_tokens, output_tokens)
        
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
        
        # Keep only last 1000 entries to prevent memory issues
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models by provider"""
        
        available = {}
        for model_id, model in self.models.items():
            provider = model.provider.value
            
            # Check if we have API client for this provider
            if provider in self.api_clients:
                if provider not in available:
                    available[provider] = []
                available[provider].append(model_id)
        
        return available


# Example usage and testing
async def test_orchestrator_v2():
    """Test the enhanced orchestrator with real APIs"""
    
    orchestrator = ModelOrchestratorV2()
    
    print("="*80)
    print("Model Orchestrator V2 - Real API Integration Test")
    print("="*80)
    
    # Check available models
    available = orchestrator.get_available_models()
    print("\nAvailable Models by Provider:")
    for provider, models in available.items():
        print(f"  {provider}: {len(models)} models")
        for model in models[:3]:  # Show first 3
            print(f"    - {model}")
    
    # Test simple request (if API keys are set)
    if available:
        print("\n" + "="*80)
        print("Testing API Call")
        print("="*80)
        
        try:
            response = await orchestrator.route_request(
                prompt="What is 2+2? Answer in one word.",
                strategy="cost_optimize"
            )
            
            print(f"\nModel used: {response.model}")
            print(f"Provider: {response.provider}")
            print(f"Response: {response.content}")
            print(f"Latency: {response.latency_ms}ms")
            print(f"Tokens: {response.usage}")
            
        except Exception as e:
            print(f"API call failed: {e}")
            print("Make sure you have set the appropriate API keys")
    
    # Test consensus (if multiple providers available)
    if len(available) >= 2:
        print("\n" + "="*80)
        print("Testing Consensus")
        print("="*80)
        
        try:
            consensus = await orchestrator.consensus_call(
                prompt="What is the capital of France?",
                num_models=min(3, sum(len(m) for m in available.values()))
            )
            
            print(f"\nConsensus: {consensus['consensus']}")
            print(f"Models used: {consensus['models_used']}")
            print(f"Individual results: {len(consensus['individual_results'])}")
            
        except Exception as e:
            print(f"Consensus call failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_orchestrator_v2())