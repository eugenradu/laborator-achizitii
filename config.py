import os
from dotenv import load_dotenv

# Încarcă variabilele de mediu din fișierul .env
load_dotenv()

class Config:
    # Cheia secretă pentru sesiunile Flask (obligatorie pentru Flask-Login)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'o_cheie_secreta_fallback_pentru_dev' # O valoare fallback pentru dev, dar folosește .env în prod
    
    # Configurare pentru PostgreSQL
    DB_USER = os.environ.get('POSTGRES_USER')
    DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    DB_HOST = os.environ.get('POSTGRES_HOST')
    DB_PORT = os.environ.get('POSTGRES_PORT', '5432')
    DB_NAME = os.environ.get('POSTGRES_DB')

    # Șirul de conectare la baza de date PostgreSQL
    # Format: postgresql://user:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME])
        else "sqlite:///laborator_achizitii_fallback.db" # Fallback la SQLite pentru dezvoltare locală fără PG, în caz de eroare de config
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Recomandat pentru a dezactiva avertismentele SQLAlchemy