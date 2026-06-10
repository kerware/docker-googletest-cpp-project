#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports/clang-tidy
docker compose run --rm clang-tidy
