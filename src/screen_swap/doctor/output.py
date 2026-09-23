import logging
from dataclasses import dataclass
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
