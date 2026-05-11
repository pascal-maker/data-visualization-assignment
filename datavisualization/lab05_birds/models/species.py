from typing import Optional#import
from decimal import Decimal#
from sqlmodel import SQLModel, Field

class SpeciesBase(SQLModel):#class that inherits from SQLModel
    name: str#name of the species
    scientific_name: str#scientific name of the species
    family: str#family of the species
    conservation_status: str#conservation status of the species
    wingspan_cm: Decimal = Field(max_digits=5, decimal_places=2)#wingspan of the species

class Species(SpeciesBase, table=True):#this is a table
    __tablename__ = "species"#this is a species table
    id: Optional[int] = Field(default=None, primary_key=True)#id of the species

class SpeciesCreate(SpeciesBase):#class that inherits from SpeciesBase
    pass

class SpeciesRead(SpeciesBase):#class that inherits from SpeciesBase
    id: int#id of the species
