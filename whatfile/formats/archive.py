import io
import os
import tarfile
import zipfile
from pathlib import Path

from ..utils import human_size, which, run


def describe(path: str) -> dict:
    p = Path(path)
    ext = p.suffix.lower()

    if ext in (".zip", ".jar", ".war", ".xlsx", ".docx"):
        return _describe_zip(path)
    elif ext in (".tar", ".gz", ".bz2", ".xz", ".zst"):
        return _describe_tar(path)
    elif ext == ".7z":
        return _describe_7z(path)
    elif ext == ".rar":
        return _describe_rar(path)
    return {"format": "archive"}


def _describe_zip(path: str) -> dict:
    try:
        with zipfile.ZipFile(path, "r") as zf:
            infos = zf.infolist()
            total = len(infos)
            dirs = sum(1 for i in infos if i.is_dir())
            files = total - dirs
            compressed = os.path.getsize(path)
            uncompressed = sum(i.file_size for i in infos)
            return {
                "format": "ZIP",
                "files": files,
                "dirs": dirs,
                "compressed": human_size(compressed),
                "uncompressed": human_size(uncompressed),
            }
    except Exception as e:
        return {"format": "ZIP", "note": str(e)}


def _describe_tar(path: str) -> dict:
    try:
        mode = "r"
        p = Path(path)
        ext = p.suffix.lower()
        if ext == ".gz":
            mode = "r:gz"
        elif ext == ".bz2":
            mode = "r:bz2"
        elif ext == ".xz":
            mode = "r:xz"
        elif ext == ".zst":
            mode = "r:zst"

        with tarfile.open(path, mode) as tf:
            members = tf.getmembers()
            files = sum(1 for m in members if m.isfile())
            dirs = sum(1 for m in members if m.isdir())
            compressed = os.path.getsize(path)
            uncompressed = sum(m.size for m in members)
            return {
                "format": f"tar/{ext.lstrip('.')}".upper(),
                "files": files,
                "dirs": dirs,
                "compressed": human_size(compressed),
                "uncompressed": human_size(uncompressed),
            }
    except Exception as e:
        return {"format": "TAR", "note": str(e)}


def _describe_7z(path: str) -> dict:
    if not which("7z"):
        return {"format": "7z", "note": "install p7zip for details"}
    out = run(["7z", "l", path])
    if not out:
        return {"format": "7z"}
    files = out.count("\n")
    return {"format": "7z", "files": files}


def _describe_rar(path: str) -> dict:
    if not which("unrar"):
        return {"format": "RAR", "note": "install unrar for details"}
    out = run(["unrar", "l", path])
    if not out:
        return {"format": "RAR"}
    return {"format": "RAR"}
