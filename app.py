from flask import Flask, request, jsonify
import json
from typing import Dict, Any

from models.buyer import BuyerProfile
from services.llm_service import LLMService
from services.catalog_service import CatalogService
from services.memory_service import MemoryService
from services.purchase_service import PurchaseService
from config import Config

app = Flask(__name__)

# Initialize services
llm_service = LLMService()
catalog_service = CatalogService()
memory_service = MemoryService()
purchase_service = PurchaseService(memory_service, catalog_service)

@app.route('/')
def home():
    """API information endpoint"""
    return jsonify({
        "message": "AI Shopping Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "POST /buyer": "Add/update buyer profile",
            "GET /buyer/<user_id>": "Get buyer profile",
            "POST /analyze/<user_id>": "Analyze buyer and get recommendations",
            "GET /search/<category>": "Search products by category",
            "POST /purchase": "Simulate a purchase",
            "GET /transactions/<user_id>": "Get transaction history",
            "GET /categories": "Get all product categories"
        }
    })

@app.route('/buyer', methods=['POST'])
def add_buyer():
    """Add or update buyer profile"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'user_id' not in data:
            return jsonify({"error": "user_id is required"}), 400
        
        # Create buyer profile
        buyer_profile = BuyerProfile.from_json(data)
        
        # Store in memory
        success = memory_service.store_buyer_profile(buyer_profile)
        
        if success:
            return jsonify({
                "message": "Buyer profile stored successfully",
                "user_id": buyer_profile.user_id,
                "history_count": len(buyer_profile.history)
            }), 201
        else:
            return jsonify({"error": "Failed to store buyer profile"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@app.route('/buyer/<user_id>', methods=['GET'])
def get_buyer(user_id):
    """Get buyer profile"""
    try:
        buyer_profile = memory_service.get_buyer_profile(user_id)
        
        if buyer_profile:
            return jsonify({
                "user_id": buyer_profile.user_id,
                "history": buyer_profile.history,
                "categories": buyer_profile.get_product_categories(),
                "price_range": buyer_profile.get_price_range()
            })
        else:
            return jsonify({"error": "Buyer not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Error retrieving buyer: {str(e)}"}), 500

@app.route('/analyze/<user_id>', methods=['POST'])
def analyze_and_recommend(user_id):
    """Analyze buyer history and provide recommendations"""
    try:
        # Get buyer profile
        buyer_profile = memory_service.get_buyer_profile(user_id)
        if not buyer_profile:
            return jsonify({"error": "Buyer not found"}), 404
        
        # Analyze buyer history
        analysis = llm_service.analyze_buyer_history(buyer_profile)
        
        # Get product recommendation
        recommendation = llm_service.recommend_product_category(buyer_profile, analysis)
        
        # Get justification
        justification = llm_service.justify_recommendation(recommendation, buyer_profile)
        
        # Search for products in recommended category
        recommended_products = catalog_service.search_by_category(
            recommendation.get('recommended_category', 'electronics'),
            Config.MAX_SEARCH_RESULTS
        )
        
        # Rank products based on buyer preferences
        ranked_products = catalog_service.rank_products_by_preferences(
            recommended_products, buyer_profile
        )
        
        return jsonify({
            "user_id": user_id,
            "analysis": analysis,
            "recommendation": recommendation,
            "justification": justification,
            "recommended_products": ranked_products,
            "current_categories": buyer_profile.get_product_categories(),
            "price_range": buyer_profile.get_price_range()
        })
        
    except Exception as e:
        return jsonify({"error": f"Error analyzing buyer: {str(e)}"}), 500

@app.route('/search/<category>', methods=['GET'])
def search_products(category):
    """Search products by category"""
    try:
        max_results = request.args.get('max_results', Config.MAX_SEARCH_RESULTS, type=int)
        user_id = request.args.get('user_id')
        
        # Search products
        products = catalog_service.search_by_category(category, max_results)
        
        # If user_id provided, rank by their preferences
        if user_id:
            buyer_profile = memory_service.get_buyer_profile(user_id)
            if buyer_profile:
                products = catalog_service.rank_products_by_preferences(products, buyer_profile)
        
        return jsonify({
            "category": category,
            "total_found": len(products),
            "products": products
        })
        
    except Exception as e:
        return jsonify({"error": f"Error searching products: {str(e)}"}), 500

@app.route('/purchase', methods=['POST'])
def simulate_purchase():
    """Simulate a product purchase"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'user_id' not in data or 'product_id' not in data:
            return jsonify({"error": "user_id and product_id are required"}), 400
        
        # Simulate purchase
        result = purchase_service.simulate_purchase(data['user_id'], data['product_id'])
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"error": f"Purchase failed: {str(e)}"}), 500

@app.route('/transactions/<user_id>', methods=['GET'])
def get_transactions(user_id):
    """Get transaction history for a user"""
    try:
        transactions = purchase_service.get_transaction_history(user_id)
        
        return jsonify({
            "user_id": user_id,
            "total_transactions": len(transactions),
            "transactions": transactions
        })
        
    except Exception as e:
        return jsonify({"error": f"Error retrieving transactions: {str(e)}"}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all available product categories"""
    try:
        categories = catalog_service.get_all_categories()
        
        return jsonify({
            "categories": categories,
            "total_categories": len(categories)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error retrieving categories: {str(e)}"}), 500

@app.route('/buyers', methods=['GET'])
def get_all_buyers():
    """Get all stored buyer profiles"""
    try:
        buyers = memory_service.get_all_buyers()
        
        return jsonify({
            "total_buyers": len(buyers),
            "buyers": buyers
        })
        
    except Exception as e:
        return jsonify({"error": f"Error retrieving buyers: {str(e)}"}), 500

if __name__ == '__main__':
    print("🛍️  AI Shopping Assistant API Starting...")
    print(f"📊 Memory Type: {Config.MEMORY_TYPE}")
    print(f"🔑 Using DeepSeek API")
    print(f"📦 Total Products in Catalog: {len(catalog_service.products)}")
    print(f"🏷️  Available Categories: {', '.join(catalog_service.get_all_categories())}")
    print("\n✅ Server ready! Access the API at http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 