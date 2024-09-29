import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

import os

env = os.getenv("ENV", "prod")  # Varsayılan olarak 'prod' al
db_name = "test_db" if env == "test" else "prod_db"

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@postgres.svc.cluster.local/{db_name}"


#Veritabanı bilgilerini geri döndürmemiz gerekiyor kayıt için.
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()