from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import HTMLResponse

from pigeonvision import main

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


static = Path(__file__).parent / "static"

static_files = {
    "index.html": (static / "index.html").read_text(),
    "favicon.ico": (static / "favicon.ico").read_bytes(),
}


@app.get("/")
async def root():
    return HTMLResponse(static_files["index.html"], status_code=200)


@app.get("/favicon.ico")
async def favicon():
    return static_files["favicon.ico"]


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    certainty_word, message = main(request.query)
    return {"ok": True, "summary": certainty_word, "more": message}
