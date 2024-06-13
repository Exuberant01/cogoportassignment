from pydantic import BaseModel
from typing import List

class ConfigurationFieldCreate(BaseModel):
    field_name: str
    field_type: str
    is_required: bool

class CountryCreate(BaseModel):
    country_code: str
    country_name: str
    configurations: List[ConfigurationFieldCreate]

class ConfigurationFieldResponse(BaseModel):
    id: int
    field_name: str
    field_type: str
    is_required: bool

class CountryResponse(BaseModel):
    id: int
    country_code: str
    country_name: str
    configurations: List[ConfigurationFieldResponse]
