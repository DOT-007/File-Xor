from urllib.parse import urlparse


def normalize_base_url(base: str) -> str:
    """Normalize a base URL: ensure scheme (https) and no trailing slash.

    Returns an empty string if base is falsy.
    """
    if not base:
        return ""
    base = base.strip()
    if not base:
        return ""
    if not (base.startswith("http://") or base.startswith("https://")):
        base = "https://" + base
    return base.rstrip('/')


def is_valid_http_url(url: str) -> bool:
    if not url:
        return False
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False
