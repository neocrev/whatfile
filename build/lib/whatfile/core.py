import os
import mimetypes
from pathlib import Path

from .formats import image, audio, video, archive, pdf, generic

EXTENSION_MAP = {
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".gif": "image",
    ".webp": "image", ".bmp": "image", ".tiff": "image", ".tif": "image",
    ".svg": "image", ".ico": "image", ".avif": "image", ".heic": "image",
    ".mp3": "audio", ".flac": "audio", ".ogg": "audio", ".wav": "audio",
    ".aac": "audio", ".m4a": "audio", ".opus": "audio", ".wma": "audio",
    ".mp4": "video", ".mkv": "video", ".avi": "video", ".mov": "video",
    ".webm": "video", ".wmv": "video", ".flv": "video",
    ".zip": "archive", ".tar": "archive", ".gz": "archive", ".bz2": "archive",
    ".xz": "archive", ".7z": "archive", ".rar": "archive", ".zst": "archive",
    ".pdf": "pdf",
    ".docx": "doc", ".xlsx": "doc",
}


def classify(path: str) -> str:
    ext = Path(path).suffix.lower()
    return EXTENSION_MAP.get(ext, "unknown")


def whatfile(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    stat = p.stat()
    base = {
        "path": path,
        "name": p.name,
        "size": stat.st_size,
        "created": stat.st_ctime,
        "modified": stat.st_mtime,
        "kind": classify(path),
    }

    kind = base["kind"]
    try:
        if kind == "image":
            info = image.describe(path)
        elif kind == "audio":
            info = audio.describe(path)
        elif kind == "video":
            info = video.describe(path)
        elif kind == "archive":
            info = archive.describe(path)
        elif kind == "pdf":
            info = pdf.describe(path)
        else:
            info = generic.describe(path)
    except Exception as e:
        info = {"note": str(e)}

    base["info"] = info
    return base
