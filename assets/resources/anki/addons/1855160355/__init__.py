from aqt import mw, gui_hooks
from aqt.addcards import AddCards
from aqt.qt import QTimer
from typing import Callable
import re

def GetModuleCode(Name: str) -> str:
    if not Name or not Name.strip():
        return ""
    RegexKey = r'^([A-Z]{2}[A-Z\d]{3})[:\s]'
    Match = re.match(RegexKey, Name.strip())
    return f"{Match.group(1)}:" if Match else ""

def GetDeckParents(DeckID: int) -> tuple[str, str]:
    try:
        if not DeckID:
            return "", ""
        Deck = mw.col.decks.get(DeckID)
        if not Deck:
            return "", ""
        parts = Deck.get("name", "").split("::")

        if len(parts) >= 2:
            return parts[-2], parts[-1]
        elif len(parts) == 1:
            return parts[0], ""
        else:
            return "", ""
    except Exception as e:
        print(f"Error in GetDeckParents: {e}")
        return "", ""

def HandleNewCard(NewCard: AddCards):
    Editor = NewCard.editor
    UserEntry = {"Index ": "", "Chapter": "", "Subchapter": ""}

    def IsOverwriteable(value: str) -> bool:
        if value is None:
            return True
        s = value.strip()
        if s == "":
            return True
        if s.lower() in ("default", "none", "<auto>"):
            return True
        return False

    def CanUpdateField(Note, TempIndex: str, TempChapter: str, TempSubchapter: str) -> bool:
        try:
            nid = getattr(Note, "id", None)
            if not nid or nid == 0:
                return True
            if IsOverwriteable(TempIndex) or IsOverwriteable(TempChapter) or IsOverwriteable(TempSubchapter):
                return True
            if (TempIndex.strip() == UserEntry["Index"].strip() and TempChapter.strip() == UserEntry["Chapter"].strip() and TempSubchapter.strip() == UserEntry["Subchapter"].strip()):
                return True
            return False
        except Exception as e:
            print(f"Error in CanUpdateField: {e}")
            return True

    def UpdateField(DeckID: int):
        try:
            Note = Editor.note
            if not Note:
                return
            try:
                TempIndex = Note["Index"]
                TempChapter = Note["Chapter"]
                TempSubchapter = Note["Subchapter"]
            except Exception:
                return

            if CanUpdateField(Note, TempIndex, TempChapter, TempSubchapter):
                NewChapter, NewSubchapter = GetDeckParents(DeckID)
                NewIndex = GetModuleCode(NewChapter.upper())
                if (NewIndex == ""):
                    NewIndex = GetModuleCode(NewSubchapter.upper())
                NewSubChapterStrip = NewSubchapter.strip()
                if (Note["Index"].strip() != NewIndex.strip() or Note["Chapter"].strip() != NewChapter.strip() or Note["Subchapter"].strip() != NewSubChapterStrip):
                    Note["Chapter"] = NewChapter
                    Note["Subchapter"] = NewSubchapter
                    UserEntry["Chapter"] = NewChapter
                    UserEntry["Subchapter"] = NewSubchapter
                    
                    SubChapterWords = NewSubChapterStrip.split()
                    if (NewIndex == "" and len(SubChapterWords) == 3):
                        NewIndex = "".join(Word[0].upper() for Word in SubChapterWords)
                        NewIndex += ":"
                    Note["Index"] = NewIndex
                    UserEntry["Index"] = NewIndex

                    Editor.loadNoteKeepingFocus()
        except Exception as e:
            print(f"Error in UpdateField: {e}")
        
        
    TempDeckChangeHandle: Callable[[int], None] = NewCard.deckChooser.on_deck_changed
    def HandleDeckChanged(DeckID: int):
        TempDeckChangeHandle(DeckID)
        UpdateField(DeckID)


    NewCard.deckChooser.on_deck_changed = HandleDeckChanged
    try:
        note = Editor.note
        if note:
            try:
                UserEntry["Chapter"] = note["Chapter"] or ""
                UserEntry["Subchapter"] = note["Subchapter"] or ""
            except Exception:
                pass
    except Exception:
        pass


    def InitUpdate():
        try:
            UpdateField(NewCard.deckChooser.selectedId())
        except Exception as e:
            print(f"Error in InitUpdate: {e}")

    QTimer.singleShot(0, InitUpdate)

gui_hooks.add_cards_did_init.append(HandleNewCard)
