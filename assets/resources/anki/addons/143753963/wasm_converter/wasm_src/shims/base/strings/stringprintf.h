// Minimal replacement of Chromium's base/strings/stringprintf.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRINGPRINTF_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRINGPRINTF_H_

#include <stdarg.h>
#include <stdio.h>

#include <string>

namespace base {

// MARK:StringPrintf
inline std::string StringPrintf(const char* format, ...) {
  va_list arguments;
  va_start(arguments, format);

  char stack_buffer[1024];
  va_list copied_arguments;
  va_copy(copied_arguments, arguments);
  int length = vsnprintf(stack_buffer, sizeof(stack_buffer), format, copied_arguments);
  va_end(copied_arguments);

  if (length < 0) {
    va_end(arguments);
    return std::string();
  }

  std::string result;
  if (static_cast<size_t>(length) < sizeof(stack_buffer)) {
    result.assign(stack_buffer, static_cast<size_t>(length));
  } else {
    result.resize(static_cast<size_t>(length));
    vsnprintf(&result[0], static_cast<size_t>(length) + 1, format, arguments);
  }
  va_end(arguments);
  return result;
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRINGPRINTF_H_
