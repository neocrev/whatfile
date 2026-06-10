from ..utils import which, run


def describe(path: str) -> dict:
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        info = {
            "format": f"PDF {reader.pdf_header}",
            "pages": len(reader.pages),
        }
        meta = reader.metadata
        if meta:
            if meta.title:
                info["title"] = meta.title
            if meta.author:
                info["author"] = meta.author
        return info
    except ImportError:
        pass

    if which("pdfinfo"):
        out = run(["pdfinfo", path])
        if out:
            info = {"format": "PDF"}
            for line in out.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip().lower()
                    v = v.strip()
                    if k == "pages":
                        info["pages"] = int(v)
                    elif k == "title":
                        info["title"] = v
                    elif k == "author":
                        info["author"] = v
                    elif k == "pdf version":
                        info["format"] = f"PDF {v}"
            return info

    return {"format": "PDF", "note": "install pypdf for details: pip install pypdf"}
