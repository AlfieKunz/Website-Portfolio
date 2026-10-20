
import requests
import os

SHIGE_REPO_URL = 'https://api.github.com/repos/shigeyukey/third_party_hunspell_dictionaries/git/refs/heads/master'

LANGUAGE_DICT = {
'Afrikaans': 'af-ZA-3-0.bdic',
'Albanian': 'sq-3-0.bdic',
'Bulgarian': 'bg-BG-3-0.bdic',
'Catalan': 'ca-ES-3-0.bdic',
'Croatian': 'hr-HR-3-0.bdic',
'Czech': 'cs-CZ-3-0.bdic',
'Danish': 'da-DK-3-0.bdic',
'Dutch': 'nl-NL-3-0.bdic',
'English (Australia)': 'en-AU-3-0.bdic',
'English (Canada)': 'en-CA-3-0.bdic',
'English (UK)': 'en-GB-3-0.bdic',
'English (US)': 'en-US-3-0.bdic',
'Estonian': 'et-EE-3-0.bdic',
'Faroese': 'fo-FO-3-0.bdic',
'French': 'fr-FR-3-0.bdic',
'German': 'de-DE-3-0.bdic',
'Greek': 'el-GR-3-0.bdic',
'Hebrew': 'he-IL-3-0.bdic',
'Hindi': 'hi-IN-3-0.bdic',
'Hungarian': 'hu-HU-3-0.bdic',
'Indonesian': 'id-ID-3-0.bdic',
'Italian': 'it-IT-3-0.bdic',
'Korean': 'ko-3-0.bdic',
'Latvian': 'lv-LV-3-0.bdic',
'Lithuanian': 'lt-LT-3-0.bdic',
'Norwegian': 'nb-NO-3-0.bdic',
'Polish': 'pl-PL-3-0.bdic',
'Portuguese (Brazil)': 'pt-BR-3-0.bdic',
'Portuguese (Portugal)': 'pt-PT-3-0.bdic',
'Romanian': 'ro-RO-3-0.bdic',
'Russian': 'ru-RU-3-0.bdic',
'Serbian': 'sr-3-0.bdic',
'Serbo-Croatian': 'sh-3-0.bdic',
'Slovak': 'sk-SK-3-0.bdic',
'Slovenian': 'sl-SI-3-0.bdic',
'Spanish': 'es-ES-3-0.bdic',
'Swedish': 'sv-SE-3-0.bdic',
'Tamil': 'ta-IN-3-0.bdic',
'Turkish': 'tr-TR-4-0.bdic',
'Ukrainian': 'uk-UA-3-0.bdic',
'Vietnamese': 'vi-VN-3-0.bdic'
}

# debug only
def print_language_dict_html():
    base_url = "https://raw.githubusercontent.com/shigeyukey/third_party_hunspell_dictionaries/master/"
    html = "<ul>\n"
    for name, file_name in LANGUAGE_DICT.items():
        url = base_url + file_name
        html += f'  <li><a href="{url}">{name}</a></li>\n'
    html += "</ul>"
    print(html)
if __name__ == "__main__":
    print_language_dict_html()

def download_dictionary(language, output_dir=None):
    if not output_dir:
        return
    if language not in LANGUAGE_DICT:
        return None
    file_name = LANGUAGE_DICT[language]
    try:
        ref_response = requests.get(SHIGE_REPO_URL)
        if ref_response.status_code != 200:
            return None
        raw_url = f"https://raw.githubusercontent.com/shigeyukey/third_party_hunspell_dictionaries/master/{file_name}"
        download_response = requests.get(raw_url, stream=True)
        if download_response.status_code != 200:
            return None
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'wb') as file:
            for data in download_response.iter_content(1024):
                file.write(data)
        return file_path

    except Exception:
        print(f"Error downloading {file_name}: {str(Exception)}")
        return None


