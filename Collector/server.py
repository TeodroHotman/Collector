import json
import uuid
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from search import search_source

app = FastAPI()

COLLECTIONS_DIR = Path("data/collections")
COLLECTIONS_DIR.mkdir(parents=True, exist_ok=True)
latest_collection_id = None

class searchRequest(BaseModel):
    websites: list[str] = Field(default_factory=list)
    keywords: list[str]
    topics: list[str]

@app.get("/")
def home ():
    return FileResponse("index.html")

@app.post("/search")
async def search_post(request: searchRequest):
    results = search_source(request.websites, request.keywords, request.topics)
    return {"results": results}


class FinalRequest(BaseModel):
    sources: list[str]
    information: list[str]

@app.get("/final")
def final_page ():
    return FileResponse("final.html")

def finalize_data(sources, information):
    return {"sources": sources, "information": information}

@app.post("/finalize")
async def finalize_post(request: FinalRequest):
    global latest_collection_id
    collection_id = str(uuid.uuid4())
    latest_collection_id = collection_id

    data = {"collection_id": collection_id, "sources": request.sources, "information": request.information}

    file_path = COLLECTIONS_DIR / f"{collection_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return data

@app.get("/collections/{collection_id}")
def get_collection(collection_id: str):
    file_path = COLLECTIONS_DIR / f"{collection_id}.json"

    if not file_path.exists():
        return {"error": "Collection not found"}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    return data

@app.get("/final-data")
def get_final_data():
    if latest_collection_id is None:
        return {
            "sources": [],
            "information": []
        }

    file_path = COLLECTIONS_DIR / f"{latest_collection_id}.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    return data