import ipfshttpclient
import json
from typing import Dict, Any
import logging
from datetime import datetime

class IPFSStorageHandler:
    def __init__(self, ipfs_host: str = '/ip4/127.0.0.1/tcp/5001'):
        """
        Initialize IPFS storage handler.
        
        Args:
            ipfs_host: IPFS daemon address
        """
        self.client = ipfshttpclient.connect(ipfs_host)
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the IPFS handler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'ipfs_storage_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('IPFSStorage')

    async def store_data(self, data: Dict[str, Any], data_type: str) -> str:
        """
        Store data on IPFS.
        
        Args:
            data: Dictionary containing the data to store
            data_type: Type of data being stored (e.g., 'demographics', 'inventory')
            
        Returns:
            IPFS hash of the stored data
        """
        try:
            # Add metadata
            data_with_metadata = {
                "data": data,
                "type": data_type,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }

            # Convert to JSON and store on IPFS
            json_data = json.dumps(data_with_metadata)
            ipfs_info = await self.client.add(json_data)
            ipfs_hash = ipfs_info['Hash']

            self.logger.info(f"Stored {data_type} data with IPFS hash: {ipfs_hash}")
            return ipfs_hash

        except Exception as e:
            self.logger.error(f"Failed to store data on IPFS: {str(e)}")
            raise

    async def retrieve_data(self, ipfs_hash: str) -> Dict[str, Any]:
        """
        Retrieve data from IPFS.
        
        Args:
            ipfs_hash: IPFS hash of the data to retrieve
            
        Returns:
            Dictionary containing the retrieved data
        """
        try:
            # Get data from IPFS
            ipfs_data = await self.client.cat(ipfs_hash)
            data = json.loads(ipfs_data)

            self.logger.info(f"Retrieved data from IPFS hash: {ipfs_hash}")
            return data

        except Exception as e:
            self.logger.error(f"Failed to retrieve data from IPFS: {str(e)}")
            raise

    async def pin_data(self, ipfs_hash: str):
        """
        Pin data to ensure it's kept in the IPFS network.
        
        Args:
            ipfs_hash: IPFS hash of the data to pin
        """
        try:
            await self.client.pin.add(ipfs_hash)
            self.logger.info(f"Pinned data with hash: {ipfs_hash}")
        except Exception as e:
            self.logger.error(f"Failed to pin data: {str(e)}")
            raise 