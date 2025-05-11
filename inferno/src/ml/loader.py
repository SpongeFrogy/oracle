from pathlib import Path
from typing import Any, Dict, Optional, Union
import joblib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ModelLoader:
    """A class to handle loading and managing ML models.

    This class provides functionality to load ML models from disk, manage different
    versions, and handle model metadata.

    Attributes:
        model_dir (Path): Directory where models are stored
        current_model (Any): Currently loaded model
        model_metadata (Dict): Metadata about the current model
    """

    def __init__(self, model_dir: Union[str, Path]) -> None:
        """Initialize the ModelLoader.

        Args:
            model_dir: Path to the directory containing model files
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.current_model: Optional[Any] = None
        self.model_metadata: Dict[str, Any] = {}

    def load_model(self, model_path: Union[str, Path]) -> None:
        """Load a model from the specified path.

        Args:
            model_path: Path to the model file (.pkl or .joblib)

        Raises:
            FileNotFoundError: If model file doesn't exist
            ValueError: If model file format is not supported
        """
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        if model_path.suffix not in [".pkl", ".joblib"]:
            raise ValueError(f"Unsupported model format: {model_path.suffix}")

        try:
            self.current_model = joblib.load(model_path)
            self.model_metadata = {"loaded_at": datetime.now().isoformat(), "model_path": str(model_path), "model_type": type(self.current_model).__name__}
            logger.info(f"Successfully loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def get_model(self) -> Any:
        """Get the currently loaded model.

        Returns:
            The loaded model object

        Raises:
            RuntimeError: If no model is currently loaded
        """
        if self.current_model is None:
            raise RuntimeError("No model is currently loaded")
        return self.current_model

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the currently loaded model.

        Returns:
            Dictionary containing model metadata
        """
        return self.model_metadata.copy()
