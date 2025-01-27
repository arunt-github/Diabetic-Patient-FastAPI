from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://postgres:zoho@localhost/diabetic_patients',
                       echo=True)

Base = declarative_base()

Session = sessionmaker()