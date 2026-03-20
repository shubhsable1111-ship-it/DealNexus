# Inside main.py (the single-file version)
def add_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new product to Firestore."""
    try:
        data = product_data.copy()
        data.pop("id", None)
        doc_ref = db.collection("products").add(data)
        return {"id": doc_ref[1].id, "message": "Product added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_products() -> List[Dict[str, Any]]:
    """Fetch all products."""
    try:
        docs = db.collection("products").stream()
        products = []
        for doc in docs:
            product = doc.to_dict()
            product["id"] = doc.id
            products.append(product)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products")
def create_product(product: dict):
    return add_product(product)

@app.get("/products")
def fetch_products():
    return get_products()