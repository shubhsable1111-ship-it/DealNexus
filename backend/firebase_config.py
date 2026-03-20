# backend/firestore_service.py
import firebase_admin
from firebase_admin import credentials, firestore
import sys
import json
from typing import List, Dict, Any, Optional

# ---------- Initialization ----------
# Path to your service account key file (downloaded from Firebase Console)
SERVICE_ACCOUNT_KEY = "serviceAccountKey.json"

try:
    # Initialize the Firebase Admin SDK
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    # Check if app already exists to avoid duplicate initialization
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize Firebase: {e}")
    sys.exit(1)


# ---------- Product Operations ----------
def fetch_all_products() -> List[Dict[str, Any]]:
    """Retrieve all products from Firestore."""
    try:
        products_ref = db.collection("products")
        docs = products_ref.stream()
        products = []
        for doc in docs:
            product_data = doc.to_dict()
            product_data["id"] = doc.id  # include document ID
            products.append(product_data)
        return products
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []


def fetch_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single product by its document ID."""
    try:
        doc_ref = db.collection("products").document(product_id)
        doc = doc_ref.get()
        if doc.exists:
            product_data = doc.to_dict()
            product_data["id"] = doc.id
            return product_data
        else:
            return None
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")
        return None


def add_product(product_data: Dict[str, Any]) -> Optional[str]:
    """
    Add a new product to Firestore.
    Returns the document ID of the newly created product, or None on error.
    """
    try:
        # Remove 'id' if present to let Firestore generate it
        product_data_copy = product_data.copy()
        product_data_copy.pop("id", None)

        doc_ref = db.collection("products").add(product_data_copy)
        product_id = doc_ref[1].id  # doc_ref is (timestamp, document_reference)
        print(f"✅ Product added with ID: {product_id}")
        return product_id
    except Exception as e:
        print(f"❌ Error adding product: {e}")
        return None


def update_product(product_id: str, update_data: Dict[str, Any]) -> bool:
    """Update an existing product."""
    try:
        doc_ref = db.collection("products").document(product_id)
        doc_ref.update(update_data)
        print(f"✅ Product {product_id} updated.")
        return True
    except Exception as e:
        print(f"❌ Error updating product {product_id}: {e}")
        return False


def delete_product(product_id: str) -> bool:
    """Delete a product by ID."""
    try:
        doc_ref = db.collection("products").document(product_id)
        doc_ref.delete()
        print(f"✅ Product {product_id} deleted.")
        return True
    except Exception as e:
        print(f"❌ Error deleting product {product_id}: {e}")
        return False


# ---------- Batch Operations (e.g., seeding) ----------
def add_multiple_products(products_list: List[Dict[str, Any]]) -> List[str]:
    """Add multiple products in batch (each individually)."""
    added_ids = []
    for product in products_list:
        pid = add_product(product)
        if pid:
            added_ids.append(pid)
    return added_ids


# ---------- Example Usage ----------
if __name__ == "__main__":
    # Example: Fetch and print all products
    print("\n--- Fetching all products ---")
    all_products = fetch_all_products()
    for p in all_products:
        print(json.dumps(p, indent=2))

    # Example: Add a new product
    new_product = {
        "name": "Organic Basmati Rice",
        "price": 220,
        "category": "Staples",
        "imageUrl": "https://example.com/rice.jpg",
        "description": "Premium quality basmati rice, 1kg pack",
        "inStock": True,
        "quantity": 50  # available quantity
    }
    print("\n--- Adding a new product ---")
    product_id = add_product(new_product)
    if product_id:
        print(f"New product ID: {product_id}")

    # Example: Update a product (if you have an ID)
    if product_id:
        print("\n--- Updating the product ---")
        update_data = {"price": 210, "discount": 5}
        update_product(product_id, update_data)

        # Verify update
        updated_product = fetch_product_by_id(product_id)
        if updated_product:
            print("Updated product:", json.dumps(updated_product, indent=2))

    # Example: Delete a product (uncomment to test)
    # if product_id:
    #     print("\n--- Deleting the product ---")
    #     delete_product(product_id)

    # Example: Add multiple products (seed data)
    sample_products = [
        {
            "name": "Wheat Flour (Aashirvaad)",
            "price": 150,
            "category": "Staples",
            "imageUrl": "https://example.com/flour.jpg",
            "inStock": True
        },
        {
            "name": "Lays Chips",
            "price": 20,
            "category": "Snacks",
            "imageUrl": "https://example.com/lays.jpg",
            "inStock": True
        }
    ]
    print("\n--- Adding sample products ---")
    added = add_multiple_products(sample_products)
    print(f"Added {len(added)} products.")