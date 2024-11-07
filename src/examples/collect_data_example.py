from data_collection.data_collector import FoodBankDataCollector
from data_collection.validators import DataValidator

# Initialize the data collector
collector = FoodBankDataCollector(food_bank_id="FB001")

# Collect demographic data
demographic_data = collector.collect_client_demographics(
    age=35,
    family_size=4,
    employment_status="Full-time",
    zip_code="12345"
)

# Collect inventory data
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

# Validate the collected data
validator = DataValidator()
is_valid_demographic = validator.validate_demographic_data(demographic_data)
is_valid_inventory = validator.validate_inventory_data(inventory_data)

print(f"Demographic data valid: {is_valid_demographic}")
print(f"Inventory data valid: {is_valid_inventory}") 