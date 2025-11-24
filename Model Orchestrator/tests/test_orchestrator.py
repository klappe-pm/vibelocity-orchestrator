#!/usr/bin/env python3
"""
Comprehensive unit tests for Model Orchestrator
Target: 90%+ code coverage

Test Categories:
1. Model Registry Tests
2. Task Analyzer Tests
3. Model Scorer Tests
4. Model Selection Tests
5. Cost Tracking Tests
6. Guide Integration Tests
7. Error Handling Tests
8. Integration Tests
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, List
from unittest.mock import Mock, AsyncMock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import using filename with hyphens - needs special handling
import importlib.util
spec = importlib.util.spec_from_file_location(
    "model_orchestrator_consolidated",
    Path(__file__).parent.parent / "model-orchestrator-consolidated.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Extract classes
ModelOrchestrator = mod.ModelOrchestrator
ModelRegistry = mod.ModelRegistry
ModelGuideParser = mod.ModelGuideParser
TaskAnalyzer = mod.TaskAnalyzer
ModelScorer = mod.ModelScorer
TaskType = mod.TaskType
ModelProvider = mod.ModelProvider
ModelCapabilities = mod.ModelCapabilities
TaskRequirements = mod.TaskRequirements
APIResponse = mod.APIResponse


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def model_registry():
    """Create a model registry for testing"""
    return ModelRegistry()


@pytest.fixture
def task_analyzer():
    """Create a task analyzer for testing"""
    return TaskAnalyzer()


@pytest.fixture
def model_scorer():
    """Create a model scorer for testing"""
    return ModelScorer()


@pytest.fixture
def mock_guide():
    """Create a mock model guide"""
    guide = Mock()
    guide.get_recommended_models.return_value = ["codellama:34b", "magicoder:7b"]
    guide.get_fallback_chain.return_value = ["grok-code-fast-1", "codellama:34b"]
    guide.is_model_blocked.return_value = False
    return guide


@pytest.fixture
def mock_api_client():
    """Create a mock API client"""
    client = AsyncMock()
    client.chat_completion.return_value = APIResponse(
        content="Test response",
        model="test-model",
        provider="test",
        usage={"input_tokens": 100, "output_tokens": 50},
        latency_ms=200,
    )
    return client


@pytest.fixture
def orchestrator(model_registry, mock_guide, task_analyzer, model_scorer):
    """Create an orchestrator with mocked dependencies"""
    def mock_client_factory(provider):
        return AsyncMock()

    return ModelOrchestrator(
        registry=model_registry,
        guide=mock_guide,
        analyzer=task_analyzer,
        scorer=model_scorer,
        api_client_factory=mock_client_factory
    )


# ============================================================================
# Model Registry Tests
# ============================================================================

class TestModelRegistry:
    """Test ModelRegistry functionality"""

    def test_registry_initialization(self, model_registry):
        """Test that registry initializes with models"""
        assert len(model_registry.models) > 0
        assert "codellama:34b" in model_registry.models
        assert "grok-code-fast-1" in model_registry.models

    def test_get_model_exists(self, model_registry):
        """Test getting an existing model"""
        model = model_registry.get_model("codellama:34b")
        assert model is not None
        assert model.model_id == "codellama:34b"
        assert model.provider == ModelProvider.LOCAL

    def test_get_model_not_exists(self, model_registry):
        """Test getting a non-existent model"""
        model = model_registry.get_model("nonexistent-model")
        assert model is None

    def test_get_models_by_provider(self, model_registry):
        """Test filtering models by provider"""
        local_models = model_registry.get_models_by_provider(ModelProvider.LOCAL)
        assert len(local_models) > 0
        assert all(m.provider == ModelProvider.LOCAL for m in local_models)

    def test_get_available_models(self, model_registry):
        """Test getting available model IDs"""
        available = model_registry.get_available_models()
        assert len(available) > 0
        assert "codellama:34b" in available

    def test_model_capabilities_structure(self, model_registry):
        """Test that all models have required capabilities"""
        for model_id, model in model_registry.models.items():
            assert isinstance(model.provider, ModelProvider)
            assert isinstance(model.context_window, int)
            assert model.context_window > 0
            assert 0 <= model.speed <= 1
            assert 0 <= model.accuracy <= 1
            assert model.input_cost >= 0
            assert model.output_cost >= 0


# ============================================================================
# Task Analyzer Tests
# ============================================================================

class TestTaskAnalyzer:
    """Test TaskAnalyzer functionality"""

    def test_code_generation_detection(self, task_analyzer):
        """Test detection of code generation tasks"""
        req = task_analyzer.analyze("Write a Python function to sort a list")
        assert req.task_type == TaskType.CODE_GENERATION
        assert req.min_context_window >= 4096

    def test_debugging_detection(self, task_analyzer):
        """Test detection of debugging tasks"""
        req = task_analyzer.analyze("Debug this code and fix the error")
        assert req.task_type == TaskType.DEBUGGING

    def test_translation_detection(self, task_analyzer):
        """Test detection of translation tasks"""
        req = task_analyzer.analyze("Translate this text to Spanish")
        assert req.task_type == TaskType.TRANSLATION

    def test_reasoning_detection(self, task_analyzer):
        """Test detection of reasoning tasks"""
        req = task_analyzer.analyze("Think through this problem step by step")
        assert req.task_type == TaskType.REASONING
        assert req.requires_reasoning is True

    def test_vision_requirement_detection(self, task_analyzer):
        """Test detection of vision requirements"""
        req = task_analyzer.analyze("Analyze this image and describe what you see")
        assert req.requires_vision is True

    def test_function_calling_detection(self, task_analyzer):
        """Test detection of function calling requirements"""
        req = task_analyzer.analyze("Call the API function to get data")
        assert req.requires_function_calling is True

    def test_empty_prompt(self, task_analyzer):
        """Test handling of empty prompt"""
        req = task_analyzer.analyze("")
        assert req.task_type == TaskType.CONVERSATION
        assert req.min_context_window >= 4096

    def test_long_prompt_context_estimation(self, task_analyzer):
        """Test context window estimation for long prompts"""
        long_prompt = "x" * 10000
        req = task_analyzer.analyze(long_prompt)
        # Context estimation is max(4096, prompt_length * 10) = max(4096, 100000)
        assert req.min_context_window >= 100000


# ============================================================================
# Model Scorer Tests
# ============================================================================

class TestModelScorer:
    """Test ModelScorer functionality"""

    def test_score_calculation(self, model_scorer):
        """Test basic score calculation"""
        model = ModelCapabilities(
            provider=ModelProvider.LOCAL,
            model_id="test-model",
            context_window=16384,
            speed=0.8,
            accuracy=0.85,
            reasoning_depth=0.7,
            input_cost=0.0,
            output_cost=0.0,
            task_scores={TaskType.CODE_GENERATION: 0.9}
        )

        requirements = TaskRequirements(
            task_type=TaskType.CODE_GENERATION,
            min_context_window=8192
        )

        score = model_scorer.score(model, requirements)
        assert 0 <= score <= 1
        assert score > 0  # Should have non-zero score

    def test_context_window_disqualification(self, model_scorer):
        """Test that insufficient context window disqualifies model"""
        model = ModelCapabilities(
            provider=ModelProvider.LOCAL,
            model_id="test-model",
            context_window=4096,
            speed=0.8,
            accuracy=0.85,
        )

        requirements = TaskRequirements(
            task_type=TaskType.CODE_GENERATION,
            min_context_window=8192  # More than model has
        )

        score = model_scorer.score(model, requirements)
        assert score == 0.0

    def test_vision_requirement_disqualification(self, model_scorer):
        """Test that missing vision support disqualifies model"""
        model = ModelCapabilities(
            provider=ModelProvider.LOCAL,
            model_id="test-model",
            context_window=16384,
            supports_vision=False,
        )

        requirements = TaskRequirements(
            task_type=TaskType.VISION,
            requires_vision=True
        )

        score = model_scorer.score(model, requirements)
        assert score == 0.0

    def test_provider_preference_bonus(self, model_scorer):
        """Test that preferred providers get bonus"""
        model = ModelCapabilities(
            provider=ModelProvider.LOCAL,
            model_id="test-model",
            context_window=16384,
            speed=0.8,
            accuracy=0.85,
            task_scores={TaskType.CODE_GENERATION: 0.8}
        )

        # Without preference
        req1 = TaskRequirements(
            task_type=TaskType.CODE_GENERATION,
            min_context_window=8192
        )
        score1 = model_scorer.score(model, req1)

        # With preference
        req2 = TaskRequirements(
            task_type=TaskType.CODE_GENERATION,
            min_context_window=8192,
            preferred_providers=[ModelProvider.LOCAL]
        )
        score2 = model_scorer.score(model, req2)

        assert score2 > score1

    def test_cost_efficiency_factor(self, model_scorer):
        """Test that cost affects score"""
        cheap_model = ModelCapabilities(
            provider=ModelProvider.LOCAL,
            model_id="cheap-model",
            context_window=16384,
            speed=0.8,
            accuracy=0.85,
            input_cost=0.0,
            output_cost=0.0,
            task_scores={TaskType.CODE_GENERATION: 0.8}
        )

        expensive_model = ModelCapabilities(
            provider=ModelProvider.OPENAI,
            model_id="expensive-model",
            context_window=16384,
            speed=0.8,
            accuracy=0.85,
            input_cost=50.0,
            output_cost=150.0,
            task_scores={TaskType.CODE_GENERATION: 0.8}
        )

        requirements = TaskRequirements(
            task_type=TaskType.CODE_GENERATION,
            min_context_window=8192
        )

        cheap_score = model_scorer.score(cheap_model, requirements)
        expensive_score = model_scorer.score(expensive_model, requirements)

        # Cheaper model should score higher (all else being equal)
        assert cheap_score > expensive_score


# ============================================================================
# Model Selection Tests
# ============================================================================

class TestModelSelection:
    """Test model selection logic"""

    def test_basic_model_selection(self, orchestrator):
        """Test basic model selection"""
        model_id, model = orchestrator.select_model("Write a Python function")
        assert model_id is not None
        assert model is not None
        assert isinstance(model, ModelCapabilities)

    def test_guide_integration(self, orchestrator, mock_guide):
        """Test that guide recommendations are used"""
        mock_guide.get_recommended_models.return_value = ["codellama:34b"]

        model_id, model = orchestrator.select_model(
            "Write code",
            use_guide=True
        )

        assert model_id == "codellama:34b"
        mock_guide.get_recommended_models.assert_called_once()

    def test_guide_disabled(self, orchestrator, mock_guide):
        """Test selection with guide disabled"""
        model_id, model = orchestrator.select_model(
            "Write code",
            use_guide=False
        )

        assert model_id is not None
        # Guide should not be called
        mock_guide.get_recommended_models.assert_not_called()

    def test_cost_optimize_strategy(self, orchestrator):
        """Test cost optimization strategy"""
        model_id, model = orchestrator.select_model(
            "Translate this text",
            strategy="cost_optimize",
            use_guide=False
        )

        # Should prefer cheaper models
        assert model.input_cost + model.output_cost < 10

    def test_quality_first_strategy(self, orchestrator):
        """Test quality first strategy"""
        model_id, model = orchestrator.select_model(
            "Analyze this complex problem",
            strategy="quality_first",
            use_guide=False
        )

        # Should prefer high accuracy models
        assert model.accuracy >= 0.8

    def test_speed_priority_strategy(self, orchestrator):
        """Test speed priority strategy"""
        model_id, model = orchestrator.select_model(
            "Quick answer needed",
            strategy="speed_priority",
            use_guide=False
        )

        # Should prefer fast models
        assert model.speed >= 0.7

    def test_blocked_model_filtering(self, orchestrator, mock_guide):
        """Test that blocked models are filtered out"""
        mock_guide.get_recommended_models.return_value = ["blocked-model"]
        mock_guide.is_model_blocked.return_value = True

        # Should fall back to scoring system
        model_id, model = orchestrator.select_model(
            "Write code",
            use_guide=True
        )

        assert model_id != "blocked-model"


# ============================================================================
# Cost Tracking Tests
# ============================================================================

class TestCostTracking:
    """Test cost tracking functionality"""

    def test_cost_estimation(self, orchestrator):
        """Test cost estimation for a model"""
        cost = orchestrator.estimate_cost("codellama:34b", 1000, 500)
        # Local model should be free
        assert cost == 0.0

    def test_usage_tracking(self, orchestrator):
        """Test that usage is tracked correctly"""
        orchestrator.track_usage(
            model_id="codellama:34b",
            input_tokens=1000,
            output_tokens=500,
            latency_ms=250,
            success=True
        )

        assert "codellama:34b" in orchestrator.cost_tracker
        assert len(orchestrator.performance_history) == 1

        entry = orchestrator.performance_history[0]
        assert entry["model_id"] == "codellama:34b"
        assert entry["input_tokens"] == 1000
        assert entry["output_tokens"] == 500
        assert entry["latency_ms"] == 250
        assert entry["success"] is True

    def test_cost_report_generation(self, orchestrator):
        """Test cost report generation"""
        # Track some usage
        orchestrator.track_usage("codellama:34b", 1000, 500, 250)
        orchestrator.track_usage("magicoder:7b", 2000, 1000, 150)

        report = orchestrator.get_cost_report()

        assert "total_cost" in report
        assert "by_model" in report
        assert "by_provider" in report
        assert "usage_count" in report

        assert report["total_cost"] >= 0
        assert "codellama:34b" in report["by_model"]
        assert "local" in report["by_provider"]
        assert report["usage_count"]["codellama:34b"] == 1

    def test_performance_history_limit(self, orchestrator):
        """Test that performance history is limited to 1000 entries"""
        # Add 1100 entries for a model that exists
        for i in range(1100):
            orchestrator.track_usage(
                model_id="codellama:34b",  # Use a valid model
                input_tokens=100,
                output_tokens=50,
                latency_ms=200
            )

        # Should only keep last 1000
        assert len(orchestrator.performance_history) == 1000


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error handling"""

    def test_invalid_model_id(self, orchestrator):
        """Test handling of invalid model ID"""
        with pytest.raises(ValueError, match="Unknown model"):
            asyncio.run(orchestrator.call_model(
                model_id="nonexistent-model",
                messages="test"
            ))

    def test_missing_api_client(self, orchestrator):
        """Test handling of missing API client"""
        # Remove all API clients
        orchestrator.api_clients = {}

        with pytest.raises(ValueError, match="No API client"):
            asyncio.run(orchestrator.call_model(
                model_id="codellama:34b",
                messages="test"
            ))

    def test_no_suitable_models(self, orchestrator):
        """Test error when no models are suitable"""
        # Mark all models as unavailable
        for model in orchestrator.registry.models.values():
            model.available = False

        with pytest.raises(ValueError, match="No suitable models"):
            orchestrator.select_model("test prompt", use_guide=False)


# ============================================================================
# Consensus Group Tests
# ============================================================================

class TestConsensusGroup:
    """Test consensus group creation"""

    def test_consensus_group_creation(self, orchestrator):
        """Test creating a consensus group"""
        group = orchestrator.create_consensus_group(
            prompt="What is 2+2?",
            num_models=3,
            diverse=True
        )

        assert len(group) <= 3
        assert all(isinstance(item, tuple) for item in group)
        assert all(isinstance(item[1], ModelCapabilities) for item in group)

    def test_consensus_diversity(self, orchestrator):
        """Test that consensus groups have diverse providers"""
        group = orchestrator.create_consensus_group(
            prompt="Test prompt",
            num_models=3,
            diverse=True
        )

        providers = [model.provider for _, model in group]
        # Should have some diversity (at least 2 different providers if available)
        assert len(set(providers)) >= min(2, len(group))

    def test_consensus_non_diverse(self, orchestrator):
        """Test non-diverse consensus selection"""
        group = orchestrator.create_consensus_group(
            prompt="Test prompt",
            num_models=3,
            diverse=False
        )

        assert len(group) <= 3
        # Just checks it returns valid group


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for full workflows"""

    def test_end_to_end_selection_and_tracking(self, orchestrator):
        """Test complete workflow: select, track, report"""
        # Select model
        model_id, model = orchestrator.select_model("Write Python code")

        # Track usage
        orchestrator.track_usage(
            model_id=model_id,
            input_tokens=1000,
            output_tokens=500,
            latency_ms=250
        )

        # Generate report
        report = orchestrator.get_cost_report()

        assert report["total_cost"] >= 0
        assert model_id in report["by_model"]
        assert report["usage_count"][model_id] == 1

    def test_multiple_selections_same_task(self, orchestrator):
        """Test that same task type gets consistent selection"""
        model1_id, _ = orchestrator.select_model("Write code in Python", use_guide=False)
        model2_id, _ = orchestrator.select_model("Write code in Java", use_guide=False)

        # Both should be code-specialized models
        model1 = orchestrator.registry.get_model(model1_id)
        model2 = orchestrator.registry.get_model(model2_id)

        # Should have high code generation scores
        assert model1.task_scores.get(TaskType.CODE_GENERATION, 0) > 0.7
        assert model2.task_scores.get(TaskType.CODE_GENERATION, 0) > 0.7


# ============================================================================
# Guide Parser Tests
# ============================================================================

class TestModelGuideParser:
    """Test ModelGuideParser functionality"""

    def test_guide_parser_initialization(self):
        """Test guide parser initialization"""
        parser = ModelGuideParser()
        assert parser.rules is not None
        assert isinstance(parser.rules, dict)

    def test_default_rules_when_file_missing(self, tmp_path):
        """Test fallback to default rules when file is missing"""
        nonexistent_path = tmp_path / "nonexistent.md"
        parser = ModelGuideParser(str(nonexistent_path))

        # Should have default rules
        assert "task_mappings" in parser.rules
        assert "code_generation" in parser.rules["task_mappings"]

    def test_get_recommended_models(self):
        """Test getting recommended models"""
        parser = ModelGuideParser()
        models = parser.get_recommended_models("code_generation")

        assert isinstance(models, list)

    def test_is_model_blocked(self):
        """Test blocked model checking"""
        parser = ModelGuideParser()

        # Test with default blocked model
        result = parser.is_model_blocked("llama3.2")
        assert isinstance(result, bool)


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=model_orchestrator_consolidated", "--cov-report=term-missing"])
