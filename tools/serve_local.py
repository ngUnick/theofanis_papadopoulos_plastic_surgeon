"""Serve the static site locally with extensionless page URLs."""

from __future__ import annotations

import argparse
import errno
import socket
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


PROJECT_ROOT = Path(__file__).resolve().parent.parent

NESTED_GUIDE_ROUTES = {
    "/non-invasive/botouliniki-toxini": "/guide-botouliniki-toxini.html",
    "/non-invasive/yalouroniko-fillers": "/guide-yalouroniko-fillers.html",
    "/non-invasive/laser-apotrichosi": "/guide-laser-apotrichosi.html",
    "/procedures/lipoanarrofisi": "/guide-lipoanarrofisi.html",
    "/reconstructive/oules-egkavmaton": "/guide-oules-egkavmaton.html",
}


class ExtensionlessRequestHandler(SimpleHTTPRequestHandler):
    """Map an extensionless request to a matching HTML file if one exists."""

    def send_head(self):
        request_url = urlsplit(self.path)
        request_path = request_url.path

        if request_path in NESTED_GUIDE_ROUTES:
            self.path = urlunsplit(
                request_url._replace(path=NESTED_GUIDE_ROUTES[request_path])
            )
            return super().send_head()

        if request_path != "/" and not request_path.endswith("/"):
            requested_file = Path(self.translate_path(request_path))
            html_file = requested_file.with_name(f"{requested_file.name}.html")

            if not requested_file.exists() and html_file.is_file():
                self.path = urlunsplit(
                    request_url._replace(path=f"{request_path}.html")
                )

        return super().send_head()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview the site with extensionless local page URLs."
    )
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=8000,
        help="local port to use (default: 8000)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    handler = lambda *handler_args, **handler_kwargs: ExtensionlessRequestHandler(
        *handler_args, directory=str(PROJECT_ROOT), **handler_kwargs
    )

    try:
        with socket.create_connection(("localhost", args.port), timeout=0.25):
            print(
                f"Η θύρα {args.port} χρησιμοποιείται ήδη. "
                "Κλείστε τον άλλο τοπικό server και εκτελέστε ξανά το preview-site.cmd.",
                file=sys.stderr,
            )
            raise SystemExit(1)
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        pass

    try:
        with ThreadingHTTPServer(("localhost", args.port), handler) as server:
            print(f"Serving {PROJECT_ROOT} at http://localhost:{args.port}/")
            print("Press Ctrl+C to stop.")
            server.serve_forever()
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE or getattr(exc, "winerror", None) == 10048:
            print(
                f"Η θύρα {args.port} χρησιμοποιείται ήδη. "
                "Κλείστε τον άλλο τοπικό server και εκτελέστε ξανά το preview-site.cmd.",
                file=sys.stderr,
            )
            raise SystemExit(1) from None
        raise


if __name__ == "__main__":
    main()
