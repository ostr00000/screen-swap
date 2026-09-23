from __future__ import annotations

import logging
from time import sleep
from typing import TYPE_CHECKING

from screen_swap.doctor.call import load_from_current_configuration, run_doctor

if TYPE_CHECKING:
    from collections.abc import Iterator

    from screen_swap.doctor.output import MainOutput

logger = logging.getLogger(__name__)


class ScreenData:
    # kscreen-doctor -o
    LEFT = "HDMI-A-5"
    RIGHT = "DP-4"
    SMALL = "DP-5"

    ALL_CONFIGURATIONS = ("full", "table", "small", "left", "right")

    def __init__(self, json_data: MainOutput | None = None) -> None:
        if json_data is None:
            json_data = load_from_current_configuration()
        self.json_data = json_data

    def gen_screen_configuration(self, conf_name: str) -> Iterator[str]:
        match conf_name:
            case "full":
                yield f"output.{self.LEFT}.enable"
                yield f"output.{self.LEFT}.primary"
                yield f"output.{self.LEFT}.priority.1"
                yield f"output.{self.LEFT}.position.0,0"
                yield f"output.{self.LEFT}.mode.2560x1440@144"
                ##
                yield f"output.{self.RIGHT}.enable"
                yield f"output.{self.RIGHT}.priority.2"
                yield f"output.{self.RIGHT}.position.2560,0"
                yield f"output.{self.RIGHT}.mode.2560x1440@120"
                ##
                yield f"output.{self.SMALL}.enable"
                yield f"output.{self.SMALL}.priority.3"
                yield f"output.{self.SMALL}.position.5120,0"
                yield f"output.{self.SMALL}.mode.1440x900@60"

            case "table":
                yield f"output.{self.LEFT}.enable"
                yield f"output.{self.LEFT}.primary"
                yield f"output.{self.LEFT}.position.0,0"
                yield f"output.{self.LEFT}.mode.2560x1440@144"
                ##
                yield f"output.{self.RIGHT}.enable"
                yield f"output.{self.RIGHT}.position.2560,0"
                yield f"output.{self.RIGHT}.mode.2560x1440@120"
                ##
                yield f"output.{self.SMALL}.disable"

            case "small":
                yield f"output.{self.LEFT}.disable"
                ##
                yield f"output.{self.RIGHT}.disable"
                ##
                yield f"output.{self.SMALL}.enable"
                yield f"output.{self.SMALL}.primary"
                yield f"output.{self.SMALL}.position.0,0"
                yield f"output.{self.SMALL}.mode.1440x900@60"

            case "left":
                yield f"output.{self.LEFT}.enable"
                yield f"output.{self.LEFT}.primary"
                yield f"output.{self.LEFT}.position.0,0"
                yield f"output.{self.LEFT}.mode.2560x1440@60"
                ##
                yield f"output.{self.RIGHT}.disable"
                ##
                yield f"output.{self.SMALL}.disable"

            case "right":
                yield f"output.{self.LEFT}.disable"
                ##
                yield f"output.{self.RIGHT}.enable"
                yield f"output.{self.RIGHT}.primary"
                yield f"output.{self.RIGHT}.position.0,0"
                yield f"output.{self.RIGHT}.mode.2560x1440@60"
                ##
                yield f"output.{self.SMALL}.disable"

            case _:
                msg = "Unknown configuration"
                raise ValueError(msg)

    def set_configuration(self, conf_name: str) -> None:
        conf = list(self.gen_screen_configuration(conf_name))
        primary = next(
            (conf.pop(i) for i, c in enumerate(conf) if ".primary" in c),
            None,
        )

        run_doctor(["kscreen-doctor", *conf])

        if primary:
            sleep(1)
            run_doctor(["kscreen-doctor", primary])
