import tensorflow as tf
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import json
import os
from cryptography.fernet import Fernet
import yaml
from tensorflow.keras.models import save_model, load_model

class GlobalModelAggregator:
    def __init__(self, 
                 model_name: str,
                 version: str,
                 input_shape: tuple,
                 metadata: Dict = None):
        """
        Initialize the global model aggregator.
        
        Args:
            model_name: Name of the model
            version: Model version
            input_shape: Shape of input features
            metadata: Additional model metadata
        """
        self.model_name = model_name
        self.version = version
        self.input_shape = input_shape
        self.metadata = metadata or {}
        self.setup_logging()
        
        # Initialize model registry
        self.model_registry_path = "model_registry"
        os.makedirs(self.model_registry_path, exist_ok=True)

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'global_model_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('GlobalModelAggregator')

    def aggregate_models(self, 
                        local_models: List[tf.keras.Model], 
                        weights: Optional[List[float]] = None) -> tf.keras.Model:
        """
        Aggregate multiple local models into a global model.
        
        Args:
            local_models: List of local models to aggregate
            weights: Optional weights for weighted averaging
            
        Returns:
            Aggregated global model
        """
        try:
            if weights is None:
                weights = [1.0 / len(local_models)] * len(local_models)

            # Get weights from all models
            all_weights = [model.get_weights() for model in local_models]

            # Perform weighted averaging of weights
            avg_weights = []
            for weights_list_tuple in zip(*all_weights):
                layer_weights = []
                for weights_tuple in zip(*weights_list_tuple):
                    layer_weights.append(
                        np.average([w * weight for w, weight in zip(weights_tuple, weights)], axis=0)
                    )
                avg_weights.append(layer_weights)

            # Create a new model with the same architecture
            global_model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu', input_shape=self.input_shape),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])

            # Set the averaged weights
            global_model.set_weights(avg_weights)
            
            self.logger.info("Successfully aggregated local models into global model")
            return global_model

        except Exception as e:
            self.logger.error(f"Error aggregating models: {str(e)}")
            raise

    def save_model_release(self, 
                          model: tf.keras.Model, 
                          performance_metrics: Dict[str, float],
                          release_notes: str) -> str:
        """
        Save a new model release with documentation.
        
        Args:
            model: The global model to save
            performance_metrics: Model performance metrics
            release_notes: Release notes and documentation
            
        Returns:
            Path to saved model release
        """
        try:
            # Create release directory
            release_dir = os.path.join(
                self.model_registry_path,
                f"{self.model_name}_v{self.version}"
            )
            os.makedirs(release_dir, exist_ok=True)

            # Save model
            model_path = os.path.join(release_dir, "model")
            save_model(model, model_path)

            # Save metadata and documentation
            metadata = {
                "name": self.model_name,
                "version": self.version,
                "created_at": datetime.now().isoformat(),
                "input_shape": self.input_shape,
                "performance_metrics": performance_metrics,
                "release_notes": release_notes,
                **self.metadata
            }

            metadata_path = os.path.join(release_dir, "metadata.yaml")
            with open(metadata_path, 'w') as f:
                yaml.dump(metadata, f)

            self.logger.info(f"Saved model release to {release_dir}")
            return release_dir

        except Exception as e:
            self.logger.error(f"Error saving model release: {str(e)}")
            raise

    def load_model_release(self, version: Optional[str] = None) -> Tuple[tf.keras.Model, Dict]:
        """
        Load a model release.
        
        Args:
            version: Optional specific version to load
            
        Returns:
            Tuple of (model, metadata)
        """
        try:
            # Use latest version if not specified
            if version is None:
                version = self.version

            release_dir = os.path.join(
                self.model_registry_path,
                f"{self.model_name}_v{version}"
            )

            # Load model
            model_path = os.path.join(release_dir, "model")
            model = load_model(model_path)

            # Load metadata
            metadata_path = os.path.join(release_dir, "metadata.yaml")
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)

            self.logger.info(f"Loaded model release from {release_dir}")
            return model, metadata

        except Exception as e:
            self.logger.error(f"Error loading model release: {str(e)}")
            raise

    def generate_model_card(self, 
                          model_path: str, 
                          performance_metrics: Dict[str, float],
                          intended_use: str,
                          limitations: str) -> str:
        """
        Generate a model card for the release.
        
        Args:
            model_path: Path to the saved model
            performance_metrics: Model performance metrics
            intended_use: Description of intended use
            limitations: Known limitations
            
        Returns:
            Path to generated model card
        """
        try:
            model_card = {
                "model_details": {
                    "name": self.model_name,
                    "version": self.version,
                    "created_at": datetime.now().isoformat(),
                    "type": "Food Insecurity Prediction Model",
                },
                "model_parameters": {
                    "input_shape": self.input_shape,
                    "architecture": "Neural Network",
                    "framework": "TensorFlow",
                },
                "performance_metrics": performance_metrics,
                "intended_use": intended_use,
                "limitations": limitations,
                "ethical_considerations": {
                    "privacy": "Model trained using federated learning with differential privacy",
                    "bias": "Model should be regularly evaluated for demographic biases",
                },
                "additional_metadata": self.metadata
            }

            # Save model card
            card_path = os.path.join(model_path, "model_card.yaml")
            with open(card_path, 'w') as f:
                yaml.dump(model_card, f)

            self.logger.info(f"Generated model card at {card_path}")
            return card_path

        except Exception as e:
            self.logger.error(f"Error generating model card: {str(e)}")
            raise 