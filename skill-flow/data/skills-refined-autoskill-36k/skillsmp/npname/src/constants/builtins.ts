export const BUILTIN_MODULES = new Set<string>([
  // Internal HTTP modules
  "_http_agent",
  "_http_client",
  "_http_common",
  "_http_incoming",
  "_http_outgoing",
  "_http_server",

  // Internal stream modules
  "_stream_duplex",
  "_stream_passthrough",
  "_stream_readable",
  "_stream_transform",
  "_stream_wrap",
  "_stream_writable",

  // Internal TLS modules
  "_tls_common",
  "_tls_wrap",

  // Assert
  "assert",
  "assert/strict",

  // Async and events
  "async_hooks",
  "events",

  // Buffer and encoding
  "buffer",
  "string_decoder",
  "punycode",

  // Child process and cluster
  "child_process",
  "cluster",
  "worker_threads",

  // Console and debugging
  "console",
  "inspector",
  "inspector/promises",

  // Constants
  "constants",

  // Crypto
  "crypto",

  // Diagnostics and performance
  "diagnostics_channel",
  "perf_hooks",
  "trace_events",

  // DNS
  "dns",
  "dns/promises",

  // Domain (deprecated)
  "domain",

  // File system
  "fs",
  "fs/promises",

  // HTTP and networking
  "dgram",
  "http",
  "http2",
  "https",
  "net",
  "tls",

  // Module system
  "module",

  // OS and system
  "os",
  "process",
  "sys",
  "v8",
  "vm",

  // Path
  "path",
  "path/posix",
  "path/win32",

  // Query and URL
  "querystring",
  "url",

  // Readline
  "readline",
  "readline/promises",

  // REPL
  "repl",

  // Stream
  "stream",
  "stream/consumers",
  "stream/promises",
  "stream/web",

  // Timers
  "timers",
  "timers/promises",

  // TTY
  "tty",

  // Util
  "util",
  "util/types",

  // WASI
  "wasi",

  // Zlib
  "zlib",

  // Node: prefixed modules
  "node:sea",
  "node:sqlite",
  "node:test",
  "node:test/reporters",
]);
