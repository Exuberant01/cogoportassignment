from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_configuration/", response_model=schemas.Configuration)
def create_configuration(configuration: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    return crud.create_configuration(db=db, configuration=configuration)

@app.get("/get_configuration/{country_code}", response_model=list[schemas.Configuration])
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    configurations = crud.get_configurations_by_country_code(db, country_code=country_code)
    if configurations is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return configurations

@app.post("/update_configuration/", response_model=schemas.Configuration)
def update_configuration(configuration_id: int, configuration: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    db_configuration = crud.update_configuration(db, configuration_id=configuration_id, configuration=configuration)
    if db_configuration is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_configuration

@app.delete("/delete_configuration/{configuration_id}", response_model=schemas.Configuration)
def delete_configuration(configuration_id: int, db: Session = Depends(get_db)):
    db_configuration = crud.delete_configuration(db, configuration_id=configuration_id)
    if db_configuration is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_configuration
