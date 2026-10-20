from aqt.webview import AnkiWebView

# fix for Anki25.02.1~ https://forums.ankiweb.net/t/spell-checker-add-on-not-working-with-25-02-1/59287
def get_ankiwebview_page(anki_webview:"AnkiWebView"):
    if not hasattr(anki_webview, '_page'):
        # new anki Anki25.02.1~
        return anki_webview.page()
    # old anki ~ Anki25.0
    return anki_webview._page

# from .support_old_anki import get_ankiwebview_page
    # # page = editor_webview._page
    # page = get_ankiwebview_page(editor_webview)
