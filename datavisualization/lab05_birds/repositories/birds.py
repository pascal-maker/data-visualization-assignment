from sqlmodel import Session,select#importing sqlmodel and select from sqlmodel
from fastapi import HTTPException#importing http exception from fastapi
from models.birds import Bird,BirdCreate#importing bird and bird create from models.birds
from models.species import Species#importing species from models.species


class BirdRepository:#class that will handle the birds
    def __init__(self,session:Session):#constructor of the class
        self.session = session#session of the class

    def get_all(self):#function to get all the birds
        statement = select(Bird)#selecting all the birds
        return self.session.exec(statement).all()#returning all the birds

    def get_one(self,bird_id:int):#function to get one bird
        return self.session.get(Bird,bird_id)#getting the bird by id
    def insert(self,payload:BirdCreate):#function to insert a bird
        species_obj = self.session.get(Species,payload.species_id)    #getting the species by id
        if not species_obj:#checking if the species is not None
            raise HTTPException(status_code=404,detail="Species not found")#raising http exception if the species is not found
        item = Bird.model_validate(payload)#validating the payload
        self.session.add(item) #adding the item to the session
        self.session.commit()#commiting the session
        self.session.refresh(item)#refreshing the item
        return item