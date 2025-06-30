import os
from time import sleep

from dotenv import load_dotenv

import pigeonvision

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE


def schedule():
    load_dotenv()
    dev_mode = True if os.getenv("DEV") == 'true' else False
    wait = 6 * HOUR if not dev_mode else 30 * SECOND
    while True:
        print("Running scheduled tasks...", flush=True)
        if dev_mode:
            pigeonvision.cache.purge(timeout=wait)
        else:
            pigeonvision.cache.purge()
        sleep(wait)
