import pickle
from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic
from mllib.utility import logger

T = TypeVar('T')


class Model(ABC, Generic[T]):
    """The abstract class of a machine learning model.

    Attributes:
        model_name (str):the name of this model.
        parameters (dict): the hyper parameters of this model.
        model (T): the entity of ML model.
        logger (logging.Logger): the logger of this model.

    """

    def __init__(self, model_name: str, parameters: Dict[str, Any]) -> None:
        """Construct a model.

        Args:
            model_name: :the name of this model.
            parameters: the hyper parameters of this model.
        """
        self.model_name = model_name
        self.parameters = parameters
        self.model: T = None
        self.logger = logger.make_child_logger(__name__)

    @abstractmethod
    def train(self, tr_x, tr_y, va_x, va_y) -> T:
        """Train a ML model and return a object of model.

        Args:
            tr_x: feature values for training.
            tr_y: labels for training.
            va_x: feature values for validation.
            va_y: labels for validation.

        Returns:
            T: a model object

        """
        pass

    @abstractmethod
    def predict(self, te_x):
        """Predict labels from feature values, using a trained model.

        Args:
            te_x: feature values for predicting.

        Returns:
            a results of prediction

        """
        pass

    def save_model(self, dir_name: str) -> None:
        """Save(Pickle) this model.

        Args:
            dir_name: a directory name

        Raises:
            TypeError: raise if self.model is None.

        """
        if self.model is None:
            raise TypeError("The type of self.model is None.")

        with open(dir_name + "/" + self.model_name, mode="wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(dir_name: str, model_name: str) -> 'Model':
        """Load a model.

        Args:
            dir_name: a directory name
            model_name: a name of model

        Returns:
            Model

        """
        with open(dir_name + "/" + model_name, mode="rb") as f:
            return pickle.load(f)
