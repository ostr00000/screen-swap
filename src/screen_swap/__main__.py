#!/usr/bin/env python
from __future__ import annotations

import argparse
import logging

from screen_swap.nigh_light import night_light_trigger_reload
from screen_swap.screen_data import ScreenData
from screen_swap.sound import change_sound_output

logger = logging.getLogger(__name__)


def parse_bool(value: str) -> bool:
    return value.lower() in ("1", "true", "yes", "on")


class ScreenNamespace(argparse.Namespace):
    conf_name: str
    change_sound: bool
    night_light: bool


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Screen swap configuration tool")
    parser.add_argument("conf_name", help="Configuration name")
    parser.add_argument(
        "--change-sound",
        type=parse_bool,
        default=True,
        help="Change sound output (default: True)",
    )
    parser.add_argument(
        "--night-light",
        type=parse_bool,
        default=True,
        help="Trigger night light reload (default: True)",
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    args = create_parser().parse_args(namespace=ScreenNamespace())

    ScreenData().set_configuration(args.conf_name)
    if args.change_sound:
        change_sound_output(args.conf_name)
    if args.night_light:
        night_light_trigger_reload()
    logger.info("Finished successfully")


if __name__ == "__main__":
    main()
