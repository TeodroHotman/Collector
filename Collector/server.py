import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from search import search_source

app = FastAPI()

final_data = {}


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
    global final_data
    final_data = finalize_data(request.sources, request.information)
    return final_data

@app.get("/final-data")
def get_final_data():
    return final_data