#include <cstdlib>
#include <cstring>
#include <iostream>
#include <sanitizer/asan_interface.h>
#include <sys/mman.h>
#include <thread>
#include <unistd.h>
#include <vector>

int main() {
  const size_t page_size = sysconf(_SC_PAGE_SIZE);
  if (page_size == static_cast<size_t>(-1)) {
    std::cerr << "sysconf(_SC_PAGE_SIZE) returned -1";
    return EXIT_FAILURE;
  }

  const size_t size = page_size * 1024;

  void *ptr = mmap(nullptr, size, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (ptr == MAP_FAILED) {
    std::cerr << "mmap() failed with errno = " << errno;
    return EXIT_FAILURE;
  }

  ASAN_POISON_MEMORY_REGION(ptr, size);

  ASAN_UNPOISON_MEMORY_REGION(ptr, size);

  if (munmap(ptr, size) == -1) {
    std::cerr << "munmap() failed with errno = " << errno;
    return EXIT_FAILURE;
  }

  std::vector<std::thread> threads;

  for (int i = 0; i < 100; i++) {
    threads.emplace_back([]() { errno = 0; });
  }

  for (auto &t : threads)
    t.join();

  return EXIT_SUCCESS;
}
