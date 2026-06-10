import os
import shutil
import time
from .utils import human_size


def print_results(results: list[dict]) -> None:
    multi = len(results) > 1
    term_w = shutil.get_terminal_size().columns

    for i, r in enumerate(results):
        path = r.get("path", "?")
        name = r.get("name", path)

        if "error" in r:
            _print_error(name, r["error"])
            continue

        lines = _format_info(r)
        _print_box(name, lines, term_w, multi)


def _print_error(name: str, msg: str) -> None:
    print(f"\u2570\u2500 {name} \u2500 {msg}")


def _format_info(r: dict) -> list[tuple[str, str]]:
    info = r.get("info", {})
    size = human_size(r.get("size", 0))
    modified = time.strftime("%Y-%m-%d %H:%M", time.localtime(r.get("modified", 0)))

    rows = [("Size", size)]
    rows.extend(_info_rows(info))
    rows.append(("Modified", modified))
    return rows


def _info_rows(info: dict) -> list[tuple[str, str]]:
    key_map = {
        "format": "Type",
        "width": "Width",
        "height": "Height",
        "mode": "Color",
        "duration": "Duration",
        "bitrate": "Bitrate",
        "samplerate": "Sample rate",
        "codec": "Codec",
        "video": "Video codec",
        "audio": "Audio codec",
        "fps": "FPS",
        "title": "Title",
        "artist": "Artist",
        "album": "Album",
        "pages": "Pages",
        "files": "Files",
        "dirs": "Dirs",
        "compressed": "Compressed",
        "uncompressed": "Uncompressed",
        "permissions": "Permissions",
        "mime": "MIME",
        "author": "Author",
    }

    rows = []
    for k, v in info.items():
        if k in ("note", "exif", "size") or not v:
            continue
        label = key_map.get(k, k.replace("_", " ").title())
        rows.append((label, str(v)))

    if info.get("exif"):
        rows.append(("EXIF", "yes"))
    if info.get("executable"):
        rows.append(("Executable", "yes"))
    if info.get("note"):
        rows.append(("Note", info["note"]))

    return rows


def _print_box(name: str, rows: list[tuple[str, str]], term_w: int, multi: bool) -> None:
    max_key = max((len(k) for k, _ in rows), default=0)
    vals = [str(v) for _, v in rows]
    content_w = max(len(name), max_key + 3 + max(len(v) for v in vals))
    content_w = min(content_w, term_w - 4)
    if content_w < 20:
        content_w = 20

    box_w = content_w + 4

    top_dashes = box_w - len(name) - 5
    top = f"\u256d\u2500 {name} " + "\u2500" * top_dashes + "\u256e"
    print(top)

    for key, val in rows:
        val_s = str(val)
        avail = content_w - max_key - 3
        if len(val_s) > avail:
            val_s = val_s[: avail - 1] + "\u2026"
        pad = content_w - max_key - 3 - len(val_s)
        print(f"\u2502  {key.rjust(max_key)}: {val_s}{' ' * pad}\u2502")

    print(f"\u2570" + "\u2500" * (box_w - 2) + "\u256f")

    if multi:
        print()
