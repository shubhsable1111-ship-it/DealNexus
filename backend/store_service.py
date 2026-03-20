# main.py
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

# ---------- Firebase Initialization ----------
# Place your serviceAccountKey.json in the same folder
SERVICE_ACCOUNT_KEY = "serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------- FastAPI App ----------
app = FastAPI(title="OfferZone Backend", version="1.0")

# ---------- Helper Functions ----------
def collection_ref(collection: str):
    return db.collection(collection)

# ----- USER Service -----
def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new user to Firestore."""
    try:
        data = user_data.copy()
        data.pop("id", None)
        doc_ref = collection_ref("users").add(data)
        return {"id": doc_ref[1].id, "message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_users() -> List[Dict[str, Any]]:
    """Fetch all users."""
    try:
        docs = collection_ref("users").stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- STORE Service -----
def create_store(store_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new store to Firestore."""
    try:
        doc_ref = db.collection("stores").add(store_data)
        return {"message": "Store created", "id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_stores() -> List[Dict[str, Any]]:
    """Fetch all stores."""
    try:
        stores = db.collection("stores").stream()
        return [{**s.to_dict(), "id": s.id} for s in stores]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- PRODUCT Service -----
def add_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new product to Firestore."""
    try:
        doc_ref = db.collection("products").add(product_data)
        return {"message": "Product added", "id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_products() -> List[Dict[str, Any]]:
    """Fetch all products."""
    try:
        products = db.collection("products").stream()
        return [{**p.to_dict(), "id": p.id} for p in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- API Routes ----------
@app.get("/")
def home():
    return {"message": "OfferZone Backend Running 🚀"}

# ----- USER APIs -----
@app.post("/users")
def add_user(user: dict):
    return create_user(user)

@app.get("/users")
def fetch_users():
    return get_users()

# ----- STORE APIs -----
@app.post("/stores")
def add_store(store: dict):
    return create_store(store)

@app.get("/stores")
def fetch_stores():
    return get_stores()

# ----- PRODUCT APIs -----
@app.post("/products")
def create_product(product: dict):
    return add_product(product)

@app.get("/products")
def fetch_products():
    return get_products()