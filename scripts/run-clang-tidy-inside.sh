#!/usr/bin/env bash
set -euo pipefail
# Generate thorough clang-tidy output and export fixes
mkdir -p reports/clang-tidy
cmake -S . -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build --parallel || true

# Allow override of checks via env var CLANG_TIDY_CHECKS, default to a comprehensive set
# Default includes: bugprone, modernize, performance, readability, clang-analyzer
DEFAULT_CHECKS="bugprone-*,modernize-*,performance-*,readability-*,clang-analyzer-*"
CHECKS="${CLANG_TIDY_CHECKS:-$DEFAULT_CHECKS}"
echo "Running clang-tidy with checks=${CHECKS}"

files=$(find src include tests -type f \( -name '*.cpp' -o -name '*.cxx' -o -name '*.cc' -o -name '*.h' -o -name '*.hpp' \) -print)
if [ -z "${files}" ]; then
  echo 'No source files found'
else
  # Export fixes to YAML and include headers in the analysis
  clang-tidy -p build -checks="${CHECKS}" -header-filter='.*' -export-fixes=reports/clang-tidy/fixes.yaml ${files} 2>&1 | tee reports/clang-tidy/clang-tidy.txt || true
fi

python3 scripts/clang-tidy-to-html.py reports/clang-tidy/clang-tidy.txt reports/clang-tidy reports/clang-tidy/fixes.yaml || true
