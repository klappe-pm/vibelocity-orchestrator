### Multi-Model Interaction Patterns

#### Chain of Thought
Sequential processing through multiple models:
```python
chain = orchestrator.create_model_chain(tasks)
```

#### Parallel Consensus
Multiple models vote on the answer:
```python
consensus = orchestrator.create_consensus_group(prompt, num_models=3)
```

#### Hierarchical Refinement
Start cheap, refine with better models:
```python
result = await hierarchical_refinement(prompt, refinements)
```

#### Adaptive Analysis
Depth adjusts to complexity:
```python
result = await adaptive_analysis(prompt, depth="auto")
```