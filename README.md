---
title: Incident Triage Environment
emoji: 🚨
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# AI-Powered Incident Triage & Escalation System

A real-world OpenEnv environment where an AI agent learns to classify and route IT incidents efficiently.

## Overview

This environment simulates an IT incident management system where an agent must:
- Analyze incident tickets
- Classify severity (low, medium, high, critical)
- Assign priority (p1, p2, p3)
- Route to correct team (database, network, support)
- Decide escalation

## Features

- **3 Progressive Tasks**: Easy → Medium → Hard
- **Reward Function**: Partial rewards with penalization
- **OpenEnv API**: Standard reset/step/state interface
- **Docker Ready**: Production-ready deployment
- **Hugging Face Integration**: Deployed on HF Spaces

## Installation

```bash
pip install -r requirements.txt
```

## 🌐 Web Dashboards

**Easy-to-use interactive interfaces:**

### Streamlit Dashboard (Recommended)
```bash
pip install streamlit
streamlit run app.py
```
Opens at: http://localhost:8501

Features:
- 🎮 Interactive incident triage gameplay
- 📊 Real-time statistics
- 📈 Episode history tracking
- 🎯 Live feedback on decisions

### HTML Dashboard
Simply open `dashboard.html` in your browser! No dependencies needed.

For full details, see [DASHBOARD.md](DASHBOARD.md)

## Project Structure

```
.
├── server/                 # FastAPI server
├── tasks/                  # Task definitions and graders
├── tests/                  # Unit tests
├── models.py              # Environment models
├── client.py              # OpenEnv client
├── inference.py           # Inference script
├── app.py                 # Streamlit dashboard
├── dashboard.html         # HTML dashboard
├── openenv.yaml           # Configuration
├── Dockerfile             # Docker setup
└── README.md              # This file
```

## Quick Start

### 🌐 Web Dashboards

**Interactive UI to test the environment:**

1. **Streamlit Dashboard** (Recommended)
   ```bash
   pip install streamlit
   streamlit run app.py
   ```
   Opens at: http://localhost:8501

2. **HTML Dashboard** (No dependencies)
   - Simply open `dashboard.html` in your browser
   - Or serve: `python -m http.server 8000`

### 🔧 API Access

## Tasks

### Task 1: Severity Classification (Easy)
Classify incident severity correctly (low, medium, high, critical)
- Reward: 0.3 per correct classification

### Task 2: Severity + Routing (Medium)
Classify severity AND route to correct team
- Reward: 0.3 for severity + 0.3 for routing

### Task 3: Full Pipeline (Hard)
Complete severity, team, priority, and escalation decisions
- Reward: 0.3 + 0.3 + 0.2 + 0.2 (all components)

## API Reference

### Reset

```bash
curl -X POST http://localhost:7860/reset
```

Response:
```json
{
  "observation": {
    "incident_text": "...",
    "history": "...",
    "step_count": 0
  },
  "task_id": "task_easy"
}
```

### Step

```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "severity": "high",
      "team": "database",
      "priority": "p1",
      "escalate": true
    }
  }'
```

Response:
```json
{
  "observation": {...},
  "reward": 0.8,
  "done": false,
  "info": {}
}
```

## Contributing

This is a hackathon submission. For issues or improvements, please create a pull request.

## License

MIT
