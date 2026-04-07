"""
Task Graders for Incident Triage
"""
from models import Action, IncidentInfo, GraderResult


def grade_task_easy(action: Action, incident: IncidentInfo) -> GraderResult:
    """
    Grade Task 1: Severity Classification
    
    Only checks if severity is correct.
    """
    severity_correct = action.severity == incident.true_severity
    
    score = 0.3 if severity_correct else 0.0
    
    return GraderResult(
        severity_correct=severity_correct,
        team_correct=True,  # Not evaluated in this task
        priority_correct=True,  # Not evaluated in this task
        escalation_correct=True,  # Not evaluated in this task
        score=score,
    )


def grade_task_medium(action: Action, incident: IncidentInfo) -> GraderResult:
    """
    Grade Task 2: Severity & Routing
    
    Checks severity and team assignment.
    """
    severity_correct = action.severity == incident.true_severity
    team_correct = action.team == incident.true_team
    
    score = 0.0
    if severity_correct:
        score += 0.3
    if team_correct:
        score += 0.3
    
    return GraderResult(
        severity_correct=severity_correct,
        team_correct=team_correct,
        priority_correct=True,  # Not evaluated in this task
        escalation_correct=True,  # Not evaluated in this task
        score=score,
    )


def grade_task_hard(action: Action, incident: IncidentInfo) -> GraderResult:
    """
    Grade Task 3: Full Pipeline
    
    Checks severity, team, priority, and escalation.
    """
    severity_correct = action.severity == incident.true_severity
    team_correct = action.team == incident.true_team
    priority_correct = action.priority == incident.true_priority
    escalation_correct = action.escalate == incident.should_escalate
    
    score = 0.0
    if severity_correct:
        score += 0.3
    if team_correct:
        score += 0.3
    if priority_correct:
        score += 0.2
    if escalation_correct:
        score += 0.2
    
    return GraderResult(
        severity_correct=severity_correct,
        team_correct=team_correct,
        priority_correct=priority_correct,
        escalation_correct=escalation_correct,
        score=score,
    )


def get_grader(task_id: str):
    """Get appropriate grader function for task"""
    graders = {
        "task_easy": grade_task_easy,
        "task_medium": grade_task_medium,
        "task_hard": grade_task_hard,
    }
    return graders.get(task_id, grade_task_easy)
