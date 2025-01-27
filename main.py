from fastapi import FastAPI, Request
from schemas import DataModel
import joblib
import numpy as np
from torch import tensor, float32
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Patient
from database import Session, engine

api = FastAPI()
Model = joblib.load(open("model.pkl", "rb"))

api.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="Templates")

session = Session(bind = engine)

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
        status = False
        result = {"Patient ": "Not Diabetic"}
    else:
        status = True
        result = {"Patient ": "Diabetic"}
        
    new_patient = Patient(
        Name = dataset.Name,
        Pregnancies = dataset.Pregnancies,
        Glucose = dataset.Glucose,
        BloodPressure = dataset.BloodPressure,
        SkinThickness = dataset.SkinThickness,
        Insulin = dataset.Insulin,
        Bmi = dataset.Bmi,
        DiabetesPedigreeFunction = dataset.DiabetesPedigreeFunction,
        Age = dataset.Age,
        Diabetic = status 
    )
    
    session.add(new_patient)
    session.commit()
    
    return result
