# Copyright (C) lovac42 2021 <https://github.com/lovac42> SpellingPolice <https://github.com/lovac42/SpellingPolice>
# Copyright (C) Valentin 2023 <https://github.com/ValentinSchmitz> Spell Checker <https://github.com/ValentinSchmitz/spell-checker>
# Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import pickle
import zipfile
import requests
import shutil
import subprocess
import traceback
import webbrowser
from datetime import date
from functools import partial, wraps

import aqt
from aqt import mw
from aqt.operations import QueryOp
from aqt.utils import tooltip

from .const import *
from .path_manager import ADDON_NAME
from .shige_config.support_old_anki import get_ankiwebview_page


PENDING_BDIC_PATH = os.path.join(USER_PATH, "wasm_converter", "pending")


#MARK: refresh_languages
def refresh_languages(*args):
    retry_pending_bdic_copies()

    config = mw.addonManager.getConfig(__name__)
    if config.get("is_editor_only", True):
        return

    web_page = get_ankiwebview_page(mw.web)
    profile = web_page.profile()

    profile.setSpellCheckEnabled(False)
    profile.setSpellCheckLanguages({})
    profile.setSpellCheckLanguages(get_dictionaries())
    profile.setSpellCheckEnabled(get_user_data("status", default=True))


#MARK: get_dictionaries
def get_dictionaries():
    dicts = []
    for file in os.listdir(DICT_DIR):
        if file.endswith(".bdic"):
            dicts.append(file.removesuffix(".bdic"))
    return dicts


#MARK: background_op
def background_op(func=None, /, *, success=None, with_progress= None, label=None):
    if not func:
        return partial(background_op, success=success, with_progress=with_progress, label=label)

    @wraps(func)
    def wrapper(*args, **kwargs):
        def noop(*args, **kwargs):
            pass

        if success:
            op = QueryOp(
                        parent=mw,
                        op=partial(func, *args, **kwargs),
                        success=success)
        else:
            op = QueryOp(
                        parent=mw,
                        op=partial(func, *args, **kwargs),
                        success=noop)

        if with_progress:
            return op.with_progress(label=label).run_in_background()
        else:
            return op.run_in_background()

    return wrapper


@background_op(
    success=refresh_languages, with_progress=True, label="Compiling user dictionaries...")
def compile_user_dicts(*args, **kwargs):
    for dic in os.listdir(USER_DICT_PATH):
        if dic.endswith((".dic", ".txt")):
            compile_user_dict(dic.split(".")[0])


@background_op(success=refresh_languages)
def compile_personal(*args):
    compile_user_dict("personal")


#MARK: compile_user_dict
def compile_user_dict(name, *args):

    # path
    base_path = os.path.join(USER_DICT_PATH, name)

    base_path_text = base_path + ".txt"
    base_path_dic = base_path + ".dic"
    base_path_aff = base_path + ".aff" 

    # dic: word, rule id
    # aff: affix, rules for prefixes, suffixes

    # make dict from text
    tmp_files = []
    if os.path.isfile(base_path_text):
        # read text
        with open(base_path_text, "rb") as text_file:
            line_count = 0
            for line in text_file:
                line_count += 1

        # make dict
        with open(base_path_text, "r") as input_file, open(base_path_dic, "w") as output_file:
            line_count_text = str(line_count)
            # what WeirdBugFix?
            # https://github.com/valentin02s/spell-checker/commit/3a79076d3f3071a3384eeafc03c72f4058d7ec35
            dict_header = line_count_text + "\nWeirdBugFix\n"
            output_file.write(dict_header)

            for line in input_file:
                output_file.write(line)
            tmp_files.append(output_file.name)

    # check dict
    if not os.path.isfile(base_path_dic):
        return

    # check aff
    if not os.path.isfile(base_path_aff):
        set_unique_items = set()
        with open(base_path_dic, "r") as dict_file:
            for line in dict_file:
                for item in line:
                    set_unique_items.add(item)

        # make aff
        dict_content = f"SET UTF-8\nTRY {''.join(set_unique_items)}\n"
        with open(base_path_aff, "w") as affix_file:
            affix_file.write(dict_content)
            tmp_files.append(affix_file.name)

    # compile
    compile_BDIC(USER_DICT_PATH, name, remove=False)

    # del temp
    for temp_file in tmp_files:
        os.remove(temp_file)




#MARK: get_conversion_mode
def get_conversion_mode():
    config = mw.addonManager.getConfig(__name__)
    mode = config.get("bdic_conversion_mode", "wasm")
    if mode not in ("wasm", "legacy"):
        mode = "wasm"
    return mode


#MARK: set_conversion_mode
def set_conversion_mode(mode):
    config = mw.addonManager.getConfig(__name__)
    config["bdic_conversion_mode"] = mode
    mw.addonManager.writeConfig(__name__, config)


#MARK: conversion_binaries_installed
def conversion_binaries_installed():
    done_file = os.path.join(BINS_PATH, "verified")
    if not os.path.isfile(done_file):
        return False
    if not os.path.isfile(BIN_PATH):
        return False
    return True


#MARK: ensure_conversion_binaries
def ensure_conversion_binaries():
    if conversion_binaries_installed():
        print(" > True: verified file exist.")
        return True

    print(" > False: the conversion binaries are not installed.")
    done_file = os.path.join(BINS_PATH, "verified")
    try:
        zip_loc = [BINS_PATH, "bins.zip"]
        download_to_file(URL_BINARIES, *zip_loc)
        with zipfile.ZipFile(os.path.join(*zip_loc), 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                if zip_info.is_dir():
                    continue
                zip_info.filename = os.path.basename(zip_info.filename)
                zip_ref.extract(zip_info, BINS_PATH)
        os.remove(os.path.join(*zip_loc))
        save_write(done_file, str(date.today()), mode="w")
        return True
    except Exception as e:
        print(f"[{ADDON_NAME}] Error: {e}")
        return False


#MARK: downloadConversionBinaries
@background_op(
    with_progress=False, label="Spell checker:\nDownloading binaries for .bdic conversion...")
def download_conversion_binaries(*args):
    if ensure_conversion_binaries():
        aqt.mw.taskman.run_on_main(lambda: tooltip(
            "✅️SpellChecker: convert_dict binaries are ready."))
    else:
        aqt.mw.taskman.run_on_main(lambda: tooltip(
            "Error: the convert_dict binaries could not be downloaded :-/"))


#MARK: compile_BDIC
def compile_BDIC(path, name, remove=False):
    if get_conversion_mode() == "legacy":
        result = run_convert_dict_binary(path, name)
    else:
        result = run_convert_dict_wasm(path, name)

    if remove:
        for extension in (".dic", ".aff"):
            source_path = os.path.join(path, name + extension)
            if os.path.isfile(source_path):
                os.remove(source_path)
    print(f"Compiled {name}")

    if not result["success"]:
        message = result.get("message", "")
        aqt.mw.taskman.run_on_main(
            lambda: tooltip(f"Dictionary {name} seems to be broken? Process output:\n{message}"))
        return
    copy_compiled_bdic(path, name)


#MARK: copy_compiled_bdic
def copy_compiled_bdic(path, name):
    try:
        with open(os.path.join(path, name + ".bdic"), 'rb') as read_file, open(os.path.join(DICT_DIR, name + ".bdic"), 'wb') as write_file:
            write_file.write(read_file.read())
        print(f"Copied {name} to {DICT_DIR} successfully")
        discard_pending_bdic(name)
        aqt.mw.taskman.run_on_main(
            lambda: tooltip(f"✅️SpellChecker: {name} dict success! :-)"))
    except OSError as e:
        # The bdic is in use by QtWebEngine: keep the compiled file and retry
        # on the next dictionary load (setupBDIC / refresh_languages).
        print(f"[{ADDON_NAME}] could not copy {name}.bdic: {e}")
        save_pending_bdic(path, name)
        if name == "personal":
            config = mw.addonManager.getConfig(__name__)
            config["compile_is_needed"] = True
            mw.addonManager.writeConfig(__name__, config)
            aqt.mw.taskman.run_on_main(
                lambda: tooltip("❌️Error: Please close the Editor (or restart Anki)."))
        else:
            aqt.mw.taskman.run_on_main(
                lambda: tooltip(f"Error: {name} failed :-/"))


#MARK: save_pending_bdic
def save_pending_bdic(path, name):
    try:
        os.makedirs(PENDING_BDIC_PATH, exist_ok=True)
        source_path = os.path.join(path, name + ".bdic")
        pending_path = os.path.join(PENDING_BDIC_PATH, name + ".bdic")
        shutil.copyfile(source_path, pending_path)
        print(f"[{ADDON_NAME}] saved the pending dictionary: {pending_path}")
    except OSError as e:
        print(f"[{ADDON_NAME}] could not save the pending dictionary: {e}")


#MARK: discard_pending_bdic
def discard_pending_bdic(name):
    pending_path = os.path.join(PENDING_BDIC_PATH, name + ".bdic")
    if not os.path.isfile(pending_path):
        return
    try:
        os.remove(pending_path)
        print(f"[{ADDON_NAME}] discarded the pending dictionary: {pending_path}")
    except OSError as e:
        print(f"[{ADDON_NAME}] could not discard the pending dictionary: {e}")


#MARK: retry_pending_bdic_copies
def retry_pending_bdic_copies():
    if not os.path.isdir(PENDING_BDIC_PATH):
        return
    for file_name in os.listdir(PENDING_BDIC_PATH):
        if not file_name.endswith(".bdic"):
            continue
        pending_path = os.path.join(PENDING_BDIC_PATH, file_name)
        target_path = os.path.join(DICT_DIR, file_name)
        try:
            with open(pending_path, 'rb') as read_file, open(target_path, 'wb') as write_file:
                write_file.write(read_file.read())
            os.remove(pending_path)
            print(f"[{ADDON_NAME}] applied the pending dictionary: {file_name}")
        except OSError as e:
            print(f"[{ADDON_NAME}] could not apply the pending dictionary {file_name}: {e}")


#MARK: run_convert_dict_wasm
def run_convert_dict_wasm(path, name):
    aff_path = os.path.join(path, name + ".aff")
    dic_path = os.path.join(path, name + ".dic")
    output_path = os.path.join(path, name + ".bdic")
    try:
        from .wasm_converter import convert_dic_aff_to_bdic
        convert_dic_aff_to_bdic(aff_path, dic_path, output_path)
        return {"success": True, "message": ""}
    except Exception as error:
        print(f"[{ADDON_NAME}] Error: {error}")
        traceback.print_exc()
        return {"success": False, "message": str(error)}


#MARK: run_convert_dict_binary
def run_convert_dict_binary(path, name):
    if not ensure_conversion_binaries():
        return {"success": False, "message": "the convert_dict binaries are not available"}
    command = [BIN_PATH, os.path.join(path, name)]
    if os.name != 'nt':
        file_mode = os.stat(BIN_PATH).st_mode
        file_mode |= (file_mode & 0o444) >> 2  # copy R bits to X
        os.chmod(BIN_PATH, file_mode)
    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True)
    except OSError as error:
        return {"success": False, "message": str(error)}
    if res.returncode != 0:
        return {"success": False, "message": res.stdout}
    return {"success": True, "message": res.stdout}



#MARK: download
def on_download(url):
    try:
        res = requests.get(url)
    except ConnectionError as error:
        tooltip(
            "Internet connection failed. Files could not be downloaded. Please ensure you have an "
            f"internet connection and reopen Anki. Error: {error}")
        return None
    if res.status_code != 200:
        tooltip(f"Access to {url} failed. Status code: {res.status_code}. Please try again later.")
    return res

#MARK: open_path
def open_path(path):
    webbrowser.open(f'file://{path}')


#MARK: download_to_file
def download_to_file(url, loc, name):
    res = on_download(url)
    if res is None:
        return None
    save_mk_dir(loc)
    save_path = os.path.join(loc, name)
    save_write(save_path, res.content)

    return save_path


def set_user_data(name, data):
    path = os.path.join(USER_PATH, name + ".pck")
    try:
        with open(path, "w+b") as f:
            pck = pickle.dumps(data)
            f.write(pck)
    except IOError as err:
        tooltip(f"Could not write user files, check permissions. Error: {err}")


def get_user_data(name, default=None):
    if default is None:
        default = []
    path = os.path.join(USER_PATH, name + ".pck")
    if not os.path.isfile(path):
        return default
    try:
        with open(path, "rb") as f:
            pck = f.read()
            return pickle.loads(pck)
    except IOError as err:
        tooltip(f"Could not read user files, check permissions. Error: {err}")
        return default


def save_mk_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        tooltip(f"Can't create data folder, check permissions. Error: {error}")


def save_write(path, content, mode="w+b"):
    try:
        with open(path, mode) as f:
            f.write(content)
    except IOError as error:
        tooltip(f"Could not write content to disk. Error: {error}")


def save_write_unique(path, content:str, mode="a+"):
    try:
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("")

        existing_lines = set()
        with open(path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                existing_lines.add(stripped_line)

        new_content = content.strip()
        if new_content in existing_lines:
            return False

        with open(path, mode) as f:
            f.write(content)
        return True

    except Exception as e:
        print(e)
        tooltip(f"Error: Could not write content to disk")
        return False
