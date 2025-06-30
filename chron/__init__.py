from time import sleep

import pigeonvision


def schedule():
    while True:
        pigeonvision.cache.purge()
        # Purge every 6 hours
        sleep(3600 * 6)

