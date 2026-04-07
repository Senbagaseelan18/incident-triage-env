#!/usr/bin/env python3
"""
Hugging Face Spaces deployment configuration
"""

CONFIG = {
    "repo_type": "space",
    "space_sdk": "docker",
    "space_hardware": "cpu-basic",
    "private": False,
    "description": "AI-Powered Incident Triage & Escalation System - OpenEnv Environment",
    "tags": [
        "openenv",
        "reinforcement-learning",
        "environment",
        "incident-management",
        "incident-triage",
    ],
}
