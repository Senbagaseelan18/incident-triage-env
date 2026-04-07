#!/bin/bash
# Deployment script for Hugging Face Spaces

HF_REPO_ID=${HF_REPO_ID:-"your-username/incident-triage-env"}
SPACE_NAME="incident-triage-env"

echo "🚀 Deploying to Hugging Face Spaces"
echo "Repo: $HF_REPO_ID"

# Check if huggingface-cli is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "❌ huggingface-cli not found. Install with: pip install huggingface_hub"
    exit 1
fi

# Create model card
cat > ./SPACE_README.md <<EOF
# Incident Triage Environment

An OpenEnv environment for AI-powered incident triage and escalation.

## Usage

### API Endpoints

- **POST /reset** - Reset environment
- **POST /step** - Execute action
- **GET /health** - Health check
- **GET /tasks** - List tasks

### Example Request

\`\`\`bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_easy"}'
\`\`\`

## Tasks

1. **Easy** - Severity classification
2. **Medium** - Severity + routing
3. **Hard** - Full pipeline

## About OpenEnv

OpenEnv is an open-source RL framework by Meta and Hugging Face.
Learn more: https://github.com/facebookresearch/openenv
EOF

echo "✅ Created SPACE_README.md"

# Deploy to HF
echo "📤 Deploying to Hugging Face..."
huggingface-cli repo create $HF_REPO_ID --type space --space-sdk docker --private false --exist-ok

# Push to repo
git remote add huggingface https://huggingface.co/spaces/$HF_REPO_ID.git 2>/dev/null || git remote set-url huggingface https://huggingface.co/spaces/$HF_REPO_ID.git

git push huggingface main -f

echo "✅ Deployment complete!"
echo "Space URL: https://huggingface.co/spaces/$HF_REPO_ID"
