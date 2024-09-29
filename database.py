import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

# Ortam değişkenlerini yükle
load_dotenv()

# Ortam değişkeninden çalışma ortamını al (varsayılan olarak 'prod' al)
env = os.getenv("ENV", "prod")  

# Ortam değişkenine göre veritabanı adını ayarla
db_name = "test_db" if env == "test" else "prod_db"

# Veritabanı bağlantı URL'sini oluştur
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@postgres.svc.cluster.local/{db_name}"

# Engine oluştur
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Veritabanı ve tabloları oluştur
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Veritabanı oturumu döndür
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
