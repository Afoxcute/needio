import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

class QueryApiHandler:
    def __init__(self, endpoint_url: str, api_key: Optional[str] = None):
        """
        Initialize QueryAPI handler for food bank data.
        
        Args:
            endpoint_url: GraphQL endpoint URL
            api_key: Optional API key for authentication
        """
        self.endpoint = endpoint_url
        self.api_key = api_key
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the QueryAPI handler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'query_api_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('QueryAPI')

    async def index_food_bank_data(self, data: Dict, data_type: str) -> bool:
        """
        Index food bank data using the QueryAPI.
        
        Args:
            data: The data to index
            data_type: Type of data (demographics, inventory, distribution)
            
        Returns:
            bool: Success status
        """
        mutation = """
        mutation IndexFoodBankData($data: JSON!, $dataType: String!) {
            indexFoodBankData(data: $data, dataType: $dataType) {
                success
                message
            }
        }
        """
        
        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            response = requests.post(
                self.endpoint,
                headers=headers,
                json={
                    'query': mutation,
                    'variables': {
                        'data': json.dumps(data),
                        'dataType': data_type
                    }
                }
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get('data', {}).get('indexFoodBankData', {}).get('success'):
                self.logger.info(f"Successfully indexed {data_type} data")
                return True
            else:
                self.logger.error(f"Failed to index data: {result}")
                return False

        except Exception as e:
            self.logger.error(f"Error indexing data: {str(e)}")
            raise

    async def query_food_bank_data(
        self,
        food_bank_id: str,
        data_type: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Query food bank data using GraphQL.
        
        Args:
            food_bank_id: ID of the food bank
            data_type: Type of data to query
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            List of matching data entries
        """
        query = """
        query FoodBankData(
            $foodBankId: String!
            $dataType: String!
            $startDate: String
            $endDate: String
        ) {
            foodBankData(
                foodBankId: $foodBankId
                dataType: $dataType
                startDate: $startDate
                endDate: $endDate
            ) {
                id
                timestamp
                data
                metadata
            }
        }
        """
        
        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            response = requests.post(
                self.endpoint,
                headers=headers,
                json={
                    'query': query,
                    'variables': {
                        'foodBankId': food_bank_id,
                        'dataType': data_type,
                        'startDate': start_date,
                        'endDate': end_date
                    }
                }
            )
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"Retrieved {data_type} data for food bank {food_bank_id}")
            return data.get('data', {}).get('foodBankData', [])

        except Exception as e:
            self.logger.error(f"Error querying data: {str(e)}")
            raise

    async def get_aggregated_stats(
        self,
        data_type: str,
        metric: str,
        group_by: str = 'day'
    ) -> List[Dict]:
        """
        Get aggregated statistics from food bank data.
        
        Args:
            data_type: Type of data to aggregate
            metric: Metric to aggregate (e.g., 'clients_served', 'inventory_level')
            group_by: Time period to group by ('day', 'week', 'month')
            
        Returns:
            List of aggregated statistics
        """
        query = """
        query AggregatedStats($dataType: String!, $metric: String!, $groupBy: String!) {
            aggregatedStats(dataType: $dataType, metric: $metric, groupBy: $groupBy) {
                timestamp
                value
                count
            }
        }
        """
        
        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            response = requests.post(
                self.endpoint,
                headers=headers,
                json={
                    'query': query,
                    'variables': {
                        'dataType': data_type,
                        'metric': metric,
                        'groupBy': group_by
                    }
                }
            )
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"Retrieved aggregated stats for {metric}")
            return data.get('data', {}).get('aggregatedStats', [])

        except Exception as e:
            self.logger.error(f"Error getting aggregated stats: {str(e)}")
            raise 