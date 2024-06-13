from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String, unique=True, nullable=False)
    country_name = Column(String, nullable=False)
    configurations = relationship("ConfigurationField", back_populates="country")

class ConfigurationField(Base):
    __tablename__ = 'configuration_fields'
    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(String, nullable=False)
    field_type = Column(String, nullable=False)
    is_required = Column(Boolean, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", back_populates="configurations")
