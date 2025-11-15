from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests
import os

# -----------------------------
# Configuration
# -----------------------------
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "https://your-ai-server.onrender.com")  # Replace with your AI server URL
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD", "supersecretpassword")             # Same as AI server

app = FastAPI(title="Neuralic AI Admin Site")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Dashboard page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logged_in": False})

# -----------------------------
# Login route
# -----------------------------
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, password: str = Form(...)):
    if password != MASTER_PASSWORD:
        return templates.TemplateResponse("index.html", {"request": request, "logged_in": False, "error": "Invalid password"})
    
    try:
        res = requests.get(f"{AI_SERVER_URL}/admin/list_keys", params={"password": MASTER_PASSWORD}, timeout=10)
        res.raise_for_status()  # Raise error if not 200
        keys = res.json().get("keys", [])
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "logged_in": False,
            "error": f"Failed to fetch keys from AI server: {e}"
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "logged_in": False,
            "error": f"Unexpected error: {e}"
        })
    
    return templates.TemplateResponse("index.html", {"request": request, "logged_in": True, "keys": keys})

# -----------------------------
# Run with python main.py
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))  # Render sets PORT automatically
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
