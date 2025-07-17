from sklearn.preprocessing import StandardScaler
from catboost import CatBoostRegressor

from src.models.BaseModel import BaseModel


class CatBoostModel(BaseModel):
    def __init__(self):
        super().__init__("CatBoost")

    def prepare_data(self) -> None:
        self.detect_categories()

        scaler = StandardScaler()
        self.data[self.numeric_features] = scaler.fit_transform(self.data[self.numeric_features])

        for col in self.numeric_features:
            self.data[col] = self.data[col].fillna(-999)

        for col in self.categorical_features:
            self.data[col] = self.data[col].fillna("Missing")

    def create_model(self):
        return CatBoostRegressor(
            cat_features=self.categorical_features,
            verbose=0,
            random_state=42,
        )