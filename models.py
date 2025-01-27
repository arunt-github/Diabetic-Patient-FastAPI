from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    Name = Column(String(25))
    Pregnancies = Column(Integer, nullable = True)
    Glucose = Column(Integer)
    BloodPressure = Column(Integer)
    SkinThickness = Column(Integer)
    Insulin = Column(Integer, nullable=True)
    Bmi = Column(Float)
    DiabetesPedigreeFunction = Column(Float, nullable=True)
    Age = Column(Integer)
    Diabetic = Column(Boolean)
    
    
    # def __repr__(self):
    #     return f"<User {self.username}"    
    
