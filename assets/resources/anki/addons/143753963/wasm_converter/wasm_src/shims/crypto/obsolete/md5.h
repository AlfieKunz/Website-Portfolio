// Minimal replacement of Chromium's crypto/obsolete/md5.h.
// Backed by the public domain MD5 implementation in md5.cc (RFC 1321).
#ifndef CONVERT_DICT_WASM_SHIMS_CRYPTO_OBSOLETE_MD5_H_
#define CONVERT_DICT_WASM_SHIMS_CRYPTO_OBSOLETE_MD5_H_

#include <stddef.h>
#include <stdint.h>

#include <array>

#include "base/containers/span.h"

namespace crypto {
namespace obsolete {

inline constexpr size_t kMd5Size = 16;

// MARK:Md5
class Md5 {
 public:
  // MARK:Hash
  static std::array<uint8_t, kMd5Size> Hash(base::span<const uint8_t> data);
};

}  // namespace obsolete
}  // namespace crypto

#endif  // CONVERT_DICT_WASM_SHIMS_CRYPTO_OBSOLETE_MD5_H_
