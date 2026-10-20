// Minimal replacement of Chromium's base/strings/utf_string_conversions.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_UTF_STRING_CONVERSIONS_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_UTF_STRING_CONVERSIONS_H_

#include <stdint.h>

#include <string>
#include <string_view>

namespace base {

// MARK:UTF16ToUTF8
inline std::string UTF16ToUTF8(std::u16string_view input) {
  std::string output;
  size_t index = 0;
  while (index < input.size()) {
    uint32_t code_point = input[index];
    index++;
    if (code_point >= 0xD800 && code_point <= 0xDBFF && index < input.size()) {
      uint32_t low_surrogate = input[index];
      if (low_surrogate >= 0xDC00 && low_surrogate <= 0xDFFF) {
        code_point = 0x10000 + ((code_point - 0xD800) << 10) + (low_surrogate - 0xDC00);
        index++;
      }
    }

    if (code_point < 0x80) {
      output.push_back(static_cast<char>(code_point));
    } else if (code_point < 0x800) {
      output.push_back(static_cast<char>(0xC0 | (code_point >> 6)));
      output.push_back(static_cast<char>(0x80 | (code_point & 0x3F)));
    } else if (code_point < 0x10000) {
      output.push_back(static_cast<char>(0xE0 | (code_point >> 12)));
      output.push_back(static_cast<char>(0x80 | ((code_point >> 6) & 0x3F)));
      output.push_back(static_cast<char>(0x80 | (code_point & 0x3F)));
    } else {
      output.push_back(static_cast<char>(0xF0 | (code_point >> 18)));
      output.push_back(static_cast<char>(0x80 | ((code_point >> 12) & 0x3F)));
      output.push_back(static_cast<char>(0x80 | ((code_point >> 6) & 0x3F)));
      output.push_back(static_cast<char>(0x80 | (code_point & 0x3F)));
    }
  }
  return output;
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_UTF_STRING_CONVERSIONS_H_
