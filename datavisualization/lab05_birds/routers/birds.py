from typing import Annotated,List
from fastapi import APIRouter,Depends,HTTPException,status#importing fast api components
from sqlmodel import Session#importing session from sqlmodel
from database import get_session#importing get session from database

from models.birds import Bird, BirdCreate, BirdReadWithSpecies#importing bird, bird create, bird read with species from models.birds
from repositories.birds import BirdRepository#importing bird repository from repositories.birds

router = APIRouter(prefix="/birds",tags=["Birds"])#router for the birds
def get_bird_repository(session: Annotated[Session,Depends(get_session)],) -> BirdRepository:#function to get the bird repository
    return BirdRepository(session)#returning the bird repository
    
@router.get("/", response_model=List[BirdReadWithSpecies])#router to get all the birds  
async def get_birds(
    repo: Annotated[BirdRepository, Depends(get_bird_repository)]#function to get the bird repository
):
    return repo.get_all()

@router.get("/{bird_id}", response_model=BirdReadWithSpecies)#router to get one bird
async def get_one_bird(
    bird_id:int,
    repo: Annotated[BirdRepository, Depends(get_bird_repository)]#function to get the bird repository
)   :  
    item = repo.get_one(bird_id)#getting the bird by id
    if not item:#checking if the bird is not None
        raise HTTPException(status_code=404,detail="Bird not found")#raising http exception if the bird is not found
    return item

@router.post("/", response_model=BirdReadWithSpecies, status_code=status.HTTP_201_CREATED)#router to create a bird
async def create_bird(
    payload:BirdCreate,
    repo: Annotated[BirdRepository, Depends(get_bird_repository)]#function to get the bird repository
):
    return repo.insert(payload)#inserting the bird