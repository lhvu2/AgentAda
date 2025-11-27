`cd .../agentdata`
`pip install -e .`
`python -c "import agentada, inspect; print(agentada, getattr(agentada, '__file__', None))"`

**Expected output:**
```
<module 'agentada' from '/data/lhvu/projects/AgentAda/src/__init__.py'> /data/lhvu/projects/AgentAda/src/__init__.py
```