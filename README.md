# Hyatt Comfort Concierge

A runnable Streamlit prototype demonstrating an agentic hotel comfort workflow.

## What it demonstrates

- Natural-language requests for towels, sheets, blankets, and pillow types
- Hotel inventory checks
- Housekeeping task creation and verification
- Explicit in-stay comfort preference capture
- Contextual discovery of other hotel services
- A commerce handoff for pillows and blankets guests want to take home
- Failure/evaluation probes inspired by model-evaluation work

## Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The current prototype deliberately uses deterministic intent parsing so it runs without an API key. The tool boundaries are designed so the intent layer can later be replaced with an LLM tool-calling loop.

## Interview demo

1. Ask: `We have two kids and are using the pool. Can we get six pool towels?`
2. Ask for additional comfort items, such as two soft pillows and a cozy blanket.
3. Tell the agent you love the pillows and ask whether you can buy them.
4. Use the evaluation probes to discuss edge cases, verification, guardrails, and how the same agent pattern could expand to broader Hyatt guest workflows.
