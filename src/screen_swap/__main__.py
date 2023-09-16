#!/usr/bin/env python
from __future__ import annotations

import logging
import sys

from screen_swap import ScreenData

logger = logging.getLogger(__name__)


def main():
    try:
        confName = sys.argv[1]
    except IndexError:
        logger.critical(f"Missing configuration name {ScreenData.ALL_CONFIGURATIONS}")
    else:
        ScreenData().setConfiguration(confName)
        logger.info('Finished successfully')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
