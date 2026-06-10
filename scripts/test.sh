#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports reports/googletest
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build --parallel
ctest --test-dir build --output-on-failure --output-junit "$(pwd)/reports/ctest-junit.xml"
python3 scripts/junit-to-html.py "$(pwd)/reports/ctest-junit.xml" reports/googletest
