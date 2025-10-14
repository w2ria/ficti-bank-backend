import os
from dotenv import load_dotenv

load_dotenv()

# Database Config
DB_USERNAME = os.getenv('USER_DB')
DB_PASSWORD = os.getenv('PASSWORD_DB')
DB_HOST = os.getenv('HOST_DB')
DB_NAME = os.getenv('NAME_DB')
PORT = os.getenv('PORT_DB')
# DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{PORT}/{DB_NAME}?ssl=true"
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{PORT}/{DB_NAME}"


# JWT Config
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
