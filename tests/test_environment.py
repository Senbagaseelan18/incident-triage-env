"""
Unit tests for Incident Triage Environment
"""
import unittest
from models import (
    SeverityLevel, Team, Priority, Observation, Action, 
    IncidentInfo, GraderResult
)
from environment import IncidentTriageEnvironment, SAMPLE_INCIDENTS


class TestModels(unittest.TestCase):
    """Test data models"""

    def test_observation_creation(self):
        """Test Observation model"""
        obs = Observation(
            incident_id="inc-001",
            incident_text="Test incident",
            timestamp="2026-04-07T00:00:00",
            service_affected="Test Service",
        )
        self.assertEqual(obs.incident_id, "inc-001")
        self.assertEqual(obs.step_count, 0)

    def test_action_creation(self):
        """Test Action model"""
        action = Action(
            severity=SeverityLevel.HIGH,
            team=Team.DATABASE,
            priority=Priority.P1,
            escalate=True,
        )
        self.assertEqual(action.severity, SeverityLevel.HIGH)
        self.assertTrue(action.escalate)

    def test_grader_result(self):
        """Test GraderResult model"""
        result = GraderResult(
            severity_correct=True,
            team_correct=False,
            priority_correct=True,
            escalation_correct=True,
            score=0.7,
        )
        self.assertTrue(result.severity_correct)
        self.assertFalse(result.team_correct)
        self.assertEqual(result.score, 0.7)


class TestEnvironment(unittest.TestCase):
    """Test environment logic"""

    def setUp(self):
        """Set up test environment"""
        self.env = IncidentTriageEnvironment()

    def test_reset(self):
        """Test reset returns observation"""
        response = self.env.reset(task_id="task_easy")
        self.assertIsNotNone(response.observation)
        self.assertEqual(response.task_id, "task_easy")
        self.assertTrue(len(response.episode_id) > 0)

    def test_reset_selects_incident(self):
        """Test reset selects random incident"""
        response = self.env.reset()
        self.assertIsNotNone(self.env.current_incident)
        self.assertTrue(len(self.env.current_incident.incident_text) > 0)

    def test_step_requires_reset(self):
        """Test step raises error without reset"""
        action = Action(
            severity=SeverityLevel.HIGH,
            team=Team.DATABASE,
            priority=Priority.P1,
            escalate=True,
        )
        with self.assertRaises(RuntimeError):
            self.env.step(action)

    def test_step_after_reset(self):
        """Test step after reset"""
        self.env.reset(task_id="task_easy")
        
        action = Action(
            severity=SeverityLevel.HIGH,
            team=Team.DATABASE,
            priority=Priority.P1,
            escalate=True,
        )
        
        response = self.env.step(action)
        self.assertIsNotNone(response.observation)
        self.assertTrue(0.0 <= response.reward <= 1.0)
        self.assertTrue(response.done)

    def test_grading_easy_task(self):
        """Test grading for easy task"""
        self.env.reset(task_id="task_easy")
        
        # Correct severity
        action = Action(
            severity=self.env.current_incident.true_severity,
            team=Team.SUPPORT,  # Wrong but ignored in easy task
            priority=Priority.P3,  # Wrong but ignored
            escalate=False,  # Wrong but ignored
        )
        
        response = self.env.step(action)
        # Should get 0.3 for correct severity
        self.assertGreaterEqual(response.reward, 0.25)

    def test_grading_medium_task(self):
        """Test grading for medium task"""
        self.env.reset(task_id="task_medium")
        
        # Correct severity and team
        action = Action(
            severity=self.env.current_incident.true_severity,
            team=self.env.current_incident.true_team,
            priority=Priority.P3,  # Wrong but ignored
            escalate=False,  # Wrong but ignored
        )
        
        response = self.env.step(action)
        # Should get 0.6 for severity (0.3) + team (0.3)
        self.assertGreaterEqual(response.reward, 0.5)

    def test_grading_hard_task(self):
        """Test grading for hard task"""
        self.env.reset(task_id="task_hard")
        
        # Perfect action
        action = Action(
            severity=self.env.current_incident.true_severity,
            team=self.env.current_incident.true_team,
            priority=self.env.current_incident.true_priority,
            escalate=self.env.current_incident.should_escalate,
        )
        
        response = self.env.step(action)
        # Should get perfect score (may have bonus)
        self.assertGreaterEqual(response.reward, 0.9)

    def test_state(self):
        """Test state method"""
        before_reset = self.env.state()
        self.assertEqual(before_reset["status"], "not_initialized")
        
        self.env.reset()
        after_reset = self.env.state()
        self.assertEqual(after_reset["task_id"], "task_easy")
        self.assertGreater(len(after_reset["episode_id"]), 0)

    def test_sample_incidents_structure(self):
        """Test sample incidents have required fields"""
        for incident in SAMPLE_INCIDENTS:
            self.assertIn("incident_text", incident)
            self.assertIn("true_severity", incident)
            self.assertIn("true_team", incident)
            self.assertIn("true_priority", incident)
            self.assertIn("should_escalate", incident)
            self.assertIn("service_affected", incident)


if __name__ == "__main__":
    unittest.main()
