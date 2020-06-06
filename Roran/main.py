import argparse
import logging
import sys

from core.bot import Bot  # type: ignore

logger = logging.getLogger("roran")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="verbosity level"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="use specified configuration file",
    )
    args = parser.parse_args()

    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stdout_handler)

    if args.verbose == 0:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 1:
        logger.setLevel(logging.DEBUG)

    bot = Bot(config=args.config, logger=logger)
    bot.start()
