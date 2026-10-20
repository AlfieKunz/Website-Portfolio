// Minimal replacement of Chromium's base/files/file_path.h for POSIX.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_FILES_FILE_PATH_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_FILES_FILE_PATH_H_

#include <stddef.h>

#include <string>
#include <string_view>

#define FILE_PATH_LITERAL(x) x
#define PRFilePath "s"

namespace base {

// MARK:FilePath
class FilePath {
 public:
  // MARK:FilePath constructors
  FilePath() = default;
  FilePath(const char* path) : path_(path) {}
  FilePath(const std::string& path) : path_(path) {}
  FilePath(std::string_view path) : path_(path) {}

  // MARK:empty
  bool empty() const { return path_.empty(); }

  // MARK:value
  const std::string& value() const { return path_; }

  // MARK:ReplaceExtension
  FilePath ReplaceExtension(std::string_view new_extension) const {
    size_t slash_index = path_.find_last_of('/');
    size_t dot_index = path_.rfind('.');
    bool dot_is_inside_name = false;
    if (dot_index != std::string::npos) {
      if (slash_index == std::string::npos) {
        dot_is_inside_name = dot_index > 0;
      } else {
        dot_is_inside_name = dot_index > slash_index + 1;
      }
    }

    std::string base_name = path_;
    if (dot_is_inside_name) {
      base_name = path_.substr(0, dot_index);
    }

    std::string extension(new_extension);
    if (!extension.empty() && extension[0] != '.') {
      extension = "." + extension;
    }
    return FilePath(base_name + extension);
  }

 private:
  std::string path_;
};

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_FILES_FILE_PATH_H_
