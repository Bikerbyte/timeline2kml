import argparse

from converter import convert_timeline_to_kml


def build_parser():
    parser = argparse.ArgumentParser(
        description="Convert Google Maps Timeline JSON exports to KML."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file.")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path where the output KML file should be saved.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        convert_timeline_to_kml(args.input, args.output)
    except Exception as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    print(f"KML file saved to: {args.output}")


if __name__ == "__main__":
    main()
