from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Country, ConfigurationField
from schemas import CountryCreate, CountryResponse

app = FastAPI()

@app.post("/create_configuration", response_model=CountryResponse)
def create_configuration(country: CountryCreate):
    db = SessionLocal()
    db_country = Country(country_code=country.country_code, country_name=country.country_name)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    for config in country.configurations:
        db_config = ConfigurationField(field_name=config.field_name, field_type=config.field_type, is_required=config.is_required, country_id=db_country.id)
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
    return db_country

@app.get("/get_configuration/{country_code}", response_model=CountryResponse)
def get_configuration(country_code: str):
    db = SessionLocal()
    db_country = db.query(Country).filter(Country.country_code == country_code).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@app.post("/update_configuration/{country_code}", response_model=CountryResponse)
def update_configuration(country_code: str, country: CountryCreate):
    db = SessionLocal()
    db_country = db.query(Country).filter(Country.country_code == country_code).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    db_country.country_name = country.country_name
    db.query(ConfigurationField).filter(ConfigurationField.country_id == db_country.id).delete()
    for config in country.configurations:
        db_config = ConfigurationField(field_name=config.field_name, field_type=config.field_type, is_required=config.is_required, country_id=db_country.id)
        db.add(db_config)
    db.commit()
    return db_country

@app.delete("/delete_configuration/{country_code}", response_model=dict)
def delete_configuration(country_code: str):
    db = SessionLocal()
    db_country = db.query(Country).filter(Country.country_code == country_code).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    db.query(ConfigurationField).filter(ConfigurationField.country_id == db_country.id).delete()
    db.delete(db_country)
    db.commit()
    return {"detail": "Country configuration deleted"}
