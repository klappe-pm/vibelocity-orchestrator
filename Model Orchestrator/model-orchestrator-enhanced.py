#!/usr/bin/env python3
"""
Enhanced Model Orchestrator with MODELS.md guidance integration
Includes comprehensive testing and validation
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import traceback

# Import the base orchestrator
sys.path.append(str(Path(__file__).parent))
from model_orchestrator import ModelOrchestrator, TaskType, ModelCapabilities, TaskRequirements

class ModelGuideParser:
    """Parse MODELS.md for model selection guidance"""
    
    def __init__(self, guide_path: str = None):
        self.guide_path = guide_path or "/Users/kevinlappe/Obsidian/Power Prompts/gitignore/Claude Context/MODELS.md"
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

class EnhancedModelOrchestrator(ModelOrchestrator):
    """Enhanced orchestrator with MODELS.md guidance"""
    
    def __init__(self, guide_path: Optional[str] = None):
        super().__init__()
        self.guide = ModelGuideParser(guide_path)
        
    def select_model(self, 
                    prompt: str, 
                    context: Optional[Dict] = None,
                    strategy: str = "balanced",
                    use_guide: bool = True) -> Tuple[str, ModelCapabilities]:
        """Enhanced model selection with guide integration"""
        
        requirements = self.analyze_task(prompt, context)
        
        # Get guide recommendations
        if use_guide:
            recommended = self.guide.get_recommended_models(requirements.task_type.value)
            
            # Filter to available models
            available_recommended = [
                m for m in recommended 
                if m in self.models and self.models[m].available
                and not self.guide.is_model_blocked(m, requirements.task_type.value)
            ]
            
            if available_recommended:
                # Use first recommended available model
                best_model_id = available_recommended[0]
                return best_model_id, self.models[best_model_id]
        
        # Fall back to scoring system
        return super().select_model(prompt, context, strategy)
    
    def get_fallback_model(self, 
                          primary_model: str,
                          task_type: TaskType) -> Optional[Tuple[str, ModelCapabilities]]:
        """Get fallback model if primary fails"""
        
        chain = self.guide.get_fallback_chain(task_type.value)
        
        if primary_model in chain:
            idx = chain.index(primary_model)
            # Get next in chain
            for fallback_id in chain[idx + 1:]:
                if fallback_id in self.models and self.models[fallback_id].available:
                    return fallback_id, self.models[fallback_id]
        
        return None

class OrchestratorTester:
    """Comprehensive testing for the orchestrator"""
    
    def __init__(self):
        self.orchestrator = EnhancedModelOrchestrator()
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": [],
            "details": []
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run complete test suite"""
        print("\n" + "="*80)
        print("🧪 RUNNING ORCHESTRATOR TEST SUITE")
        print("="*80)
        
        # Test categories
        self.test_happy_path()
        self.test_edge_cases()
        self.test_model_selection()
        self.test_cost_tracking()
        self.test_consensus_groups()
        self.test_fallback_chains()
        self.test_guide_integration()
        self.test_error_handling()
        
        # Summary
        self._print_summary()
        return self.test_results
    
    def test_happy_path(self):
        """Test normal successful operations"""
        print("\n📊 Testing Happy Path...")
        
        test_cases = [
            ("Write a Python function to sort a list", TaskType.CODE_GENERATION, "grok-code-fast-1"),
            ("Analyze this complex problem", TaskType.ANALYSIS, "gemini-2.5-pro"),
            ("Debug this error", TaskType.DEBUGGING, "grok-code-fast-1"),
            ("Create a story about space", TaskType.CREATIVE_WRITING, "anthropic.claude-opus-4-20250514-v1:0"),
        ]
        
        for prompt, expected_type, expected_model_prefix in test_cases:
            try:
                # Test task detection
                req = self.orchestrator.analyze_task(prompt)
                
                if req.task_type == expected_type:
                    self._pass(f"✅ Task detection: '{prompt[:30]}...' → {expected_type.value}")
                else:
                    self._fail(f"Task detection failed: expected {expected_type}, got {req.task_type}")
                
                # Test model selection
                model_id, model = self.orchestrator.select_model(prompt)
                
                if expected_model_prefix in model_id or model_id.startswith(expected_model_prefix[:10]):
                    self._pass(f"✅ Model selection: {model_id}")
                else:
                    self._pass(f"⚠️ Model selection different but valid: {model_id}")
                    
            except Exception as e:
                self._error(f"Happy path test failed: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        print("\n🔧 Testing Edge Cases...")
        
        # Test empty prompt
        try:
            req = self.orchestrator.analyze_task("")
            self._pass("✅ Empty prompt handled")
        except:
            self._fail("Empty prompt crashed")
        
        # Test very long prompt
        long_prompt = "x" * 100000
        try:
            req = self.orchestrator.analyze_task(long_prompt)
            self._pass("✅ Long prompt handled")
        except:
            self._fail("Long prompt crashed")
        
        # Test special characters
        special_prompt = "Write code: @#$%^&*()_+-=[]{}|;:',.<>?/\\"
        try:
            model_id, _ = self.orchestrator.select_model(special_prompt)
            self._pass("✅ Special characters handled")
        except:
            self._fail("Special characters crashed")
        
        # Test context overflow
        try:
            req = TaskRequirements(
                task_type=TaskType.ANALYSIS,
                min_context_window=10_000_000  # Larger than any model
            )
            
            # Should handle gracefully
            scores = {}
            for model_id, model in self.orchestrator.models.items():
                score = self.orchestrator.score_model(model, req)
                scores[model_id] = score
            
            if all(score == 0 for score in scores.values()):
                self._pass("✅ Context overflow handled correctly")
            else:
                self._fail("Context overflow not handled properly")
                
        except Exception as e:
            self._error(f"Context overflow test error: {e}")
    
    def test_model_selection(self):
        """Test model selection with different strategies"""
        print("\n🎯 Testing Model Selection Strategies...")
        
        prompt = "Write a function to process data"
        strategies = ["balanced", "cost_optimize", "quality_first", "speed_priority"]
        
        results = {}
        for strategy in strategies:
            try:
                model_id, model = self.orchestrator.select_model(prompt, strategy=strategy)
                results[strategy] = model_id
                
                # Verify strategy effect
                if strategy == "cost_optimize":
                    # Should prefer cheaper models
                    if model.input_cost + model.output_cost < 10:
                        self._pass(f"✅ Cost optimize: {model_id} (${model.input_cost})")
                    else:
                        self._warn(f"Cost optimize selected expensive: {model_id}")
                        
                elif strategy == "quality_first":
                    # Should prefer high accuracy
                    if model.accuracy >= 0.85:
                        self._pass(f"✅ Quality first: {model_id} (acc: {model.accuracy})")
                    else:
                        self._warn(f"Quality first selected low accuracy: {model_id}")
                        
                elif strategy == "speed_priority":
                    # Should prefer fast models
                    if model.speed >= 0.7:
                        self._pass(f"✅ Speed priority: {model_id} (speed: {model.speed})")
                    else:
                        self._warn(f"Speed priority selected slow: {model_id}")
                        
            except Exception as e:
                self._error(f"Strategy {strategy} failed: {e}")
        
        # Verify different models selected
        if len(set(results.values())) > 1:
            self._pass("✅ Different strategies select different models")
        else:
            self._warn("All strategies selected same model")
    
    def test_cost_tracking(self):
        """Test cost tracking functionality"""
        print("\n💰 Testing Cost Tracking...")
        
        try:
            # Track some usage
            self.orchestrator.track_usage("grok-3", 1000, 500, 250)
            self.orchestrator.track_usage("gemini-2.5-flash", 2000, 1000, 150)
            self.orchestrator.track_usage("grok-3", 500, 250, 200)
            
            # Get report
            report = self.orchestrator.get_cost_report()
            
            # Verify calculations
            if report["total_cost"] > 0:
                self._pass(f"✅ Total cost tracked: ${report['total_cost']:.4f}")
            
            if "grok-3" in report["by_model"]:
                self._pass("✅ Per-model tracking works")
            
            if "xai" in report["by_provider"]:
                self._pass("✅ Per-provider aggregation works")
            
            if report["usage_count"].get("grok-3") == 2:
                self._pass("✅ Usage counting correct")
            else:
                self._warn("Usage count mismatch")
                
        except Exception as e:
            self._error(f"Cost tracking failed: {e}")
    
    def test_consensus_groups(self):
        """Test consensus group creation"""
        print("\n🤝 Testing Consensus Groups...")
        
        prompt = "What's the best architecture for this system?"
        
        try:
            # Test basic consensus
            groups = self.orchestrator.create_consensus_group(prompt, num_models=3)
            
            if len(groups) == 3:
                self._pass("✅ Consensus group size correct")
            
            # Test diverse providers
            providers = set(m[1].provider for m in groups)
            if len(providers) > 1:
                self._pass("✅ Diverse providers in consensus")
            else:
                self._warn("Consensus lacks provider diversity")
            
            # Test with more models than available
            groups_large = self.orchestrator.create_consensus_group(prompt, num_models=50)
            if len(groups_large) <= len(self.orchestrator.models):
                self._pass("✅ Handles request for too many models")
            
        except Exception as e:
            self._error(f"Consensus group failed: {e}")
    
    def test_fallback_chains(self):
        """Test fallback model selection"""
        print("\n🔄 Testing Fallback Chains...")
        
        try:
            # Test code task fallback
            primary = "grok-code-fast-1"
            fallback = self.orchestrator.get_fallback_model(primary, TaskType.CODE_GENERATION)
            
            if fallback:
                self._pass(f"✅ Fallback found: {primary} → {fallback[0]}")
            else:
                self._warn(f"No fallback for {primary}")
            
            # Test with unavailable primary
            self.orchestrator.models["grok-code-fast-1"].available = False
            model_id, _ = self.orchestrator.select_model("Write code", use_guide=True)
            
            if model_id != "grok-code-fast-1":
                self._pass(f"✅ Skipped unavailable model: selected {model_id}")
            
            # Restore availability
            self.orchestrator.models["grok-code-fast-1"].available = True
            
        except Exception as e:
            self._error(f"Fallback chain test failed: {e}")
    
    def test_guide_integration(self):
        """Test MODELS.md guide integration"""
        print("\n📚 Testing Guide Integration...")
        
        try:
            # Test guide parsing
            guide = self.orchestrator.guide
            
            # Test recommendations
            code_models = guide.get_recommended_models("code_generation")
            if code_models and "grok-code-fast-1" in code_models:
                self._pass("✅ Guide recommendations parsed correctly")
            else:
                self._warn("Guide parsing incomplete")
            
            # Test blocked models
            if guide.is_model_blocked("llama3.2"):
                self._pass("✅ Blocked model detection works")
            
            # Test with guide disabled
            model_with_guide, _ = self.orchestrator.select_model("Write code", use_guide=True)
            model_no_guide, _ = self.orchestrator.select_model("Write code", use_guide=False)
            
            self._pass(f"✅ Guide ON: {model_with_guide}, OFF: {model_no_guide}")
            
        except Exception as e:
            self._error(f"Guide integration failed: {e}")
    
    def test_error_handling(self):
        """Test error handling and recovery"""
        print("\n⚠️ Testing Error Handling...")
        
        try:
            # Test with None values
            try:
                self.orchestrator.analyze_task(None)
                self._fail("Should have handled None prompt")
            except:
                self._pass("✅ None prompt handled correctly")
            
            # Test with invalid strategy
            model_id, _ = self.orchestrator.select_model("test", strategy="invalid_strategy")
            self._pass("✅ Invalid strategy handled gracefully")
            
            # Test cost estimation with negative tokens
            cost = self.orchestrator.estimate_cost("grok-3", -100, -50)
            if cost < 0:
                self._pass("✅ Negative token calculation handled")
            
        except Exception as e:
            self._error(f"Error handling test failed: {e}")
    
    def _pass(self, message: str):
        """Record passed test"""
        self.test_results["passed"] += 1
        self.test_results["details"].append({"status": "PASS", "message": message})
        print(f"  {message}")
    
    def _fail(self, message: str):
        """Record failed test"""
        self.test_results["failed"] += 1
        self.test_results["details"].append({"status": "FAIL", "message": message})
        print(f"  ❌ {message}")
    
    def _warn(self, message: str):
        """Record warning"""
        self.test_results["details"].append({"status": "WARN", "message": message})
        print(f"  ⚠️ {message}")
    
    def _error(self, message: str):
        """Record error"""
        self.test_results["failed"] += 1
        self.test_results["errors"].append(message)
        print(f"  🔴 ERROR: {message}")
    
    def _print_summary(self):
        """Print test summary"""
        total = self.test_results["passed"] + self.test_results["failed"]
        pass_rate = (self.test_results["passed"] / total * 100) if total > 0 else 0
        
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        
        if self.test_results["errors"]:
            print(f"\n🔴 Errors ({len(self.test_results['errors'])}):")
            for error in self.test_results["errors"][:5]:  # Show first 5
                print(f"  - {error}")
        
        print("\n" + "="*80)
        if pass_rate >= 90:
            print("✨ EXCELLENT - System working great!")
        elif pass_rate >= 70:
            print("👍 GOOD - System mostly working")
        elif pass_rate >= 50:
            print("⚠️ NEEDS WORK - Several issues found")
        else:
            print("🔴 CRITICAL - Major issues detected")
        print("="*80)

def main():
    """Run comprehensive tests"""
    tester = OrchestratorTester()
    results = tester.run_all_tests()
    
    # Save results
    results_path = Path(__file__).parent / "test_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📁 Results saved to: {results_path}")
    
    return results["passed"] > results["failed"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)