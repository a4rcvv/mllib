"""Example usage of XGBoost wrapper

"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from mllib.model.xgboost_model import XGBoostModel
from mllib.utility.logger import *

root_logger = make_root_logger(logging.INFO, logging.INFO, logging.INFO, "xgb.log")

dataset = datasets.load_breast_cancer()
x, y = dataset.data, dataset.target
x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.3)

params = {
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "num_boost_round": 1000,
    "early_stopping_rounds": 10
}

xgb_model = XGBoostModel("xgb", params)

_, result = xgb_model.train(x_tr, y_tr, x_te, y_te)

pred = xgb_model.predict(x_te)
pred = np.where(pred > 0.5, 1, 0)
acc = accuracy_score(y_te, pred)
print(acc)

train_plt = result['train']['logloss']
plt.plot(train_plt, label='train')
val_plt = result['validation']['logloss']
plt.plot(val_plt, label='validation')
plt.grid()
plt.legend()
plt.xlabel('rounds')
plt.ylabel('logloss')
plt.show()
