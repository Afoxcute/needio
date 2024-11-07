import asyncio
from data_collection.data_collector import FoodBankDataCollector
from ml.federated_learning import FederatedLearningCoordinator
from ml.local_trainer import LocalTrainer
from incentives.reward_handler import RewardHandler

async def main():
    # Initialize food bank data collector
    collector = FoodBankDataCollector(food_bank_id="FB001")

    # Collect sample data
    demographic_data = collector.collect_client_demographics(
        age=35,
        family_size=4,
        employment_status="Full-time",
        zip_code="12345"
    )

    inventory_items = [
        {
            "category": "Fruits and Vegetables",
            "quantity": 100,
            "perishable": True,
            "min_stock": 50
        },
        {
            "category": "Canned Goods",
            "quantity": 200,
            "perishable": False,
            "min_stock": 100
        }
    ]

    inventory_data = collector.collect_inventory_data(inventory_items)

    # Initialize federated learning components
    input_shape = (10,)  # Example input shape
    local_trainer = LocalTrainer(
        food_bank_id="FB001",
        input_shape=input_shape
    )

    coordinator = FederatedLearningCoordinator(
        num_food_banks=3,
        input_shape=input_shape
    )

    # Initialize reward handler
    reward_handler = RewardHandler(
        contract_id="rewards.testnet",
        account_id="your-account.testnet",
        private_key="your-private-key"
    )

    # Run the system
    print("Starting federated learning system...")
    print(f"Collected demographic data: {demographic_data}")
    print(f"Collected inventory data: {inventory_data}")

if __name__ == "__main__":
    asyncio.run(main()) 