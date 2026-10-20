from aqt import gui_hooks
from aqt.editor import Editor

JSInject = r"""
(function() {
// Stops script from running too many times.
if (window.ankiBracketHandler) return;
window.ankiBracketHandler = true;

const Brackets = {'(': ')', '[': ']', '{': '}', '|': '|', '"': '"', "'": "'"};
const BracketsClose = new Set(Object.values(Brackets));
const BracketsOpen = new Set(Object.keys(Brackets));
const AllActionKeys = new Set([...BracketsOpen, ".", "Delete"]);
const AcceptedKeys = new Set([...AllActionKeys, ...BracketsClose, "Backspace", "ArrowLeft", "ArrowRight"]);
const BracketsNormOpen = ["(", "[", "{", "|", "."];

function GetSelectionText() {
    try {
        return window.getSelection();
    } catch (e) {
        return null;
    }
}

function MoveCursorLeft(NoSpaces) {
    setTimeout(() => { // Moves cursor into the brackets.
        try {
            for (let i = 0; i < Math.abs(NoSpaces); i++) {
                if (NoSpaces > 0) {
                    GetSelectionText()?.modify('move', 'backward', 'character');
                } else {
                    GetSelectionText()?.modify('move', 'forward', 'character');
                } 
            }
        } 
        catch (e) { }
    }, 0);
}

function handleKeyDown(event) {
    try {
        const { key, target } = event;

        // Skip all keys we don't care about.
        if (!AcceptedKeys.has(key)) { return; }
        
        // Check if we're in an editable field.
        if (!target) { return; }
        const isNoteEditor = target.classList.contains('rich-text-editable');
        const isMathJaxEditor = target.classList.contains('mathjax-editor') || target.getAttribute('contenteditable') === 'true' || target.tagName === 'TEXTAREA' || target.tagName === 'INPUT';
        if (!isNoteEditor && !isMathJaxEditor) { return; }
        
        const UserSelection = GetSelectionText();
        if (!UserSelection || !UserSelection.rangeCount) { return; }
        const SelectedText = UserSelection.toString();

        const CharBackslash = String.fromCharCode(92);


        if (AllActionKeys.has(key)) {

            if (SelectedText.length > 0) {

                if (key === ".") {return; }

                // If we are only selecting a bracket, or we are inputting the "." key, just replace the text.
                if ((SelectedText.length <= 2 && ((BracketsOpen.has(SelectedText) || BracketsClose.has(SelectedText)) || (SelectedText[0] === CharBackslash && (BracketsOpen.has(SelectedText[1]) || BracketsClose.has(SelectedText[1]))))) || key === ".") {
                    return;
                }

                if (key !== "Delete") {event.preventDefault(); }
                // Wrap user selected case.
                const Lead = SelectedText.substring(0, SelectedText.length - SelectedText.trimStart().length); 
                const Trail = SelectedText.substring(SelectedText.trimEnd().length);
                var TrimmedSelection = SelectedText.trim();
                var LengthToSelect = SelectedText.trim().length;
                var DidntDeleteAction = (key === "Delete");

                // If the user is selecting, for example, "(hello!)", and hits an open bracket key, we replace the brackets.
                var PadBackwards = 0;
                if ((BracketsOpen.has(SelectedText[0]) && Brackets[SelectedText[0]] === SelectedText[SelectedText.length - 1]) || (SelectedText[0] == CharBackslash && SelectedText[SelectedText.length - 2] === CharBackslash && BracketsOpen.has(SelectedText[1]) && Brackets[SelectedText[1]] === SelectedText[SelectedText.length - 1])) {
                    var BackslashMode = (SelectedText[0] === CharBackslash);

                    if (key === "Delete") {
                        // Removes the brackets in this particular case.
                        event.preventDefault();
                        DidntDeleteAction = false;
                        var TrimIndex = BackslashMode ? 2 : 1;
                        TrimmedSelection = TrimmedSelection.slice(TrimIndex, -TrimIndex)
                        PadBackwards -= 1
                    } else {
                        // If we are replacing left-right text, we need to add a backspace before the {,} keys.
                        var TrimIndex = TrimmedSelection.length - (BackslashMode ? 8 : 7);
                        var IsLeftRight = (key === "{") && (TrimmedSelection.substring(TrimIndex, TrimIndex + 6) === CharBackslash + "right");                   
                        TrimmedSelection = (IsLeftRight ? CharBackslash : "") + key + TrimmedSelection.substring((BackslashMode ? 2 : 1), TrimmedSelection.length - (BackslashMode ? 2 : 1)) + (IsLeftRight ? CharBackslash : "") + Brackets[key];
                        if (IsLeftRight) {PadBackwards += 1}
                    }
                    LengthToSelect -= BackslashMode ? 4 : 2;

                } else if (key !== "Delete") {
                    TrimmedSelection = key + TrimmedSelection + Brackets[key];
                }
                
                if (!DidntDeleteAction) {
                    document.execCommand('insertText', false, Lead + TrimmedSelection + Trail);
                    PadBackwards += Trail.length

                    // Reselect the user's original text highlights (including the helpful trim) :).
                    setTimeout(() => {
                        try {
                            // For some reason, the selection is always one character to the right at all times - move to the left once, and as well for any present trail.
                            for (let i = 0; i <= PadBackwards; i++) {
                                UserSelection.modify("move", "backward", "character");
                            }
                            for (let i = 0; i < LengthToSelect; i++) {
                                UserSelection.modify("extend", "backward", "character");
                            }
                        } catch (e) {}
                    }, 0);
                }

            } else {

                if (key === "Delete") {return; }

                // Attempts to get character immediately to the left.
                var LeftChar = '';
                try {
                    UserSelection.modify('extend', 'backward', 'character');
                    LeftChar = UserSelection.toString();
                    UserSelection.collapseToEnd();
                } catch (e) {}

                if (key in Brackets && key === Brackets[key] && SelectedText.length === 0) {
                    try {
                        UserSelection.modify('extend', 'forward', 'character');
                        // Tests if the next character in the stream is the same as what the user is typing. If so, we skip over it.
                        if (UserSelection.toString() === key && (key !== "|" || (key === "|" && LeftChar !== "|"))) {
                            event.preventDefault();
                            UserSelection.collapseToEnd();
                            return;
                        } else {
                            // Undoes UserSelection.modify.
                            UserSelection.collapseToStart();
                        }
                    } catch (e) {}
                }

                // If the key is either " or ', and the last character is alphanumeric (or brackets or colon), exit.
                if ((key === "'" || key === '"') && LeftChar && (/[a-zA-Z0-9)\]}]/.test(LeftChar) || (key === LeftChar))) { return; }

                // If the last character is a colon, exit (we like being able to write :( emoticons :D).
                if (key === "(" && LeftChar === ":") { return; }
                
                // Auto closes left with right text.
                if (BracketsNormOpen.includes(key)) {
                    // Gets the previous 5 characters (including the backslash key).
                    var LeftStringProceding = '';
                    try {
                        for (let i = 1; i <= 5; i++) {
                            UserSelection.modify("extend", "backward", "character");
                        }
                        LeftStringProceding = UserSelection.toString();
                    } catch (e) {}

                    var CloseRight = false;
                    var RightPadText = '';
                    if (LeftStringProceding) {
                        if (LeftStringProceding == (CharBackslash + "left")) {
                            // The user is attempting to open a left bracket.
                            CloseRight = true;
                            if (key === "{") RightPadText = CharBackslash; // Forgive the user if they forget the backslash when using {.
                        } else if (key === "{" && (LeftStringProceding == "left" + CharBackslash)) {
                            // Anki requires a backslash before any { character - allow for this.
                            UserSelection.modify('extend', 'backward', 'character');
                            LeftStringProceding = UserSelection.toString();
                            CloseRight = (LeftStringProceding[0] == CharBackslash);
                        }
                    }
                    UserSelection.collapseToEnd();

                    if (CloseRight) {
                        event.preventDefault();
                        // Enter the right closing text, then move the cursor back into the bracket.
                        RightPadText += key + '\u00A0\u00A0' + CharBackslash + "right"
                        var ExtraPad = 0
                        if (key === "{") {RightPadText += CharBackslash; ExtraPad++; }
                        if (key === "."){
                            RightPadText += "|_";
                            ExtraPad++;
                        } else {
                            RightPadText += Brackets[key]
                        }
                        document.execCommand('insertText', false, RightPadText);
                        MoveCursorLeft(8 + ExtraPad)
                        return;
                    }  
                }
                
                if (key === ".") return;
                event.preventDefault();

                let RightChar = '';
                try {
                    UserSelection.modify('extend', 'forward', 'character');
                    RightChar = UserSelection.toString();
                    UserSelection.collapseToStart(); // Undoes UserSelection.modify.
                } catch (e) {}

                const OpenBracket = key;
                const ClosedBracket = Brackets[key];
                let ModifiedTextInput = OpenBracket;
                let CursorLeftDelta = 1;

                // LaTeX requires \{\} for bracket pairs - detech this.
                if (key === "{" && LeftChar === CharBackslash) {
                    ModifiedTextInput += CharBackslash;
                    CursorLeftDelta += 1;
                }
                ModifiedTextInput += ClosedBracket;

                // Checks if we are in a position such as "hello _(world" - if so, we add a space before "w" to get "hello (_) world".
                if (LeftChar === ' ' && RightChar && RightChar !== ' ' && /[^.,!%^*;:_`~)\]\}\s\\]/.test(RightChar)) {
                    ModifiedTextInput += ' ';
                    CursorLeftDelta += 1; 
                }

                document.execCommand('insertText', false, ModifiedTextInput);
                MoveCursorLeft(CursorLeftDelta);
            }
            return;
        }

        if (BracketsClose.has(key) && SelectedText.length == 0) {
            // Attempts to close actions like \begin{cases} with \end{cases}.
            // Finds the open bracket associated with the closing bracket, then attempts to find it in the backstream of text.
            let OpenBracketMatch = '';
            for (const [Open, Closed] of Object.entries(Brackets)) {
                if (Closed === key) {
                    OpenBracketMatch = Open;
                    break;
                }
            }
            var LeftPad = '', WordAction = '';
            try {
                for (let i = 1; i <= 13; i++) {
                    UserSelection.modify("extend", "backward", "character");
                    LeftPad = UserSelection.toString();
                    if (LeftPad[0] == OpenBracketMatch) {
                        WordAction = LeftPad;
                        break;
                    }
                }
            } catch (e) {}

            if (WordAction) {
                // Gets the previous 6 characters (including the backslash key).
                try {
                    for (let i = 1; i <= 6; i++) {
                        UserSelection.modify("extend", "backward", "character");
                    }
                    LeftPad = UserSelection.toString();
                } catch (e) {}
                UserSelection.collapseToEnd();

                if (LeftPad && LeftPad == (CharBackslash + "begin" + WordAction)) {
                    event.preventDefault();

                    var EndText = '\u00A0\u00A0';
                    var PadLength = 6 + WordAction.length
                    if (WordAction === "{cases+") {
                        // Removes the +.
                        UserSelection.modify('extend', 'backward', 'character');
                        document.execCommand('delete', false, null);

                        WordAction = "{cases";
                        PadLength -= 1;
                        //Adds helper text.
                        const CasesExtraPad = "&" + CharBackslash + "text{if }" + CharBackslash + " a " + CharBackslash + CharBackslash +" b &" + CharBackslash + "text{else}";
                        EndText += CasesExtraPad;
                        PadLength += CasesExtraPad.length + 1;
                    }
                    EndText += CharBackslash + "end" + WordAction + "}";

                    // Checks if the next character is the key - if so, we skip over it.
                    UserSelection.modify('extend', 'forward', 'character');
                    if (UserSelection.toString() === key) {
                        UserSelection.collapseToEnd();
                        MoveCursorLeft(-1);
                    } else {
                        UserSelection.collapseToStart();
                        EndText = key + EndText;
                    }
                    // Close with \endWordAction}, then move the cursor back into the bracket.
                    document.execCommand('insertText', false, EndText);
                    MoveCursorLeft(PadLength);
                    return;
                }
            } else {
                UserSelection.collapseToEnd();
            }

            // If the cursor is to the left of a closing bracket, and they press that key, just move the cursor to the right.
            try {
                UserSelection.modify('extend', 'forward', 'character');
                const ExtendedText = UserSelection.toString();

                if (ExtendedText === key) {
                    event.preventDefault();
                    UserSelection.collapseToEnd();
                } else { // Normal key action.
                    UserSelection.collapseToStart();
                }
            } catch (e) {}

            return;
        }
        
        // If we enter a backspace on an empty bracket "(_)", we should remove both braces.
        if (key === 'Backspace' && SelectedText.length === 0) {
            try {
                // Gets the characters immediately to the left & right of the cursor.
                UserSelection.modify('extend', 'backward', 'character');
                const LeftChar = UserSelection.toString();
                UserSelection.collapseToEnd();

                UserSelection.modify('extend', 'forward', 'character');
                const RightChar = UserSelection.toString();
                UserSelection.collapseToStart();

                if (BracketsOpen.has(LeftChar)) {
                    if (RightChar === Brackets[LeftChar]) {
                        // We are deleting an empty brace - select and remove both brackets.
                        event.preventDefault();
                        UserSelection.modify('move', 'backward', 'character');
                        UserSelection.modify('extend', 'forward', 'character');
                        UserSelection.modify('extend', 'forward', 'character');
                        document.execCommand('delete', false, null);
                        return;
                    } else if (RightChar === CharBackslash) { // = '\' (for some reason, we can't test this directly with === "\\") :(
                        // In Anki, MathJax equations are represented via \(_\). We also want to delete _all_ of this.
                        // Gets the characters two to the left & right of the cursor.
                        let LeftString = ''
                        UserSelection.modify('extend', 'backward', 'character');
                        UserSelection.modify('extend', 'backward', 'character');
                        LeftString = UserSelection.toString();
                        UserSelection.collapseToEnd();

                        let RightString = ''
                        UserSelection.modify('extend', 'forward', 'character');
                        UserSelection.modify('extend', 'forward', 'character');
                        RightString = UserSelection.toString();
                        UserSelection.collapseToStart();
                        
                        if (LeftString[0] === CharBackslash && RightString[0] === CharBackslash && BracketsClose.has(RightString[1])) {
                            if (BracketsOpen.has(LeftString[1]) ) {
                                event.preventDefault();
                                for (let i = 1; i <= 2; i++) {
                                    UserSelection.modify('move', 'backward', 'character');
                                }
                                for (let i = 1; i <= 4; i++) {
                                    UserSelection.modify('extend', 'forward', 'character');
                                }
                                document.execCommand('delete', false, null);
                                return;
                            }
                        }
                    }
                }              
            } catch (e) { }
        }

        // If we are moving left or right on an instance of \( or \) (ie: MathJax), we move twice.
        if (SelectedText.length === 0 && (key === 'ArrowLeft' || key === 'ArrowRight')) {
            var EqnCharTest = '';
            try {
                for (let i = 1; i <= 2; i++) {
                    UserSelection.modify('extend', key === 'ArrowRight' ? 'forward' : 'backward', 'character');
                }
                EqnCharTest = UserSelection.toString();
                if (key === 'ArrowRight') UserSelection.collapseToStart(); else UserSelection.collapseToEnd();
            } catch (e) {} 
            if (EqnCharTest && EqnCharTest[0] === CharBackslash && (BracketsOpen.has(EqnCharTest[1]) || BracketsClose.has(EqnCharTest[1]))) {
                event.preventDefault();
                MoveCursorLeft(key === 'ArrowRight' ? -2 : 2);
            }
        }

    } catch (e) {
        console.error("AnkiBracketHandler Error:", e);
    }
}
document.addEventListener('keydown', handleKeyDown, true);
})();
"""

def on_editor_did_init(editor: Editor):
    editor.web.eval(JSInject)

def on_editor_did_load_note(editor: Editor):
    editor.web.eval(JSInject)

gui_hooks.editor_did_init.append(on_editor_did_init)
gui_hooks.editor_did_load_note.append(on_editor_did_load_note)