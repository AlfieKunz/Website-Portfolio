// Minimal replacement of Chromium's base/check.h.
// The checks stay active in the WASM test build.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_CHECK_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_CHECK_H_

#include <stdio.h>
#include <stdlib.h>

namespace shim_check {

// MARK:CheckFailed
inline void CheckFailed(const char* expression, const char* file, int line) {
  fprintf(stderr, "CHECK failed: %s at %s:%d\n", expression, file, line);
  fflush(stderr);
  abort();
}

}  // namespace shim_check

#define CHECK(condition)                     \
  do {                                       \
    if (!(condition)) {                      \
      shim_check::CheckFailed(#condition, __FILE__, __LINE__); \
    }                                        \
  } while (0)

#define DCHECK(condition) CHECK(condition)

#define CHECK_EQ(first, second) CHECK((first) == (second))
#define CHECK_NE(first, second) CHECK((first) != (second))
#define CHECK_LT(first, second) CHECK((first) < (second))
#define CHECK_LE(first, second) CHECK((first) <= (second))
#define CHECK_GT(first, second) CHECK((first) > (second))
#define CHECK_GE(first, second) CHECK((first) >= (second))

#define DCHECK_EQ(first, second) CHECK_EQ(first, second)
#define DCHECK_NE(first, second) CHECK_NE(first, second)
#define DCHECK_LT(first, second) CHECK_LT(first, second)
#define DCHECK_LE(first, second) CHECK_LE(first, second)
#define DCHECK_GT(first, second) CHECK_GT(first, second)
#define DCHECK_GE(first, second) CHECK_GE(first, second)

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_CHECK_H_
