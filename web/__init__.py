from pathlib import Path

import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from starlette.responses import Response

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

for file in static.glob("**/*"):
    if file.is_file():
        suffix = file.suffix.lstrip('.')
        if suffix in suffixes:
            content_type, encoding = suffixes[suffix]
            app.mount(
                f"/{file.relative_to(static)}",
                Response(
                    file.read_bytes(),
                    media_type=content_type,
                    headers={
                        "Content-Encoding": encoding} if encoding == "binary"
                    else {},
                ),
                name=f"static-{file.name}"
            )

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
    certainty_word, message = main(request.query)
    return {"ok": True, "summary": certainty_word, "more": message}
