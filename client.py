"""
OpenEnv Client for Incident Triage Environment
"""
import requests
from typing import Dict, Any, Optional
from models import Action, Observation, StepResponse, ResetResponse


class IncidentTriageClient:
    """Client for interacting with the Incident Triage environment"""

    def __init__(self, base_url: str = "http://localhost:7860"):
        """
        Initialize client
        
        Args:
            base_url: Base URL of the environment server
        """
        self.base_url = base_url.rstrip("/")

    def reset(self, task_id: str = "task_easy") -> ResetResponse:
        """
        Reset environment and get initial observation
        
        Args:
            task_id: Task to run
            
        Returns:
            ResetResponse with observation and episode info
        """
        response = requests.post(
            f"{self.base_url}/reset",
            json={"task_id": task_id},
        )
        response.raise_for_status()
        data = response.json()
        return ResetResponse(**data)

    def step(self, action: Dict[str, Any]) -> StepResponse:
        """
        Execute action in environment
        
        Args:
            action: Agent's action dictionary
            
        Returns:
            StepResponse with observation, reward, and done flag
        """
        response = requests.post(
            f"{self.base_url}/step",
            json={"action": action},
        )
        response.raise_for_status()
        data = response.json()
        return StepResponse(**data)

    def state(self) -> Dict[str, Any]:
        """Get current environment state"""
        response = requests.get(f"{self.base_url}/state")
        response.raise_for_status()
        return response.json()

    def health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
