from sklearn.ensemble import RandomForestRegressor
import pandas as pd

from src.models.BaseModel import BaseModel


class RandomForestModel(BaseModel):
    def __init__(self):
        super().__init__("RandomForest")

    def prepare_data(self) -> None:
        self.detect_categories()

        for col in self.numeric_features:
            self.data[col] = self.data[col].fillna(self.data[col].median())

        for col in self.categorical_features:
            self.data[col] = self.data[col].fillna("Missing")

        target_column_name = self.data.columns[-1]
        target_column = self.data[target_column_name]

        self.data = self.data.drop(columns=[target_column_name])

        self.data = pd.get_dummies(self.data, columns=self.categorical_features)

        self.data[target_column_name] = target_column

    def create_model(self):
        return RandomForestRegressor(
            random_state=42
        )

