import os
from fastapi.templating import Jinja2Templates

ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".csv"}
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_CATEGORIES = 10

UPLOAD_DIR = "./uploads"
PLOTS_DIR = "./plots"
MODELS_DIR = "./models"

templates = Jinja2Templates(directory="templates")


def make_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
