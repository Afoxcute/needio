from data_storage.ipfs_handler import IPFSStorageHandler
from typing import Dict, Optional
from cryptography.fernet import Fernet

class FoodBankDataCollector:
    def __init__(self, food_bank_id: str, encryption_key: Optional[str] = None, 
                 ipfs_host: str = '/ip4/127.0.0.1/tcp/5001'):
        """
        Initialize the data collector for a specific food bank.
        
        Args:
            food_bank_id: Unique identifier for the food bank
            encryption_key: Optional encryption key for sensitive data
            ipfs_host: IPFS daemon address
        """
        self.food_bank_id = food_bank_id
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.ipfs_storage = IPFSStorageHandler(ipfs_host)
        self.setup_logging()

    async def store_client_demographics(self, demographics: Dict) -> str:
        """Store demographic data on IPFS"""
        return await self.ipfs_storage.store_data(
            data=demographics,
            data_type="demographics"
        )

    async def store_inventory_data(self, inventory_data: Dict) -> str:
        """Store inventory data on IPFS"""
        return await self.ipfs_storage.store_data(
            data=inventory_data,
            data_type="inventory"
        )

    async def store_distribution_data(self, distribution_data: Dict) -> str:
        """Store distribution data on IPFS"""
        return await self.ipfs_storage.store_data(
            data=distribution_data,
            data_type="distribution"
        ) 