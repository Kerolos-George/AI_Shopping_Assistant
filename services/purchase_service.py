from typing import Dict, Any, List
import datetime
import json
from models.buyer import BuyerProfile
from services.memory_service import MemoryService
from services.catalog_service import CatalogService

class PurchaseService:
    """Service for handling simulated purchases"""
    
    def __init__(self, memory_service: MemoryService, catalog_service: CatalogService):
        self.memory_service = memory_service
        self.catalog_service = catalog_service
        self.transaction_log = []
    
    def simulate_purchase(self, user_id: str, product_id: int) -> Dict[str, Any]:
        """Simulate a product purchase"""
        try:
            # Get product details
            product = self.catalog_service.get_product_by_id(product_id)
            if not product:
                return {
                    "success": False,
                    "message": "Product not found",
                    "transaction_id": None
                }
            
            # Get buyer profile
            buyer_profile = self.memory_service.get_buyer_profile(user_id)
            if not buyer_profile:
                return {
                    "success": False,
                    "message": "Buyer profile not found",
                    "transaction_id": None
                }
            
            # Create transaction
            transaction_id = f"TXN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}_{product_id}"
            
            transaction = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "product_id": product_id,
                "product": product["name"],
                "category": product["category"],
                "price": product["price"],
                "brand": product["brand"],
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed"
            }
            
            # Log transaction
            self.transaction_log.append(transaction)
            
            # Update buyer history
            history_entry = {
                "product": product["name"],
                "category": product["category"],
                "price": product["price"],
                "date": datetime.datetime.now().isoformat()
            }
            
            success = self.memory_service.update_buyer_history(user_id, history_entry)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully purchased {product['name']} for ${product['price']}",
                    "transaction_id": transaction_id,
                    "transaction": transaction
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to update buyer history",
                    "transaction_id": transaction_id
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Purchase failed: {str(e)}",
                "transaction_id": None
            }
    
    def get_transaction_history(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get transaction history for a specific user or all users"""
        if user_id:
            return [txn for txn in self.transaction_log if txn["user_id"] == user_id]
        return self.transaction_log.copy()
    
    def get_transaction_by_id(self, transaction_id: str) -> Dict[str, Any]:
        """Get a specific transaction by ID"""
        for transaction in self.transaction_log:
            if transaction["transaction_id"] == transaction_id:
                return transaction
        return None 