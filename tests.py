import os
import sys
import tempfile
import tarfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from whatfile import whatfile
from whatfile import utils


def test_generic_file():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        f.write("hello world")
        path = f.name

    try:
        result = whatfile(path)
        assert result["kind"] == "unknown"
        assert result["info"]["size"] == "11 B"
        assert "permissions" in result["info"]
    finally:
        os.unlink(path)


def test_zip():
    path = "/tmp/test_whatfile.zip"
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("a.txt", "a" * 100)
        zf.writestr("b.txt", "b" * 200)
        zf.writestr("sub/c.txt", "c" * 50)

    try:
        result = whatfile(path)
        assert result["kind"] == "archive"
        assert result["info"]["format"] == "ZIP"
        assert result["info"]["files"] == 3
        assert "dirs" in result["info"]
        assert "compressed" in result["info"]
        assert "uncompressed" in result["info"]
    finally:
        os.unlink(path)


def test_tar_gz():
    path = "/tmp/test_whatfile.tar.gz"
    with tarfile.open(path, "w:gz") as tf:
        for name, content in [("a.txt", b"a" * 100), ("b.txt", b"b" * 200)]:
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            tf.addfile(info, io.BytesIO(content))

    try:
        result = whatfile(path)
        assert result["kind"] == "archive"
        assert result["info"]["format"] == "TAR/GZ"
        assert result["info"]["files"] == 2
    finally:
        os.unlink(path)


def test_display_output():
    from whatfile.display import _format_info, _info_rows

    result = {
        "path": "/tmp/test.txt",
        "name": "test.txt",
        "size": 1234,
        "modified": 1000000000,
        "kind": "unknown",
        "info": {"mime": "text/plain", "note": "no specific handler"},
    }

    rows = _format_info(result)
    assert len(rows) >= 3
    labels = [r[0] for r in rows]
    assert "Size" in labels
    assert "MIME" in labels
    assert "Modified" in labels


def test_human_size():
    assert utils.human_size(0) == "0 B"
    assert utils.human_size(500) == "500 B"
    assert utils.human_size(1024) == "1.0 KB"
    assert utils.human_size(1536) == "1.5 KB"
    assert utils.human_size(1048576) == "1.0 MB"
    assert utils.human_size(1073741824) == "1.0 GB"


def test_human_time():
    assert utils.human_time(0) == "0:00"
    assert utils.human_time(30) == "0:30"
    assert utils.human_time(90) == "1:30"
    assert utils.human_time(3661) == "1:01:01"


def test_file_not_found():
    try:
        whatfile("/nonexistent/path")
        assert False, "should raise"
    except FileNotFoundError:
        pass


import io

if __name__ == "__main__":
    test_generic_file()
    test_zip()
    test_tar_gz()
    test_display_output()
    test_human_size()
    test_human_time()
    test_file_not_found()
    print("ALL TESTS PASSED")
