# pyrefly: ignore [missing-import]
from sqlmodel import Session, select#
# pyrefly: ignore [missing-import]
from fastapi import HTTPException
# pyrefly: ignore [missing-import]
from models.birdspotting import BirdSpotting, BirdSpottingCreate
# pyrefly: ignore [missing-import]
from models.birds import Bird


class BirdSpottingRepository:#this class will handle the birdspotting
    def __init__(self, session: Session):#constructor of the class
        self.session = session

    def get_all(self):#function to get all the birdspotting
        statement = select(BirdSpotting)#selecting all the birdspotting
        return self.session.exec(statement).all()

    def get_one(self, spotting_id: int):#function to get one birdspotting
        return self.session.get(BirdSpotting, spotting_id)#getting the birdspotting by id

    def insert(self, payload: BirdSpottingCreate):#function to insert a birdspotting
        bird = self.session.get(Bird, payload.bird_id)#getting the bird by id
        if not bird:#checking if the bird is not None
            raise HTTPException(status_code=404, detail="Bird not found")#raising http exception if the bird is not found
        item = BirdSpotting.model_validate(payload)#validating the payload
        self.session.add(item)#adding the item to the session
        self.session.commit()#commiting the session
        self.session.refresh(item)#refreshing the item
        return item #returning the item