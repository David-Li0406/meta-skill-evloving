# File Uploads with Remote Functions

## Form-based (`form()`)

### Single File

```ts
// data.remote.ts
import { form } from "$app/server";
import * as v from "valibot";
import { writeFile } from "fs/promises";
import { extname } from "path";

export const uploadAvatar = form(
  v.object({
    username: v.pipe(v.string(), v.nonEmpty()),
    avatar: v.pipe(
      v.file("画像を選択してください"),
      v.mimeType(
        ["image/jpeg", "image/png", "image/webp"],
        "JPEG/PNG/WebPのみ",
      ),
      v.maxSize(1024 * 1024 * 10, "10MB以下"),
    ),
  }),
  async ({ username, avatar }) => {
    const filename = `uploads/${crypto.randomUUID()}${extname(avatar.name)}`;
    await writeFile(filename, Buffer.from(await avatar.arrayBuffer()));
    return { success: true, path: filename };
  },
);
```

```svelte
<!-- +page.svelte -->
<form {...uploadAvatar} enctype="multipart/form-data">
  <input {...uploadAvatar.fields.username.as('text')} />
  <input {...uploadAvatar.fields.avatar.as('file')} />

  {#each uploadAvatar.fields.avatar.issues() as issue}
    <p class="error">{issue.message}</p>
  {/each}

  <button>Upload</button>
</form>
```

### Multiple Files

```ts
export const uploadGallery = form(
  v.object({
    images: v.pipe(
      v.array(v.file()),
      v.minLength(1, "最低1枚"),
      v.maxLength(10, "最大10枚"),
    ),
  }),
  async ({ images }) => {
    const paths = await Promise.all(
      images.map(async (img) => {
        const path = `gallery/${crypto.randomUUID()}${extname(img.name)}`;
        await writeFile(path, Buffer.from(await img.arrayBuffer()));
        return path;
      }),
    );
    return { paths };
  },
);
```

```svelte
<input {...uploadGallery.fields.images.as('file')} multiple />
```

### Custom Enhancement (Progress/Reset)

```svelte
<script>
  import { uploadAvatar } from './data.remote';
  let isUploading = $state(false);
</script>

<form {...uploadAvatar.enhance(async ({ form, submit }) => {
  isUploading = true;
  try {
    await submit();
    form.reset();
  } finally {
    isUploading = false;
  }
})} enctype="multipart/form-data">
  <input {...uploadAvatar.fields.avatar.as('file')} />
  <button disabled={isUploading}>
    {isUploading ? 'Uploading...' : 'Upload'}
  </button>
</form>
```

### Preflight Validation (Client-side)

```svelte
<script>
  import * as v from 'valibot';
  const preflight = v.object({
    avatar: v.pipe(v.file(), v.maxSize(1024 * 1024 * 5, '5MB以下'))
  });
</script>

<form {...uploadAvatar.preflight(preflight)} enctype="multipart/form-data">
```

## Programmatic Uploads (D&D, Paste)

`command()` uses devalue serialization which does NOT support File/Blob natively.
For programmatic uploads, use `form()` with hidden form + `.enhance()`:

```ts
// data.remote.ts
export const uploadFile = form(
  v.object({
    file: v.pipe(v.file(), v.maxSize(1024 * 1024 * 10)),
  }),
  async ({ file }) => {
    const path = `uploads/${crypto.randomUUID()}${extname(file.name)}`;
    await writeFile(path, Buffer.from(await file.arrayBuffer()));
    return { path };
  },
);
```

```svelte
<script>
  import { uploadFile } from './data.remote';

  let fileInput: HTMLInputElement;
  let formEl: HTMLFormElement;

  function handleFileSelect() {
    if (fileInput.files?.length) {
      formEl.requestSubmit(); // programmatically submit
    }
  }
</script>

<!-- Hidden form for programmatic submission -->
<form
  bind:this={formEl}
  {...uploadFile.enhance(async ({ form, submit }) => {
    const result = await submit();
    console.log('Uploaded:', result);
    form.reset();
  })}
  enctype="multipart/form-data"
  style="display: contents;"
>
  <input
    {...uploadFile.fields.file.as('file')}
    bind:this={fileInput}
    onchange={handleFileSelect}
  />
</form>
```

### Drag & Drop

```svelte
<script>
  import { uploadFile } from './data.remote';

  let isDragging = $state(false);
  let fileInput: HTMLInputElement;
  let formEl: HTMLFormElement;

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    isDragging = false;

    const dt = new DataTransfer();
    for (const file of e.dataTransfer?.files || []) {
      dt.items.add(file);
    }
    fileInput.files = dt.files;
    formEl.requestSubmit();
  }
</script>

<form
  bind:this={formEl}
  {...uploadFile.enhance(async ({ submit }) => await submit())}
  enctype="multipart/form-data"
  hidden
>
  <input {...uploadFile.fields.file.as('file')} bind:this={fileInput} />
</form>

<div
  class:dragging={isDragging}
  ondrop={handleDrop}
  ondragover={(e) => { e.preventDefault(); isDragging = true; }}
  ondragleave={() => isDragging = false}
>
  Drop files here
</div>
```

## Valibot File Schema Reference

| Validator           | Example                                   |
| ------------------- | ----------------------------------------- |
| `v.file()`          | `v.file('Required')`                      |
| `v.blob()`          | `v.blob('Invalid blob')`                  |
| `v.mimeType()`      | `v.mimeType(['image/png', 'image/jpeg'])` |
| `v.maxSize()`       | `v.maxSize(1024 * 1024 * 5)` (5MB)        |
| `v.array(v.file())` | Multiple files                            |

## Best Practices

1. **Always validate MIME type** - Don't trust file extensions
2. **Set size limits** - Prevent DoS attacks
3. **Use preflight()** - Instant client feedback
4. **Store outside web root** - Security
5. **Use enhance()** - For loading states and form reset
