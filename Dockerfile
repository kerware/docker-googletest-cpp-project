# Image de build et de test C++/GoogleTest.
# Compatible Docker Desktop Windows avec backend WSL2.
FROM ubuntu:24.04 AS cpp-test-env

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ninja-build \
        git \
        ca-certificates \
        libgtest-dev \
        libgmock-dev \
        lcov \
        gcovr \
        cppcheck \
        clang-tidy \
        valgrind \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . /workspace

RUN cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug \
    && cmake --build build --parallel \
    && ctest --test-dir build --output-on-failure

CMD ["ctest", "--test-dir", "build", "--output-on-failure"]
