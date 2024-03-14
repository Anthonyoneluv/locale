from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import hashlib
import secrets
from datetime import datetime
from model import lga, state, region, search_response
from cachetools import cached, TTLCache
from db import dbs

LGA = lga.LGA
State = state.State
Region = region.Region
SearchResponse = search_response.SearchResponse

api_keys_db = dbs.api_keys_db
db = dbs.db
cache = TTLCache(maxsize=100, ttl=300)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST"],
    allow_headers=["*"]
)

# Generate API key for a new user
def generate_api_key():
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()

# Authentication middleware
async def authenticate(api_key: Optional[str] = Header(None)):
    if api_key is None or api_key not in api_keys_db:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return True

@app.post("/register/")
async def register(email: str):
    is_registered = validate_email(email)

    if not is_registered:
        api_key = generate_api_key()
        api_keys_db[api_key] = [email, datetime.now()]
        save_to_db(f"{email},{api_key},{datetime.now()}\n")
        return {"message": api_key}
    
    return {"message": "email address aleardy registered"}

@cached(cache)
@app.get("/search/")
async def search(query: str, auth: bool = Depends(authenticate)):
    regions = [r for r in db["regions"] if query.lower() in r["name"].lower()]
    states = [s for s in db["states"] if query.lower() in s["name"].lower()]
    lgas = [l for l in db["lgas"] if query.lower() in l["name"].lower()]
    return SearchResponse(regions=regions, states=states, lgas=lgas)

@app.get("/regions/")
async def get_regions(auth: bool = Depends(authenticate)):
    return db["regions"]

@app.get("/states/")
async def get_states(auth: bool = Depends(authenticate)):
    return db["states"]

@app.get("/lgas/")
async def get_lgas(auth: bool = Depends(authenticate)):
    return db["lgas"]


def save_to_db(data):
    with open("db/db.csv", "a") as db_e:
        db_e.write(data)

def validate_email(email: str):
    emails = []

    with open("db/db.csv") as db_e:
        next(db_e)
        for line in db_e:
            clean_line = line.strip()
            clean_line = clean_line.split(",")
            emails.append(clean_line[0])
        
    if email in emails:
        return True
    
    return False


def load_database():
    with open("db/db.csv") as db_e:
        next(db_e)
        for line in db_e:
            clean_line = line.strip()
            clean_line = clean_line.split(",")

            api_keys_db[clean_line[1]] = [clean_line[0], clean_line[2]]
        
load_database()