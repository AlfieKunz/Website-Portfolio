// MD5 (RFC 1321) implemented for the convert_dict WASM build because the
// .bdic v2 header requires an MD5 digest and Chromium's MD5 lives in //base.

#include "crypto/obsolete/md5.h"

#include <string.h>

#include <array>

namespace crypto {
namespace obsolete {

namespace {

constexpr uint32_t kInitialState[4] = {0x67452301, 0xEFCDAB89, 0x98BADCFE,
                                       0x10325476};

constexpr uint32_t kShiftAmounts[64] = {
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20, 5, 9,  14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21};

constexpr uint32_t kSineTable[64] = {
    0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF, 0x4787C62A,
    0xA8304613, 0xFD469501, 0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
    0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821, 0xF61E2562, 0xC040B340,
    0x265E5A51, 0xE9B6C7AA, 0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8,
    0x676F02D9, 0x8D2A4C8A, 0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70, 0x289B7EC6, 0xEAA127FA,
    0xD4EF3085, 0x04881D05, 0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92,
    0xFFEFF47D, 0x85845DD1, 0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
    0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391};

// MARK:RotateLeft
inline uint32_t RotateLeft(uint32_t value, uint32_t count) {
  return (value << count) | (value >> (32 - count));
}

// MARK:Md5Transform
void Md5Transform(uint32_t state[4], const uint8_t block[64]) {
  uint32_t words[16];
  for (int index = 0; index < 16; index++) {
    words[index] = static_cast<uint32_t>(block[index * 4]) |
                   (static_cast<uint32_t>(block[index * 4 + 1]) << 8) |
                   (static_cast<uint32_t>(block[index * 4 + 2]) << 16) |
                   (static_cast<uint32_t>(block[index * 4 + 3]) << 24);
  }

  uint32_t a = state[0];
  uint32_t b = state[1];
  uint32_t c = state[2];
  uint32_t d = state[3];

  for (uint32_t index = 0; index < 64; index++) {
    uint32_t mixed = 0;
    uint32_t word_index = 0;
    if (index < 16) {
      mixed = (b & c) | (~b & d);
      word_index = index;
    } else if (index < 32) {
      mixed = (d & b) | (~d & c);
      word_index = (5 * index + 1) % 16;
    } else if (index < 48) {
      mixed = b ^ c ^ d;
      word_index = (3 * index + 5) % 16;
    } else {
      mixed = c ^ (b | ~d);
      word_index = (7 * index) % 16;
    }

    uint32_t rotated = RotateLeft(
        a + mixed + kSineTable[index] + words[word_index], kShiftAmounts[index]);
    a = d;
    d = c;
    c = b;
    b = b + rotated;
  }

  state[0] += a;
  state[1] += b;
  state[2] += c;
  state[3] += d;
}

}  // namespace

// MARK:Md5::Hash
std::array<uint8_t, kMd5Size> Md5::Hash(base::span<const uint8_t> data) {
  uint32_t state[4] = {kInitialState[0], kInitialState[1], kInitialState[2],
                       kInitialState[3]};

  const uint8_t* input = data.data();
  size_t remaining = data.size();
  while (remaining >= 64) {
    Md5Transform(state, input);
    input += 64;
    remaining -= 64;
  }

  uint8_t buffer[128];
  memset(buffer, 0, sizeof(buffer));
  memcpy(buffer, input, remaining);
  buffer[remaining] = 0x80;

  size_t padded_size = 64;
  if (remaining >= 56) {
    padded_size = 128;
  }
  uint64_t total_bit_count = static_cast<uint64_t>(data.size()) * 8;
  for (int index = 0; index < 8; index++) {
    buffer[padded_size - 8 + index] =
        static_cast<uint8_t>((total_bit_count >> (8 * index)) & 0xFF);
  }

  Md5Transform(state, buffer);
  if (padded_size == 128) {
    Md5Transform(state, buffer + 64);
  }

  std::array<uint8_t, kMd5Size> digest;
  for (int index = 0; index < 4; index++) {
    digest[index * 4] = static_cast<uint8_t>(state[index] & 0xFF);
    digest[index * 4 + 1] = static_cast<uint8_t>((state[index] >> 8) & 0xFF);
    digest[index * 4 + 2] = static_cast<uint8_t>((state[index] >> 16) & 0xFF);
    digest[index * 4 + 3] = static_cast<uint8_t>((state[index] >> 24) & 0xFF);
  }
  return digest;
}

}  // namespace obsolete
}  // namespace crypto
