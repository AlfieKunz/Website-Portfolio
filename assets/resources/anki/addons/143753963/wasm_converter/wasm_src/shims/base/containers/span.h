// Minimal replacement of Chromium's base::span for the convert_dict WASM build.
#ifndef CONVERT_DICT_WASM_SHIMS_BASE_CONTAINERS_SPAN_H_
#define CONVERT_DICT_WASM_SHIMS_BASE_CONTAINERS_SPAN_H_

#include <stddef.h>
#include <stdint.h>

#include <cstring>
#include <type_traits>
#include <utility>

namespace base {

inline constexpr size_t dynamic_extent = static_cast<size_t>(-1);

// MARK:span
template <typename T>
class span {
 public:
  using element_type = T;
  using value_type = std::remove_cv_t<T>;
  using size_type = size_t;

  constexpr span() : data_(nullptr), size_(0) {}
  constexpr span(T* data, size_type size) : data_(data), size_(size) {}

  // MARK:array constructor
  template <size_t N>
  constexpr span(T (&array)[N]) : data_(array), size_(N) {}

  constexpr T* data() const { return data_; }
  constexpr size_type size() const { return size_; }
  constexpr bool empty() const { return size_ == 0; }

  constexpr T& operator[](size_type index) const { return data_[index]; }
  constexpr T& front() const { return data_[0]; }
  constexpr T& back() const { return data_[size_ - 1]; }

  constexpr T* begin() const { return data_; }
  constexpr T* end() const { return data_ + size_; }

  // MARK:first
  constexpr span<T> first(size_type count) const {
    return span<T>(data_, count);
  }

  // MARK:first<Count>
  template <size_t Count>
  constexpr span<T> first() const {
    return span<T>(data_, Count);
  }

  // MARK:last
  constexpr span<T> last(size_type count) const {
    return span<T>(data_ + (size_ - count), count);
  }

  // MARK:last<Count>
  template <size_t Count>
  constexpr span<T> last() const {
    return span<T>(data_ + (size_ - Count), Count);
  }

  // MARK:subspan
  constexpr span<T> subspan(size_type offset, size_type count = dynamic_extent) const {
    size_type remaining_count = count;
    if (count == dynamic_extent) {
      remaining_count = size_ - offset;
    }
    return span<T>(data_ + offset, remaining_count);
  }

  // MARK:subspan<Offset, Count>
  template <size_t Offset, size_t Count = dynamic_extent>
  constexpr span<T> subspan() const {
    if (Count == dynamic_extent) {
      return span<T>(data_ + Offset, size_ - Offset);
    }
    return span<T>(data_ + Offset, Count);
  }

  // MARK:split_at
  template <size_t Offset>
  constexpr std::pair<span<T>, span<T>> split_at() const {
    span<T> first_part(data_, Offset);
    span<T> second_part(data_ + Offset, size_ - Offset);
    return std::pair<span<T>, span<T>>(first_part, second_part);
  }

  // MARK:copy_from
  void copy_from(span<const T> source) const {
    size_t copy_size = size_;
    if (source.size() < copy_size) {
      copy_size = source.size();
    }
    std::memcpy(data_, source.data(), copy_size);
  }

 private:
  T* data_;
  size_type size_;
};

// MARK:as_byte_span
template <typename Container>
inline span<const uint8_t> as_byte_span(const Container& container) {
  return span<const uint8_t>(
      reinterpret_cast<const uint8_t*>(container.data()),
      container.size() * sizeof(typename Container::value_type));
}

// MARK:byte_span_from_ref
template <typename T>
inline span<uint8_t> byte_span_from_ref(T& value) {
  return span<uint8_t>(reinterpret_cast<uint8_t*>(&value), sizeof(T));
}

}  // namespace base

#endif  // CONVERT_DICT_WASM_SHIMS_BASE_CONTAINERS_SPAN_H_
