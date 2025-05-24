import requests

from pigeonvision import persistent

url = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'


def fetch_tlds() -> set[str]:
    """
    Fetches the list of top-level domains (TLDs) from IANA and returns them
    as a set.

    :return: A set of TLDs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        tlds = {line.strip().lower() for line in response.text.splitlines() if
                line and not line.startswith('#')}
        return tlds
    except requests.RequestException as e:
        print(f"Error fetching TLDs: {e}")
        return set()


def get_tlds() -> set[str]:
    """
    Returns the set of TLDs. If the TLDs are not cached, it fetches them.

    :return: A set of TLDs.
    """
    file = persistent.LOCAL_APP_DATA / 'tlds.txt'
    if file.exists():
        try:
            with open(file, 'r') as f:
                tlds = {line.strip().lower() for line in f if line.strip()}
            return tlds
        except Exception as e:
            print(f"Error reading cached TLDs: {e}")
    else:
        tlds = fetch_tlds()
        if tlds:
            try:
                with open(file, 'w') as f:
                    for tld in sorted(tlds):
                        f.write(f"{tld}\n")
            except Exception as e:
                print(f"Error writing TLDs to cache: {e}")
    return tlds if tlds else set()
