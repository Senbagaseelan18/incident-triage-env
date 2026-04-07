"""
FastAPI Server for Incident Triage Environment
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models import Action, ResetResponse, StepResponse
from environment import IncidentTriageEnvironment

# Initialize FastAPI app
app = FastAPI(
    title="Incident Triage Environment",
    description="OpenEnv environment for AI-powered incident triage",
    version="1.0.0",
)

# Global environment instance
env = IncidentTriageEnvironment()


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("Incident Triage Environment server started")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Incident Triage Environment",
        "version": "1.0.0",
        "description": "OpenEnv environment for AI-powered incident triage",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/reset")
async def reset(body: dict):
    """
    Reset environment and get initial observation
    
    Args:
        body: Request body with optional task_id
    """
    try:
        task_id = body.get("task_id", "task_easy")
        response = env.reset(task_id=task_id)
        return response.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
async def step(body: dict):
    """
    Execute action and receive reward
    
    Args:
        body: Request body with action
    """
    try:
        action_dict = body.get("action", {})
        
        # Parse action
        action = Action(
            severity=action_dict.get("severity"),
            team=action_dict.get("team"),
            priority=action_dict.get("priority"),
            escalate=action_dict.get("escalate", False),
        )
        
        response = env.step(action)
        return response.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
async def state():
    """Get current environment state"""
    try:
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks")
async def list_tasks():
    """List available tasks"""
    from environment import TASK_CONFIGS
    return {
        "tasks": [
            {
                "id": config.task_id,
                "name": config.name,
                "description": config.description,
                "difficulty": config.difficulty,
            }
            for config in TASK_CONFIGS.values()
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
