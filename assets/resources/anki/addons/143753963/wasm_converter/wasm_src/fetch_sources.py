# Downloads the pinned Chromium sources for the convert_dict WASM build.

import os
import urllib.request

CHROMIUM_REPOSITORY = "https://github.com/chromium/chromium"
CHROMIUM_TAG = "157.0.8096.1"
CHROMIUM_COMMIT = "098f266e40b8f4f4f531949f14417e4eaae8deae"

SOURCE_BASE_URL = f"https://raw.githubusercontent.com/chromium/chromium/{CHROMIUM_TAG}"

SOURCE_FILES = [
    "chrome/tools/convert_dict/convert_dict.cc",
    "chrome/tools/convert_dict/aff_reader.h",
    "chrome/tools/convert_dict/aff_reader.cc",
    "chrome/tools/convert_dict/dic_reader.h",
    "chrome/tools/convert_dict/dic_reader.cc",
    "chrome/tools/convert_dict/hunspell_reader.h",
    "chrome/tools/convert_dict/hunspell_reader.cc",
    "third_party/hunspell/google/bdict.h",
    "third_party/hunspell/google/bdict.cc",
    "third_party/hunspell/google/bdict_writer.h",
    "third_party/hunspell/google/bdict_writer.cc",
    "third_party/hunspell/google/bdict_reader.h",
    "third_party/hunspell/google/bdict_reader.cc",
]


# MARK:download_source_file
def download_source_file(relative_path, sources_directory):
    download_url = f"{SOURCE_BASE_URL}/{relative_path}"
    output_path = os.path.join(sources_directory, *relative_path.split("/"))
    output_directory = os.path.dirname(output_path)
    os.makedirs(output_directory, exist_ok=True)

    request = urllib.request.Request(
        download_url,
        headers={"User-Agent": "anki-spell-checker-convert-dict-wasm"},
    )
    with urllib.request.urlopen(request) as response:
        content = response.read()
    with open(output_path, "wb") as output_file:
        output_file.write(content)
    print(f"downloaded: {relative_path} ({len(content)} bytes)")


# MARK:write_source_version
def write_source_version(script_directory):
    version_info_path = os.path.join(script_directory, "SOURCE_VERSION.txt")
    with open(version_info_path, "w", encoding="utf-8") as version_file:
        version_file.write(f"repository: {CHROMIUM_REPOSITORY}\n")
        version_file.write(f"tag: {CHROMIUM_TAG}\n")
        version_file.write(f"commit: {CHROMIUM_COMMIT}\n")
    print(f"wrote: {version_info_path}")


# MARK:main
def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    sources_directory = os.path.join(script_directory, "sources")

    for relative_path in SOURCE_FILES:
        download_source_file(relative_path, sources_directory)

    write_source_version(script_directory)
    print("done")


if __name__ == "__main__":
    main()
