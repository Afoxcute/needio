import json
import boto3
from typing import Dict, Any
import logging
from datetime import datetime
from botocore.exceptions import ClientError

class NearLakeHandler:
    def __init__(self, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        """
        Initialize Near Lake storage handler.
        
        Args:
            bucket_name: AWS S3 bucket name
            aws_access_key_id: AWS access key
            aws_secret_access_key: AWS secret key
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the Near Lake handler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'near_lake_storage_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('NearLakeStorage')

    async def store_data(self, data: Dict[str, Any], data_type: str) -> str:
        """
        Store data in Near Lake (S3).
        
        Args:
            data: Dictionary containing the data to store
            data_type: Type of data being stored
            
        Returns:
            S3 object key
        """
        try:
            # Add metadata
            data_with_metadata = {
                "data": data,
                "type": data_type,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }

            # Create unique key for S3 object
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_key = f"{data_type}/{timestamp}.json"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=json.dumps(data_with_metadata),
                ContentType='application/json'
            )

            self.logger.info(f"Stored {data_type} data with key: {object_key}")
            return object_key

        except ClientError as e:
            self.logger.error(f"Failed to store data in Near Lake: {str(e)}")
            raise

    async def retrieve_data(self, object_key: str) -> Dict[str, Any]:
        """
        Retrieve data from Near Lake (S3).
        
        Args:
            object_key: S3 object key
            
        Returns:
            Dictionary containing the retrieved data
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            data = json.loads(response['Body'].read())

            self.logger.info(f"Retrieved data from key: {object_key}")
            return data

        except ClientError as e:
            self.logger.error(f"Failed to retrieve data from Near Lake: {str(e)}")
            raise 