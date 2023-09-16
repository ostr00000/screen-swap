#!/usr/bin/env python
from __future__ import annotations

import logging
import sys

from screen_swap.screen_data import ScreenData

logger = logging.getLogger(__name__)


def main():
    try:
        conf_name = sys.argv[1]
    except IndexError:
        logger.critical("Missing configuration name %s", ScreenData.ALL_CONFIGURATIONS)
    else:
        ScreenData().set_configuration(conf_name)
        logger.info("Finished successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
