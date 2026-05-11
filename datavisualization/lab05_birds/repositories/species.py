from sqlmodel import Session, select#importing sqlmodel and select from sqlmodel
from models.species import Species, SpeciesCreate#importing species and species create from models.species

class SpeciesRepository:#class that will handle the species
    def __init__(self, session: Session):#constructor of the class
        self.session = session#session of the class

    def get_all(self):#function to get all the species
        statement = select(Species)#selecting all the species
        return self.session.exec(statement).all()

    def insert(self, payload: SpeciesCreate):#function to insert a species
        item = Species.model_validate(payload)#validating the payload
        self.session.add(item)#adding the item to the session
        self.session.commit()#commiting the session
        self.session.refresh(item)#refreshing the item
        return item #returning the item
