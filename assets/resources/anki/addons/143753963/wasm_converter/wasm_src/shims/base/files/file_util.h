// Minimal replacement of Chromium's base/files/file_util.h (the OpenFile /
// CloseFile helpers used by convert_dict).
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_FILES_FILE_UTIL_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_FILES_FILE_UTIL_H_

#include <stdio.h>

#include "base/files/file_path.h"

namespace base {

// MARK:OpenFile
inline FILE* OpenFile(const FilePath& path, const char* mode) {
  return fopen(path.value().c_str(), mode);
}

// MARK:CloseFile
inline void CloseFile(FILE* file) {
  if (file != nullptr) {
    fclose(file);
  }
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_FILES_FILE_UTIL_H_
