"""
Interactive Web Dashboard for Incident Triage Environment
Built with Streamlit - Simple, interactive, no frontend coding needed
"""
import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Set page config
st.set_page_config(
    page_title="Incident Triage Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    .success {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .error {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    .warning {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "https://senbagaseelanv-incident-triage-env.hf.space"

# Session state initialization
if "episode_id" not in st.session_state:
    st.session_state.episode_id = None
if "observation" not in st.session_state:
    st.session_state.observation = None
if "task_id" not in st.session_state:
    st.session_state.task_id = "task_easy"
if "total_episodes" not in st.session_state:
    st.session_state.total_episodes = 0
if "total_reward" not in st.session_state:
    st.session_state.total_reward = 0.0
if "episode_history" not in st.session_state:
    st.session_state.episode_history = []

# Header
st.markdown("# 🚨 Incident Triage Management System", unsafe_allow_html=True)
st.markdown("**Interactive AI Training Environment**")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Task selection
    task_id = st.selectbox(
        "Select Task Difficulty",
        ["task_easy", "task_medium", "task_hard"],
        format_func=lambda x: {
            "task_easy": "🟢 Easy - Severity Only",
            "task_medium": "🟡 Medium - Severity + Routing",
            "task_hard": "🔴 Hard - Full Pipeline"
        }[x]
    )
    st.session_state.task_id = task_id
    
    st.markdown("---")
    
    # Statistics
    st.header("📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Episodes", st.session_state.total_episodes)
    with col2:
        avg_reward = (
            st.session_state.total_reward / st.session_state.total_episodes
            if st.session_state.total_episodes > 0
            else 0.0
        )
        st.metric("Avg Reward", f"{avg_reward:.2f}")
    
    st.markdown("---")
    
    # API Status
    st.header("🔗 API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ Connection Failed")

# Main content area
# Create tabs
tab1, tab2, tab3 = st.tabs(["🎮 Play", "📈 History", "ℹ️ About"])

with tab1:
    st.header("Interactive Incident Triage")
    
    # Start new episode
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 New Incident", use_container_width=True):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/reset",
                    json={"task_id": st.session_state.task_id},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.observation = data.get("observation")
                    st.session_state.episode_id = data.get("episode_id")
                    st.success("✅ New incident loaded!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display current incident
    if st.session_state.observation:
        obs = st.session_state.observation
        
        # Incident details
        st.subheader("📋 Incident Details")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.text_input("Incident ID", value=obs.get("incident_id", ""), disabled=True)
            st.text_area(
                "Incident Description",
                value=obs.get("incident_text", ""),
                height=100,
                disabled=True
            )
        with col2:
            st.text_input("Service Affected", value=obs.get("service_affected", ""), disabled=True)
            st.text_input("Step Count", value=str(obs.get("step_count", 0)), disabled=True)
        
        st.markdown("---")
        
        # Decision form
        st.subheader("🤖 Make Triage Decision")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            severity = st.selectbox(
                "Severity Level",
                ["low", "medium", "high", "critical"],
                format_func=lambda x: f"🔴 {x.upper()}" if x == "critical" 
                           else f"🟠 {x.upper()}" if x == "high"
                           else f"🟡 {x.upper()}" if x == "medium"
                           else f"🟢 {x.upper()}"
            )
        
        with col2:
            team = st.selectbox(
                "Route to Team",
                ["database", "network", "support"],
                format_func=lambda x: {
                    "database": "🗄️ Database",
                    "network": "🌐 Network",
                    "support": "👨‍💼 Support"
                }[x]
            )
        
        with col3:
            priority = st.selectbox(
                "Priority",
                ["p1", "p2", "p3"],
                format_func=lambda x: {
                    "p1": "🚨 P1 (Urgent)",
                    "p2": "⚠️ P2 (High)",
                    "p3": "📋 P3 (Low)"
                }[x]
            )
        
        with col4:
            escalate = st.checkbox("Escalate?", value=False)
        
        st.markdown("---")
        
        # Submit decision
        if st.button("✅ Submit Decision", use_container_width=True, type="primary"):
            try:
                action_data = {
                    "severity": severity,
                    "team": team,
                    "priority": priority,
                    "escalate": escalate
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/step",
                    json={"action": action_data},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    reward = result.get("reward", 0.0)
                    done = result.get("done", False)
                    info = result.get("info", {})
                    
                    # Update statistics
                    st.session_state.total_reward += reward
                    st.session_state.total_episodes += 1
                    
                    # Store in history
                    episode_entry = {
                        "episode": st.session_state.total_episodes,
                        "task": st.session_state.task_id,
                        "action": action_data,
                        "reward": reward,
                        "grader": info.get("grader_result", {}),
                        "timestamp": datetime.now().isoformat()
                    }
                    st.session_state.episode_history.append(episode_entry)
                    
                    # Display result
                    st.markdown("---")
                    st.subheader("⚡ Result")
                    
                    # Reward display
                    reward_color = "green" if reward > 0.7 else "orange" if reward > 0.3 else "red"
                    st.markdown(
                        f'<div style="background-color: {"#d4edda" if reward_color == "green" else "#fff3cd" if reward_color == "orange" else "#f8d7da"}; '
                        f'padding: 2rem; border-radius: 8px; text-align: center; color: {"#155724" if reward_color == "green" else "#856404" if reward_color == "orange" else "#721c24"};">'
                        f'<h2>Reward: {reward:.2f}</h2>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Grader details
                    grader = info.get("grader_result", {})
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        status = "✅" if grader.get("severity_correct") else "❌"
                        st.metric("Severity", status)
                    with col2:
                        status = "✅" if grader.get("team_correct") else "❌"
                        st.metric("Team", status)
                    with col3:
                        status = "✅" if grader.get("priority_correct") else "❌"
                        st.metric("Priority", status)
                    with col4:
                        status = "✅" if grader.get("escalation_correct") else "❌"
                        st.metric("Escalation", status)
                    
                    if done:
                        st.success("✅ Episode Complete!")
                    
                else:
                    st.error(f"❌ Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👉 Click 'New Incident' to start!")

with tab2:
    st.header("📈 Episode History")
    
    if st.session_state.episode_history:
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Episodes", len(st.session_state.episode_history))
        with col2:
            avg_reward = sum(e["reward"] for e in st.session_state.episode_history) / len(st.session_state.episode_history)
            st.metric("Avg Reward", f"{avg_reward:.2f}")
        with col3:
            max_reward = max(e["reward"] for e in st.session_state.episode_history)
            st.metric("Best Reward", f"{max_reward:.2f}")
        with col4:
            min_reward = min(e["reward"] for e in st.session_state.episode_history)
            st.metric("Worst Reward", f"{min_reward:.2f}")
        
        st.markdown("---")
        
        # Detailed history
        st.subheader("Detailed Results")
        for entry in reversed(st.session_state.episode_history):
            with st.expander(
                f"Episode {entry['episode']} - "
                f"Task: {entry['task']} - "
                f"Reward: {entry['reward']:.2f}"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Decision:**")
                    st.json(entry["action"])
                with col2:
                    st.write("**Grader Result:**")
                    st.json(entry["grader"])
                st.write(f"**Timestamp:** {entry['timestamp']}")
    else:
        st.info("No episodes yet. Start playing to see history!")

with tab3:
    st.header("ℹ️ About This Project")
    
    st.markdown("""
    ## 🚨 Incident Triage Environment
    
    An **OpenEnv Reinforcement Learning environment** for training AI agents to triage 
    IT incidents and route them to the correct teams.
    
    ### 🎯 What It Does
    - Simulates real-world incident management
    - Tests agent decision-making on severity, routing, priority, and escalation
    - Provides rewards based on correctness
    - Supports 3 difficulty levels
    
    ### 📊 Task Difficulty
    
    **🟢 Easy - Severity Classification**
    - Only classify severity (low/medium/high/critical)
    - Max reward: 0.3
    
    **🟡 Medium - Severity & Routing**
    - Classify severity AND route to correct team
    - Max reward: 0.6
    
    **🔴 Hard - Full Pipeline**
    - Classify severity, route team, assign priority, decide escalation
    - Max reward: 1.0
    
    ### 💡 Real-World Applications
    - IT Operations (incident management)
    - Customer Support (ticket routing)
    - Healthcare (patient triage)
    - Finance (fraud detection routing)
    
    ### 🔗 Links
    - **GitHub:** https://github.com/Senbagaseelan18/incident-triage-env
    - **HF Space:** https://huggingface.co/spaces/SenbagaseelanV/incident-triage-env
    - **API:** https://senbagaseelanv-incident-triage-env.hf.space
    
    ### 📚 Available Endpoints
    - `GET /health` - Health check
    - `POST /reset` - Start new episode
    - `POST /step` - Submit action
    - `GET /state` - Get current state
    - `GET /tasks` - List tasks
    """)
