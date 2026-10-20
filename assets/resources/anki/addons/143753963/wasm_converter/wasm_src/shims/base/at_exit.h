// Minimal replacement of Chromium's base/at_exit.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_AT_EXIT_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_AT_EXIT_H_

namespace base {

// MARK:AtExitManager
class AtExitManager {
 public:
  // MARK:AtExitManager constructor
  AtExitManager() = default;

  AtExitManager(const AtExitManager&) = delete;
  AtExitManager& operator=(const AtExitManager&) = delete;
};

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_AT_EXIT_H_
