
from outline_wiki_api import const


def get_base_url(url: str | None = None) -> str:
    """Return the base URL with the trailing slash stripped.
    If the URL is a Falsy value, return the default URL.
    Returns:
        The base URL
    """
    if not url:
        return const.DEFAULT_URL

    return url.rstrip("/")

