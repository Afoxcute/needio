import logging
from typing import Dict, List, Optional
from datetime import datetime
import json
from near_api.account import Account
from near_api.signer import Signer
from near_api.contract import Contract

class RewardHandler:
    def __init__(self, 
                 contract_id: str,
                 account_id: str,
                 private_key: str,
                 network: str = 'testnet'):
        """
        Initialize the reward handler.
        
        Args:
            contract_id: NEAR contract ID for rewards
            account_id: NEAR account ID
            private_key: Private key for signing transactions
            network: NEAR network (testnet/mainnet)
        """
        self.contract_id = contract_id
        self.account_id = account_id
        self.network = network
        self.setup_logging()
        
        # Initialize NEAR account
        self.signer = Signer(account_id, private_key)
        self.account = Account(self.signer, network)
        
        # Initialize reward contract
        self.contract = Contract(self.account, contract_id)

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'rewards_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('RewardHandler')

    async def calculate_rewards(self, 
                              food_bank_id: str,
                              contribution_metrics: Dict[str, float]) -> float:
        """
        Calculate rewards based on contribution metrics.
        
        Args:
            food_bank_id: ID of the food bank
            contribution_metrics: Dictionary of contribution metrics
            
        Returns:
            Calculated reward amount
        """
        try:
            # Weights for different contribution factors
            weights = {
                'data_quality': 0.3,
                'model_improvement': 0.4,
                'participation_frequency': 0.3
            }
            
            # Calculate weighted score
            score = sum(
                metrics * weights[metric_type]
                for metric_type, metrics in contribution_metrics.items()
            )
            
            # Convert score to tokens (example conversion)
            token_reward = score * 100  # 100 tokens per point
            
            self.logger.info(f"Calculated reward of {token_reward} tokens for {food_bank_id}")
            return token_reward

        except Exception as e:
            self.logger.error(f"Error calculating rewards: {str(e)}")
            raise

    async def distribute_rewards(self, 
                               food_bank_id: str,
                               amount: float,
                               reward_type: str) -> str:
        """
        Distribute rewards to a food bank.
        
        Args:
            food_bank_id: ID of the food bank
            amount: Amount of tokens to distribute
            reward_type: Type of reward (tokens/credits)
            
        Returns:
            Transaction hash
        """
        try:
            # Call the reward contract
            result = await self.contract.function_call(
                "distribute_reward",
                {
                    "food_bank_id": food_bank_id,
                    "amount": str(amount),
                    "reward_type": reward_type,
                    "timestamp": datetime.now().isoformat()
                },
                gas=300000000000000  # Gas limit
            )
            
            self.logger.info(f"Distributed {amount} {reward_type} to {food_bank_id}")
            return result['transaction']['hash']

        except Exception as e:
            self.logger.error(f"Error distributing rewards: {str(e)}")
            raise

    async def get_reward_balance(self, food_bank_id: str) -> Dict[str, float]:
        """
        Get reward balance for a food bank.
        
        Args:
            food_bank_id: ID of the food bank
            
        Returns:
            Dictionary of reward balances by type
        """
        try:
            result = await self.contract.view_function(
                "get_reward_balance",
                {"food_bank_id": food_bank_id}
            )
            return result

        except Exception as e:
            self.logger.error(f"Error getting reward balance: {str(e)}")
            raise

    async def redeem_rewards(self, 
                           food_bank_id: str,
                           amount: float,
                           reward_type: str,
                           redemption_option: str) -> str:
        """
        Redeem rewards for benefits.
        
        Args:
            food_bank_id: ID of the food bank
            amount: Amount to redeem
            reward_type: Type of reward to redeem
            redemption_option: What the rewards are being redeemed for
            
        Returns:
            Transaction hash
        """
        try:
            result = await self.contract.function_call(
                "redeem_rewards",
                {
                    "food_bank_id": food_bank_id,
                    "amount": str(amount),
                    "reward_type": reward_type,
                    "redemption_option": redemption_option,
                    "timestamp": datetime.now().isoformat()
                },
                gas=300000000000000
            )
            
            self.logger.info(
                f"Redeemed {amount} {reward_type} for {redemption_option} "
                f"by {food_bank_id}"
            )
            return result['transaction']['hash']

        except Exception as e:
            self.logger.error(f"Error redeeming rewards: {str(e)}")
            raise

    async def get_redemption_options(self) -> List[Dict]:
        """
        Get available redemption options.
        
        Returns:
            List of redemption options and their costs
        """
        try:
            return await self.contract.view_function("get_redemption_options", {})

        except Exception as e:
            self.logger.error(f"Error getting redemption options: {str(e)}")
            raise 