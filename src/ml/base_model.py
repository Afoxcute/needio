import tensorflow as tf
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import logging

class FoodInsecurityModel:
    def __init__(self, input_shape: Tuple[int, ...]):
        """
        Initialize the food insecurity prediction model.
        
        Args:
            input_shape: Shape of input features
        """
        self.model = self._build_model(input_shape)
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the model"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'model_training_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('FoodInsecurityModel')

    def _build_model(self, input_shape: Tuple[int, ...]) -> tf.keras.Model:
        """
        Build the neural network model.
        
        Args:
            input_shape: Shape of input features
            
        Returns:
            Compiled TensorFlow model
        """
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC()]
        )

        return model

    def preprocess_data(self, data: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess raw data for model training.
        
        Args:
            data: Dictionary containing raw data
            
        Returns:
            Tuple of features and labels arrays
        """
        try:
            # Extract features
            features = []
            labels = []

            # Process demographic data
            if 'demographics' in data:
                for entry in data['demographics']:
                    feature_vector = [
                        entry['family_size'],
                        entry['employment_status_encoded'],
                        entry['zip_code_stats']['poverty_rate'],
                        entry['zip_code_stats']['unemployment_rate']
                    ]
                    features.append(feature_vector)
                    
                    # Label is 1 if client needed emergency food assistance
                    labels.append(entry['needed_assistance'])

            features_array = np.array(features)
            labels_array = np.array(labels)

            self.logger.info(f"Preprocessed {len(features)} data points")
            return features_array, labels_array

        except Exception as e:
            self.logger.error(f"Error preprocessing data: {str(e)}")
            raise

    def train(self, 
             features: np.ndarray, 
             labels: np.ndarray, 
             epochs: int = 10, 
             batch_size: int = 32) -> Dict:
        """
        Train the model on local data.
        
        Args:
            features: Input features
            labels: Target labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            Dictionary containing training history
        """
        try:
            history = self.model.fit(
                features,
                labels,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                verbose=1
            )

            self.logger.info("Model training completed successfully")
            return history.history

        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            raise

    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model.
        
        Args:
            features: Input features
            
        Returns:
            Array of predictions
        """
        try:
            predictions = self.model.predict(features)
            self.logger.info(f"Generated predictions for {len(features)} samples")
            return predictions

        except Exception as e:
            self.logger.error(f"Error generating predictions: {str(e)}")
            raise

    def get_model_weights(self) -> List[np.ndarray]:
        """
        Get the current model weights.
        
        Returns:
            List of model weight arrays
        """
        return self.model.get_weights()

    def set_model_weights(self, weights: List[np.ndarray]):
        """
        Set the model weights.
        
        Args:
            weights: List of weight arrays to set
        """
        self.model.set_weights(weights)
        self.logger.info("Updated model weights")

    def evaluate(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        """
        Evaluate the model performance.
        
        Args:
            features: Input features
            labels: True labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        try:
            loss, accuracy, auc = self.model.evaluate(features, labels, verbose=0)
            metrics = {
                'loss': loss,
                'accuracy': accuracy,
                'auc': auc
            }
            
            self.logger.info(f"Model evaluation metrics: {metrics}")
            return metrics

        except Exception as e:
            self.logger.error(f"Error evaluating model: {str(e)}")
            raise

    def save_model(self, filepath: str):
        """Save the model to disk"""
        try:
            self.model.save(filepath)
            self.logger.info(f"Model saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            raise

    def load_model(self, filepath: str):
        """Load the model from disk"""
        try:
            self.model = tf.keras.models.load_model(filepath)
            self.logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise 