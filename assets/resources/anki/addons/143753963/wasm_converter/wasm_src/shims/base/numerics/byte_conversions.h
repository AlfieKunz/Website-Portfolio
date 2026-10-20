// Minimal replacement of Chromium's base/numerics/byte_conversions.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_NUMERICS_BYTE_CONVERSIONS_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_NUMERICS_BYTE_CONVERSIONS_H_

#include <stdint.h>

#include "base/containers/span.h"

namespace base {

// MARK:U16FromLittleEndian
inline uint16_t U16FromLittleEndian(span<const uint8_t> bytes) {
  return static_cast<uint16_t>(
      static_cast<uint16_t>(bytes[0]) |
      static_cast<uint16_t>(static_cast<uint16_t>(bytes[1]) << 8));
}

// MARK:U32FromLittleEndian
inline uint32_t U32FromLittleEndian(span<const uint8_t> bytes) {
  return static_cast<uint32_t>(bytes[0]) |
         (static_cast<uint32_t>(bytes[1]) << 8) |
         (static_cast<uint32_t>(bytes[2]) << 16) |
         (static_cast<uint32_t>(bytes[3]) << 24);
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_NUMERICS_BYTE_CONVERSIONS_H_
