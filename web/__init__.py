import os
from pathlib import Path

import dotenv
import markdown
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from pigeonvision import main

dotenv.load_dotenv()
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
    return HTMLResponse(template.render(
        readme_html=readme_html,
        turnstile_site_key=os.getenv("TURNSTILE_SITE_KEY"),
        dev=os.getenv("DEV", "false")
    ))


class QueryRequest(BaseModel):
    query: str
    token: str


def verify_turnstile(token: str) -> bool:
    if os.getenv("DEV") == 'true':
        return True
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    payload = {
        "secret": os.getenv("TURNSTILE_SECRET_KEY"),
        "response": token,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    outcome = response.json()

    if outcome.get("success"):
        return True
    return False


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    if not verify_turnstile(request.token):
        return {"ok": False, "error": "Turnstile verification failed."}
    certainty_word, message, certainty = main(request.query)
    return {"ok": True, "summary": certainty_word, "more": message,
            "certainty": certainty}
