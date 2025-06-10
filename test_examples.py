import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_api():
    """Test the AI Shopping Assistant API with example data"""
    
    print("🧪 Testing AI Shopping Assistant API...")
    print("=" * 50)
    
    # Example buyer profile
    buyer_data = {
        "user_id": "A123",
        "history": [
            {"product": "Bluetooth headphones", "category": "electronics", "price": 120},
            {"product": "Running shoes", "category": "sportswear", "price": 80},
            {"product": "Blender", "category": "kitchen", "price": 70},
        ]
    }
    
    try:
        # 1. Add buyer profile
        print("\n1. Adding buyer profile...")
        response = requests.post(f"{BASE_URL}/buyer", json=buyer_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 2. Get buyer profile
        print("\n2. Getting buyer profile...")
        response = requests.get(f"{BASE_URL}/buyer/A123")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 3. Analyze and get recommendations
        print("\n3. Getting AI recommendations...")
        response = requests.post(f"{BASE_URL}/analyze/A123")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Analysis: {result.get('analysis', {})}")
        print(f"Recommendation: {result.get('recommendation', {})}")
        print(f"Justification: {result.get('justification', '')}")
        
        # 4. Search products in AI-recommended category
        recommended_category = result.get('recommendation', {}).get('recommended_category', 'electronics')
        print(f"\n4. Searching {recommended_category} products (AI recommended)...")
        response = requests.get(f"{BASE_URL}/search/{recommended_category}?user_id=A123")
        print(f"Status: {response.status_code}")
        products = response.json().get('products', [])
        if products:
            print(f"Found {len(products)} products:")
            for product in products:
                print(f"  - {product['name']} (${product['price']})")
        
        # 5. Simulate purchase
        if products:
            print("\n5. Simulating purchase...")
            purchase_data = {
                "user_id": "A123",
                "product_id": products[0]['id']
            }
            response = requests.post(f"{BASE_URL}/purchase", json=purchase_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 6. Get transaction history
        print("\n6. Getting transaction history...")
        response = requests.get(f"{BASE_URL}/transactions/A123")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 7. Get all categories
        print("\n7. Getting all categories...")
        response = requests.get(f"{BASE_URL}/categories")
        print(f"Status: {response.status_code}")
        categories = response.json().get('categories', [])
        print(f"Available categories: {', '.join(categories)}")
        
        print("\n✅ API tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_api() 