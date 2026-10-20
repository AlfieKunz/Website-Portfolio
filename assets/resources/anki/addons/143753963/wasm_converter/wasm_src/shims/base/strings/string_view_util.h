// Minimal replacement of Chromium's base/strings/string_view_util.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_VIEW_UTIL_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_VIEW_UTIL_H_

#include <stdint.h>

#include <string_view>

#include "base/containers/span.h"

namespace base {

// MARK:as_string_view
inline std::string_view as_string_view(span<const uint8_t> bytes) {
  return std::string_view(reinterpret_cast<const char*>(bytes.data()), bytes.size());
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_STRINGS_STRING_VIEW_UTIL_H_
