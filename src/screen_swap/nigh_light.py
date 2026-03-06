from subprocess import check_call
from time import sleep


def night_light_trigger_reload():
    sleep(2)

    base = [
        'qdbus',
        'org.kde.KWin.NightLight',
        '/org/kde/KWin/NightLight',
    ]
    cmd = [*base, 'org.kde.KWin.NightLight.preview', '3000']
    check_call(cmd)

    sleep(1)

    cmd = [*base, 'org.kde.KWin.NightLight.stopPreview']
    check_call(cmd)
