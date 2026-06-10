import os
from ..utils import human_size, which, run


def describe(path: str) -> dict:
    stat = os.stat(path)
    info = {
        "size": human_size(stat.st_size),
        "permissions": oct(stat.st_mode & 0o777),
    }
    if stat.st_mode & 0o100:
        info["executable"] = True

    mime = _detect_mime(path)
    if mime:
        info["mime"] = mime

    return info


def _detect_mime(path: str) -> str | None:
    try:
        import magic
        return magic.from_file(path, mime=True)
    except ImportError:
        pass
    if which("file"):
        out = run(["file", "--mime-type", "-b", path])
        if out:
            return out
    return None
