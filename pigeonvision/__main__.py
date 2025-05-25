import argparse

import pigeonvision

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pigeonvision on a query."
    )
    parser.add_argument("query",
                        help="The query to analyze (e.g., domain, URL, etc.)")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Enable verbose logging (default: False)"
    )
    parser.add_argument(
        "--level", "-l",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)"
    )
    args = parser.parse_args()

    short, explanation, _ = pigeonvision.main(args.query, args.verbose,
                                              args.level.upper())
    print(short)
    print(explanation)
