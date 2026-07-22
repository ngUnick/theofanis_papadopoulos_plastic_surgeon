"""Validate the static GEO/medical release without third-party dependencies."""

from __future__ import annotations

import json
import html
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
HOST = "https://theofanispapadopoulos.gr"
ROUTES = {
    "/": "index.html",
    "/about": "about.html",
    "/procedures": "procedures.html",
    "/non-invasive": "non-invasive.html",
    "/reconstructive": "reconstructive.html",
    "/media": "media.html",
    "/faq": "faq.html",
    "/contact": "contact.html",
    "/non-invasive/botouliniki-toxini": "guide-botouliniki-toxini.html",
    "/non-invasive/yalouroniko-fillers": "guide-yalouroniko-fillers.html",
    "/non-invasive/laser-apotrichosi": "guide-laser-apotrichosi.html",
    "/procedures/lipoanarrofisi": "guide-lipoanarrofisi.html",
    "/reconstructive/oules-egkavmaton": "guide-oules-egkavmaton.html",
    "/privacy": "privacy.html",
    "/image-credits": "image-credits.html",
}
INDEXABLE = set(ROUTES) - {"/privacy", "/image-credits"}
ALLOWED_SCHEMA = {"Physician", "WebPage", "MedicalWebPage", "BreadcrumbList", "FAQPage"}


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.contact_ctas = 0
        self.images: list[str] = []
        self.iframes: list[str] = []
        self.scripts: list[str] = []
        self.canonicals: list[str] = []
        self.og_urls: list[str] = []
        self.robots: list[str] = []
        self.json_docs: list[dict] = []
        self._json = False
        self._json_parts: list[str] = []
        self._main = False
        self.main_text: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if attrs.get("id"):
            self.ids.append(str(attrs["id"]))
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(str(attrs["href"]))
            if attrs.get("href") == "/contact" and "btn" in str(attrs.get("class", "")).split():
                self.contact_ctas += 1
        if tag == "img" and attrs.get("src"):
            self.images.append(str(attrs["src"]))
        if tag == "iframe" and attrs.get("src"):
            self.iframes.append(str(attrs["src"]))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(str(attrs["src"]))
        if tag == "link" and attrs.get("rel") == "canonical" and attrs.get("href"):
            self.canonicals.append(str(attrs["href"]))
        if tag == "meta" and attrs.get("property") == "og:url" and attrs.get("content"):
            self.og_urls.append(str(attrs["content"]))
        if tag == "meta" and attrs.get("name") == "robots" and attrs.get("content"):
            self.robots.append(str(attrs["content"]))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._json = True
            self._json_parts = []
        if tag == "main":
            self._main = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json:
            self.json_docs.append(json.loads("".join(self._json_parts)))
            self._json = False
        if tag == "main":
            self._main = False

    def handle_data(self, data: str) -> None:
        if self._json:
            self._json_parts.append(data)
        if self._main:
            self.main_text.append(data)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def local_asset_exists(value: str, route: str) -> bool:
    path = urlsplit(value).path
    if not path or path in ROUTES:
        return True
    if not path.startswith("/"):
        parent = route.rsplit("/", 1)[0] or "/"
        path = f"{parent.rstrip('/')}/{path}"
    candidate = ROOT / path.lstrip("/")
    return candidate.is_file()


def main() -> int:
    errors: list[str] = []
    documents: dict[str, Document] = {}
    ids_by_route: dict[str, set[str]] = {}

    for route, source in ROUTES.items():
        page = ROOT / source
        if not page.is_file():
            fail(errors, f"missing source: {source}")
            continue
        parser = Document()
        try:
            parser.feed(page.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            fail(errors, f"{source}: parse error: {exc}")
            continue
        documents[route] = parser
        ids_by_route[route] = set(parser.ids)
        if len(parser.ids) != len(set(parser.ids)):
            fail(errors, f"{source}: duplicate id")
        expected = HOST + (route if route != "/" else "/")
        if parser.canonicals != [expected]:
            fail(errors, f"{source}: canonical {parser.canonicals!r}, expected {expected}")
        if parser.og_urls != [expected]:
            fail(errors, f"{source}: og:url {parser.og_urls!r}, expected {expected}")
        if route in {"/privacy", "/image-credits"}:
            if not any("noindex" in value.lower() for value in parser.robots):
                fail(errors, f"{source}: missing noindex")
        elif any("noindex" in value.lower() for value in parser.robots):
            fail(errors, f"{source}: unexpected noindex")
        if parser.iframes:
            fail(errors, f"{source}: iframe remains")
        for src in parser.images:
            if urlsplit(src).scheme in {"http", "https"}:
                fail(errors, f"{source}: remote image {src}")
            elif not local_asset_exists(src, route):
                fail(errors, f"{source}: missing image {src}")
        for src in parser.scripts:
            if urlsplit(src).scheme in {"http", "https"}:
                fail(errors, f"{source}: remote script {src}")
            elif not local_asset_exists(src, route):
                fail(errors, f"{source}: missing script {src}")
        if len(parser.scripts) != len(set(parser.scripts)):
            fail(errors, f"{source}: duplicate script source")
        for schema in parser.json_docs:
            for node in schema.get("@graph", [schema]):
                types = node.get("@type", [])
                types = [types] if isinstance(types, str) else types
                unexpected = set(types) - ALLOWED_SCHEMA
                if unexpected:
                    fail(errors, f"{source}: unsupported schema types {sorted(unexpected)}")

    for route, parser in documents.items():
        source = ROUTES[route]
        for href in parser.hrefs:
            parsed = urlsplit(href)
            if parsed.scheme in {"mailto", "tel", "http", "https"}:
                continue
            if ".html" in parsed.path:
                fail(errors, f"{source}: internal .html link {href}")
                continue
            target_route = parsed.path or route
            if not target_route.startswith("/"):
                candidate = (ROOT / target_route)
                if not candidate.is_file():
                    fail(errors, f"{source}: missing relative target {href}")
                continue
            if target_route not in ROUTES:
                fail(errors, f"{source}: unknown internal route {href}")
                continue
            if parsed.fragment and parsed.fragment not in ids_by_route.get(target_route, set()):
                fail(errors, f"{source}: missing fragment target {href}")

    for route in [value for value in ROUTES if "guide" not in value]:
        if route not in documents or not ROUTES[route].startswith("guide-"):
            continue
    for route, source in ROUTES.items():
        if not source.startswith("guide-"):
            continue
        words = re.findall(r"\w+", " ".join(documents[route].main_text), flags=re.UNICODE)
        if not 900 <= len(words) <= 1400:
            fail(errors, f"{source}: {len(words)} words, expected 900-1400")
        if documents[route].contact_ctas != 1:
            fail(errors, f"{source}: expected exactly one final /contact CTA")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {node.text for node in sitemap.findall("s:url/s:loc", ns)}
    expected_urls = {HOST + (route if route != "/" else "/") for route in INDEXABLE}
    if sitemap_urls != expected_urls:
        fail(errors, f"sitemap mismatch: missing={sorted(expected_urls-sitemap_urls)}, extra={sorted(sitemap_urls-expected_urls)}")

    combined = "\n".join((ROOT / source).read_text(encoding="utf-8") for source in ROUTES.values())
    for forbidden in (
        "img.youtube.com",
        "output=embed",
        "<iframe",
        "GoogleAnalyticsObject",
        "gtag(",
        "clarity(",
        "Plastic Surgeon",
        "ουδέτερ",
        "testimonials",
        "πριν–μετά",
        "χωρίς συγκρίσεις",
        "face-breast-body.webp",
        "Το παρόν περιεχόμενο είναι ενημερωτικό",
        "Οι πληροφορίες είναι γενικές και δεν υποκαθιστούν",
        "Το περιεχόμενο είναι ενημερωτικό και δεν υποκαθιστά",
        "υπηρεσία του ιατρείου",
        "Ο ιστότοπος παρέχει γενικές πληροφορίες",
        "Δεν υφίσταται σύγκρουση συμφερόντων",
    ):
        if forbidden.lower() in combined.lower():
            fail(errors, f"forbidden remote/embed/analytics marker: {forbidden}")

    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    for image in (
        "photos/home-non-invasive.webp",
        "photos/home-procedures.webp",
        "photos/home-reconstructive.webp",
    ):
        if image not in homepage:
            fail(errors, f"index.html: missing homepage category image {image}")
    if len(re.findall(r'class="pill(?:\s|\")', homepage)) != 3:
        fail(errors, "index.html: expected exactly three category pills")
    for source in ("procedures.html", "non-invasive.html"):
        content = (ROOT / source).read_text(encoding="utf-8")
        if re.search(r'class="pill(?:\s|\")', content):
            fail(errors, f"{source}: catalogue pill remains")

    footer_notice = (
        "Οι πληροφορίες του ιστοτόπου είναι γενικές και δεν αντικαθιστούν "
        "την ιατρική εξέταση ή την εξατομικευμένη συμβουλή."
    )
    for source in ROUTES.values():
        content = (ROOT / source).read_text(encoding="utf-8")
        if content.count(footer_notice) != 1:
            fail(errors, f"{source}: expected exactly one shared footer notice")
        for old_label in ("Βίντεο και συνεντεύξεις", "Βίντεο και κοινωνικά δίκτυα"):
            if re.search(rf">\s*{re.escape(old_label)}\s*<", content, flags=re.IGNORECASE):
                fail(errors, f"{source}: old visible media label remains: {old_label}")

    faq_source = (ROOT / "faq.html").read_text(encoding="utf-8")
    def visible_text(fragment: str) -> str:
        return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())
    visible_faqs = [
        (visible_text(question), visible_text(answer))
        for question, answer in re.findall(
            r'<details class="faq">\s*<summary>(.*?)</summary>(.*?)</details>',
            faq_source,
            flags=re.DOTALL,
        )
    ]
    faq_nodes = []
    for schema in documents["/faq"].json_docs:
        for node in schema.get("@graph", [schema]):
            types = node.get("@type", [])
            if "FAQPage" in (types if isinstance(types, list) else [types]):
                faq_nodes = [
                    (item.get("name", ""), item.get("acceptedAnswer", {}).get("text", ""))
                    for item in node.get("mainEntity", [])
                ]
    if faq_nodes != visible_faqs:
        fail(errors, "faq.html: FAQPage questions/answers do not exactly match visible text")
    if len(visible_faqs) != 20:
        fail(errors, f"faq.html: expected 20 visible FAQs, found {len(visible_faqs)}")
    for question, answer in visible_faqs:
        word_count = len(re.findall(r"\w+", answer, flags=re.UNICODE))
        if not 30 <= word_count <= 55:
            fail(errors, f"faq.html: answer for {question!r} has {word_count} words, expected 30-55")

    credits = (ROOT / "image-credits.html").read_text(encoding="utf-8")
    for asset_name in (
        "Hair follicle.svg",
        "Human body features-textless.svg",
        "Scheme human hand bones - no text.svg",
    ):
        if asset_name not in credits:
            fail(errors, f"image-credits.html: missing homepage source {asset_name}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for agent in ("OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Applebot", "GPTBot", "ClaudeBot", "CCBot", "Applebot-Extended", "Google-Extended"):
        if f"User-agent: {agent}" not in robots:
            fail(errors, f"robots.txt: missing {agent}")

    apache = (ROOT / ".htaccess").read_text(encoding="utf-8")
    ordered_markers = [
        "# Canonical host and HTTPS in one hop",
        "# /index.html -> /",
        "# Flat source files for nested guide URLs",
        "# Root-level *.html -> extensionless",
        "# Canonicalize trailing slashes",
        "# Explicit nested public routes",
        "# Internally map remaining extensionless routes",
    ]
    positions = [apache.find(marker) for marker in ordered_markers]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        fail(errors, ".htaccess: canonical redirect/rewrite sections are missing or out of order")
    for public_route, source in ROUTES.items():
        if not source.startswith("guide-"):
            continue
        route_pattern = public_route.lstrip("/")
        if f"RewriteRule ^{route_pattern}$ {source} [L]" not in apache:
            fail(errors, f".htaccess: missing nested mapping for {public_route}")
        if f"RewriteRule ^{source[:-5]}\\.html$ {public_route} [R=301,L]" not in apache:
            fail(errors, f".htaccess: missing flat-source redirect for {source}")

    print(f"Validated {len(documents)} HTML pages and {len(sitemap_urls)} sitemap URLs.")
    print("Guide word counts:")
    for route, source in ROUTES.items():
        if source.startswith("guide-"):
            count = len(re.findall(r"\w+", " ".join(documents[route].main_text), flags=re.UNICODE))
            print(f"  {source}: {count}")
    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
