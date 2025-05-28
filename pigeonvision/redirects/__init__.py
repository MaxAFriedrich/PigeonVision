import requests
import logging


def follow_redirects(url) -> (list, int, int):
    """
    :param url: The URL to follow redirects for.
    :return: final url, number of redirects, status code
    """
    logger = logging.getLogger(__name__)
    logger.debug("Following redirects for %s", url)
    session = requests.Session()

    response = session.get(url, allow_redirects=True, timeout=10)
    last_url = response.history[-1].url if response.history else response.url
    num_redirects = len(response.history)
    status_code = response.status_code
    logger.debug(response.history)
    if num_redirects == 0:
        return [last_url], num_redirects, status_code
    else:
        return response.history, num_redirects, status_code