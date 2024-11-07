import asyncio
from incentives.reward_handler import RewardHandler

async def main():
    # Initialize reward handler
    reward_handler = RewardHandler(
        contract_id="rewards.testnet",
        account_id="your-account.testnet",
        private_key="your-private-key",
        network="testnet"
    )

    # Example food bank and contribution metrics
    food_bank_id = "FB001"
    contribution_metrics = {
        "data_quality": 0.85,  # 85% quality score
        "model_improvement": 0.92,  # 92% improvement contribution
        "participation_frequency": 0.78  # 78% participation rate
    }

    # Calculate rewards
    reward_amount = await reward_handler.calculate_rewards(
        food_bank_id,
        contribution_metrics
    )
    print(f"Calculated reward amount: {reward_amount} tokens")

    # Distribute rewards
    tx_hash = await reward_handler.distribute_rewards(
        food_bank_id,
        reward_amount,
        "tokens"
    )
    print(f"Rewards distributed. Transaction hash: {tx_hash}")

    # Check reward balance
    balance = await reward_handler.get_reward_balance(food_bank_id)
    print(f"Current reward balance: {balance}")

    # Get redemption options
    options = await reward_handler.get_redemption_options()
    print("\nAvailable redemption options:")
    for option in options:
        print(f"- {option['name']}: {option['cost']} tokens")

    # Redeem rewards for a benefit
    if balance.get("tokens", 0) >= 100:
        redeem_tx = await reward_handler.redeem_rewards(
            food_bank_id,
            100,
            "tokens",
            "supplier_discount"
        )
        print(f"\nRedeemed 100 tokens for supplier discount.")
        print(f"Redemption transaction hash: {redeem_tx}")

if __name__ == "__main__":
    asyncio.run(main()) 