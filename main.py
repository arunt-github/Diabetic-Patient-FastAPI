from fastapi import FastAPI, Request
from schemas import DataModel
import joblib
import numpy as np
from torch import tensor, float32
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

api = FastAPI()
Model = joblib.load(open("model.pkl", "rb"))

api.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="Templates")


@api.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@api.post("/submit")
async def get_data(dataset: DataModel, request: Request):

    data = [
        dataset.Pregnancies,
        dataset.Glucose,
        dataset.BloodPressure,
        dataset.SkinThickness,
        dataset.Insulin,
        dataset.Bmi,
        dataset.DiabetesPedigreeFunction,
        dataset.Age,
    ]

    data = np.array(data)
    data = tensor(data, dtype=float32)

    Model.eval()
    prediction = Model(data).detach().numpy()
    prediction = np.round(prediction)

    if prediction == 0:
        result = {"Patient ": "Not Diabetic"}
    else:
        result = {"Patient ": "Diabetic"}

    return result
