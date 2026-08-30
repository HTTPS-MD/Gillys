import os # For accessing environment variables
import bcrypt
from dotenv import load_dotenv # For loading the .env file
from pymongo import MongoClient # For connecting to MongoDB

# =====================================================================
# TROUBLESHOOTING NOTE: "SSL handshake failed" / "ServerSelectionTimeoutError"
# 1. Cause: MongoDB Atlas blocked the connection due to security (IP not allowed).
# 2. Fix: Go to MongoDB Atlas Dashboard -> Security -> Network Access.
# 3. Click "Add IP Address" -> Select "Add Current IP Address" (or 0.0.0.0/0 for all networks).
# 4. If IP is already whitelisted and error persists, the 'certifi' library might be needed.
# =====================================================================

load_dotenv() # Loads hidden variables into the environment
uri = os.getenv("MONGODB_URI")  # Retrieves the database connection string

client = MongoClient(uri) # Establishes an active connection to the MongoDB server using the uri
db = client["gillys_database"] # Selects the database (auto-creates on first insert)
user_collection = db["users"]  # Selects the collection (auto-creates on first insert)

def user_signin(username, password):
    user_account = user_collection.find_one({"username" : username})

    if user_account:
        stored_hash = user_account["password"]
        password_bytes = password.encode('utf-8')
        result = bcrypt.checkpw(password_bytes, stored_hash)

        if result:
            return True

        else:
            return False

    else:
        return False



def user_signup(username, password):
    duplicate_username = user_collection.find_one({"username": username})

    if duplicate_username:
        return False

    bytes_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(bytes_pw, salt)
    user_collection.insert_one({"username": username, "password": hash_pw})

    return True




