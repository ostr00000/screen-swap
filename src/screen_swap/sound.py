from subprocess import check_call, check_output

from screen_swap.screen_data import ScreenData

OUTPUT_LINEOUT = "analog-output-lineout"
OUTPUT_HEADPHONES = "analog-output-headphones"


def change_sound_output(conf_name: str) -> None:
    if conf_name not in ScreenData.ALL_CONFIGURATIONS:
        raise ValueError

    match conf_name:
        case "full" | "table" | "left" | "right":
            out = "analog-output-headphones"
        case "small":
            out = "analog-output-lineout"
        case _:
            raise KeyError(conf_name)

    sink_cmd = ["pactl", "get-default-sink"]
    sink = check_output(sink_cmd, text=True).strip()
    change_cmd = ["pactl", "set-sink-port", sink, out]
    check_call(change_cmd)
