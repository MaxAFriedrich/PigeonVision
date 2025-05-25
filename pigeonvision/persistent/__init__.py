from pathlib import Path

import platformdirs
import logging
from dotenv import load_dotenv

LOCAL_APP_DATA = Path(platformdirs.user_data_dir('pigeonvision'))
LOCAL_CACHE = Path(platformdirs.user_cache_dir('pigeonvision'))


def load():
    """
    Load the pigeonvision persistent data directories.
    """
    logger = logging.getLogger(__name__)

    LOCAL_APP_DATA.mkdir(parents=True, exist_ok=True)
    LOCAL_CACHE.mkdir(parents=True, exist_ok=True)
    load_dotenv(Path(__file__).parent.parent / '.env')
