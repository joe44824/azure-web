from pathlib import Path
from typing import List, Tuple
from fastapi import UploadFile
import datetime

UPLOAD_DIR = Path("uploads")

if not UPLOAD_DIR.exists():
    UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    dest = UPLOAD_DIR / file.filename
    contents = file.file.read()
    with open(dest, "wb") as f:
        f.write(contents)
    return file.filename


def list_uploaded_files() -> List[Tuple[str, int, datetime.datetime]]:
    """
    Returns (filename, size_in_bytes, modified_time).
    Uses file mtime as "upload time".
    """
    if not UPLOAD_DIR.exists():
        return []

    files = []
    for path in UPLOAD_DIR.iterdir():
        if path.is_file():
            st = path.stat()
            files.append((path.name, st.st_size, datetime.datetime.fromtimestamp(st.st_mtime)))
    return files


def format_size(n: int) -> str:
    """Convert bytes to human‑readable string."""
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 / 1024:.1f} MB"