import logging as lg
import sys

import colorlog as clg


def setup_logger(verbose: bool) -> None:
    logger = lg.getLogger('egiti')
    logger.handlers.clear()
    logger.setLevel(lg.DEBUG if verbose else lg.INFO)

    stream_handler = lg.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(clg.ColoredFormatter(
        fmt="{log_color}"
            + ("[{asctime} {levelname}] " if verbose else "")
            + "{name}: {message}{reset}",

        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red'
        },
        style='{',
        datefmt="%H:%M:%S"

    ))

    logger.addHandler(stream_handler)
