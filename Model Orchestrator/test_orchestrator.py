#!/usr/bin/env python3
"""Test script for model orchestrator"""

import sys
import os

# Test imports
print('Testing imports...')
from model_orchestrator import ModelOrchestrator, TaskType, ModelCapabilities, TaskRequirements
print('✓ Imports successful')

# Test basic initialization
print('\nTesting orchestrator initialization...')
orchestrator = ModelOrchestrator()
print('✓ Orchestrator initialized')

# Test model loading
print(f'\nModel inventory:')
print(f'✓ Loaded {len(orchestrator.models)} models')

# Test task type enum
print('\nTesting task types...')
task_types = [TaskType.CODE_GENERATION, TaskType.REASONING, TaskType.ANALYSIS]
for tt in task_types:
    print(f'  ✓ {tt.value}')

# Test model guide parser if available
if orchestrator.guide:
    print('\n✓ MODELS.md guidance loaded')
else:
    print('\nℹ MODELS.md guidance not loaded (optional)')

print('\n=== All core tests passed ===')
