#!/usr/bin/env python
from __future__ import annotations

import json
import logging
import shlex
import sys
from dataclasses import dataclass
from subprocess import run
from typing import TypedDict

logger = logging.getLogger(__name__)


class Size(TypedDict):
    height: int
    width: int


class Mode(TypedDict):
    id: str
    name: str
    refreshRate: float
    size: Size


class Pos(TypedDict):
    x: int
    y: int


class Output(TypedDict):
    clones: list[int]
    connected: bool
    currentModeId: str
    enabled: bool
    followPreferredMode: bool
    icon: str
    id: int
    modes: list[Mode]
    name: str
    pos: Pos
    preferredModes: list[str]
    primary: bool
    replicationSource: int
    rotation: int
    scale: int
    size: Size
    sizeMM: Size
    type: int


class Screen(TypedDict):
    currentSize: Size
    id: int
    maxActiveOutputsCount: int
    maxSize: Size
    minSize: Size


class MainOutput(TypedDict):
    features: int
    outputs: list[Output]
    screen: Screen
    tabletModeAvailable: bool
    tabletModeEngaged: bool


@dataclass
class MonitorParam:
    name: str
    width: int
    height: int


class ScreenData:
    # kscreen-doctor -o
    LEFT = 'HDMI-A-5'
    RIGHT = 'DP-3'
    SMALL = 'DP-4'
    # ~/.local/share/kscreen/outputs/ has mapping fullname (may be duplicated) to name

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
        if result.returncode:
            raise IOError


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
