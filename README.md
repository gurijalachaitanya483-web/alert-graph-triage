# Alert Graph Triage

A small infrastructure alert triage demo based on the resume's graph analysis theme. It groups simultaneous alerts by dependency connection and ranks likely upstream services. The sample topology and alerts are invented; no employer infrastructure is included.

## Run

```bash
python app.py
python -m unittest discover -s tests
```

## Method

An undirected Union-Find graph groups related alerts into incidents. Directed dependency edges then rank each alerted service by how many other alerted services depend on it transitively. The output is a triage hint, not causal proof. Everything uses Python's standard library.

## Resume description

Implemented an infrastructure alert grouping and root-cause triage demo using Union-Find and directed dependency traversal in Python.
