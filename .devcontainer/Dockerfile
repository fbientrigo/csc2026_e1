# .devcontainer/Dockerfile
# ROOT (CERN) base image. "latest" can change OS under you, so perf install is resilient.
FROM rootproject/root:latest

ENV DEBIAN_FRONTEND=noninteractive

# Base tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        cmake \
        ninja-build \
        g++ \
        gdb \
        valgrind \
        python3 \
        python3-pip && \
    \
    # Clang + sanitizer runtimes.
    # Prefer LLVM 20 when available (Codespaces currently ships clang 20).
    (apt-get install -y --no-install-recommends \
        clang-20 \
        clang-tidy-20 \
        llvm-20 \
        lld-20 \
        compiler-rt-20 \
        libclang-rt-20-dev \
      || apt-get install -y --no-install-recommends \
        clang \
        clang-tidy \
        llvm \
        lld \
        compiler-rt \
        libclang-rt-dev) && \
    \
    # perf package name varies by Ubuntu release and kernel packaging
    # Try the common providers. Do not fail the build if perf cannot be installed.
    (apt-get install -y --no-install-recommends linux-tools-common linux-tools-generic || true) && \
    (apt-get install -y --no-install-recommends linux-perf || true) && \
    \
    rm -rf /var/lib/apt/lists/*

# Python tooling (docs/tests)
RUN python3 -m pip install --break-system-packages \
        pytest \
        pytest-cov \
        mkdocs \
        mkdocs-material

WORKDIR /work
