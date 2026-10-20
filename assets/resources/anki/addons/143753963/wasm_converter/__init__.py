# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

from .dict_engine import (
    ConvertDictWasmEngine,
    convert_dic_aff_to_bdic,
    get_engine,
    is_engine_ready,
    shutdown_engine,
)

__all__ = [
    "ConvertDictWasmEngine",
    "convert_dic_aff_to_bdic",
    "get_engine",
    "is_engine_ready",
    "shutdown_engine",
]
