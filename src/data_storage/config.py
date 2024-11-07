from dataclasses import dataclass
from typing import Dict

@dataclass
class NearLakeConfig:
    # AWS S3 configuration
    BUCKET_NAME: str = "food-bank-federated-learning"
    AWS_REGION: str = "us-east-1"
    
    # Storage policies
    RETENTION_PERIOD_DAYS: int = 365
    
    # Data types and their storage requirements
    DATA_TYPES: Dict[str, Dict] = {
        'demographics': {
            'encrypted': True,
            'retention_days': 365
        },
        'inventory': {
            'encrypted': False,
            'retention_days': 180
        },
        'distribution': {
            'encrypted': False,
            'retention_days': 180
        }
    }

    # QueryAPI configuration
    GRAPHQL_ENDPOINT: str = "https://near-queryapi.yourdomain.com/graphql" 