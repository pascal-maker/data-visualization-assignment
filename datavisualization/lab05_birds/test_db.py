from database import get_session, create_db_and_tables#importing get_session and create_db_and_tables from database
from models.species import Species, SpeciesCreate#importing Species and SpeciesCreate from models.species
from repositories.species import SpeciesRepository#importing SpeciesRepository from repositories.species
try:
    create_db_and_tables()#creating the database tables
    session = next(get_session())#getting the session
    repo = SpeciesRepository(session)#creating the repository
    res = repo.insert(SpeciesCreate(name="Testing"))#inserting the species
    print("Success:", res)#printing the result
except Exception as e:
    import traceback#importing traceback
    traceback.print_exc()
