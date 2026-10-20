# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import base64
import json
import os
import threading
import traceback
from typing import Callable, Dict, Optional

from aqt import gui_hooks, mw

try:
    from PyQt6.QtCore import (
        QCoreApplication,
        QObject,
        Qt,
        QThread,
        pyqtSignal,
        pyqtSlot,
    )
    from PyQt6.QtWebChannel import QWebChannel
except ImportError:
    from aqt.qt import QCoreApplication, QObject, Qt, QThread
    from aqt.qt import pyqtSignal, pyqtSlot
    from aqt.qt import QWebChannel

from ..path_manager import ADDON_NAME

WASM_FOLDER = os.path.dirname(os.path.abspath(__file__))
BUILT_JS_PATH = os.path.join(WASM_FOLDER, "built", "convert_dict.js")
BUILT_WASM_PATH = os.path.join(WASM_FOLDER, "built", "convert_dict.wasm")
ENGINE_JS_NAME = "dict_engine.js"
ENGINE_HTML_NAME = "dict_engine.html"

ENGINE_READY_TIMEOUT = 120.0
CONVERT_TIMEOUT = 600.0
BDIC_SIGNATURE = b"BDic"


# MARK:_is_main_thread
def _is_main_thread():
    app = QCoreApplication.instance()
    if app is None:
        return True
    return QThread.currentThread() is app.thread()


# MARK:_MainThreadDispatcher
class _MainThreadDispatcher(QObject):

    run = pyqtSignal(object)
    run_blocking = pyqtSignal(object)

    # MARK:_MainThreadDispatcher constructor
    def __init__(self):
        super().__init__()
        app = QCoreApplication.instance()
        if app is not None:
            main_thread = app.thread()
            if QThread.currentThread() is not main_thread:
                self.moveToThread(main_thread)

        self.run.connect(self._execute, Qt.ConnectionType.QueuedConnection)
        self.run_blocking.connect(self._execute, Qt.ConnectionType.BlockingQueuedConnection)

    # MARK:_execute
    @pyqtSlot(object)
    def _execute(self, func: Callable[[], None]) -> None:
        try:
            func()
        except Exception as e:
            print(f"[{ADDON_NAME}] Error: {e}")
            traceback.print_exc()


_dispatcher = _MainThreadDispatcher()


# MARK:run_on_main_thread
def run_on_main_thread(func: Callable[[], None]):
    if _is_main_thread():
        func()
    else:
        _dispatcher.run.emit(func)


# MARK:run_on_main_thread_blocking
def run_on_main_thread_blocking(func: Callable[[], None]):
    if _is_main_thread():
        func()
    else:
        _dispatcher.run_blocking.emit(func)


# MARK:_read_qt_resource
def _read_qt_resource(path: str):
    try:
        from PyQt6.QtCore import QFile, QIODevice
    except ImportError:  # pragma: no cover
        from aqt.qt import QFile, QIODevice  # type: ignore

    qt_file = QFile(path)
    if not qt_file.open(QIODevice.OpenModeFlag.ReadOnly):
        raise RuntimeError(f"could not read Qt resource: {path}")
    try:
        return bytes(qt_file.readAll().data()).decode("utf-8")
    finally:
        qt_file.close()


# MARK:ConvertDictBridge
class ConvertDictBridge(QObject):
    # MARK:ConvertDictBridge constructor
    def __init__(self, engine: "ConvertDictWasmEngine"):
        super().__init__()
        self._engine = engine

    # MARK:onLog
    @pyqtSlot(str)
    def onLog(self, message: str):
        self._engine.handle_log(message)

    # MARK:onReady
    @pyqtSlot()
    def onReady(self):
        self._engine.resolve_waiter("ready")

    # MARK:onResult
    @pyqtSlot(str)
    def onResult(self, bdic_base64: str):
        self._engine.resolve_waiter("result", bdic_base64)

    # MARK:onError
    @pyqtSlot(str)
    def onError(self, message: str):
        self._engine.reject_waiters(message)


# MARK:ConvertDictWasmEngine
class ConvertDictWasmEngine:

    # MARK:ConvertDictWasmEngine constructor
    def __init__(self):
        self._view = None
        self._bridge: Optional[ConvertDictBridge] = None
        self._channel = None

        self._ready = False

        self._waiters: Dict[str, dict] = {}
        self._waiters_lock = threading.Lock()
        self._op_lock = threading.RLock()

        self._last_messages = []

    # MARK:_prepare_waiter
    def _prepare_waiter(self, name: str):
        waiter = {"event": threading.Event(), "value": None, "error": None}
        with self._waiters_lock:
            self._waiters[name] = waiter
        return waiter

    # MARK:_wait
    def _wait(self, waiter: dict, name: str, timeout: float):
        if not waiter["event"].wait(timeout):
            with self._waiters_lock:
                if self._waiters.get(name) is waiter:
                    self._waiters.pop(name, None)
            raise TimeoutError(f"timeout waiting for the convert_dict engine ({name})")
        if waiter["error"]:
            raise RuntimeError(waiter["error"])
        return waiter["value"]

    # MARK:resolve_waiter
    def resolve_waiter(self, name: str, value=None):
        with self._waiters_lock:
            waiter = self._waiters.pop(name, None)
        if waiter is None:
            return
        waiter["value"] = value
        waiter["event"].set()

    # MARK:reject_waiters
    def reject_waiters(self, message: str):
        print(f"[{ADDON_NAME}] engine error: {message}")
        with self._waiters_lock:
            waiters = list(self._waiters.values())
            self._waiters.clear()
        for waiter in waiters:
            waiter["error"] = message
            waiter["event"].set()

    # MARK:handle_log
    def handle_log(self, message: str):
        self._last_messages.append(message)
        if len(self._last_messages) > 50:
            self._last_messages.pop(0)
        print(f"[{ADDON_NAME}:js] {message}")

    # MARK:_run_js
    def _run_js(self, code: str):
        if self._view is not None:
            self._view.run_javascript(code)

    # MARK:_create_and_load
    def _create_and_load(self):
        if self._view is not None:
            return

        from .dict_web_view import ConvertDictWebView

        self._view = ConvertDictWebView(parent=mw)
        self._view.set_log_callback(self.handle_log)

        self._bridge = ConvertDictBridge(self)
        self._channel = QWebChannel(self._view.web_view.page())
        self._channel.registerObject("convertDictBridge", self._bridge)
        self._view.web_view.page().setWebChannel(self._channel)

        html = self._build_engine_html()
        print(f"[{ADDON_NAME}] loading the convert_dict engine page")
        self._view.load_html(html, on_load_finished=self._on_page_loaded)

    # MARK:_on_page_loaded
    def _on_page_loaded(self, ok: bool) -> None:
        if ok:
            print(f"[{ADDON_NAME}] convert_dict engine page loaded")
        else:
            self.reject_waiters("the convert_dict engine page could not be loaded")

    # MARK:_build_engine_html
    def _build_engine_html(self):
        template_path = os.path.join(WASM_FOLDER, ENGINE_HTML_NAME)
        engine_js_path = os.path.join(WASM_FOLDER, ENGINE_JS_NAME)

        for path in (template_path, engine_js_path, BUILT_JS_PATH, BUILT_WASM_PATH):
            if not os.path.exists(path):
                raise FileNotFoundError(f"a convert_dict engine file is missing: {path}")

        with open(template_path, "r", encoding="utf-8") as template_file:
            html = template_file.read()
        with open(engine_js_path, "r", encoding="utf-8") as engine_js_file:
            engine_js = engine_js_file.read()
        with open(BUILT_JS_PATH, "r", encoding="utf-8") as built_js_file:
            built_js = built_js_file.read()
        with open(BUILT_WASM_PATH, "rb") as built_wasm_file:
            built_wasm_base64 = base64.b64encode(built_wasm_file.read()).decode("ascii")

        html = html.replace("__QWEBCHANNEL_JS__", _read_qt_resource(":/qtwebchannel/qwebchannel.js"))
        html = html.replace("__CONVERT_DICT_JS__", built_js)
        html = html.replace("__CONVERT_DICT_WASM_B64__", built_wasm_base64)
        html = html.replace("__CONVERT_DICT_ENGINE_JS__", engine_js)
        return html

    # MARK:ensure_ready
    def ensure_ready(self):
        if self._ready:
            return True
        with self._op_lock:
            if self._ready:
                return True

            ready_waiter = self._prepare_waiter("ready")
            run_on_main_thread(self._create_and_load)
            self._wait(ready_waiter, "ready", ENGINE_READY_TIMEOUT)

            self._ready = True
            print(f"[{ADDON_NAME}] convert_dict engine ready")
            return True

    # MARK:_read_as_base64
    @staticmethod
    def _read_as_base64(path: str) -> str:
        with open(path, "rb") as input_file:
            file_bytes = input_file.read()
        return base64.b64encode(file_bytes).decode("ascii")

    # MARK:convert
    def convert(self, aff_path: str, dic_path: str, output_path: str):
        with self._op_lock:
            self.ensure_ready()

            aff_base64 = self._read_as_base64(aff_path)
            dic_base64 = self._read_as_base64(dic_path)

            waiter = self._prepare_waiter("result")
            code = f"convertDictEngine.convert({json.dumps(aff_base64)}, {json.dumps(dic_base64)});"
            run_on_main_thread(lambda: self._run_js(code))

            result_base64 = self._wait(waiter, "result", CONVERT_TIMEOUT)

            bdic_bytes = base64.b64decode(result_base64)
            if not bdic_bytes.startswith(BDIC_SIGNATURE):
                raise RuntimeError("the conversion result is not a bdic file")

            output_directory = os.path.dirname(output_path)
            if output_directory:
                os.makedirs(output_directory, exist_ok=True)
            with open(output_path, "wb") as output_file:
                output_file.write(bdic_bytes)
            return True

    # MARK:ready
    @property
    def ready(self):
        return self._ready

    # MARK:show_for_debug
    def show_for_debug(self) -> None:
        if self._view is not None:
            run_on_main_thread(self._view.show_for_debug)

    # MARK:hide_for_debug
    def hide_for_debug(self) -> None:
        if self._view is not None:
            run_on_main_thread(self._view.hide_for_debug)

    # MARK:cleanup
    def cleanup(self) -> None:
        with self._op_lock:
            self._ready = False
            if self._view is not None:
                try:
                    self._view.cleanup()
                except Exception:
                    pass
                self._view = None
            self._bridge = None
            self._channel = None


# MARK:module level API
_engine_lock = threading.Lock()
_engine: Optional[ConvertDictWasmEngine] = None


# MARK:get_engine
def get_engine():
    global _engine
    with _engine_lock:
        if _engine is None:
            _engine = ConvertDictWasmEngine()
        return _engine


# MARK:is_engine_ready
def is_engine_ready():
    return (_engine is not None) and _engine.ready


# MARK:convert_dic_aff_to_bdic
def convert_dic_aff_to_bdic(aff_path: str, dic_path: str, output_path: str):
    engine = get_engine()
    engine.ensure_ready()
    return engine.convert(aff_path, dic_path, output_path)


# MARK:shutdown_engine
def shutdown_engine():
    global _engine
    with _engine_lock:
        engine = _engine
        _engine = None
    if engine is None:
        return

    # MARK:cleanup
    def cleanup():
        try:
            engine.cleanup()
        except Exception as e:
            print(f"[{ADDON_NAME}] Error: {e}")

    run_on_main_thread_blocking(cleanup)


# MARK:_on_profile_will_close
def _on_profile_will_close(*args, **kwargs) -> None:
    global _engine
    with _engine_lock:
        engine = _engine
        _engine = None
    if engine is not None:
        engine.cleanup()


try:
    gui_hooks.profile_will_close.append(_on_profile_will_close)
except Exception:  # pragma: no cover
    pass
