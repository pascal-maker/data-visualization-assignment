from typing import Annotated, List#
from fastapi import APIRouter, Depends, HTTPException, status#
# pyrefly: ignore [missing-import]
from sqlmodel import Session#
from database import get_session
# pyrefly: ignore [missing-import]
from models.birdspotting import BirdSpotting, BirdSpottingCreate, BirdSpottingReadWithBird
# pyrefly: ignore [missing-import]
from repositories.birdspotting import BirdSpottingRepository

router = APIRouter(prefix="/birdspotting", tags=["Birdspotting"])#router for the birdspotting


def get_birdspotting_repository(session: Annotated[Session, Depends(get_session)]) -> BirdSpottingRepository:#function to get the birdspotting repository
    return BirdSpottingRepository(session)#returning the birdspotting repository


@router.get("/", response_model=List[BirdSpottingReadWithBird])#router to get all the birdspotting
async def get_birdspotting(
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]#function to get the birdspotting repository
):
    return repo.get_all()#returning all the birdspotting


@router.get("/{birdspotting_id}", response_model=BirdSpottingReadWithBird)#router to get one birdspotting
async def get_one_birdspotting(
    birdspotting_id: int,
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]#function to get the birdspotting repository
):
    item = repo.get_one(birdspotting_id)#getting the birdspotting by id
    if not item:
        raise HTTPException(status_code=404, detail="Birdspotting not found")#raising http exception if the birdspotting is not found
    return item


@router.post("/", response_model=BirdSpottingReadWithBird, status_code=status.HTTP_201_CREATED)#router to add a birdspotting    
async def add_birdspotting(
    payload: BirdSpottingCreate,
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]#function to get the birdspotting repository
):
    return repo.insert(payload)#returning the inserted birdspotting