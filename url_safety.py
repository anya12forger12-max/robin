"""URL validation for onion search results and scraped pages.

Search results come from third-party pages and must never be treated as
trusted destinations. In particular, a URL like
``http://example.onion@169.254.169.254/`` has an ``.onion`` *userinfo*
component but connects to the metadata service, bypassing Tor.
"""

from urllib.parse import urlparse


def is_safe_onion_url(url: str) -> bool:
    """Return True only for http(s) URLs whose real host is an onion service."""
    if not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return False
    if parsed.scheme not in ('http', 'https') or not parsed.hostname:
        return False
    if parsed.username or parsed.password:
        return False
    host = parsed.hostname.lower().rstrip('.')
    if not host.endswith('.onion'):
        return False
    # Onion v2/v3 hostnames contain only these characters.
    if any(char not in 'abcdefghijklmnopqrstuvwxyz0123456789.-' for char in host):
        return False
    try:
        parsed.port
    except ValueError:
        return False
    return True


def extract_onion_link(value: str) -> str | None:
    """Return *value* if it is a safe absolute onion URL, else None."""
    if not isinstance(value, str):
        return None
    url = value.strip()
    if not is_safe_onion_url(url):
        return None
    return url
