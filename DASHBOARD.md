# 🌐 Web Dashboards for Incident Triage Environment

Two interactive web interfaces to interact with the Incident Triage Environment:

## Option 1: Streamlit Dashboard (Recommended)

**Modern, interactive Python dashboard with full features**

### Features
- 🎮 Interactive incident triage gameplay
- 📊 Real-time statistics and metrics
- 📈 Episode history with detailed results
- 📋 Task difficulty selection
- ⚡ Beautiful, responsive UI
- 🎯 Live feedback on decisions

### How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py

# Opens automatically at http://localhost:8501
```

### Deploy to Hugging Face Spaces

The Streamlit app can be deployed directly to HF Spaces:

```bash
# Create a new Streamlit Space on HF
# Push this directory to the Space

git push huggingface main
```

### What You Can Do

1. **Select Task Difficulty**
   - Easy (severity only)
   - Medium (severity + routing)
   - Hard (full pipeline)

2. **Load Incidents**
   - Click "New Incident" to get a random incident

3. **Make Decisions**
   - Classify severity (low/medium/high/critical)
   - Route to team (database/network/support)
   - Assign priority (p1/p2/p3)
   - Decide escalation

4. **View Results**
   - See reward score (0.0 - 1.0)
   - Check which decisions were correct
   - Track improvement over episodes

5. **Monitor Progress**
   - View episode history
   - Track average reward
   - See best performing episodes

---

## Option 2: HTML Dashboard

**Standalone HTML/JavaScript dashboard - no backend needed**

### Features
- 📱 Pure HTML + CSS + JavaScript
- 🔗 Calls REST API directly
- 📊 Real-time statistics
- 🎯 Clean, modern interface
- ✅ No dependencies required

### How to Use

**Option A: Local File**
```bash
# Simply open in browser
open dashboard.html
# or
Start-Process dashboard.html  # PowerShell
```

**Option B: Serve with Python**
```bash
# Serve on localhost:8000
python -m http.server 8000

# Then visit http://localhost:8000/dashboard.html
```

**Option C: Host on Server**
- Upload `dashboard.html` to any web server
- Access from browser

### What You Can Do

Same as Streamlit dashboard:
1. Load incidents
2. Make triage decisions
3. View results with grading
4. Track statistics
5. View episode history

---

## Comparison

| Feature | Streamlit | HTML |
|---------|-----------|------|
| **Setup** | Python required | None |
| **Code** | Python | HTML/JS |
| **Features** | More | Same |
| **Deployment** | HF Spaces | Anywhere |
| **Mobile** | Responsive | Responsive |
| **Performance** | Good | Excellent |
| **Customization** | Python/Streamlit | HTML/CSS/JS |

---

## API Integration

Both dashboards connect to the live API:

```
https://senbagaseelanv-incident-triage-env.hf.space
```

### Endpoints Used

- **GET /health** - Check if API is online
- **POST /reset** - Get new incident
- **POST /step** - Submit decision and get reward

---

## Running Both Simultaneously

You can run both dashboards at the same time:

```bash
# Terminal 1 - Streamlit
streamlit run app.py

# Terminal 2 - Simple HTTP server for HTML
python -m http.server 9000

# Then access:
# - Streamlit: http://localhost:8501
# - HTML: http://localhost:9000/dashboard.html
```

---

## Customization

### Streamlit (app.py)

```python
# Change API URL
API_BASE_URL = "your-custom-url"

# Customize colors/theme
st.set_page_config(page_title="Custom Title")

# Add new features
# - Charts
# - Agent comparison
# - Leaderboard
```

### HTML (dashboard.html)

```html
<!-- Modify colors -->
primaryColor = "#YOUR-COLOR"

<!-- Add features -->
<!-- Charts, graphs, animations -->

<!-- Customize styling -->
/* CSS in <style> section */
```

---

## Troubleshooting

### Dashboard won't connect to API
- Check API status: https://senbagaseelanv-incident-triage-env.hf.space/health
- Verify network connection
- Check browser console for CORS errors

### Streamlit won't start
- Ensure streamlit is installed: `pip install streamlit`
- Check port 8501 is available
- Run: `streamlit run app.py`

### HTML dashboard issues
- Use modern browser (Chrome, Firefox, Safari, Edge)
- Check browser console (F12) for errors
- Ensure API URL is correct

---

## Advanced Features to Add

```python
# Potential enhancements:
1. Multi-agent comparison
2. Learning progress visualization
3. Performance leaderboard
4. Agent training integration
5. Export results to CSV
6. Custom incident creation
7. Real-time multiplayer
8. Replay system
```

---

## Links

- **Live API:** https://senbagaseelanv-incident-triage-env.hf.space
- **GitHub:** https://github.com/Senbagaseelan18/incident-triage-env
- **HF Space:** https://huggingface.co/spaces/SenbagaseelanV/incident-triage-env
- **Streamlit Docs:** https://docs.streamlit.io
- **REST API Docs:** Available at `/docs` endpoint

---

**Happy triaging! 🚨**
