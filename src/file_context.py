from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from PIL import Image
from pypdf import PdfReader


def _read_text_like(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)


def _read_image_metadata(path: Path) -> str:
    with Image.open(path) as img:
        exif = {}
        if hasattr(img, "getexif"):
            exif_raw = img.getexif()
            exif = {str(k): str(v) for k, v in exif_raw.items()} if exif_raw else {}

        payload = {
            "file": path.name,
            "format": img.format,
            "mode": img.mode,
            "size": {"width": img.width, "height": img.height},
            "exif": exif,
        }
        return json.dumps(payload, ensure_ascii=True)


def build_file_context(file_paths: Iterable[str], max_chars: int = 12000) -> str:
    chunks: list[str] = []

    for raw in file_paths:
        path = Path(raw.strip()).expanduser().resolve()
        if not path.exists() or not path.is_file():
            chunks.append(f"[SKIPPED] {raw} (missing or not a file)")
            continue

        suffix = path.suffix.lower()
        try:
            if suffix in {".txt", ".md", ".py", ".json", ".csv", ".yaml", ".yml"}:
                content = _read_text_like(path)
                chunks.append(f"[DOC] {path.name}\n{content}")
            elif suffix == ".pdf":
                content = _read_pdf(path)
                chunks.append(f"[PDF] {path.name}\n{content}")
            elif suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}:
                metadata = _read_image_metadata(path)
                chunks.append(f"[IMAGE] {path.name}\n{metadata}")
            else:
                chunks.append(f"[SKIPPED] {path.name} (unsupported type)")
        except Exception as exc:
            chunks.append(f"[ERROR] {path.name}: {exc}")

    context = "\n\n".join(chunks)
    if len(context) <= max_chars:
        return context

    return context[:max_chars] + "\n\n[TRUNCATED] Context exceeded limit."
