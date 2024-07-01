from __future__ import annotations

import json
import logging
import shlex
from subprocess import run
from typing import TYPE_CHECKING, cast

from screen_swap.screen_doctor_output import MainOutput

if TYPE_CHECKING:
    from collections.abc import Iterator


logger = logging.getLogger(__name__)


class ScreenData:
    # kscreen-doctor -o
    LEFT = "HDMI-A-0"
    RIGHT = "DisplayPort-0"
    SMALL = "DisplayPort-1"

    ALL_CONFIGURATIONS = ("full", "table", "small", "left", "right")

    def __init__(self, json_data: MainOutput | None = None) -> None:
        if json_data is None:
            json_data = self.load_from_current_configuration()
        self.json_data = json_data

    @classmethod
    def load_from_current_configuration(cls) -> MainOutput:
        result = run(
            ["/usr/bin/kscreen-doctor", "-j"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stderr:
            err_msg = result.stderr.strip()
            logging.getLogger(f"{__name__}.kscreen-doctor").error(err_msg)
        result.check_returncode()

        return cast(MainOutput, json.loads(result.stdout))

    def gen_screen_configuration(self, conf_name: str) -> Iterator[str]:
        match conf_name:
            case "full":
                yield f"output.{self.LEFT}.enable"
                yield f"output.{self.LEFT}.primary"
                yield f"output.{self.LEFT}.position.0,0"
                yield f"output.{self.LEFT}.mode.2560x1440@144"
                yield f"output.{self.RIGHT}.enable"
                yield f"output.{self.RIGHT}.position.2560,0"
                yield f"output.{self.RIGHT}.mode.2560x1440@120"
                yield f"output.{self.SMALL}.enable"
                yield f"output.{self.SMALL}.position.5120,0"
                yield f"output.{self.SMALL}.mode.1280x1024@75"

            case "table":
                yield f"output.{self.LEFT}.enable"
                yield f"output.{self.LEFT}.primary"
                yield f"output.{self.LEFT}.position.0,0"
                yield f"output.{self.LEFT}.mode.2560x1440@144"
                yield f"output.{self.RIGHT}.enable"
                yield f"output.{self.RIGHT}.position.2560,0"
                yield f"output.{self.RIGHT}.mode.2560x1440@120"
                yield f"output.{self.SMALL}.disable"

            case "small":
                yield f"output.{self.LEFT}.disable"
                yield f"output.{self.RIGHT}.disable"
                yield f"output.{self.SMALL}.enable"
                yield f"output.{self.SMALL}.primary"
                yield f"output.{self.SMALL}.position.0,0"
                yield f"output.{self.SMALL}.mode.1280x1024@75"

            case "left":
                yield f"output.{self.LEFT}.enable"
                yield f"output.{self.LEFT}.primary"
                yield f"output.{self.LEFT}.position.0,0"
                yield f"output.{self.LEFT}.mode.2560x1440@60"
                yield f"output.{self.RIGHT}.disable"
                yield f"output.{self.SMALL}.disable"

            case "right":
                yield f"output.{self.LEFT}.disable"
                yield f"output.{self.RIGHT}.enable"
                yield f"output.{self.RIGHT}.primary"
                yield f"output.{self.RIGHT}.position.0,0"
                yield f"output.{self.RIGHT}.mode.2560x1440@60"
                yield f"output.{self.SMALL}.disable"

            case _:
                msg = "Unknown configuration"
                raise ValueError(msg)

    def set_configuration(self, conf_name: str) -> None:
        conf = self.gen_screen_configuration(conf_name)
        args = ["kscreen-doctor", *conf]
        logger.info("Running: %s", shlex.join(args))
        result = run(args, check=True)
        result.check_returncode()
