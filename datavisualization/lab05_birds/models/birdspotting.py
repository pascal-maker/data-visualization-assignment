from datetime import datetime#
from typing import Optional#

from sqlmodel import SQLModel,Field,Relationship#
from models.birds import Bird, BirdRead#

class BirdSpottingBase(SQLModel):#class that inherits from SQLModel
    spotted_at:datetime = Field(default_factory=datetime.now)#date and time of the bird spotting
    location:str#location of the bird spotting
    observer_name:str#observer name of the bird spotting
    notes:Optional[str] = None#notes of the bird spotting

class BirdSpotting(BirdSpottingBase,table=True):#this bird is a table
    __tablename__ = "birdspotting"#this is a birdspotting table
    id: Optional[int] = Field(default=None,primary_key=True)#id of the bird spotting
    bird_id: int = Field(foreign_key="birds.id", ondelete="CASCADE")#foreign key of the bird spotting
    bird: Optional[Bird] = Relationship()#relationship of the bird spotting

class BirdSpottingCreate(BirdSpottingBase):#class that inherits from BirdSpottingBase
    bird_id:int#bird id of the bird spotting

class BirdSpottingRead(BirdSpottingBase):#class that inherits from BirdSpottingBase
    id: int#id of the bird spotting
    bird_id: int#bird id of the bird spotting

class BirdSpottingReadWithBird(BirdSpottingRead):#class that inherits from BirdSpottingRead
    bird: Optional[BirdRead] = None#relationship of the bird spotting