import tensorflow as tf
from ml.global_model_aggregator import GlobalModelAggregator
from ml.local_trainer import LocalTrainer

async def main():
    # Initialize local trainers
    food_banks = ["FB001", "FB002", "FB003"]
    input_shape = (10,)  # Example input shape
    local_trainers = [
        LocalTrainer(fb_id, input_shape) 
        for fb_id in food_banks
    ]

    # Train local models
    local_models = []
    for trainer in local_trainers:
        # Example training data
        features = tf.random.normal((100, 10))
        labels = tf.random.uniform((100, 1))
        
        trainer.train_local_model(features, labels)
        local_models.append(trainer.local_model)

    # Initialize global model aggregator
    aggregator = GlobalModelAggregator(
        model_name="food_insecurity_predictor",
        version="1.0.0",
        input_shape=input_shape,
        metadata={
            "description": "Food insecurity prediction model",
            "contributors": food_banks
        }
    )

    # Aggregate local models
    global_model = aggregator.aggregate_models(local_models)

    # Example performance metrics
    performance_metrics = {
        "accuracy": 0.85,
        "precision": 0.83,
        "recall": 0.87,
        "auc": 0.89
    }

    # Save model release
    release_path = aggregator.save_model_release(
        model=global_model,
        performance_metrics=performance_metrics,
        release_notes="Initial release of food insecurity prediction model"
    )

    # Generate model card
    model_card_path = aggregator.generate_model_card(
        model_path=release_path,
        performance_metrics=performance_metrics,
        intended_use="""
        This model is intended to help predict food insecurity trends and optimize
        food distribution. It can be used by food banks, policymakers, and aid
        organizations to better understand and respond to community needs.
        """,
        limitations="""
        1. Model performance may vary across different demographic groups
        2. Predictions should be used as one of many inputs in decision-making
        3. Regular retraining is recommended as patterns may change over time
        """
    )

    print(f"Model released at: {release_path}")
    print(f"Model card available at: {model_card_path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 