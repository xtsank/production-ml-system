import pandas as pd
import os

from src.settings import (UPLOAD_DIR,
                          MAX_FILE_SIZE,
                          ALLOWED_EXTENSIONS,
                          MAX_CATEGORIES)


class DataProcessor:
    def __init__(self):
        self.file = None
        self.filename = None
        self.data = None

    def set_file(self, file):
        self.file = file

    def set_filename(self, filename):
        self.filename = filename

    def get_data(self):
        return self.data

    def _check_extension(self, errors) -> None:
        file_extension = os.path.splitext(self.file.filename)[1]

        if file_extension not in ALLOWED_EXTENSIONS:
            errors.append({
                "error": "Invalid file type",
                "allowed_types": list(ALLOWED_EXTENSIONS)
            })

    def _check_size(self, errors) -> None:
        file_size = self.file.size

        if file_size > MAX_FILE_SIZE:
            errors.append({
                "error": "File too large",
                "max_size": MAX_FILE_SIZE,
                "actual_size": file_size
            })

    def check_file(self) -> []:
        errors = []

        self._check_extension(errors)
        self._check_size(errors)

        return errors

    async def save_local(self) -> None:
        file_path = os.path.join(UPLOAD_DIR, self.file.filename)

        contents = await self.file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        await self.file.seek(0)

    def _exists(self):
        return os.path.exists(os.path.join(UPLOAD_DIR, self.filename))

    def read(self):
        if not self._exists():
            return None

        if self.filename.endswith(".csv"):
            self.data = pd.read_csv(os.path.join(UPLOAD_DIR, self.filename))
        else:
            self.data = pd.read_excel(os.path.join(UPLOAD_DIR, self.filename))

        return self.data

    def find_data_summary(self):
        summary = {
            'total_rows': self.data.shape[0],
            'total_columns': self.data.shape[1],
            'total_missing_values': self.data.isna().sum().sum(),
            'num_numeric': 0,
            'num_categorical': 0
        }

        numeric_columns = \
            self.data.select_dtypes(include=['int64', 'float64'])
        numeric_features = numeric_columns.columns.tolist()

        categorical_columns = \
            self.data.select_dtypes(include=['object', 'category', 'bool'])
        categorical_features = categorical_columns.columns.tolist()

        for col in numeric_features[:]:
            if self.data[col].nunique() < MAX_CATEGORIES:
                categorical_features.append(col)
                numeric_features.remove(col)

        summary['num_numeric'] = len(numeric_features)
        summary['num_categorical'] = len(categorical_features)

        return summary
