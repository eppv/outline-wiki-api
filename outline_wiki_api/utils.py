import os
import logging
from typing import Union, Tuple
from pathlib import Path
from .const import DEFAULT_URL, MIME_TYPES

log = logging.getLogger(__name__)


def get_base_url(url: str | None = None) -> str:
    """Return the base URL with the trailing slash stripped.
    If the URL is a Falsy value, tries to retrieve URL from environment
    and if it's Falsy anyway return the default URL.
    Returns:
        The base URL
    """
    if not url:
        url = os.getenv("OUTLINE_URL")
        if not url:
            return DEFAULT_URL
    return url.rstrip("/")


def get_token(token: str | None = None) -> str:
    if not token:
        token = os.getenv("OUTLINE_TOKEN")
    return token


def get_supported_mime_type(ext):
    for mime_type, ext_list in MIME_TYPES.items():
        if ext in ext_list:
            return mime_type
    raise ValueError(f"No supported MIME type found for {ext} file extension.")


def get_file_object_for_import(path: Union[str, Path]) -> Tuple:
    root, filename = os.path.split(path)
    file, ext = os.path.splitext(filename)
    try:
        mime_type = get_supported_mime_type(ext)
        return filename, open(path, "rb"), mime_type
    except ValueError as e:
        log.error(f"Unsupported file format extension: '{ext}'. "
                  "Supported formats are: plain text, markdown, docx, csv, tsv, html", exc_info=e)






