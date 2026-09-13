from __future__ import annotations

import argparse
import sys

from kept import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="kept",
        description="Bee remembers what you said. Kept makes sure you do it.",
    )
    parser.add_argument("--version", action="store_true", help="print version and exit")
    sub = parser.add_subparsers(dest="command")

    web = sub.add_parser("web", help="run the dashboard")
    web.add_argument("--host", default=None)
    web.add_argument("--port", type=int, default=None)

    sub.add_parser("daemon", help="run the Bee stream daemon (Phase 1)")
    sub.add_parser("version", help="print version")

    args = parser.parse_args(argv)
    if args.version or args.command == "version":
        print(__version__)
        return 0
    if args.command == "web":
        from kept.config import load_settings
        from kept.web.app import run

        settings = load_settings()
        host = args.host or settings.kept_web_host
        port = args.port or settings.kept_web_port
        run(host=host, port=port)
        return 0
    if args.command == "daemon":
        print(
            "kept daemon lands in Phase 1. Capture fixtures first — see docs/FIXTURES.md",
            file=sys.stderr,
        )
        return 2
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
