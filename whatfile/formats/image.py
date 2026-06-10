def describe(path: str) -> dict:
    try:
        from PIL import Image
        img = Image.open(path)
        info = {
            "format": img.format or "unknown",
            "width": img.width,
            "height": img.height,
            "mode": img.mode,
        }
        exif = getattr(img, "_getexif", None)
        if exif:
            data = exif()
            if data:
                info["exif"] = bool(data)
        img.close()
        return info
    except ImportError:
        return _describe_fallback(path)


def _describe_fallback(path: str) -> dict:
    return {"format": "image", "note": "install Pillow for details: pip install Pillow"}
