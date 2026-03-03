# Quality Gates

Apply in this order when relevant to repository stack:

1. Formatting
2. Lint
3. Type check
4. Unit tests
5. Integration/smoke tests

## Suggested commands by stack

### Node
- `npm run format --if-present`
- `npm run lint --if-present`
- `npm run typecheck --if-present`
- `npm test --if-present`

### Python
- `ruff check .`
- `python3 -m mypy .` (if configured)
- `python3 -m pytest -q`

### Go
- `gofmt -w .` (or verify formatting policy)
- `go test ./...`

### Rust
- `cargo fmt --check`
- `cargo clippy -- -D warnings`
- `cargo test`

If a command is unavailable in current repo, log it and proceed with available checks.
