from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import build_rag_chain

app = FastAPI()

chain_cache = {}

class VideoRequest(BaseModel):
    youtube_url: str

class QueryRequest(BaseModel):
    youtube_url: str
    question: str

@app.post("/load")
def load_video(request: VideoRequest):
    try:
        chain_cache[request.youtube_url] = build_rag_chain(request.youtube_url)
        return {"message": "Video loaded successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask")
def ask(request: QueryRequest):
    if request.youtube_url not in chain_cache:
        raise HTTPException(status_code=400, detail="Load the video first using /load")
    answer = chain_cache[request.youtube_url].invoke(request.question)
    return {"answer": answer}