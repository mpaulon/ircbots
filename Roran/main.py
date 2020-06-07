import argparse
import logging

import colorlog

from core.bot import Bot  # type: ignore


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

    # logging 
    logger = logging.getLogger("roran")

    format_string = "%(asctime)s - %(levelname)s - %(message)s"
    stdout_handler = logging.StreamHandler()
    stdout_formatter = colorlog.ColoredFormatter(f"%(log_color)s {format_string}")
    stdout_handler.setFormatter(stdout_formatter)
    file_handler = logging.FileHandler("main.log")
    file_formatter = logging.Formatter(format_string)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    if args.verbose == 0:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 1:
        logger.setLevel(logging.DEBUG)

    bot = Bot(config=args.config, logger=logger)
    bot.start()
