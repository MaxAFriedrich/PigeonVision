import os
import uuid
from pathlib import Path

import dotenv
import markdown
import requests
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

import web.slugify
from pigeonvision import main

dotenv.load_dotenv()
app = FastAPI()

static = Path(__file__).parent / "static"

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
        slug=slugify.slug,
        readme_html=readme_html,
        turnstile_site_key=os.getenv("TURNSTILE_SITE_KEY"),
        dev=os.getenv("DEV", "false")
    ))


@app.get(f"/{slugify.slug}-script.js")
async def script():
    script_path = Path(__file__).parent / "script.js"
    if script_path.exists():
        return HTMLResponse(script_path.read_text(),
                            media_type="application/javascript")
    return HTMLResponse("<p>Script not found.</p>", status_code=404)


@app.get(f"/{slugify.slug}-style.css")
async def style():
    style_path = Path(__file__).parent / "style.css"
    if style_path.exists():
        return HTMLResponse(style_path.read_text(), media_type="text/css")
    return HTMLResponse("<p>Style not found.</p>", status_code=404)


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


jobs = {}


def new_job() -> str:
    job_id = str(uuid.uuid4())
    while job_id in jobs:
        job_id = str(uuid.uuid4())
    jobs[job_id] = None
    return job_id


@app.get("/job/{job_id}")
async def get_job(job_id: str):
    if job_id not in jobs:
        return {"ok": False, "error": "Job not found."}
    result = jobs[job_id]
    if result is None:
        return {"ok": False, "error": "Job is still processing."}
    del jobs[job_id]
    return {"ok": True, "result": result}


def run_query(request: QueryRequest, job_id: str) -> None:
    if not verify_turnstile(request.token):
        jobs[job_id] = {"ok": False, "error": "Turnstile verification failed."}
        return
    certainty_word, message, certainty = main(request.query)
    jobs[job_id] = {"ok": True, "summary": certainty_word, "more": message,
                    "certainty": certainty}


@app.post("/query")
async def query_endpoint(
        request: QueryRequest,
        background_tasks: BackgroundTasks
):
    job_id = new_job()
    background_tasks.add_task(run_query, request, job_id)
    return {"ok": True, "id": job_id}
