from fastapi import FastAPI, HTTPException
import json, os

app = FastAPI()

@app.get("/")
def index():
    return {"Index Message":"Welcome to Timerist's JSON api!"}

@app.get("/users/{user_email}/{settings_filename}")
def read_settings(user_email: str, settings_filename: str):
    try:
        with open(f"../users/{user_email}/{settings_filename}", "r", encoding="utf-8") as f:
            data = f.read()
            f.close()
            return {"user_email": user_email,"settings_filename": settings_filename,"settings": json.loads(data)} 
    except:
        raise HTTPException(status_code=404, detail="User or filename not found.")
