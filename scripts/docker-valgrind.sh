#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports/valgrind
docker compose run --rm valgrind
