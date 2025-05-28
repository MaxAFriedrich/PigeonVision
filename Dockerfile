FROM python:3.11-bookworm

# Install poetry

RUN pip install --no-cache-dir poetry

# Set the working directory
WORKDIR /app
# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/
# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root \
    && rm -rf /root/.cache/pypoetry

# Copy the rest of the application code \
COPY . /app/

# Generate build slug

RUN poetry run python web/slugify.py

# Set the entrypoint to run the application
ENTRYPOINT ["poetry", "run", "uvicorn", "web:app", "--host", "0.0.0", "--port", "80"]
