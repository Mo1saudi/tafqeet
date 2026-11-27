import argparse
import sys

from . import egp_to_words, number_to_words, to_western


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="tafqeet",
        description="Write a number or an Egyptian pound amount in Arabic words.",
    )
    p.add_argument("number", help="the number; Arabic-Indic digits are accepted")
    p.add_argument("--egp", action="store_true", help="treat it as an amount in Egyptian pounds")
    p.add_argument("--check", action="store_true", help="cheque style: wrap with 'فقط' and 'لا غير' (with --egp)")
    args = p.parse_args(argv)
    raw = to_western(args.number).replace("٫", ".").replace("٬", "").replace(",", "")
    try:
        if args.egp:
            print(egp_to_words(raw, check_style=args.check))
        else:
            print(number_to_words(int(raw)))
    except (ValueError, TypeError) as exc:
        print("error:", exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
