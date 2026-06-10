from ..utils import human_time, which, run


def describe(path: str) -> dict:
    if not which("ffprobe"):
        return {"format": "video", "note": "install ffprobe (ffmpeg) for details"}

    out = run([
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ])
    if not out:
        return {"format": "video", "note": "ffprobe returned no data"}

    import json as j
    try:
        data = j.loads(out)
    except Exception:
        return {"format": "video"}

    fmt = data.get("format", {})
    streams = data.get("streams", [])
    vstream = next((s for s in streams if s.get("codec_type") == "video"), {})
    astream = next((s for s in streams if s.get("codec_type") == "audio"), {})

    info = {
        "format": fmt.get("format_name", "video").upper(),
        "duration": human_time(float(fmt["duration"])) if fmt.get("duration") else "?",
        "size": f"{vstream.get('width', '?')}x{vstream.get('height', '?')}",
        "video": vstream.get("codec_name", ""),
        "audio": astream.get("codec_name", ""),
        "fps": vstream.get("r_frame_rate", ""),
        "bitrate": f"{int(fmt['bit_rate'])/1000:.0f} kbps" if fmt.get("bit_rate") else "",
    }
    return {k: v for k, v in info.items() if v}
