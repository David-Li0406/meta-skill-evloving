# Line length and shell transcripts

Keep prose readable and avoid noisy command examples.

## MD013 - Line length

Keep lines within the configured length limit.
Wrap prose at natural breakpoints.

Bad:

```markdown
This is a very long line that is hard to read because it keeps going without
wrapping at a reasonable length.
```

Good:

```markdown
This is a long line that is easier to read when wrapped at a reasonable
length.
```

## MD014 - Dollar signs used before commands without showing output

Avoid prefixing commands with `$` unless you also show output.

Bad:

````markdown
```sh
$ npm test
$ npm run build
```
````

Good:

````markdown
```sh
npm test
npm run build
```
````

Good (prompt plus output):

````markdown
```sh
$ echo "ok"
ok
```
````
