"""
Data models for the Incident Triage Environment
"""
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    """Incident severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Team(str, Enum):
    """Support teams"""
    DATABASE = "database"
    NETWORK = "network"
    SUPPORT = "support"


class Priority(str, Enum):
    """Ticket priority levels"""
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"


class Observation(BaseModel):
    """Environment observation returned to agent"""
    incident_id: str = Field(..., description="Unique incident identifier")
    incident_text: str = Field(..., description="Full incident description")
    timestamp: str = Field(..., description="Incident timestamp")
    customer_name: Optional[str] = Field(None, description="Customer name")
    service_affected: str = Field(..., description="Service or system affected")
    step_count: int = Field(default=0, description="Current step count")
    history: str = Field(default="", description="Previous actions history")


class Action(BaseModel):
    """Agent action for triage decision"""
    severity: SeverityLevel = Field(..., description="Classified severity level")
    team: Team = Field(..., description="Assigned support team")
    priority: Priority = Field(..., description="Assigned priority")
    escalate: bool = Field(default=False, description="Whether to escalate further")


class IncidentInfo(BaseModel):
    """Ground truth incident information"""
    incident_id: str
    incident_text: str
    true_severity: SeverityLevel
    true_team: Team
    true_priority: Priority
    should_escalate: bool
    timestamp: str
    customer_name: Optional[str] = None
    service_affected: str = ""


class StepResponse(BaseModel):
    """Response from environment step"""
    observation: Observation
    reward: float = Field(..., ge=0.0, le=1.0, description="Reward in [0, 1]")
    done: bool = Field(..., description="Whether episode is done")
    info: Dict[str, Any] = Field(default_factory=dict, description="Additional info")


class ResetResponse(BaseModel):
    """Response from environment reset"""
    observation: Observation
    task_id: str = Field(..., description="Task identifier")
    episode_id: str = Field(..., description="Episode identifier")


class GraderResult(BaseModel):
    """Result from task grader"""
    severity_correct: bool
    team_correct: bool
    priority_correct: bool
    escalation_correct: bool
    score: float = Field(..., ge=0.0, le=1.0)


class TaskConfig(BaseModel):
    """Configuration for a task"""
    task_id: str
    name: str
    description: str
    difficulty: str
    requires_severity: bool = True
    requires_team: bool = True
    requires_priority: bool = True
    requires_escalation: bool = True
