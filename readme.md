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

## Качество кода

Проект проходит следующие проверки:

[![Flake8](https://img.shields.io/badge/flake8-checked-brightgreen?logo=python)](https://flake8.pycqa.org/)
[![Bandit](https://img.shields.io/badge/bandit-checked-yellow?logo=security)](https://bandit.readthedocs.io/)

Запуск проверок:
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
bandit -r src/ -ll
```

## Технологии
- Python: FastAPI, pandas, scikit-learn, catboost

- Визуализация: matplotlib