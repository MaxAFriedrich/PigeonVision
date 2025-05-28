# adding slugs to common files to prevent caching of files across builds
import time
from pathlib import Path

slug = (Path(__file__).parent / "slug").read_text().split("\n")[0].strip()


def generate_slug():
    global slug
    slug = str(hex(int(time.time())))
    with open(Path(__file__).parent / "slug", "w") as f:
        f.write(slug)


if __name__ == "__main__":
    generate_slug()
