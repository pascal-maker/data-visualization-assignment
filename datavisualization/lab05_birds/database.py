import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from sqlmodel import Session,SQLModel,create_engine
load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")#get the postgres user from the environment
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")#get the postgres password from the environment
POSTGRES_PORT = os.getenv("POSTGRES_PORT")#get the postgres port from the environment
POSTGRES_DB = os.getenv("POSTGRES_DB")#get the postgres database from the environment

if os.getenv("ENVIRONMENT") == "DOCKER":#check if the environment is docker
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")#
else:
    POSTGRES_HOST = "127.0.0.1"#
DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"#
)
engine = create_engine(DATABASE_URL,echo=True)    

def get_session():#function to get the session
    with Session(engine) as session:
        yield session#returning the session

def create_db_and_tables():#function to create the database and tables
    SQLModel.metadata.create_all(engine)#creating the database and tables