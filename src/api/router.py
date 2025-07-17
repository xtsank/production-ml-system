from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter, File, UploadFile, Request

from src.settings import templates, PLOTS_DIR, MODELS_DIR
from src.data.DataProcessor import DataProcessor
from src.models.CatBoostModel import CatBoostModel
from src.models.RandomForestModel import RandomForestModel
from src.visualization.ResultsVisualizer import ResultsVisualizer

main_router = APIRouter()
data_processor = DataProcessor()
cb_model = CatBoostModel()
rf_model = RandomForestModel()
res_visualizer = ResultsVisualizer()

@main_router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        { "request": request }
    )


@main_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    data_processor.set_file(file)

    errors = data_processor.check_file()

    if errors:
        return JSONResponse(status_code=400,
                            content = {"errors": errors})

    await data_processor.save_local()

    return {"status": "success", "file": file.filename}

@main_router.get("/analyze/{filename}")
async def analyze(filename: str, request: Request):
    data_processor.set_filename(filename)
    raw_data = data_processor.read() 

    if raw_data is None:
        return JSONResponse(
            status_code=404,
            content={"error": "File not found"}
        )

    summary = data_processor.find_data_summary()

    context = {
        "request": request,
        "filename": filename,
        "summary": summary,
        "data_preview": raw_data.head(10).to_dict(orient='records')
    }

    return templates.TemplateResponse(
        "analysis.html",
        context=context
    )

@main_router.post("/train/{filename}")
async def train(filename: str):
    data = data_processor.get_data()

    models = [cb_model, rf_model]

    for model in models:
        model.set_data(data)
        model.prepare_data()
        model.train()

    return {"status": "success", "file": filename}


@main_router.get("/results/{filename}")
async def result(filename: str, request: Request):
    models = [cb_model, rf_model]
    results = []

    for model in models:
        metrics = model.get_metrics()
        plot_data = model.get_plot_data()

        res_visualizer.add_data(plot_data)

        actual_vs_predicted_filename = PLOTS_DIR + f"/{model.model_name}_actual_vs_predicted.png"
        res_visualizer.plot_actual_vs_predicted(actual_vs_predicted_filename)

        feature_importance_filename = PLOTS_DIR + f"/{model.model_name}_feature_importance.png"
        res_visualizer.plot_feature_importance(feature_importance_filename)

        results.append({
            "model_name": model.model_name,
            "metrics": metrics,
            "actual_vs_predicted_plot": actual_vs_predicted_filename,
            "feature_importance_plot": feature_importance_filename
        })

        model.save(MODELS_DIR + f"/{model.model_name}.pkl")

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "filename": filename,
            "results": results
        }
    )

@main_router.get("/download_model/{model_name}")
async def download_model(model_name: str):
    model_path = MODELS_DIR + f"/{model_name}.pkl"
    try:
        return FileResponse(
            model_path,
            filename=f"{model_name}_model.pkl",
            media_type="application/octet-stream"
        )
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"error": "File not found"}
        )






