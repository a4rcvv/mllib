import numpy
import xgboost as xgb
from typing import Dict, Any, TypeVar, Generic

from mllib.model.model import Model


class XGBoostModel(Model[xgb.Booster]):
    """The wrapper class of XGBoost.



    Attributes:
        model_name (str):the name of this model.
        parameters (dict): the hyper parameters of this model.
        model (T): the entity of ML model.
        logger (logging.Logger): the logger of this model.
        num_boost_round (int): the number of boosting iterations.
        early_stopping_rounds (int): if the validation score doesn't improve during early_stopping_rounds rounds of
        iteration, early stopping will be activated.

    """

    def __init__(self, model_name: str, parameters: Dict[str, Any]):
        """Construct a model.

         Args:
            model_name: :the name of this model.
            parameters: the hyper parameters of this model.
        """
        super().__init__(model_name, parameters)
        self.num_boost_round = 10
        self.early_stopping_rounds = None

    def train(self, tr_x, tr_y, va_x, va_y) -> (xgb.Booster, Dict):
        dtrain = xgb.DMatrix(tr_x, label=tr_y)
        dvalid = xgb.DMatrix(va_x, label=va_y)
        evals = [(dtrain, 'train'), (dvalid, 'validation')]
        evals_result = {}

        try:
            self.num_boost_round = self.parameters["num_boost_round"]
        except KeyError:
            self.logger.warning("parameters[\"num_boost_round\"] not found. 10 will be used as its default value.")

        try:
            self.early_stopping_rounds = self.parameters["early_stopping_rounds"]
        except KeyError:
            self.logger.warning("parameters[\"early_stopping_rounds\"] not found. None will be used as its default "
                                "value.")

        self.logger.info("Training is started. The model name is " + self.model_name)
        bst: xgb.Booster = xgb.train(self.parameters, dtrain, num_boost_round=self.num_boost_round,
                                     early_stopping_rounds=self.early_stopping_rounds, evals=evals,
                                     evals_result=evals_result)
        self.model: xgb.Booster = bst
        self.logger.info("Training is finished.")
        return bst, evals_result

    def predict(self, te_x) -> numpy.array:
        if self.model is None:
            self.logger.error("A trained model doesn't exist. This function returns None.")
            return None
        dtest = xgb.DMatrix(te_x)

        return self.model.predict(dtest)
