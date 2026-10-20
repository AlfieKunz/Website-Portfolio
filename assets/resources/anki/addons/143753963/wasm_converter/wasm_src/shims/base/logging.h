// Minimal replacement of Chromium's base/logging.h.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_LOGGING_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_LOGGING_H_

#include <stdio.h>
#include <stdlib.h>

#include <sstream>
#include <string>

namespace shim_logging {

enum LogSeverity {
  LOG_INFO = 0,
  LOG_WARNING = 1,
  LOG_ERROR = 2,
  LOG_FATAL = 3,
};

// MARK:LogMessage
class LogMessage {
 public:
  // MARK:LogMessage constructor
  LogMessage(LogSeverity severity, const char* file, int line)
      : severity_(severity), file_(file), line_(line) {}

  // MARK:LogMessage destructor
  ~LogMessage() {
    fprintf(stderr, "%s:%d: %s\n", file_, line_, stream_.str().c_str());
    fflush(stderr);
    if (severity_ == LOG_FATAL) {
      abort();
    }
  }

  // MARK:stream
  std::ostringstream& stream() { return stream_; }

 private:
  LogSeverity severity_;
  const char* file_;
  int line_;
  std::ostringstream stream_;
};

}  // namespace shim_logging

#define LOG(severity) \
  shim_logging::LogMessage(shim_logging::LOG_##severity, __FILE__, __LINE__).stream()

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_LOGGING_H_
