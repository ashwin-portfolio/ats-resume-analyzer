"""
Small, dependency-light validation helpers.

These helpers avoid importing FastAPI/SQLAlchemy/etc. so they can be reused in:
- API routes
- background jobs
- tests
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Optional, Sequence


_REPORT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
_FILENAME_SAFE_RE = re.compile(r"[^a-zA-Z0-9._\s-]")


def sanitize_filename(filename: str, *, default: str = "resume", max_length: int = 255) -> str:
    """
    Sanitize a user-provided filename to mitigate path traversal and odd characters.

    - Strips directory components
    - Removes dangerous characters (keeps alnum, dot, underscore, hyphen, space)
    - Caps length
    """
    if not filename:
        return default

    # Remove any path components (prevents directory traversal)
    filename = os.path.basename(filename)

    # Remove or replace dangerous characters
    filename = _FILENAME_SAFE_RE.sub("", filename)

    if max_length > 0 and len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        # Keep extension; cap overall length.
        ext_max = min(len(ext), 20)  # extensions are small; cap defensively
        filename = name[: max(1, max_length - ext_max)] + ext[:ext_max]

    return filename or default


def get_lower_extension(filename: str) -> Optional[str]:
    """
    Return the lowercase extension including dot (e.g. '.pdf'), or None if missing.
    """
    if not filename or "." not in filename:
        return None
    return "." + filename.rsplit(".", 1)[-1].lower()


def is_valid_report_id(report_id: str) -> bool:
    """
    Report IDs are expected to be short opaque tokens (e.g. UUID-ish).
    We allow alphanumeric + '_' + '-' with a conservative length bound.
    """
    if not report_id:
        return False
    return _REPORT_ID_RE.fullmatch(report_id) is not None


@dataclass(frozen=True)
class UploadInfo:
    sanitized_filename: str
    file_extension: str  # includes dot, lowercase


def normalize_upload_filename(
    filename: str,
    *,
    allowed_extensions: Sequence[str],
    allow_legacy_doc: bool = True,
) -> UploadInfo:
    """
    Sanitize a filename and validate its extension.

    Raises:
        ValueError: with a user-facing message suitable for 4xx errors.
    """
    if not filename:
        raise ValueError("File must have a filename")

    sanitized = sanitize_filename(filename)
    ext = get_lower_extension(sanitized)
    if ext is None:
        raise ValueError(f"File must have an extension. Allowed: {', '.join(allowed_extensions)}")

    # `.doc` is commonly uploaded but is not parseable by python-docx.
    if ext == ".doc" and allow_legacy_doc:
        raise ValueError("Legacy .doc files are not supported. Please convert to .docx.")

    allowed_set = {e.lower() for e in allowed_extensions}
    if ext not in allowed_set:
        raise ValueError(f"Invalid file format. Allowed: {', '.join(allowed_extensions)}")

    return UploadInfo(sanitized_filename=sanitized, file_extension=ext)


def clamp_int(value: int, *, min_value: int, max_value: int) -> int:
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value

