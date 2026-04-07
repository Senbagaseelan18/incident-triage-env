"""
Core OpenEnv Environment Implementation
"""
import uuid
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from models import (
    Observation, Action, IncidentInfo, StepResponse, ResetResponse,
    SeverityLevel, Team, Priority, GraderResult, TaskConfig
)

# Sample incidents for the environment
SAMPLE_INCIDENTS = [
    {
        "incident_text": "Database is down, customers cannot access their accounts. This is impacting 5000+ users.",
        "true_severity": SeverityLevel.CRITICAL,
        "true_team": Team.DATABASE,
        "true_priority": Priority.P1,
        "should_escalate": True,
        "service_affected": "User Portal"
    },
    {
        "incident_text": "Intermittent network connectivity issues in the East Coast data center.",
        "true_severity": SeverityLevel.HIGH,
        "true_team": Team.NETWORK,
        "true_priority": Priority.P1,
        "should_escalate": True,
        "service_affected": "Data Center"
    },
    {
        "incident_text": "Customer unable to reset password through web interface.",
        "true_severity": SeverityLevel.LOW,
        "true_team": Team.SUPPORT,
        "true_priority": Priority.P3,
        "should_escalate": False,
        "service_affected": "Authentication"
    },
    {
        "incident_text": "Slow query performance in reporting database, queries taking 10x longer than baseline.",
        "true_severity": SeverityLevel.MEDIUM,
        "true_team": Team.DATABASE,
        "true_priority": Priority.P2,
        "should_escalate": False,
        "service_affected": "Analytics"
    },
    {
        "incident_text": "Network latency spike affecting multiple services, response times increased by 50%.",
        "true_severity": SeverityLevel.HIGH,
        "true_team": Team.NETWORK,
        "true_priority": Priority.P1,
        "should_escalate": True,
        "service_affected": "All Services"
    },
    {
        "incident_text": "Minor UI bug reported by single user in admin panel.",
        "true_severity": SeverityLevel.LOW,
        "true_team": Team.SUPPORT,
        "true_priority": Priority.P3,
        "should_escalate": False,
        "service_affected": "Admin Portal"
    },
    {
        "incident_text": "API endpoint returning 500 errors intermittently, 10% of requests failing.",
        "true_severity": SeverityLevel.HIGH,
        "true_team": Team.DATABASE,
        "true_priority": Priority.P1,
        "should_escalate": True,
        "service_affected": "API"
    }
]

TASK_CONFIGS = {
    "task_easy": TaskConfig(
        task_id="task_easy",
        name="Severity Classification",
        description="Classify incident severity only",
        difficulty="easy",
        requires_severity=True,
        requires_team=False,
        requires_priority=False,
        requires_escalation=False,
    ),
    "task_medium": TaskConfig(
        task_id="task_medium",
        name="Severity & Routing",
        description="Classify severity and route to team",
        difficulty="medium",
        requires_severity=True,
        requires_team=True,
        requires_priority=False,
        requires_escalation=False,
    ),
    "task_hard": TaskConfig(
        task_id="task_hard",
        name="Full Pipeline",
        description="Complete severity, team, priority, and escalation",
        difficulty="hard",
        requires_severity=True,
        requires_team=True,
        requires_priority=True,
        requires_escalation=True,
    ),
}


class IncidentTriageEnvironment:
    """OpenEnv Environment for Incident Triage & Escalation"""

    def __init__(self):
        self.current_incident: Optional[IncidentInfo] = None
        self.current_task_id: str = "task_easy"
        self.episode_id: str = ""
        self.step_count: int = 0
        self.max_steps: int = 1
        self.episode_history: List[str] = []

    def reset(self, task_id: str = "task_easy") -> ResetResponse:
        """
        Reset environment and return initial observation
        
        Args:
            task_id: Task to run (task_easy, task_medium, task_hard)
            
        Returns:
            ResetResponse with observation and task info
        """
        if task_id not in TASK_CONFIGS:
            task_id = "task_easy"

        self.current_task_id = task_id
        self.episode_id = str(uuid.uuid4())[:8]
        self.step_count = 0
        self.episode_history = []

        # Select random incident
        incident_data = random.choice(SAMPLE_INCIDENTS)
        self.current_incident = IncidentInfo(
            incident_id=str(uuid.uuid4())[:8],
            incident_text=incident_data["incident_text"],
            true_severity=incident_data["true_severity"],
            true_team=incident_data["true_team"],
            true_priority=incident_data["true_priority"],
            should_escalate=incident_data["should_escalate"],
            timestamp=datetime.now().isoformat(),
            service_affected=incident_data["service_affected"],
        )

        observation = Observation(
            incident_id=self.current_incident.incident_id,
            incident_text=self.current_incident.incident_text,
            timestamp=self.current_incident.timestamp,
            service_affected=self.current_incident.service_affected,
            step_count=self.step_count,
            history="Episode started",
        )

        return ResetResponse(
            observation=observation,
            task_id=self.current_task_id,
            episode_id=self.episode_id,
        )

    def step(self, action: Action) -> StepResponse:
        """
        Execute action and return reward
        
        Args:
            action: Agent's triage decision
            
        Returns:
            StepResponse with observation, reward, and done flag
        """
        if self.current_incident is None:
            raise RuntimeError("Environment not reset. Call reset() first.")

        self.step_count += 1

        # Grade the action
        grader_result = self._grade_action(action)
        
        # Calculate reward based on task
        reward = self._calculate_reward(grader_result)

        # Update history
        history_msg = (
            f"Step {self.step_count}: severity={action.severity}, "
            f"team={action.team}, priority={action.priority}, "
            f"escalate={action.escalate}"
        )
        self.episode_history.append(history_msg)

        # Episode ends after 1 step (single decision per incident)
        done = self.step_count >= self.max_steps

        observation = Observation(
            incident_id=self.current_incident.incident_id,
            incident_text=self.current_incident.incident_text,
            timestamp=self.current_incident.timestamp,
            service_affected=self.current_incident.service_affected,
            step_count=self.step_count,
            history="\n".join(self.episode_history),
        )

        info = {
            "grader_result": grader_result.model_dump(),
            "task_id": self.current_task_id,
        }

        return StepResponse(
            observation=observation,
            reward=reward,
            done=done,
            info=info,
        )

    def _grade_action(self, action: Action) -> GraderResult:
        """Grade agent's action against ground truth"""
        task_config = TASK_CONFIGS[self.current_task_id]
        
        severity_correct = (
            action.severity == self.current_incident.true_severity
            if task_config.requires_severity else True
        )
        
        team_correct = (
            action.team == self.current_incident.true_team
            if task_config.requires_team else True
        )
        
        priority_correct = (
            action.priority == self.current_incident.true_priority
            if task_config.requires_priority else True
        )
        
        escalation_correct = (
            action.escalate == self.current_incident.should_escalate
            if task_config.requires_escalation else True
        )

        score = 0.0
        if task_config.requires_severity and severity_correct:
            score += 0.3
        if task_config.requires_team and team_correct:
            score += 0.3
        if task_config.requires_priority and priority_correct:
            score += 0.2
        if task_config.requires_escalation and escalation_correct:
            score += 0.2

        return GraderResult(
            severity_correct=severity_correct,
            team_correct=team_correct,
            priority_correct=priority_correct,
            escalation_correct=escalation_correct,
            score=score,
        )

    def _calculate_reward(self, grader_result: GraderResult) -> float:
        """Calculate reward with bonus/penalty"""
        reward = grader_result.score
        
        # Penalize wrong actions (not full penalty, allows learning)
        task_config = TASK_CONFIGS[self.current_task_id]
        wrong_count = 0
        
        if task_config.requires_severity and not grader_result.severity_correct:
            wrong_count += 1
        if task_config.requires_team and not grader_result.team_correct:
            wrong_count += 1
        if task_config.requires_priority and not grader_result.priority_correct:
            wrong_count += 1
        if task_config.requires_escalation and not grader_result.escalation_correct:
            wrong_count += 1
        
        # Small penalty for each wrong component
        penalty = wrong_count * 0.05
        reward = max(0.0, reward - penalty)
        
        # Bonus for perfect
        if grader_result.score == 1.0:
            reward = min(1.0, reward + 0.1)
        
        return round(reward, 2)

    def state(self) -> Dict:
        """Return current environment state"""
        if self.current_incident is None:
            return {"status": "not_initialized"}
        
        return {
            "episode_id": self.episode_id,
            "task_id": self.current_task_id,
            "incident_id": self.current_incident.incident_id,
            "step_count": self.step_count,
            "history": self.episode_history,
        }
