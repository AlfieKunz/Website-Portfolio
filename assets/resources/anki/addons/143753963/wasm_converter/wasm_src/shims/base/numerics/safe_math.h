// Minimal replacement of Chromium's base/numerics/safe_math.h (only the
// CheckedNumeric operations used by bdict.cc).
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_NUMERICS_SAFE_MATH_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_NUMERICS_SAFE_MATH_H_

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

namespace base {

// MARK:CheckedNumeric
template <typename T>
class CheckedNumeric {
 public:
  // MARK:CheckedNumeric constructor
  template <typename U>
  CheckedNumeric(U value) : value_(static_cast<T>(value)), valid_(true) {}

  // MARK:operator+=
  template <typename U>
  CheckedNumeric& operator+=(U value) {
    T converted_value = static_cast<T>(value);
    T result = 0;
    if (__builtin_add_overflow(value_, converted_value, &result)) {
      valid_ = false;
    } else {
      value_ = result;
    }
    return *this;
  }

  // MARK:IsValid
  bool IsValid() const { return valid_; }

  // MARK:ValueOrDie
  T ValueOrDie() const {
    if (!valid_) {
      fprintf(stderr, "CheckedNumeric: the value is out of range\n");
      fflush(stderr);
      abort();
    }
    return value_;
  }

 private:
  T value_;
  bool valid_;
};

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_NUMERICS_SAFE_MATH_H_
