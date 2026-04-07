#!/bin/bash
# Validation script for submission

if [ -z "$1" ]; then
    echo "Usage: ./validate-submission.sh <space-url>"
    echo "Example: ./validate-submission.sh https://your-username-incident-triage-env.hf.space"
    exit 1
fi

SPACE_URL=$1
CHECKS_PASSED=0
CHECKS_TOTAL=3

echo "🧪 Validating Incident Triage Environment"
echo "==========================================="
echo ""

# Check 1: Health endpoint
echo "Check 1/3: Health endpoint..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$SPACE_URL/health")
if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ Health check passed"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "❌ Health check failed (HTTP $HEALTH_RESPONSE)"
fi
echo ""

# Check 2: Reset endpoint
echo "Check 2/3: Reset endpoint..."
RESET_RESPONSE=$(curl -s -X POST "$SPACE_URL/reset" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_easy"}')

if echo "$RESET_RESPONSE" | grep -q "observation\|episode_id"; then
    echo "✅ Reset endpoint works"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "❌ Reset endpoint failed"
    echo "Response: $RESET_RESPONSE"
fi
echo ""

# Check 3: Step endpoint
echo "Check 3/3: Step endpoint..."
STEP_RESPONSE=$(curl -s -X POST "$SPACE_URL/step" \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "severity": "high",
      "team": "database",
      "priority": "p1",
      "escalate": true
    }
  }')

if echo "$STEP_RESPONSE" | grep -q "reward\|done"; then
    echo "✅ Step endpoint works"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "❌ Step endpoint failed"
    echo "Response: $STEP_RESPONSE"
fi
echo ""

# Summary
echo "==========================================="
echo "Results: $CHECKS_PASSED/$CHECKS_TOTAL checks passed!"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo "✅ All checks passed!"
    exit 0
else
    echo "❌ Some checks failed"
    exit 1
fi
