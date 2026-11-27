# Multi-stage static Rust build targeting distroless nonroot (< 15 MB)
FROM rust:1-alpine AS builder
WORKDIR /app
RUN apk add --no-cache musl-dev build-base cmake

COPY Cargo.toml Cargo.lock ./
RUN mkdir -p src && touch src/lib.rs && printf 'fn main() {}\n' > src/main.rs && cargo build --release && rm -rf src

COPY src ./src
RUN touch src/main.rs src/lib.rs && cargo build --release --bin dark-gravity-mcp && ldd /app/target/release/dark-gravity-mcp || true

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/target/release/dark-gravity-mcp /usr/local/bin/dark-gravity-mcp
USER 65532:65532
ENV DARK_GRAVITY_BASE_URL=https://lgcorzo.github.io \
    DARK_GRAVITY_CACHE_DIR=/tmp/dark-gravity-mcp-cache \
    DARK_GRAVITY_MCP_TRANSPORT=streamable-http \
    DARK_GRAVITY_MCP_BIND=0.0.0.0:8080
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/dark-gravity-mcp"]
