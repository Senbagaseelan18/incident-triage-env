"""
Inference script for Incident Triage Environment
Demonstrates an AI agent running through the environment

Usage:
    python inference.py --task task_easy
    python inference.py --task task_medium
    python inference.py --task task_hard
"""
import sys
import argparse
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime

# Local imports
from environment import IncidentTriageEnvironment
from models import Action, SeverityLevel, Team, Priority


class IncidentTriageAgent:
    """AI Agent for Incident Triage using OpenAI"""

    def __init__(self, model: str = "gpt-4"):
        """Initialize agent with OpenAI model"""
        self.model = model
        try:
            import openai
            # Note: In a real scenario, API key would be loaded from .env
            self.openai_client = openai  
            self.use_ai = False  # Set to False if no API key available
        except ImportError:
            self.use_ai = False
            print("[WARNING] OpenAI not available, using rule-based agent")

    def decide(self, incident_text: str, service_affected: str) -> Action:
        """
        Decide on triage action using AI or rules

        Args:
            incident_text: Description of the incident
            service_affected: Service affected

        Returns:
            Action with severity, team, priority, escalate
        """
        if self.use_ai:
            return self._decide_with_ai(incident_text, service_affected)
        else:
            return self._decide_with_rules(incident_text, service_affected)

    def _decide_with_ai(self, incident_text: str, service_affected: str) -> Action:
        """Use OpenAI to make decision"""
        # Placeholder for real OpenAI integration
        return self._decide_with_rules(incident_text, service_affected)

    def _decide_with_rules(
        self, incident_text: str, service_affected: str
    ) -> Action:
        """Rule-based decision logic (fallback)"""
        text_lower = incident_text.lower()

        # Severity detection
        if any(
            word in text_lower
            for word in ["critical", "down", "crash", "5000+", "all users"]
        ):
            severity = SeverityLevel.CRITICAL
        elif any(
            word in text_lower
            for word in ["high", "spike", "error", "failing", "latency"]
        ):
            severity = SeverityLevel.HIGH
        elif any(
            word in text_lower
            for word in ["slow", "intermittent", "performance", "10x"]
        ):
            severity = SeverityLevel.MEDIUM
        else:
            severity = SeverityLevel.LOW

        # Team routing based on service
        if any(
            word in text_lower or word in service_affected.lower()
            for word in ["database", "db", "query", "postgres", "mysql", "sql"]
        ):
            team = Team.DATABASE
        elif any(
            word in text_lower or word in service_affected.lower()
            for word in ["network", "latency", "bandwidth", "connectivity", "data center"]
        ):
            team = Team.NETWORK
        else:
            team = Team.SUPPORT

        # Priority based on severity
        if severity == SeverityLevel.CRITICAL:
            priority = Priority.P1
        elif severity == SeverityLevel.HIGH:
            priority = Priority.P1
        elif severity == SeverityLevel.MEDIUM:
            priority = Priority.P2
        else:
            priority = Priority.P3

        # Escalation for critical/high
        escalate = severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]

        return Action(
            severity=severity,
            team=team,
            priority=priority,
            escalate=escalate,
        )


def run_inference(task_id: str = "task_easy", num_episodes: int = 3):
    """
    Run inference across multiple episodes

    Args:
        task_id: Task to run
        num_episodes: Number of episodes to run
    """
    env = IncidentTriageEnvironment()
    agent = IncidentTriageAgent()

    total_reward = 0.0
    total_steps = 0
    successful_episodes = 0
    all_rewards = []

    # Run episodes
    for episode_num in range(num_episodes):
        # Reset environment
        reset_response = env.reset(task_id=task_id)
        obs = reset_response.observation
        episode_id = reset_response.episode_id

        # Print START marker
        print(
            f"[START] task={task_id} env=incident-triage model=gpt-4 "
            f"episode={episode_num + 1}/{num_episodes}"
        )

        step_count = 0
        episode_reward = 0.0
        error_msg = None

        try:
            # Get initial observation
            incident_text = obs.incident_text
            service_affected = obs.service_affected

            # Agent decides
            action = agent.decide(incident_text, service_affected)

            # Execute step
            step_response = env.step(action)
            reward = step_response.reward
            done = step_response.done
            grader_info = step_response.info.get("grader_result", {})

            step_count += 1
            episode_reward += reward
            total_reward += reward
            total_steps += step_count
            all_rewards.append(reward)

            # Print STEP marker (exact format required)
            action_str = json.dumps(
                {
                    "severity": action.severity.value,
                    "team": action.team.value,
                    "priority": action.priority.value,
                    "escalate": action.escalate,
                }
            )
            print(
                f"[STEP] step={step_count} action={action_str} "
                f"reward={reward:.2f} done={str(done).lower()} error=null"
            )

            if done:
                successful_episodes += 1

        except Exception as e:
            error_msg = str(e)
            print(f"[STEP] step={step_count} action=null reward=0.00 done=true error={error_msg}")

        # Print END marker (exact format required)
        success = error_msg is None
        avg_reward = episode_reward / max(step_count, 1)
        print(
            f"[END] success={str(success).lower()} steps={step_count} "
            f"score={episode_reward:.2f} rewards=[{', '.join(f'{r:.2f}' for r in all_rewards[-step_count:])}]"
        )
        print()

    # Print final summary
    print("=" * 80)
    print("INFERENCE SUMMARY")
    print("=" * 80)
    print(f"Task:                {task_id}")
    print(f"Episodes:            {num_episodes}")
    print(f"Successful:          {successful_episodes}/{num_episodes}")
    print(f"Total Reward:        {total_reward:.2f}")
    print(f"Mean Reward:         {total_reward / num_episodes:.2f}")
    print(f"Max Reward:          {max(all_rewards):.2f}")
    print(f"Min Reward:          {min(all_rewards):.2f}")
    print(f"Total Steps:         {total_steps}")
    print(f"Avg Steps/Episode:   {total_steps / num_episodes:.1f}")
    print("=" * 80)

    return {
        "success": successful_episodes == num_episodes,
        "episodes": num_episodes,
        "successful": successful_episodes,
        "total_reward": total_reward,
        "avg_reward": total_reward / num_episodes,
        "all_rewards": all_rewards,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run inference on Incident Triage Environment"
    )
    parser.add_argument(
        "--task",
        type=str,
        default="task_easy",
        choices=["task_easy", "task_medium", "task_hard"],
        help="Task to run",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=3,
        help="Number of episodes to run",
    )

    args = parser.parse_args()

    print(f"Starting inference at {datetime.now().isoformat()}")
    print()

    result = run_inference(task_id=args.task, num_episodes=args.episodes)

    sys.exit(0 if result["success"] else 1)
