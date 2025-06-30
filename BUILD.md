# Building PigeonVision

This document explains how to build PigeonVision, both for development and production use.

## Development Setup

1. Clone the repo
2. Make sure you have poetry and python3.11 or higher installed.
3. Run `poetry install` to install the dependencies.
4. Copy the `.env.example` file to `.env` and fill in the required environment variables.
5. Run `poetry run uvicorn app.main:app --reload` to start the development server.

## Production Setup

Grab a copy of the `.env.example` file and fill in the required environment variables. Make sure you rename it to `.env`.

Create a `docker-compose.yml` file in the folder you want to store the cache, logs and other data in. The file should look like this:

```yaml
services:
  pigeonvision:
    image: ghcr.io/maxafriedrich/pigeonvision/pigeonvision:latest
    volumes:
      - ./.env:/app/.env
      - ./data/cache:/root/.cache/pigeonvision
      - ./data/data:/root/.local/share/pigeonvision
    restart: always

  caddy:
    image: caddy:latest
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
    ports:
      - "443:443"
    restart: always
    depends_on:
      - pigeonvision

  watchtower:
    image: containrrr/watchtower:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: always
    command: --interval 43200 --cleanup
```

Then create a `Caddyfile` in the same folder with the following content:

```caddyfile
pigeonvision.net
{
	reverse_proxy pigeonvision:80
	tls internal
}
```

You can then put your server behind cloudflare.

You can then run `docker-compose up -d` to start the services.
