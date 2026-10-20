// Minimal replacement of Chromium's base/i18n/icu_string_conversions.h.
//
// ICU is not bundled in the WASM build. The dictionaries handled by the add-on
// are UTF-8 (wooorm/dictionaries is normalized to UTF-8 when generated), so
// only UTF-8, ISO-8859-1, Windows-1252 and ASCII are supported here.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_I18N_ICU_STRING_CONVERSIONS_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_I18N_ICU_STRING_CONVERSIONS_H_

#include <stdint.h>
#include <stdio.h>

#include <string>

namespace base {

namespace OnStringConversionError {

enum Type {
  ABORT,
  SKIP,
  FAIL,
  SUBSTITUTE,
};

}  // namespace OnStringConversionError

// MARK:IsContinuationByte
inline bool IsContinuationByte(uint8_t byte) {
  return (byte & 0xC0) == 0x80;
}

// MARK:Utf8ToUtf16
inline bool Utf8ToUtf16(const std::string& input,
                        OnStringConversionError::Type error_handling,
                        std::u16string* output) {
  size_t index = 0;
  while (index < input.size()) {
    uint8_t first_byte = static_cast<uint8_t>(input[index]);
    uint32_t code_point = 0;
    size_t sequence_length = 0;
    if (first_byte < 0x80) {
      code_point = first_byte;
      sequence_length = 1;
    } else if ((first_byte & 0xE0) == 0xC0) {
      code_point = first_byte & 0x1F;
      sequence_length = 2;
    } else if ((first_byte & 0xF0) == 0xE0) {
      code_point = first_byte & 0x0F;
      sequence_length = 3;
    } else if ((first_byte & 0xF8) == 0xF0) {
      code_point = first_byte & 0x07;
      sequence_length = 4;
    } else {
      if (error_handling == OnStringConversionError::FAIL) {
        return false;
      }
      output->push_back(0xFFFD);
      index++;
      continue;
    }

    bool invalid_sequence = sequence_length > input.size() - index;
    if (!invalid_sequence) {
      for (size_t offset = 1; offset < sequence_length; offset++) {
        uint8_t next_byte = static_cast<uint8_t>(input[index + offset]);
        if (!IsContinuationByte(next_byte)) {
          invalid_sequence = true;
          break;
        }
        code_point = (code_point << 6) | (next_byte & 0x3F);
      }
    }

    if (invalid_sequence) {
      if (error_handling == OnStringConversionError::FAIL) {
        return false;
      }
      output->push_back(0xFFFD);
      index++;
      continue;
    }

    index += sequence_length;
    if (code_point < 0x10000) {
      output->push_back(static_cast<char16_t>(code_point));
    } else {
      uint32_t code_point_offset = code_point - 0x10000;
      output->push_back(static_cast<char16_t>(0xD800 + (code_point_offset >> 10)));
      output->push_back(static_cast<char16_t>(0xDC00 + (code_point_offset & 0x3FF)));
    }
  }
  return true;
}

// MARK:Windows1252CodePoint
inline char16_t Windows1252CodePoint(uint8_t byte) {
  static const uint16_t table[32] = {
      0x20AC, 0x0081, 0x201A, 0x0192, 0x201E, 0x2026, 0x2020, 0x2021,
      0x02C6, 0x2030, 0x0160, 0x2039, 0x0152, 0x008D, 0x017D, 0x008F,
      0x0090, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014,
      0x02DC, 0x2122, 0x0161, 0x203A, 0x0153, 0x009D, 0x017E, 0x0178};
  if (byte >= 0x80 && byte <= 0x9F) {
    return static_cast<char16_t>(table[byte - 0x80]);
  }
  return static_cast<char16_t>(byte);
}

// MARK:SingleByteToUtf16
inline void SingleByteToUtf16(const std::string& input,
                              bool windows_1252,
                              std::u16string* output) {
  for (size_t index = 0; index < input.size(); index++) {
    uint8_t byte = static_cast<uint8_t>(input[index]);
    if (windows_1252) {
      output->push_back(Windows1252CodePoint(byte));
    } else {
      output->push_back(static_cast<char16_t>(byte));
    }
  }
}

// MARK:NormalizeCodepageName
inline std::string NormalizeCodepageName(const char* codepage) {
  std::string normalized;
  if (codepage == nullptr) {
    return normalized;
  }
  for (const char* character = codepage; *character != '\0'; character++) {
    char upper = *character;
    if (upper >= 'a' && upper <= 'z') {
      upper = static_cast<char>(upper - ('a' - 'A'));
    }
    if (upper == '-' || upper == '_') {
      continue;
    }
    normalized.push_back(upper);
  }
  return normalized;
}

// MARK:CodepageToUTF16
inline bool CodepageToUTF16(const std::string& input,
                            const char* codepage,
                            OnStringConversionError::Type error_handling,
                            std::u16string* output) {
  output->clear();
  std::string normalized = NormalizeCodepageName(codepage);
  if (normalized == "UTF8") {
    return Utf8ToUtf16(input, error_handling, output);
  }
  if (normalized == "ISO88591" || normalized == "LATIN1") {
    SingleByteToUtf16(input, false, output);
    return true;
  }
  if (normalized == "WINDOWS1252" || normalized == "CP1252") {
    SingleByteToUtf16(input, true, output);
    return true;
  }
  if (normalized == "ASCII" || normalized == "USASCII") {
    for (size_t index = 0; index < input.size(); index++) {
      uint8_t byte = static_cast<uint8_t>(input[index]);
      char16_t code_point = static_cast<char16_t>(byte);
      if (byte >= 0x80) {
        code_point = 0xFFFD;
      }
      output->push_back(code_point);
    }
    return true;
  }
  fprintf(stderr, "CodepageToUTF16: unsupported encoding: %s\n", codepage);
  return false;
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_I18N_ICU_STRING_CONVERSIONS_H_
