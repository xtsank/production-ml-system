from src.settings import make_dirs
from src.api.router import main_router
from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles


app = FastAPI()

make_dirs()

app.mount("/plots", StaticFiles(directory="./plots"), name="plots")

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app)
