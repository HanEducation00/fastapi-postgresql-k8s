import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

# Ortam değişkenine göre uygun .env dosyasını yükle
env = os.getenv("ENV", "test")  # Varsayılan olarak "test"
if env == "prod":
    load_dotenv("prod.env")  # Prod ortamı için .env dosyasını yükle
else:
    load_dotenv("test.env")  # Test ortamı için .env dosyasını yükle

# SQLALCHEMY_DATABASE_URL'u al
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

# Veritabanı motorunu oluştur
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Veritabanı bilgilerini geri döndürmemiz gerekiyor kayıt için
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
