from fastapi import FastAPI#importing fastapi
from database import create_db_and_tables#importing create_db_and_tables from database
from routers.species import router as species_router#importing species router
from routers.birds import router as birds_router#importing birds router
from routers.birdspotting import router as birdspotting_router#importing birdspotting router
app = FastAPI(title="Birds API")#creating the app


@app.on_event("startup")#event handler for startup
def on_startup():#function to handle startup
    create_db_and_tables()
@app.get("/")#route to get the root
async def root():#function to get the root
    return {"message": "Hello World"}

app.include_router(species_router)#including species router
app.include_router(birds_router)#including birds router
app.include_router(birdspotting_router)#including birdspotting router