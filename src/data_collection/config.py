from dataclasses import dataclass
from typing import List

@dataclass
class DataCollectionConfig:
    # Food categories for standardization
    FOOD_CATEGORIES: List[str] = (
        "Fruits and Vegetables",
        "Grains and Cereals",
        "Protein Foods",
        "Dairy Products",
        "Canned Goods",
        "Beverages",
        "Snacks",
        "Baby Food",
        "Condiments",
        "Other"
    )

    # Employment status categories
    EMPLOYMENT_STATUSES: List[str] = (
        "Full-time",
        "Part-time",
        "Unemployed",
        "Retired",
        "Student",
        "Other"
    )

    # Data collection frequency (in hours)
    INVENTORY_UPDATE_FREQUENCY: int = 24
    DISTRIBUTION_UPDATE_FREQUENCY: int = 24
    DEMOGRAPHICS_UPDATE_FREQUENCY: int = 168  # Weekly

    # Privacy settings
    MIN_ANONYMIZATION_THRESHOLD: int = 5  # Minimum number of records to report
    ZIP_CODE_DIGITS_TO_KEEP: int = 3  # Number of ZIP code digits to retain 