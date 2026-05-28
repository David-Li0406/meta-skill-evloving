### Toolboxes

Toolboxes allow you to extend Amp with simple scripts instead of needing to provide an MCP server.

When Amp starts it invokes each executable in the directory indicated by `AMP_TOOLBOX`, with the environment variable `TOOLBOX_ACTION` set to `describe`.

The tool is expected to write its description to `stdout` as a list of key-value pairs, one per line.

```
#!/usr/bin/env bun

const action = process.env.TOOLBOX_ACTION

if (action === 'describe') showDescription()
else if (action === 'execute') runTests()

function showDescription() {
	process.stdout.write(
		[
			'name: run-tests',
			'description: use this tool instead of Bash to run tests in a workspace',
			'dir: string the workspace directory',
		].join('\n'),
	)
}
```

When Amp decides to use your tool it runs the executable again, setting `TOOLBOX_ACTION` to `execute`.

The tool receives parameters in the same format on `stdin` and then performs its work:

```
function runTests() {
	let dir = require('fs')
		.readFileSync(0, 'utf-8')
		.split('\n')
		.filter((line) => line.startsWith('dir: '))

	dir = dir.length > 0 ? dir[0].replace('dir: ', '') : '.'

	require('child_process').spawnSync('pnpm', ['-C', dir, 'run', 'test', '--no-color', '--run'], {
		stdio: 'inherit',
	})
}
```

If your tool needs object or array parameters, the executable can write its [tool schema](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool) as JSON instead to `stdout`. In this case it’ll also receive inputs as JSON.

We recommend using tools to express specific, deterministic and project-local behavior, like:

- querying a development database,
- running test and build actions in the project,
- exposing CLIs tools in a controlled manner.

See [appendix.md](appendix.md) for the full technical reference.
