from pydantic import BaseModel
# from typing import Optional


class DataModel(BaseModel):
    Name : str
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    Bmi: float
    DiabetesPedigreeFunction: float
    Age: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "Name" : "Sruthi",
                "Pregnancies": 6,
                "Glucose": 148,
                "BloodPressure": 72,
                "SkinThickness": 35,
                "Insulin": 0,
                "Bmi": 33.6,
                "DiabetesPedigreeFunction": 0.627,
                "Age": 50,
            }
        }
