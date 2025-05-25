from pathlib import Path

import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from pigeonvision import main

app = FastAPI()

static = Path(__file__).parent / "static"

suffixes = {
    "html": ("text/html", "text"),
    "css": ("text/css", "text"),
    "js": ("application/javascript", "text"),
    "png": ("image/png", "binary"),
    "jpg": ("image/jpeg", "binary"),
    "jpeg": ("image/jpeg", "binary"),
    "svg": ("image/svg+xml", "text"),
    "ico": ("image/x-icon", "binary"),
    "webmanifest": ("application/manifest+json", "text"),
}

app.mount("/static", StaticFiles(directory=static), name="static")

templates = Environment(
    loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
    autoescape=select_autoescape(['html', 'xml'])
)


@app.get("/", response_class=HTMLResponse)
async def root():
    readme_path = Path(__file__).parent.parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        readme_html = markdown.markdown(md_content)
    else:
        readme_html = "<p>README not found.</p>"
    template = templates.get_template("index.html")
    return HTMLResponse(template.render(readme_html=readme_html))


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    certainty_word, message, certainty = main(request.query)
    return {"ok": True, "summary": certainty_word, "more": message,
            "certainty": certainty}
