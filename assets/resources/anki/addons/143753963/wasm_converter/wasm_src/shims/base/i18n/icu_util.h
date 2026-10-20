// Minimal replacement of Chromium's base/i18n/icu_util.h.
// The WASM build does not bundle ICU.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_I18N_ICU_UTIL_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_I18N_ICU_UTIL_H_

namespace base {
namespace i18n {

// MARK:InitializeICU
inline void InitializeICU() {}

}  // namespace i18n
}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_I18N_ICU_UTIL_H_
