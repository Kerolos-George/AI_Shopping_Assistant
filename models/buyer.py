from typing import Dict, List, Any
from dataclasses import dataclass
import json

@dataclass
class BuyerProfile:
    """Data class representing a buyer's profile and history"""
    user_id: str
    history: List[Dict[str, Any]]
    
    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'BuyerProfile':
        """Create BuyerProfile from JSON data"""
        return cls(
            user_id=json_data.get('user_id', ''),
            history=json_data.get('history', [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert BuyerProfile to dictionary"""
        return {
            'user_id': self.user_id,
            'history': self.history
        }
    
    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        """Add a new transaction to buyer history"""
        self.history.append(transaction)
    
    def get_product_categories(self) -> List[str]:
        """Extract unique product categories from history"""
        categories = set()
        for item in self.history:
            if 'category' in item:
                categories.add(item['category'])
        return list(categories)
    
    def get_price_range(self) -> Dict[str, float]:
        """Calculate price range from purchase history"""
        prices = []
        for item in self.history:
            if 'price' in item:
                prices.append(float(item['price']))
        
        if not prices:
            return {'min': 0, 'max': 1000, 'avg': 100}
        
        return {
            'min': min(prices),
            'max': max(prices),
            'avg': sum(prices) / len(prices)
        } 