import json
import os
from typing import Dict, Any, Optional
from models.buyer import BuyerProfile
from config import Config

class MemoryService:
    """Service for handling buyer history storage and retrieval"""
    
    def __init__(self):
        self.memory_type = Config.MEMORY_TYPE
        self.file_path = Config.MEMORY_FILE_PATH
        self.in_memory_storage = {}
        
        # Initialize file storage if needed
        if self.memory_type == "file" and not os.path.exists(self.file_path):
            self._initialize_file_storage()
    
    def _initialize_file_storage(self):
        """Initialize empty file storage"""
        with open(self.file_path, 'w') as f:
            json.dump({}, f)
    
    def store_buyer_profile(self, buyer_profile: BuyerProfile) -> bool:
        """Store buyer profile in memory"""
        try:
            if self.memory_type == "memory":
                self.in_memory_storage[buyer_profile.user_id] = buyer_profile.to_dict()
            elif self.memory_type == "file":
                # Load existing data
                data = {}
                if os.path.exists(self.file_path):
                    with open(self.file_path, 'r') as f:
                        data = json.load(f)
                
                # Update with new profile
                data[buyer_profile.user_id] = buyer_profile.to_dict()
                
                # Save back to file
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error storing buyer profile: {e}")
            return False
    
    def get_buyer_profile(self, user_id: str) -> Optional[BuyerProfile]:
        """Retrieve buyer profile from memory"""
        try:
            if self.memory_type == "memory":
                if user_id in self.in_memory_storage:
                    return BuyerProfile.from_json(self.in_memory_storage[user_id])
            elif self.memory_type == "file":
                if os.path.exists(self.file_path):
                    with open(self.file_path, 'r') as f:
                        data = json.load(f)
                        if user_id in data:
                            return BuyerProfile.from_json(data[user_id])
            return None
        except Exception as e:
            print(f"Error retrieving buyer profile: {e}")
            return None
    
    def update_buyer_history(self, user_id: str, transaction: Dict[str, Any]) -> bool:
        """Add a new transaction to buyer history"""
        try:
            buyer_profile = self.get_buyer_profile(user_id)
            if buyer_profile:
                buyer_profile.add_transaction(transaction)
                return self.store_buyer_profile(buyer_profile)
            return False
        except Exception as e:
            print(f"Error updating buyer history: {e}")
            return False
    
    def get_all_buyers(self) -> Dict[str, Dict[str, Any]]:
        """Get all stored buyer profiles"""
        try:
            if self.memory_type == "memory":
                return self.in_memory_storage.copy()
            elif self.memory_type == "file":
                if os.path.exists(self.file_path):
                    with open(self.file_path, 'r') as f:
                        return json.load(f)
            return {}
        except Exception as e:
            print(f"Error retrieving all buyers: {e}")
            return {} 