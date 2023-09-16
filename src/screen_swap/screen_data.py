from __future__ import annotations

import json
import logging
import shlex
from subprocess import run

from screen_swap import MainOutput

logger = logging.getLogger(__name__)


class ScreenData:
    # kscreen-doctor -o
    LEFT = 'HDMI-A-5'
    RIGHT = 'DP-3'
    SMALL = 'DP-4'

    ALL_CONFIGURATIONS = ['full', 'table', 'small']

    def __init__(self, jsonData: MainOutput = None):
        if jsonData is None:
            jsonData = self.loadFromCurrentConfiguration()
        self.jsonData = jsonData

    @classmethod
    def loadFromCurrentConfiguration(cls):
        result = run(['kscreen-doctor', '-j'], capture_output=True, text=True)
        if result.stderr:
            errMsg = result.stderr.strip()
            logging.getLogger(f'{__name__}.kscreen-doctor').error(errMsg)
        result.check_returncode()

        return json.loads(result.stdout)

    def genScreenConfiguration(self, confName: str):
        match confName:
            case 'full':
                yield f'output.{self.LEFT}.enable'
                yield f'output.{self.LEFT}.primary'
                yield f'output.{self.LEFT}.position.0,0'
                yield f'output.{self.LEFT}.mode.2560x1440@144'

                yield f'output.{self.RIGHT}.enable'
                yield f'output.{self.RIGHT}.position.2560,0'
                yield f'output.{self.RIGHT}.mode.2560x1440@120'

                yield f'output.{self.SMALL}.enable'
                yield f'output.{self.SMALL}.position.5120,0'
                yield f'output.{self.SMALL}.mode.1280x1024@75'

            case 'table':
                yield f'output.{self.LEFT}.enable'
                yield f'output.{self.LEFT}.primary'
                yield f'output.{self.LEFT}.position.0,0'
                yield f'output.{self.LEFT}.mode.2560x1440@144'

                yield f'output.{self.RIGHT}.enable'
                yield f'output.{self.RIGHT}.position.2560,0'
                yield f'output.{self.RIGHT}.mode.2560x1440@120'

                yield f'output.{self.SMALL}.disable'

            case 'small':
                yield f'output.{self.LEFT}.disable'

                yield f'output.{self.RIGHT}.disable'

                yield f'output.{self.SMALL}.enable'
                yield f'output.{self.SMALL}.primary'
                yield f'output.{self.SMALL}.position.0,0'
                yield f'output.{self.SMALL}.mode.1280x1024@75'

            case _:
                raise ValueError("Unknown configuration")

    def setConfiguration(self, confName: str):
        conf = self.genScreenConfiguration(confName)
        args = ['kscreen-doctor', *conf]
        logger.info(f"Running: {shlex.join(args)}")
        result = run(args)
        result.check_returncode()
