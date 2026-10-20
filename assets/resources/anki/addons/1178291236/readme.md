# Highlight Color Shortcut

_Set a keyboard shortcut to highlight selected text quickly._

![Screenshot](https://github.com/BigFatDuck1/highlightcolorshortcut_anki/blob/master/images/screenshot.png)

![Screenshot](https://github.com/BigFatDuck1/highlightcolorshortcut_anki/blob/master/images/capture.gif)

## Installation

Easiest way to install is to get it here:
<https://ankiweb.net/shared/info/1178291236>

## Description

Simple anki addon for customizing keyboard shortcuts to quickly highlight text. Similar to my other add-on, <https://github.com/BigFatDuck1/boldcolorshortcut-anki>.

You can toggle whether you want the text to be **bolded** after highlighting.
Change this in the config.json file:
```"bold": "on"``` or ```"bold": "off"```.

### Current defaults are

* **R**ed
* **O**range
* **Y**ellow
* **G**reen
* **L**ight Green
* **B**lue
* **P**urple
* Brow**n** (N)
* **W**hite
* Cyan (**D**)

Shortcut is `Ctrl + Alt + (First letter)`
\
(exceptions placed in brackets, e.g. `Ctrl + Alt + O` for orange or `Ctrl + Alt + D` for cyan)

I used `Alt` to not clash with my other add-on.

Colour names can be standard colour names like "red", or red/green/blue colour codes like `#ffffff`.

Make sure the keyboard shortcut you have chosen does not overlap with other anki keyboard shortcuts, as those take precedent!

\
_Credits_

Thanks to [Glutaminate's Mini Format Pack](https://github.com/glutanimate/mini-format-pack/blob/master/src/mini_format_pack/main.py), I took the Highlight code from there.
