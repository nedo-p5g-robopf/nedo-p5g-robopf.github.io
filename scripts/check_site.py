#!/usr/bin/env python3
"""Check the actual Jekyll output, including internal fragments and asset links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.lang = None
        self.h1_count = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1_count += 1
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    prefix = sys.argv[2].rstrip("/") if len(sys.argv) > 2 else ""
    pages = {p.resolve(): Page(p) for p in root.rglob("*.html")}
    errors = []
    if len(pages) < 20:
        errors.append(f"Expected at least 20 rendered pages, found {len(pages)}")
    for path, page in pages.items():
        label = path.relative_to(root)
        if page.lang != "ja" or page.h1_count != 1:
            errors.append(f"{label}: expected lang=ja and one h1")
        if page.duplicates:
            errors.append(f"{label}: duplicate IDs {page.duplicates}")
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            local = unquote(parsed.path)
            if local.startswith("/"):
                if prefix and not (local == prefix or local.startswith(prefix + "/")):
                    errors.append(f"{label}: link missing baseurl {link}")
                    continue
                local = local[len(prefix):] if prefix else local
                target = root / local.lstrip("/")
            elif not local:
                target = path
            else:
                target = path.parent / local
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.is_file():
                errors.append(f"{label}: missing target {link}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f"{label}: missing anchor {link}")
    sitemap = ET.parse(root / "sitemap.xml")
    urls = [n.text for n in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    if len(urls) != len(set(urls)):
        errors.append("Sitemap contains duplicate URLs")
    if len(urls) != len(pages) - 1:
        errors.append("Sitemap must include all pages except the 404 page")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(pages)} HTML pages; local links, fragments, language, headings; {len(urls)} sitemap entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
