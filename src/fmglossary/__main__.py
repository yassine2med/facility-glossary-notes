"""Command line: python -m fmglossary list|define|example|calc|export"""

from __future__ import annotations

import argparse
import sys

from .glossary import TERMS, find, fmt, to_markdown


def main(argv: list[str] | None = None) -> int:
    """Return 0 on success, 2 for an unknown term, missing value or invalid input."""
    parser = argparse.ArgumentParser(prog="fmglossary", description="Facility glossary with runnable KPIs")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list all terms")
    for name, text in (("define", "definition and formula of a term"), ("example", "run the worked example of a term"),
                       ("calc", "calculate a term with your own numbers (name=value ...)")):
        p = sub.add_parser(name, help=text)
        p.add_argument("term")
        if name == "calc":
            p.add_argument("values", nargs="+", help="for example operating_hours=8000 failures=4")
    ex = sub.add_parser("export", help="write the glossary as Markdown")
    ex.add_argument("-o", "--output", help="file to write (default: print)")
    args = parser.parse_args(argv)

    if args.command == "list":
        for t in TERMS:
            print(f"{t.key:<15} {t.name}")
        return 0
    if args.command == "export":
        text = to_markdown()
        if args.output:
            with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text + "\n")
            print(f"Glossary written to {args.output}")
        else:
            print(text)
        return 0
    term = find(args.term)
    if term is None:
        print(f"Unknown term: {args.term}. Run 'list' to see the names.", file=sys.stderr)
        return 2
    if args.command == "define":
        print(f"{term.name}\n{term.definition}\nFormula: {term.formula} ({term.unit})")
        print("Inputs: " + ", ".join(term.args()))
        return 0
    if args.command == "example":
        print(f"{term.name}: {term.note}")
        print("Inputs: " + ", ".join(f"{k}={v}" for k, v in term.example.items()))
        print(f"Result: {fmt(term.run_example())} {term.unit}")
        return 0
    values = {}
    for item in args.values:
        key, sep, raw = item.partition("=")
        try:
            if not sep or key not in term.args():
                raise KeyError(key)
            values[key] = float(raw)
        except KeyError:
            print(f"Unexpected input '{item}'. {term.name} needs: {', '.join(term.args())}", file=sys.stderr)
            return 2
        except ValueError:
            print(f"'{raw}' is not a number", file=sys.stderr)
            return 2
    if set(values) != set(term.args()):
        print(f"{term.name} needs: {', '.join(term.args())}", file=sys.stderr)
        return 2
    try:
        print(f"{fmt(term.func(**values))} {term.unit}")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
