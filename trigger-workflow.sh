#!/bin/bash
# Trigger the Daily Dynatrace Health workflow
# Usage: ./trigger-workflow.sh "your_github_token"

if [ -z "$1" ]; then
    echo "❌ Error: GitHub token required"
    echo "Usage: ./trigger-workflow.sh <github_token>"
    echo ""
    echo "To get a token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select scopes: repo (full), workflow"
    echo "4. Copy the token"
    exit 1
fi

TOKEN=$1
OWNER="marcdubrulle-arch"
REPO="dynatrace-daily-health"
WORKFLOW_ID="daily-health.yml"

echo "🚀 Triggering workflow: $WORKFLOW_ID"
echo ""

curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW_ID/dispatches" \
  -d '{"ref":"main"}' \
  2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Workflow triggered successfully!"
    echo ""
    echo "Check status at:"
    echo "  https://github.com/$OWNER/$REPO/actions"
    echo ""
    echo "Waiting for the workflow to start..."
    sleep 5
    
    # Get recent runs
    RUNS=$(curl -s \
      -H "Authorization: token $TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=1")
    
    RUN_ID=$(echo $RUNS | grep -o '"id": [0-9]*' | head -1 | grep -o '[0-9]*')
    if [ ! -z "$RUN_ID" ]; then
        echo "Run ID: $RUN_ID"
        echo "View at: https://github.com/$OWNER/$REPO/actions/runs/$RUN_ID"
    fi
else
    echo "❌ Failed to trigger workflow"
    exit 1
fi
