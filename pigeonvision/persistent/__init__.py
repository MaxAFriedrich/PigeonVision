import logging
from pathlib import Path

import platformdirs
from dotenv import load_dotenv

LOCAL_APP_DATA = Path(platformdirs.user_data_dir('pigeonvision'))
LOCAL_CACHE = Path(platformdirs.user_cache_dir('pigeonvision'))


def load():
    """
    Load the pigeonvision persistent data directories.
    """
    print(
        f"App data directory: {LOCAL_APP_DATA}, Cache directory: {LOCAL_CACHE}")
    logger = logging.getLogger(__name__)

    LOCAL_APP_DATA.mkdir(parents=True, exist_ok=True)
    LOCAL_CACHE.mkdir(parents=True, exist_ok=True)

    logger.info("Local app data loaded as: %s", LOCAL_APP_DATA)
    logger.info("Local cache loaded as: %s", LOCAL_CACHE)

    load_dotenv(Path(__file__).parent.parent / '.env')
