from typing import Optional
from sqlmodel import SQLModel,Field,Relationship
from models.species import Species, SpeciesRead

class BirdBase(SQLModel):#class that inherits from SQLModel
    nickname:str#nickname of the bird
    ring_code:str#ring code of the bird
    age: int = Field(ge=0)#age of the bird

class Bird(BirdBase,table=True):#this bird is a table
    __tablename__ = "birds"#this is a bird table
    id: Optional[int] = Field(default=None,primary_key=True)#id of the bird
    species_id: int = Field(foreign_key="species.id", ondelete="RESTRICT")#foreign key of the bird
    species: Optional[Species] = Relationship()    #relationship of the bird

class BirdCreate(BirdBase):#class that inherits from BirdBase
    species_id:int#species id of the bird

class BirdRead(BirdBase):#class that inherits from BirdBase
    id: int#id of the bird
    species_id: int#species id of the bird

class BirdReadWithSpecies(BirdRead):#class that inherits from BirdRead
    species: Optional[SpeciesRead] = None#relationship of the bird

