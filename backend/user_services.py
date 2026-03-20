# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# main.py
from fastapi import FastAPI, HTTPException
from firebase_config import db

app = FastAPI()

def create_user(user_data):
    try:
        doc_ref = db.collection("users").add(user_data)
        return {"message": "User created", "id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_users():
    try:
        users = db.collection("users").stream()
        return [{**u.to_dict(), "id": u.id} for u in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users")
def add_user(user: dict):
    return create_user(user)

@app.get("/users")
def fetch_users():
    return get_users()
