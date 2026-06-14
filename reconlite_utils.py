"""Validation and command-building helpers for ReconLite.

These functions avoid network, database, and subprocess side effects so they
can be tested safely in CI.
"""

from __future__ import annotations

import ipaddress
import re


HOSTNAME_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)


def parse_ports(raw_ports: str) -> list[int]:
    """Parse comma-separated TCP ports and validate the 1-65535 range."""
    if raw_ports is None or raw_ports.strip() == "":
        raise ValueError("ports are required as comma-separated numbers")

    ports: list[int] = []
    for raw_part in raw_ports.split(","):
        part = raw_part.strip()
        if part == "":
            raise ValueError("ports cannot contain empty values")
        if not part.isdigit():
            raise ValueError(f"invalid port '{part}': ports must be numeric")

        port = int(part)
        if port < 1 or port > 65535:
            raise ValueError(f"invalid port '{part}': port must be between 1 and 65535")
        ports.append(port)

    return ports


def parse_positive_int(
    value: str,
    name: str,
    minimum: int = 1,
    maximum: int | None = None,
) -> int:
    """Parse and validate a positive integer option used by scanner controls."""
    if value is None or str(value).strip() == "":
        raise ValueError(f"{name} is required")

    try:
        parsed = int(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc

    if parsed < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    if maximum is not None and parsed > maximum:
        raise ValueError(f"{name} must be at most {maximum}")

    return parsed


def is_private_or_local_scope(scope: str) -> bool:
    """Return True when a scope is localhost, loopback, or private IP/CIDR."""
    if scope is None:
        return False

    normalized = scope.strip().lower()
    if normalized == "localhost":
        return True
    if normalized == "":
        return False

    try:
        network = ipaddress.ip_network(normalized, strict=False)
    except ValueError:
        return False

    return network.is_private or network.is_loopback


def _is_valid_ip_cidr_or_hostname(scope: str) -> bool:
    try:
        ipaddress.ip_network(scope, strict=False)
        return True
    except ValueError:
        return HOSTNAME_PATTERN.match(scope) is not None


def validate_scan_scope(scope: str, allow_public_scan: bool = False) -> str:
    """Validate a scan scope and return the normalized value when allowed.

    Public IP/CIDR scopes are rejected by default. Set ``allow_public_scan`` only
    for explicitly authorized environments where public scopes are in scope.
    """
    if scope is None or scope.strip() == "":
        raise ValueError("scan scope is required")

    normalized = scope.strip()
    if is_private_or_local_scope(normalized):
        return normalized.lower() if normalized.lower() == "localhost" else normalized

    if not _is_valid_ip_cidr_or_hostname(normalized):
        raise ValueError("scan scope must be a valid IP address, CIDR range, or hostname")

    if not allow_public_scan:
        raise ValueError(
            "public scan scopes are disabled by default; use private/local scopes "
            "or set ALLOW_PUBLIC_SCAN=true only for explicitly authorized targets"
        )

    return normalized


def build_scanner_command(
    scanner_path: str,
    masscan_rate: int,
    timeout: int,
    chunk_size: int,
    ports: list[int],
) -> list[str]:
    """Build a list-based scanner subprocess command without shell syntax."""
    if not scanner_path or scanner_path.strip() == "":
        raise ValueError("scanner_path is required")
    if not ports:
        raise ValueError("at least one port is required")

    port_arg = ",".join(str(port) for port in ports)
    return [
        "python3",
        scanner_path,
        str(masscan_rate),
        str(timeout),
        str(chunk_size),
        port_arg,
    ]
