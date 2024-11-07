from typing import Dict, List
import pandas as pd
from datetime import datetime

class DataValidator:
    @staticmethod
    def validate_demographic_data(data: Dict) -> bool:
        """Validate demographic data structure and values"""
        required_fields = ["client_id", "age_group", "family_size_range", 
                         "employment_status", "zip_code_prefix", "timestamp"]
        
        # Check required fields
        if not all(field in data for field in required_fields):
            return False
            
        # Validate timestamp format
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            return False
            
        return True

    @staticmethod
    def validate_inventory_data(data: Dict) -> bool:
        """Validate inventory data structure and values"""
        required_fields = ["timestamp", "food_bank_id", "inventory_summary", 
                         "stock_levels"]
        
        if not all(field in data for field in required_fields):
            return False
            
        # Validate inventory summary
        if not isinstance(data["inventory_summary"], dict):
            return False
            
        return True

    @staticmethod
    def validate_distribution_data(data: Dict) -> bool:
        """Validate distribution event data"""
        required_fields = ["event_id", "food_bank_id", "date", 
                         "clients_served", "distribution_summary"]
        
        if not all(field in data for field in required_fields):
            return False
            
        # Validate numeric fields
        if not isinstance(data["clients_served"], int):
            return False
            
        return True 