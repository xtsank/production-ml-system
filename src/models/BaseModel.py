from abc import ABC, abstractmethod
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

from src.settings import MAX_CATEGORIES


class BaseModel(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.train_metrics = {}
        self.plot_data = {}
        self.data = pd.DataFrame()
        self.numeric_features = []
        self.categorical_features = []

    @abstractmethod
    def prepare_data(self) -> None:
        pass

    @abstractmethod
    def create_model(self):
        pass

    def set_data(self, data: pd.DataFrame) -> None:
        self.data = data

    def detect_categories(self):
        allowed_dtypes = ['int64', 'float64', 'object', 'category', 'bool']
        self.data = self.data.select_dtypes(include=allowed_dtypes)

        self.numeric_features = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_features = self.data.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

        for col in self.numeric_features:
            if self.data[col].nunique() < MAX_CATEGORIES:
                self.categorical_features.append(col)
                self.numeric_features.remove(col)

    def train(self):
        x = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        self.model = self.create_model()
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)

        self.train_metrics = {
            'MAE': mean_absolute_error(y_test, y_pred),
            'R2': r2_score(y_test, y_pred)
        }

        self.plot_data = {
            'actual_vs_predicted': {
                'y_true': y_test,
                'y_pred': y_pred,
                'feature_names': x.columns.tolist()
            }
        }

        if hasattr(self.model, 'feature_importances_'):
            self.plot_data['feature_importance'] = {
                'importances': self.model.feature_importances_,
                'feature_names': x.columns.tolist()
            }

    def save(self, path: str):
        joblib.dump(self.model, path)

    def get_metrics(self) -> dict:
        return self.train_metrics

    def get_plot_data(self) -> dict:
        return self.plot_data
