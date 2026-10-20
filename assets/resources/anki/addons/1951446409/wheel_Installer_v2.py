# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>｣

import os
import sys
import shutil
import zipfile
import platform

def load_simpleaudio_mac_or_win():
    os_type = platform.system()
    python_version = sys.version_info[:2]
    arch = platform.machine()

    platform_folder = ""
    sub_folder = ""

    if os_type == "Darwin":

        platform_folder = "simpleaudio_for_mac"

        if arch == "x86_64":
            sub_folder = "MacOS_86_64"

            if python_version == (3, 9):
                wheel_name = "simpleaudio_patched-1.0.5-cp39-cp39-macosx_10_9_x86_64.whl"
            elif python_version == (3, 10):
                wheel_name = "simpleaudio_patched-1.0.5-cp310-cp310-macosx_10_9_x86_64.whl"
            elif python_version == (3, 11):
                wheel_name = "simpleaudio_patched-1.0.5-cp311-cp311-macosx_10_9_x86_64.whl"
            elif python_version == (3, 12):
                wheel_name = "simpleaudio_patched-1.0.5-cp312-cp312-macosx_10_9_x86_64.whl"
            elif python_version == (3, 13):
                wheel_name = "simpleaudio_patched-1.0.5-cp313-cp313-macosx_10_13_x86_64.whl"
            else:
                return

        elif arch == "arm64":
            sub_folder = "MacOS_arm64"

            if python_version == (3, 9):
                wheel_name = "simpleaudio_patched-1.0.5-cp39-cp39-macosx_11_0_arm64.whl"
            elif python_version == (3, 10):
                wheel_name = "simpleaudio_patched-1.0.5-cp310-cp310-macosx_11_0_arm64.whl"
            elif python_version == (3, 11):
                wheel_name = "simpleaudio_patched-1.0.5-cp311-cp311-macosx_11_0_arm64.whl"
            elif python_version == (3, 12):
                wheel_name = "simpleaudio_patched-1.0.5-cp312-cp312-macosx_11_0_arm64.whl"
            elif python_version == (3, 13):
                wheel_name = "simpleaudio_patched-1.0.5-cp313-cp313-macosx_11_0_arm64.whl"
            else:
                return


    elif os_type == "Windows":

        platform_folder = "simpleaudio_for_win"

        if python_version == (3, 9):
            wheel_name = "simpleaudio_patched-1.0.5-cp39-cp39-win_amd64.whl"
        elif python_version == (3, 10):
            wheel_name = "simpleaudio_patched-1.0.5-cp310-cp310-win_amd64.whl"
        elif python_version == (3, 11):
            wheel_name = "simpleaudio_patched-1.0.5-cp311-cp311-win_amd64.whl"
        elif python_version == (3, 12):
            wheel_name = "simpleaudio_patched-1.0.5-cp312-cp312-win_amd64.whl"
        elif python_version == (3, 13):
            wheel_name = "simpleaudio_patched-1.0.5-cp313-cp313-win_amd64.whl"
        else:
            return

    addon_path = os.path.dirname(__file__)
    if sub_folder:
        simpleaudio_wheel_path = os.path.join(addon_path, platform_folder, sub_folder, wheel_name)
    else:
        simpleaudio_wheel_path = os.path.join(addon_path, platform_folder, wheel_name)

    ## load wheel ###
    if os.path.exists(simpleaudio_wheel_path):
        unzip_wheel = os.path.join(addon_path, "unzip_wheel")

        if os.path.exists(unzip_wheel):
            shutil.rmtree(unzip_wheel)

        os.makedirs(unzip_wheel, exist_ok=True)
        with zipfile.ZipFile(simpleaudio_wheel_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_wheel)
        sys.path.insert(0, unzip_wheel)

        try:
            import simpleaudio
            print("simpleaudio import Success")
            return True
        except ImportError as e:
            print(f"simpleaudio import Failure: {e}")
            return False