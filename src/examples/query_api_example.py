import asyncio
from data_storage.query_handler import QueryApiHandler
from datetime import datetime, timedelta

async def main():
    # Initialize QueryAPI handler
    query_handler = QueryApiHandler(
        endpoint_url="https://your-queryapi-endpoint.com/graphql",
        api_key="your_api_key"
    )

    # Index some sample data
    sample_data = {
        "food_bank_id": "FB001",
        "clients_served": 150,
        "inventory_level": 1000,
        "timestamp": datetime.now().isoformat()
    }
    
    success = await query_handler.index_food_bank_data(
        data=sample_data,
        data_type="distribution"
    )
    print(f"Data indexing {'successful' if success else 'failed'}")

    # Query data for the last 7 days
    end_date = datetime.now().isoformat()
    start_date = (datetime.now() - timedelta(days=7)).isoformat()
    
    data = await query_handler.query_food_bank_data(
        food_bank_id="FB001",
        data_type="distribution",
        start_date=start_date,
        end_date=end_date
    )
    print(f"Retrieved {len(data)} records")

    # Get aggregated stats
    stats = await query_handler.get_aggregated_stats(
        data_type="distribution",
        metric="clients_served",
        group_by="day"
    )
    print("Daily client statistics:", stats)

if __name__ == "__main__":
    asyncio.run(main()) 