from __future__ import annotations

import json
import logging
import shlex
from subprocess import CompletedProcess, run
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from screen_swap.doctor.output import MainOutput

logger = logging.getLogger(__name__)


def run_doctor(command: list[str], *args, **kwargs) -> CompletedProcess[str]:
    logger.info("Running: %s", shlex.join(command))

    result = run(command, *args, capture_output=True, text=True, check=True, **kwargs)
    if e := result.stderr.strip():
        logger.error(e)
        if "not found" in e.lower():
            msg = f"kscreen-doctor failed with stderr msg: {e}"
            raise RuntimeError(msg)
    return result


def load_from_current_configuration() -> MainOutput:
    result = run_doctor(["/usr/bin/kscreen-doctor", "-j"])
    return cast("MainOutput", json.loads(result.stdout))
