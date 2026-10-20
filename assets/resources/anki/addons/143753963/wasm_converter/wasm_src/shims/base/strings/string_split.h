// Minimal replacement of Chromium's base/strings/string_split.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_SPLIT_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_SPLIT_H_

#include <stddef.h>

#include <string>
#include <string_view>
#include <vector>

#include "base/strings/string_util.h"

namespace base {

enum WhitespaceHandling {
  KEEP_WHITESPACE,
  TRIM_WHITESPACE,
};

enum SplitResult {
  SPLIT_WANT_ALL,
  SPLIT_WANT_NONEMPTY,
};

// MARK:TrimAsciiWhitespaceView
inline std::string_view TrimAsciiWhitespaceView(std::string_view input) {
  size_t begin_index = 0;
  size_t end_index = input.size();
  while (begin_index < end_index && IsAsciiWhitespace(input[begin_index])) {
    begin_index++;
  }
  while (end_index > begin_index && IsAsciiWhitespace(input[end_index - 1])) {
    end_index--;
  }
  return input.substr(begin_index, end_index - begin_index);
}

// MARK:SplitString
inline std::vector<std::string> SplitString(std::string_view input,
                                            std::string_view separators,
                                            WhitespaceHandling whitespace,
                                            SplitResult result_type) {
  std::vector<std::string> parts;
  if (input.empty()) {
    return parts;
  }

  size_t start_index = 0;
  while (true) {
    size_t separator_index = input.find_first_of(separators, start_index);
    std::string_view piece;
    if (separator_index == std::string_view::npos) {
      piece = input.substr(start_index);
    } else {
      piece = input.substr(start_index, separator_index - start_index);
    }

    if (whitespace == TRIM_WHITESPACE) {
      piece = TrimAsciiWhitespaceView(piece);
    }
    if (result_type == SPLIT_WANT_ALL || !piece.empty()) {
      parts.emplace_back(piece);
    }

    if (separator_index == std::string_view::npos) {
      break;
    }
    start_index = separator_index + 1;
  }
  return parts;
}

// MARK:JoinString
inline std::string JoinString(const std::vector<std::string>& parts,
                              std::string_view separator) {
  std::string joined;
  for (size_t index = 0; index < parts.size(); index++) {
    if (index > 0) {
      joined.append(separator);
    }
    joined.append(parts[index]);
  }
  return joined;
}

// MARK:JoinString views overload
inline std::string JoinString(const std::vector<std::string_view>& parts,
                              std::string_view separator) {
  std::string joined;
  for (size_t index = 0; index < parts.size(); index++) {
    if (index > 0) {
      joined.append(separator);
    }
    joined.append(parts[index]);
  }
  return joined;
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_SPLIT_H_
