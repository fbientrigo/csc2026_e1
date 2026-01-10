# TT-E1 Debugging with Sanitizers

Goal: use sanitizers to turn “mysterious crashes” into actionable diagnostics, then fix the root cause.

## Success criteria

- `analyze` runs with **no ASan/UBSan findings**
- `ctest` passes in the sanitizer build directory
- At least one regression test exists for the bug you fixed

## Build + run (starter)

```bash
cd exercises/TT-E1-debugging-sanitizers/starter

rm -rf build-asan
CC=clang CXX=clang++ cmake -B build-asan -G Ninja -DCMAKE_BUILD_TYPE=Debug -DENABLE_SANITIZERS=ON
cmake --build build-asan -j"$(nproc)"

./build-asan/analyze

## Optional
ctest --test-dir build-asan --output-on-failure
```


## Stretch
* Make ThreadSanitizer clean (if applicable)
* Add a second test to cover an edge case
