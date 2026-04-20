import colorlog as clg
import logging as lg
import sys


def setup_logger(verbose: bool) -> None:    
    logger = lg.getLogger('egiti')
    logger.handlers.clear()
    logger.setLevel(lg.DEBUG if verbose else lg.INFO)

    stream_handler = lg.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(clg.ColoredFormatter(
        fmt="{log_color}[{name}@{levelname}]: {message}{reset}",
        style='{',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red'
        }
    ))

    logger.addHandler(stream_handler)