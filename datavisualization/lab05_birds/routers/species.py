from typing import Annotated, List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, status
# pyrefly: ignore [missing-import]
from sqlmodel import Session    

from database import get_session
# pyrefly: ignore [missing-import]
from models.species import Species, SpeciesCreate
# pyrefly: ignore [missing-import]
from repositories.species import SpeciesRepository

router = APIRouter(prefix="/species", tags=["Species"])

def get_species_repository(session: Annotated[Session, Depends(get_session)]) -> SpeciesRepository:#function to get the species repository
    return SpeciesRepository(session)#returning the species repository

@router.get("/", response_model=List[Species])#router to get all the species
async def get_all_species(
    repo: Annotated[SpeciesRepository, Depends(get_species_repository)]#function to get the species repository
):
    return repo.get_all()#returning all the species

@router.post("/", response_model=Species, status_code=status.HTTP_201_CREATED)#router to create a species
async def create_species(
    payload: SpeciesCreate,
    repo: Annotated[SpeciesRepository, Depends(get_species_repository)]#function to get the species repository
):
    return repo.insert(payload)#inserting the species
