# whatfile

Show detailed metadata for any file — images, audio, video, archives, PDFs, and more.

```bash
pip install whatfile
whatfile image.jpg song.mp3 video.mp4
```

## Backends

| Format | Info shown | Required |
|--------|-----------|----------|
| JPEG, PNG, GIF, WebP, etc. | dimensions, color mode, format | Pillow (pip) |
| MP3, FLAC, OGG, WAV, etc. | duration, bitrate, tags | tinytag (pip) or ffprobe |
| MP4, MKV, AVI, MOV, etc. | codec, resolution, duration | ffprobe |
| ZIP, TAR, GZ, BZ2, XZ | file count, compression ratio | stdlib |
| PDF | pages, version, title, author | pypdf (pip) or pdfinfo |
| Any file | size, permissions, MIME type | — |

## Examples

```bash
whatfile photo.jpg
whatfile *.mp3
whatfile document.pdf archive.tar.gz script.py
```

## License

MIT
