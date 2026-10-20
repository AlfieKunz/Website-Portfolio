# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>｣

import os
import sys
import shutil
import platform

def load_simpleaudio():
    os_type = platform.system()

    if os_type == "Linux":

        python_version = sys.version_info[:2]

        if python_version == (3, 9):
            libasound = "simpleaudio_patched-1.0.5-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64"
        elif python_version == (3, 10):
            libasound = "simpleaudio_patched-1.0.5-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64"
        elif python_version == (3, 11):
            libasound = "simpleaudio_patched-1.0.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64"
        elif python_version == (3, 12):
            libasound = "simpleaudio_patched-1.0.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64"
        elif python_version == (3, 13):
            libasound = "simpleaudio_patched-1.0.5-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64"
        else:
            return

        addon_path = os.path.dirname(os.path.dirname(__file__))
        current_path = os.path.dirname(__file__)
        libasound_folder = os.path.join(current_path, libasound)

        for item in os.listdir(libasound_folder):
            if "simpleaudio_patched.libs" in item:
                source_path = os.path.join(libasound_folder, item)
                destination_path = os.path.join(addon_path, item)
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
