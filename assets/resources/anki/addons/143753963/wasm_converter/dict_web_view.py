# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

from typing import Callable, Optional

try:
    from PyQt6.QtCore import Qt, QUrl
    from PyQt6.QtWidgets import QVBoxLayout, QWidget
    from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except ImportError:  # pragma: no cover - fallback for older Anki versions
    from aqt.qt import Qt, QUrl, QVBoxLayout, QWidget  # type: ignore
    from aqt.qt import QWebEnginePage, QWebEngineSettings, QWebEngineView  # type: ignore

from ..path_manager import ADDON_NAME


# MARK:ConvertDictWebEnginePage
class ConvertDictWebEnginePage(QWebEnginePage):

    # MARK:ConvertDictWebEnginePage constructor
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_callback: Optional[Callable[[str], None]] = None

    # MARK:javaScriptConsoleMessage
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        if self.log_callback is None:
            return
        try:
            self.log_callback(f"{message} ({source_id}:{line_number})")
        except Exception:
            pass


# MARK:ConvertDictWebView
class ConvertDictWebView(QWidget):

    # MARK:ConvertDictWebView constructor
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setFixedSize(2, 2)

        self._view = QWebEngineView(self)
        self._page = ConvertDictWebEnginePage(self._view)
        self._view.setPage(self._page)

        settings = self._view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)
        self.setLayout(layout)

        # keep JavaScript running even though the widget is not visible
        try:
            self._page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
        except Exception:
            pass

        self._page_loaded = False
        # The page stays "visible" for the renderer (hidden pages may be
        # throttled), so the widget is parked far off-screen instead of being
        # hidden completely.
        self.move(-32000, -32000)
        self.show()

    # MARK:web_view
    @property
    def web_view(self):
        return self._view

    # MARK:set_log_callback
    def set_log_callback(self, callback: Optional[Callable[[str], None]]):
        self._page.log_callback = callback

    # MARK:load_html
    def load_html(self, html: str, on_load_finished: Optional[Callable[[bool], None]] = None):
        if on_load_finished is not None:
            self._view.loadFinished.connect(lambda ok: on_load_finished(bool(ok)))
        self._page_loaded = True
        self._view.setHtml(html, QUrl("about:blank"))

    # MARK:run_javascript
    def run_javascript(self, code: str):
        if not self._page_loaded:
            print(f"[{ADDON_NAME}] Error: page is not loaded yet")
            return
        self._view.page().runJavaScript(code)

    # MARK:run_javascript_with_callback
    def run_javascript_with_callback(self, code: str, callback):
        if not self._page_loaded:
            print(f"[{ADDON_NAME}] Error: page is not loaded yet")
            if callback:
                callback(None)
            return
        self._view.page().runJavaScript(code, callback)

    # MARK:show_for_debug
    def show_for_debug(self):
        self.setFixedSize(360, 260)
        self.move(80, 80)
        self.show()
        self.raise_()
        self.activateWindow()

    # MARK:hide_for_debug
    def hide_for_debug(self):
        self.setFixedSize(2, 2)
        self.move(-32000, -32000)

    # MARK:cleanup
    def cleanup(self):
        try:
            self._view.stop()
            self._view.setPage(None)
            self._view.deleteLater()
        except Exception:
            pass
        self._page_loaded = False
        self.close()
