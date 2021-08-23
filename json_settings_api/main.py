from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Optional
import json, os

app = FastAPI()

def render_template(html_template):
    with open(html_template, "r", encoding="utf-8") as outfile:
        buffer = outfile.read()
        outfile.close()
    return buffer

@app.get("/")
async def index():
    return HTMLResponse(content=render_template("templates/index.html"))


@app.get("/users/{user_email}/{settings_filename}")
async def read_settings(user_email: str, settings_filename: str):
    try:
        with open(f"../users/{user_email}/{settings_filename}", "r", encoding="utf-8") as f:
            data = f.read()
            f.close()
            if settings_filename.endswith(".json"):
                return {"user_email": user_email,"settings_filename": settings_filename,"settings": json.loads(data)}
            return {"user_email": user_email,"settings_filename": settings_filename,"settings": data}  
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Filename not found.")