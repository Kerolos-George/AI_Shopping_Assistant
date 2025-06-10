from typing import Dict, List, Any
import json
from models.buyer import BuyerProfile

class CatalogService:
    """Service for handling product catalog operations"""
    
    def __init__(self):
        self.products = self._load_mock_catalog()
    
    def _load_mock_catalog(self) -> List[Dict[str, Any]]:
        """Load mock product catalog"""
        return [
            # Electronics
            {"id": 1, "name": "Wireless Bluetooth Headphones", "category": "electronics", "price": 120, "rating": 4.5, "brand": "AudioTech"},
            {"id": 2, "name": "Smartphone Case", "category": "electronics", "price": 25, "rating": 4.2, "brand": "ProtectPro"},
            {"id": 3, "name": "Laptop Stand", "category": "electronics", "price": 45, "rating": 4.3, "brand": "DeskMaster"},
            {"id": 4, "name": "Wireless Charger", "category": "electronics", "price": 35, "rating": 4.1, "brand": "ChargeFast"},
            {"id": 5, "name": "Smart Watch", "category": "electronics", "price": 200, "rating": 4.6, "brand": "TimeTech"},
            
            # Sportswear
            {"id": 6, "name": "Running Shoes", "category": "sportswear", "price": 80, "rating": 4.4, "brand": "RunFast"},
            {"id": 7, "name": "Yoga Mat", "category": "sportswear", "price": 30, "rating": 4.3, "brand": "FlexFit"},
            {"id": 8, "name": "Sports Water Bottle", "category": "sportswear", "price": 15, "rating": 4.2, "brand": "HydroSport"},
            {"id": 9, "name": "Gym Bag", "category": "sportswear", "price": 50, "rating": 4.1, "brand": "FitCarry"},
            {"id": 10, "name": "Athletic Wear Set", "category": "sportswear", "price": 65, "rating": 4.5, "brand": "ActiveWear"},
            
            # Home Decor
            {"id": 11, "name": "Table Lamp", "category": "home_decor", "price": 40, "rating": 4.2, "brand": "LightUp"},
            {"id": 12, "name": "Wall Art Print", "category": "home_decor", "price": 20, "rating": 4.0, "brand": "ArtSpace"},
            {"id": 13, "name": "Throw Pillow", "category": "home_decor", "price": 25, "rating": 4.3, "brand": "ComfyHome"},
            {"id": 14, "name": "Decorative Vase", "category": "home_decor", "price": 35, "rating": 4.1, "brand": "ElegantDecor"},
            {"id": 15, "name": "Scented Candle Set", "category": "home_decor", "price": 30, "rating": 4.4, "brand": "AromaBliss"},
            
            # Books
            {"id": 16, "name": "Self-Help Book", "category": "books", "price": 15, "rating": 4.3, "brand": "WisdomPress"},
            {"id": 17, "name": "Fiction Novel", "category": "books", "price": 12, "rating": 4.5, "brand": "StoryWorld"},
            {"id": 18, "name": "Cookbook", "category": "books", "price": 25, "rating": 4.2, "brand": "ChefMaster"},
            {"id": 19, "name": "Travel Guide", "category": "books", "price": 18, "rating": 4.1, "brand": "ExploreMore"},
            {"id": 20, "name": "Art Book", "category": "books", "price": 35, "rating": 4.4, "brand": "VisualArts"},
            
            # Fashion
            {"id": 21, "name": "Designer Handbag", "category": "fashion", "price": 150, "rating": 4.6, "brand": "StyleLux"},
            {"id": 22, "name": "Casual T-Shirt", "category": "fashion", "price": 20, "rating": 4.2, "brand": "ComfortWear"},
            {"id": 23, "name": "Denim Jeans", "category": "fashion", "price": 60, "rating": 4.3, "brand": "DenimCraft"},
            {"id": 24, "name": "Sunglasses", "category": "fashion", "price": 40, "rating": 4.1, "brand": "SunShield"},
            {"id": 25, "name": "Leather Wallet", "category": "fashion", "price": 35, "rating": 4.4, "brand": "LeatherPro"},
            
            # Kitchen
            {"id": 26, "name": "Coffee Maker", "category": "kitchen", "price": 85, "rating": 4.5, "brand": "BrewMaster"},
            {"id": 27, "name": "Cutting Board Set", "category": "kitchen", "price": 30, "rating": 4.3, "brand": "ChopSafe"},
            {"id": 28, "name": "Non-stick Pan", "category": "kitchen", "price": 45, "rating": 4.4, "brand": "CookEasy"},
            {"id": 29, "name": "Spice Rack", "category": "kitchen", "price": 25, "rating": 4.2, "brand": "FlavorOrganize"},
            {"id": 30, "name": "Blender", "category": "kitchen", "price": 70, "rating": 4.3, "brand": "BlendPro"}
        ]
    
    def search_by_category(self, category: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Search products by category"""
        category_products = [p for p in self.products if p['category'].lower() == category.lower()]
        return category_products[:max_results]
    
    def rank_products_by_preferences(self, products: List[Dict[str, Any]], buyer_profile: BuyerProfile) -> List[Dict[str, Any]]:
        """Rank products based on buyer's price range and preferences"""
        if not products:
            return products
        
        price_range = buyer_profile.get_price_range()
        target_price = price_range['avg']
        
        # Calculate score based on price proximity and rating
        def calculate_score(product):
            price_score = 1 / (1 + abs(product['price'] - target_price) / target_price)
            rating_score = product['rating'] / 5.0
            return (price_score * 0.6) + (rating_score * 0.4)  # Weight price more heavily
        
        # Sort by score (descending)
        ranked_products = sorted(products, key=calculate_score, reverse=True)
        return ranked_products
    
    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """Get a specific product by ID"""
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None
    
    def get_all_categories(self) -> List[str]:
        """Get all available product categories"""
        categories = set(product['category'] for product in self.products)
        return sorted(list(categories)) 