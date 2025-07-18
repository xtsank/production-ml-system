# Production Data ML System

Система загрузки, анализа и предсказания производственных данных на основе ML

## Функционал
- Загрузка CSV/Excel файлов
- Автоматическая предобработка данных
- Обучение моделей RandomForest и CatBoost
- Визуализация результатов
- Сохранение моделей для повторного использования

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/xtsank/production-ml-system.git
cd production-ml-system
```
2. Установить зависимости:
```bash
pip install -r requirements.txt
```
3. Запустить: 
```bash
python3 -m src.main
```

## Использование

1. Открыть http://localhost:8000 в браузере

2. Загрузить файл с данными через интерфейс

3. Получить результаты анализа

## API Endpoints

- POST /upload - загрузка файла

- GET /analyze - запуск анализа

- POST /train - обучение модели

- GET /results - получение результатов

- GET /download_model - загрузка обученной модели

## Технологии
- Python: FastAPI, pandas, scikit-learn, catboost

- Визуализация: matplotlib