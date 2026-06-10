from ..utils import human_time, which, run


def describe(path: str) -> dict:
    try:
        import tinytag
        tag = tinytag.TinyTag.get(path)
        info = {
            "format": (tag.audio or "unknown").upper(),
            "duration": human_time(tag.duration) if tag.duration else "?",
            "bitrate": f"{tag.bitrate} kbps" if tag.bitrate else "?",
            "samplerate": f"{tag.samplerate} Hz" if tag.samplerate else "?",
            "title": tag.title or "",
            "artist": tag.artist or "",
            "album": tag.album or "",
        }
        return {k: v for k, v in info.items() if v}
    except ImportError:
        pass

    if which("ffprobe"):
        return _describe_ffprobe(path)

    return {"format": "audio", "note": "install tinytag for details: pip install tinytag"}


def _describe_ffprobe(path: str) -> dict:
    out = run([
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ])
    if not out:
        return {"format": "audio", "note": "ffprobe returned no data"}

    import json as j
    try:
        data = j.loads(out)
    except Exception:
        return {"format": "audio"}

    fmt = data.get("format", {})
    streams = data.get("streams", [])
    stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

    info = {
        "format": fmt.get("format_name", "audio").upper(),
        "duration": human_time(float(fmt["duration"])) if fmt.get("duration") else "?",
        "bitrate": f"{int(fmt['bit_rate'])/1000:.0f} kbps" if fmt.get("bit_rate") else "?",
        "codec": stream.get("codec_name", ""),
        "samplerate": f"{stream.get('sample_rate', '?')} Hz",
    }
    tags = fmt.get("tags") or stream.get("tags") or {}
    for k in ("title", "artist", "album"):
        if tags.get(k):
            info[k] = tags[k]

    return {k: v for k, v in info.items() if v}
