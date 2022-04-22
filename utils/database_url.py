from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs, unquote, urlsplit


@dataclass(frozen=True)
class DatabaseConnectionInfo:
    hostname: Optional[str]
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]
    name: Optional[str]
    options: dict[str, Optional[str]]


def parse(url: str) -> DatabaseConnectionInfo:
    """Parses a database URL."""

    url = urlsplit(url)
    path = url.path[1:]
    query = parse_qs(url.query)
    port = url.port

    # Handle postgres percent-encoded paths.
    hostname = url.hostname or ""
    if "%2f" in hostname.lower():
        # Switch to url.netloc to avoid lower cased paths
        hostname = url.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = hostname.replace("%2f", "/").replace("%2F", "/")

    # Update with environment configuration.
    name = unquote(path or "") or None
    username = unquote(url.username or "") or None
    password = unquote(url.password or "") or None
    port = port or None

    # Pass the query string into OPTIONS.
    options = {}
    for key, values in query.items():
        options[key] = values[-1] or None

    return DatabaseConnectionInfo(
        hostname=hostname or None,
        port=port or None,
        username=username or None,
        password=password or None,
        name=name or None,
        options=options,
    )
