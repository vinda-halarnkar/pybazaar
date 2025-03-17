import os

class Config:
    PORT= int(os.environ.get('PORT', 5002))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'IqOakHHdbiu98dnhjflz4a9kdg0ae4zwurBejbZo8MOi'


    #Mysql settings
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'vinda'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    DB_NAME = os.environ.get('DB_NAME') or 'pybazaar'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables event system for performance



