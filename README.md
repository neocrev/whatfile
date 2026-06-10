# whatfile

> Show detailed metadata for any file -- images, audio, video, archives, PDFs, and more.

[![PyPI version](https://img.shields.io/pypi/v/whatfile)](https://pypi.org/project/whatfile/)
[![Python versions](https://img.shields.io/pypi/pyversions/whatfile)](https://pypi.org/project/whatfile/)
[![License](https://img.shields.io/pypi/l/whatfile)](LICENSE)

## Install

```bash
pip install whatfile
```

No heavy dependencies required. Optional backends (Pillow, tinytag, pypdf) add more detail automatically when installed.

## Usage

```bash
whatfile photo.jpg song.mp3 video.mp4 archive.zip document.pdf script.py
```

## Quick demo

<img src="assets/whatfile-demo.svg" alt="whatfile terminal demo" width="600">

## Backends

| Format | Info shown | Optional dep |
|--------|-----------|--------------|
| JPEG, PNG, GIF, WebP, BMP, TIFF, AVIF | dimensions, color mode, format | `pip install Pillow` |
| MP3, FLAC, OGG, WAV, M4A, OPUS | duration, bitrate, samplerate, tags | `pip install tinytag` (or ffprobe) |
| MP4, MKV, AVI, MOV, WebM | codec, resolution, fps, duration, bitrate | ffprobe (from ffmpeg) |
| ZIP, TAR, GZ, BZ2, XZ, 7z, RAR | file count, compressed/uncompressed size | stdlib (7z/unrar for extra) |
| PDF | pages, version, title, author | `pip install pypdf` (or pdfinfo) |
| Any file | size, permissions, MIME type | none |

Everything works out of the box. Optional backends enrich the output -- no errors if missing.

## More examples

```bash
# Multiple files at once
whatfile report.pdf screenshot.png backup.tar.gz

# Wildcard (shell expansion)
whatfile ~/Music/*.flac

# All files in directory
whatfile ~/Downloads/*
```

## How it works

`whatfile` classifies files by extension, then dispatches to the appropriate backend. Each backend inspects the file and returns structured metadata. A pretty box-drawing display renders the result.

Detection order per format:
1. **Image** -- Pillow (if installed) extracts dimensions, mode, format
2. **Audio** -- tinytag (if installed) for tags + codec info; falls back to ffprobe
3. **Video** -- ffprobe for codecs, resolution, duration
4. **Archive** -- stdlib zipfile/tarfile for entries + compression ratio; 7z/unrar subprocess for extra formats
5. **PDF** -- pypdf (if installed) for pages, version, metadata; falls back to pdfinfo
6. **Generic** -- os.stat for size/permissions; python-magic or `file` command for MIME type

## License

MIT
