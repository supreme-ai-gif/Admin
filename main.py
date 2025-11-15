# admin_site/main.py
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

# -----------------------------
# Configuration
# -----------------------------
AI_SERVER_URL = "https://genetic-ai.onrender.com"  # Replace with your AI server URL
MASTER_PASSWORD = "supersecretpassword"      # Same as AI server

app = FastAPI(title="Neuralic AI Admin Site")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Dashboard page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logged_in": False})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, password: str = Form(...)):
    if password != MASTER_PASSWORD:
        return templates.TemplateResponse("index.html", {"request": request, "logged_in": False, "error": "Invalid password"})
    
    # Fetch current keys from AI server
    res = requests.get(f"{AI_SERVER_URL}/admin/list_keys", params={"password": MASTER_PASSWORD})
    keys = res.json().get("keys", [])
    
    return templates.TemplateResponse("index.html", {"request": request, "logged_in": True, "keys": keys})
