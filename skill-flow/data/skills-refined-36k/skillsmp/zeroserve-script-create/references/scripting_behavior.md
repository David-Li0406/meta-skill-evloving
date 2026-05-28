# Zeroserve script behavior

## Execution model
- Scripts are eBPF programs stored under `.zeroserve/scripts/*.o` in the site tarball.
- Zeroserve loads scripts in sorted path order and runs them for every request.
- A per-request metadata map is shared across scripts in the chain.
- If a script calls `zs_respond`, its response is used and later scripts are skipped.
- If a script calls `zs_reverse_proxy`, the request is proxied and later scripts are skipped.
- Script failures are logged but do not abort the chain.

## Packaging and compilation
- `zeroserve --pack` compiles any `.c` files in `.zeroserve/scripts/` into `.o` files.
- The resulting `.o` is included in the tarball and the `.c` is omitted.
- Manual compile (if needed):
  - `clang -O2 -target bpf -emit-llvm -c input.c -o tmp.bc`
  - `llc -march=bpf -bpf-stack-size=4096 -mcpu=v3 -filetype=obj tmp.bc -o out.o`

## Request and response notes
- Request mutations (URI and headers) are visible to later scripts and reverse proxy backends.
- `zs_meta_set` keys prefixed with `zs.response.header.` apply to all responses
  (static files, `zs_respond`, and reverse proxy).

## Safety and performance
- Avoid long or unbounded loops; scripts are expected to be fast.
- Keep stack usage small (BPF stack is limited; 4096 bytes is typical).
