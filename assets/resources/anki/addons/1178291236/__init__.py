# Custom Highlight Color Shortcut
# Highlight code taken from Glutaminate's Mini Format Pack
# https://github.com/glutanimate/mini-format-pack/blob/master/src/mini_format_pack/main.py


from aqt import mw
from aqt import gui_hooks
from functools import partial
from anki.utils import isWin, isMac

config = mw.addonManager.getConfig(__name__)
bold_config = config['bold']

# Code for highlight
def highlightcolor(editor, color):
    """
    Wrap the selected text in an appropriate tag with a background color.
    """
    # On Linux, the standard 'hiliteColor' method works. On Windows and OSX
    # the formatting seems to get filtered out

    editor.web.eval("""
        if (!setFormat('hiliteColor', '%s')) {
            setFormat('backcolor', '%s');
        }
        """ % (color, color))

    if isWin or isMac:
        # remove all Apple style classes, which is needed for
        # text highlighting on platforms other than Linux
        editor.web.eval("""
            var matches = document.querySelectorAll(".Apple-style-span");
            for (var i = 0; i < matches.length; i++) {
                matches[i].removeAttribute("class");
            }
        """)

# Code that links keyboard shortcut to highlight action
def updateColour(editor, colour):
    highlightcolor(editor,colour)
    if bold_config == "on":
        editor.toggleBold()



def onSetupShortcuts(cuts, editor):
    for color_code, keyboard_shortcut in config['keys']:
        def append_function(hex_code):
            return updateColour(editor, hex_code)
        append_this = partial(append_function,color_code)
        cuts.append((keyboard_shortcut,append_this))

gui_hooks.editor_did_init_shortcuts.append(onSetupShortcuts)
