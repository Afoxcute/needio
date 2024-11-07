import asyncio
from data_collection.data_collector import FoodBankDataCollector
from data_storage.config import IPFSConfig

async def main():
    # Initialize collector with IPFS support
    collector = FoodBankDataCollector(
        food_bank_id="FB001",
        ipfs_host=IPFSConfig.IPFS_HOST
    )

    # Collect and store demographic data
    demographic_data = collector.collect_client_demographics(
        age=35,
        family_size=4,
        employment_status="Full-time",
        zip_code="12345"
    )
    ipfs_hash = await collector.store_client_demographics(demographic_data)
    print(f"Demographic data stored with IPFS hash: {ipfs_hash}")

    # Collect and store inventory data
    inventory_items = [
        {
            "category": "Fruits and Vegetables",
            "quantity": 100,
            "perishable": True,
            "min_stock": 50
        }
    ]
    inventory_data = collector.collect_inventory_data(inventory_items)
    ipfs_hash = await collector.store_inventory_data(inventory_data)
    print(f"Inventory data stored with IPFS hash: {ipfs_hash}")

if __name__ == "__main__":
    asyncio.run(main()) 