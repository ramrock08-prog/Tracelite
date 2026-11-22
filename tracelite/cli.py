"""Command-line entry point for TraceLite:  `tracelite <command>`."""

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tracelite",
        description="A tiny, local, zero-dependency LLM observability tracker.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("report", help="print the cost / latency / error report")
    sub.add_parser("dashboard", help="serve the local web dashboard")
    diff_parser = sub.add_parser("diff", help="LLM regression check vs the saved baseline")
    diff_parser.add_argument(
        "--save", action="store_true", help="save current answers as the baseline"
    )

    args = parser.parse_args(argv)

    if args.command == "report":
        from .tracker import report

        report()
    elif args.command == "dashboard":
        from .dashboard import main as run_dashboard

        run_dashboard()
    elif args.command == "diff":
        from . import diff

        diff.run(save=args.save)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
