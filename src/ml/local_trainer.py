import tensorflow as tf
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime
from differential_privacy import dp_optimizer

class LocalTrainer:
    def __init__(self, 
                 food_bank_id: str,
                 input_shape: tuple,
                 dp_epsilon: float = 1.0):
        """
        Initialize local trainer for a food bank.
        
        Args:
            food_bank_id: Unique identifier for the food bank
            input_shape: Shape of input features
            dp_epsilon: Privacy budget for differential privacy
        """
        self.food_bank_id = food_bank_id
        self.input_shape = input_shape
        self.dp_epsilon = dp_epsilon
        self.setup_logging()
        
        # Initialize local model
        self.local_model = self._build_model()

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'local_training_{self.food_bank_id}_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger(f'LocalTrainer_{self.food_bank_id}')

    def _build_model(self) -> tf.keras.Model:
        """Build the local model with privacy-preserving training"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=self.input_shape),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Use DP-SGD optimizer
        optimizer = dp_optimizer.DPKerasAdamOptimizer(
            l2_norm_clip=1.0,
            noise_multiplier=1.0,
            num_microbatches=1,
            learning_rate=0.001
        )

        model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model

    def train_local_model(self, 
                         features: np.ndarray, 
                         labels: np.ndarray,
                         epochs: int = 5,
                         batch_size: int = 32) -> Dict[str, float]:
        """
        Train the local model with differential privacy.
        
        Args:
            features: Training features
            labels: Training labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            Training history
        """
        try:
            history = self.local_model.fit(
                features,
                labels,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                verbose=1
            )
            
            self.logger.info(f"Completed local training for {epochs} epochs")
            return history.history

        except Exception as e:
            self.logger.error(f"Error in local training: {str(e)}")
            raise

    def get_model_update(self) -> List[np.ndarray]:
        """
        Get the local model weights for sharing.
        
        Returns:
            List of model weight arrays
        """
        return self.local_model.get_weights()

    def update_local_model(self, global_weights: List[np.ndarray]):
        """
        Update local model with global weights.
        
        Args:
            global_weights: Global model weights
        """
        try:
            self.local_model.set_weights(global_weights)
            self.logger.info("Updated local model with global weights")
        except Exception as e:
            self.logger.error(f"Error updating local model: {str(e)}")
            raise 