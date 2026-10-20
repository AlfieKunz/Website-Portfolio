@echo off
setlocal

rem Builds ..\built\convert_dict.js and convert_dict.wasm with the Emscripten SDK.

if "%EMSDK_PATH%"=="" set EMSDK_PATH=C:\_github\emsdk

call "%EMSDK_PATH%\emsdk_env.bat"

rem The Chromium sources live next to this script (fetched by fetch_sources.py).
set SOURCE_DIR=%~dp0sources
set SHIM_DIR=%~dp0shims
rem The built module is bundled with the add-on runner (release output).
set OUTPUT_DIR=%~dp0..\built

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

rem The JS glue is intentionally kept unminified so that convert_dict.js
rem stays human-readable (the wasm binary is still optimized with -O2).
call emcc ^
  "%SOURCE_DIR%\chrome\tools\convert_dict\convert_dict.cc" ^
  "%SOURCE_DIR%\chrome\tools\convert_dict\aff_reader.cc" ^
  "%SOURCE_DIR%\chrome\tools\convert_dict\dic_reader.cc" ^
  "%SOURCE_DIR%\chrome\tools\convert_dict\hunspell_reader.cc" ^
  "%SOURCE_DIR%\third_party\hunspell\google\bdict.cc" ^
  "%SOURCE_DIR%\third_party\hunspell\google\bdict_writer.cc" ^
  "%SOURCE_DIR%\third_party\hunspell\google\bdict_reader.cc" ^
  "%SHIM_DIR%\crypto\obsolete\md5.cc" ^
  -include "%SHIM_DIR%\wasm_prelude.h" ^
  -I "%SOURCE_DIR%" ^
  -I "%SHIM_DIR%" ^
  -std=gnu++20 ^
  -O2 ^
  --minify 0 ^
  -sMODULARIZE=1 ^
  -sEXPORT_NAME=createConvertDictModule ^
  -sINVOKE_RUN=0 ^
  -sEXPORTED_FUNCTIONS=_main ^
  -sEXPORTED_RUNTIME_METHODS=FS,callMain ^
  -sINCOMING_MODULE_JS_API=noInitialRun,print,printErr,onAbort,wasmBinary,locateFile ^
  -sALLOW_MEMORY_GROWTH=1 ^
  -sFORCE_FILESYSTEM=1 ^
  -sENVIRONMENT=web,node ^
  -sASSERTIONS=1 ^
  -o "%OUTPUT_DIR%\convert_dict.js"

if errorlevel 1 (
  echo Build failed.
  endlocal
  exit /b 1
)

echo Build finished: "%OUTPUT_DIR%\convert_dict.js" and "%OUTPUT_DIR%\convert_dict.wasm"
endlocal
