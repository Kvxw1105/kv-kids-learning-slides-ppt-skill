#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render PPTX to PDF and per-slide PNG files")
    parser.add_argument("pptx")
    parser.add_argument("--out", default="rendered")
    parser.add_argument("--dpi", type=int, default=144)
    args = parser.parse_args()

    office = shutil.which("libreoffice") or shutil.which("soffice")
    if not office:
        print("LibreOffice/soffice not found", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    source = Path(args.pptx).resolve()
    subprocess.run(
        [office, "--headless", "--convert-to", "pdf", "--outdir", str(out), str(source)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    pdf = out / f"{source.stem}.pdf"
    if not pdf.exists():
        candidates = sorted(out.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            print("LibreOffice did not produce a PDF", file=sys.stderr)
            return 3
        pdf = candidates[0]

    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        prefix = out / "slide"
        subprocess.run(
            [pdftoppm, "-png", "-r", str(args.dpi), str(pdf), str(prefix)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    else:
        magick = shutil.which("magick") or shutil.which("convert")
        if not magick:
            print("PDF rendered, but no pdftoppm/ImageMagick found for PNG export", file=sys.stderr)
            print(out)
            return 0
        subprocess.run(
            [magick, "-density", str(args.dpi), str(pdf), str(out / "slide-%02d.png")],
            check=True,
        )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
