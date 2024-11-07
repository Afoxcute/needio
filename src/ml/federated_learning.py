import tensorflow as tf
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime
from cryptography.fernet import Fernet
from differential_privacy import dp_optimizer
import tenseal as ts  # For homomorphic encryption

class FederatedLearningCoordinator:
    def __init__(self, 
                 num_food_banks: int,
                 input_shape: tuple,
                 encryption_key: Optional[str] = None,
                 dp_epsilon: float = 1.0):
        """
        Initialize the federated learning coordinator.
        
        Args:
            num_food_banks: Number of participating food banks
            input_shape: Shape of input features
            encryption_key: Key for encrypting model updates
            dp_epsilon: Privacy budget for differential privacy
        """
        self.num_food_banks = num_food_banks
        self.input_shape = input_shape
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.dp_epsilon = dp_epsilon
        self.setup_logging()
        
        # Initialize global model
        self.global_model = self._build_model()
        
        # Setup homomorphic encryption context
        self.context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        self.context.global_scale = 2**40

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=f'federated_learning_{datetime.now().strftime("%Y%m%d")}.log'
        )
        self.logger = logging.getLogger('FederatedLearning')

    def _build_model(self) -> tf.keras.Model:
        """Build the neural network model"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=self.input_shape),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Use DP-SGD optimizer for differential privacy
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

    def encrypt_weights(self, weights: List[np.ndarray]) -> bytes:
        """
        Encrypt model weights using homomorphic encryption.
        
        Args:
            weights: List of model weight arrays
            
        Returns:
            Encrypted weights as bytes
        """
        try:
            # Flatten weights and convert to tenseal vector
            flat_weights = np.concatenate([w.flatten() for w in weights])
            encrypted_weights = ts.ckks_vector(self.context, flat_weights)
            
            # Additional layer of encryption
            return self.cipher_suite.encrypt(encrypted_weights.serialize())

        except Exception as e:
            self.logger.error(f"Error encrypting weights: {str(e)}")
            raise

    def decrypt_weights(self, encrypted_weights: bytes) -> List[np.ndarray]:
        """
        Decrypt model weights.
        
        Args:
            encrypted_weights: Encrypted weights bytes
            
        Returns:
            List of decrypted weight arrays
        """
        try:
            # Decrypt outer layer
            decrypted_bytes = self.cipher_suite.decrypt(encrypted_weights)
            
            # Deserialize tenseal vector
            encrypted_vector = ts.ckks_vector_from(self.context, decrypted_bytes)
            decrypted_flat = encrypted_vector.decrypt()
            
            # Reshape back to original weight shapes
            weights = []
            start_idx = 0
            for layer in self.global_model.layers:
                shape = layer.get_weights()[0].shape
                size = np.prod(shape)
                weights.append(decrypted_flat[start_idx:start_idx + size].reshape(shape))
                start_idx += size
                
            return weights

        except Exception as e:
            self.logger.error(f"Error decrypting weights: {str(e)}")
            raise

    def aggregate_updates(self, 
                         encrypted_updates: List[bytes], 
                         weights: Optional[List[float]] = None) -> None:
        """
        Aggregate encrypted model updates from food banks.
        
        Args:
            encrypted_updates: List of encrypted model updates
            weights: Optional weights for weighted averaging
        """
        try:
            if weights is None:
                weights = [1.0 / len(encrypted_updates)] * len(encrypted_updates)

            # Decrypt and aggregate updates
            decrypted_updates = [self.decrypt_weights(update) for update in encrypted_updates]
            
            # Weighted average of updates
            aggregated_weights = []
            for layer_idx in range(len(decrypted_updates[0])):
                layer_updates = [update[layer_idx] for update in decrypted_updates]
                weighted_avg = sum(w * u for w, u in zip(weights, layer_updates))
                aggregated_weights.append(weighted_avg)

            # Update global model
            self.global_model.set_weights(aggregated_weights)
            self.logger.info("Successfully aggregated model updates")

        except Exception as e:
            self.logger.error(f"Error aggregating updates: {str(e)}")
            raise

    def get_global_model_weights(self) -> bytes:
        """
        Get encrypted global model weights.
        
        Returns:
            Encrypted global model weights
        """
        try:
            weights = self.global_model.get_weights()
            return self.encrypt_weights(weights)
        except Exception as e:
            self.logger.error(f"Error getting global model weights: {str(e)}")
            raise

    def evaluate_global_model(self, 
                            test_features: np.ndarray, 
                            test_labels: np.ndarray) -> Dict[str, float]:
        """
        Evaluate the global model performance.
        
        Args:
            test_features: Test set features
            test_labels: Test set labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        try:
            metrics = self.global_model.evaluate(test_features, test_labels, verbose=0)
            return dict(zip(self.global_model.metrics_names, metrics))
        except Exception as e:
            self.logger.error(f"Error evaluating global model: {str(e)}")
            raise 