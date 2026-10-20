// Minimal replacement of Chromium's base/strings/string_util.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_UTIL_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_UTIL_H_

#include <stddef.h>

#include <string>
#include <string_view>

namespace base {

enum TrimPositions {
  TRIM_NONE = 0,
  TRIM_LEADING = 1 << 0,
  TRIM_TRAILING = 1 << 1,
  TRIM_ALL = TRIM_LEADING | TRIM_TRAILING,
};

// MARK:IsAsciiWhitespace
inline bool IsAsciiWhitespace(char character) {
  if (character == ' ') {
    return true;
  }
  if (character == '\t') {
    return true;
  }
  if (character == '\n') {
    return true;
  }
  if (character == '\r') {
    return true;
  }
  if (character == '\f') {
    return true;
  }
  if (character == '\v') {
    return true;
  }
  return false;
}

// MARK:TrimWhitespaceASCII
inline bool TrimWhitespaceASCII(std::string_view input,
                                TrimPositions positions,
                                std::string* output) {
  size_t begin_index = 0;
  size_t end_index = input.size();
  if (positions & TRIM_LEADING) {
    while (begin_index < end_index && IsAsciiWhitespace(input[begin_index])) {
      begin_index++;
    }
  }
  if (positions & TRIM_TRAILING) {
    while (end_index > begin_index && IsAsciiWhitespace(input[end_index - 1])) {
      end_index--;
    }
  }
  // The copy avoids aliasing between the input view and the output string.
  std::string trimmed(input.substr(begin_index, end_index - begin_index));
  output->swap(trimmed);
  return true;
}

// MARK:ReplaceSubstringsAfterOffset
inline void ReplaceSubstringsAfterOffset(std::string* str,
                                         size_t start_offset,
                                         std::string_view find,
                                         std::string_view replace) {
  if (find.empty()) {
    return;
  }
  size_t position = str->find(find, start_offset);
  while (position != std::string::npos) {
    str->replace(position, find.size(), replace);
    position = str->find(find, position + replace.size());
  }
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_UTIL_H_
