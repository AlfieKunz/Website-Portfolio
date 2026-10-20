// Minimal replacement of Chromium's base/process/memory.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_PROCESS_MEMORY_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_PROCESS_MEMORY_H_

namespace base {

// MARK:EnableTerminationOnHeapCorruption
inline void EnableTerminationOnHeapCorruption() {}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_PROCESS_MEMORY_H_
