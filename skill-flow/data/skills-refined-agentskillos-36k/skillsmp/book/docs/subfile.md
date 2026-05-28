How to refer to tex files in subfolders with local paths

If you mean **including one `.tex` file from another** (most common), LaTeX paths are *relative to the “main” file you compile* (the root/master document), not relative to the file that contains the `\input`.

### Basic: `\input` / `\include`

From `main.tex`:

<pre class="overflow-visible! px-0!" data-start="261" data-end="376"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>% main.tex</span><span>
</span><span>\input</span><span>{sections/intro}        </span><span>% no .tex needed</span><span>
</span><span>\input</span><span>{subfolder/more/stuff}  </span><span>% works the same</span><span>
</span></span></code></div></div></pre>

Notes:

* Forward slashes `/` work on all OSes (use them even on Windows).
* `\include{...}` is similar but page-breaks and works best for chapter-like chunks.

### Prefer a single “source root” with `\subfile`-style structure

If you want each section file to be compilable on its own (optional), use `subfiles`:

<pre class="overflow-visible! px-0!" data-start="691" data-end="763"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>% main.tex</span><span>
</span><span>\usepackage</span><span>{subfiles}
</span><span>\subfile</span><span>{sections/intro.tex}
</span></span></code></div></div></pre>

Then in `sections/intro.tex`:

<pre class="overflow-visible! px-0!" data-start="796" data-end="880"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}
</span><span>\begin</span><span>{document}
...
</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

### Set search paths so you don’t repeat folder prefixes

Use `\graphicspath` for images and `\input@path` for TeX inputs.

**Images:**

<pre class="overflow-visible! px-0!" data-start="1017" data-end="1098"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\usepackage</span><span>{graphicx}
</span><span>\graphicspath</span><span>{{figures/}{figures/ch1/}{assets/}}
</span></span></code></div></div></pre>

**TeX inputs (requires `\makeatletter`):**

<pre class="overflow-visible! px-0!" data-start="1143" data-end="1273"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\makeatletter</span><span>
</span><span>\def</span><span>\input@path</span><span>{{sections/}{appendices/}{tex/}}
</span><span>\makeatother</span><span>

</span><span>\input</span><span>{intro}   </span><span>% will search those folders</span><span>
</span></span></code></div></div></pre>

### If you mean “local file links” (PDF hyperlinks)

For linking to local files (not always portable and PDF viewers may restrict this):

<pre class="overflow-visible! px-0!" data-start="1412" data-end="1494"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\usepackage</span><span>{hyperref}
</span><span>\href</span><span>{</span><span>run:./docs/appendix.pdf</span><span>}{Open appendix PDF}
</span></span></code></div></div></pre>

---

If you tell me whether you mean  **(A) `\input/\include`** ,  **(B) images/bib** , or  **(C) clickable local file links** , I can give the cleanest setup for your folder layout.

How does the subfiles work?

`subfiles` lets you write each chapter/section as a **standalone mini-document** *and* also include it in a  **main document** —using the  **same source file** .

## The core idea

* You have a **root** file: `main.tex` (the one that defines class, packages, macros, layout).
* Each subfile (e.g. `sections/intro.tex`) declares:

  <pre class="overflow-visible! px-0!" data-start="326" data-end="378"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}
  </span></span></code></div></div></pre>

  That means:

  * If you compile `sections/intro.tex` directly, it *loads* `../main.tex` as the preamble.
  * If you compile `main.tex`, then `\subfile{sections/intro.tex}` *inserts the content* without duplicating the whole preamble.

So you get:

* Fast compile of a single chapter while writing.
* One consistent preamble for the whole thesis/report.

## Minimal working structure

**Folder**

<pre class="overflow-visible! px-0!" data-start="774" data-end="842"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>project/
  </span><span>main</span><span>.tex</span><span>
  sections/
    intro</span><span>.tex</span><span>
    method</span><span>.tex</span><span>
</span></span></code></div></div></pre>

### `main.tex`

<pre class="overflow-visible! px-0!" data-start="859" data-end="1057"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>{article}

</span><span>\usepackage</span><span>{subfiles}
</span><span>\usepackage</span><span>{lipsum} </span><span>% demo text</span><span>

</span><span>\begin</span><span>{document}

</span><span>\section</span><span>{Main}
</span><span>\subfile</span><span>{sections/intro.tex}
</span><span>\subfile</span><span>{sections/method.tex}

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

### `sections/intro.tex`

<pre class="overflow-visible! px-0!" data-start="1084" data-end="1203"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}

</span><span>\begin</span><span>{document}

</span><span>\section</span><span>{Introduction}
</span><span>\lipsum</span><span>[1-2]

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

### `sections/method.tex`

<pre class="overflow-visible! px-0!" data-start="1231" data-end="1344"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}

</span><span>\begin</span><span>{document}

</span><span>\section</span><span>{Method}
</span><span>\lipsum</span><span>[3-4]

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

## What `\subfile{...}` does (vs `\input`)

* `\input{...}`: just pastes the file contents into the main file.
* `\subfile{...}`: behaves like `\input` when included **but** also supports the file being compiled on its own (because the subfile has its own `\documentclass` + `\begin{document}` wrapper).

## Images, paths, and relative locations

A common “gotcha” is graphics paths when compiling subfiles.

### Best practice

Define all paths in `main.tex`:

<pre class="overflow-visible! px-0!" data-start="1803" data-end="1880"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\usepackage</span><span>{graphicx}
</span><span>\graphicspath</span><span>{{figures/}{sections/figures/}}
</span></span></code></div></div></pre>

Then in `sections/intro.tex` you can do:

<pre class="overflow-visible! px-0!" data-start="1923" data-end="1976"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\includegraphics</span><span>[width=</span><span>\linewidth</span><span>]{myplot}
</span></span></code></div></div></pre>

Because when compiling the subfile, it still loads the main preamble (including `\graphicspath`).

If you want paths that depend on “where the subfile lives”, `subfiles` also provides `\subfix{...}` which helps adjust relative paths in subfiles.

Example:

<pre class="overflow-visible! px-0!" data-start="2234" data-end="2286"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\includegraphics</span><span>{</span><span>\subfix</span><span>{figures/myplot}}
</span></span></code></div></div></pre>

When compiled from `main.tex`, it resolves normally; when compiled from within `sections/`, it adjusts.

## Cross-references and bibliography

* Labels/refs inside one subfile work normally in the full build.
* When compiling a single subfile, references to labels in *other* subfiles may show as `??` unless you compile the main doc occasionally (or use your editor’s build tools to run LaTeX enough times).
* Bibliography: usually keep the `\bibliography{...}` / `\addbibresource{...}` in `main.tex`. Subfiles will inherit it when compiled standalone (since they load main).

## When to use `subfiles`

Use it if you want:

* compile-per-chapter workflow,
* consistent preamble,
* clean modular structure.

If you *never* compile individual chapters, `\input` is simpler.

If you tell me your folder layout (where `main.tex`, chapter files, and figures live), I can show the cleanest `subfiles` setup + path handling for that exact structure.

how does it work with one more layer, that is if intro.tex refers to subsection1.tex etc?

It works fine — just remember  **everything is still “rooted” in the document you compile** .

With `subfiles`, there are two common patterns for a second layer (intro → subsection files). The cleanest is:

## Pattern A (recommended): Only the top-level chapter is a subfile; deeper layers use `\input`

**Structure**

<pre class="overflow-visible! px-0!" data-start="315" data-end="402"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>main</span><span>.tex</span><span>
sections/
  intro</span><span>.tex</span><span>
  intro/
    subsection1</span><span>.tex</span><span>
    subsection2</span><span>.tex</span><span>
</span></span></code></div></div></pre>

**main.tex**

<pre class="overflow-visible! px-0!" data-start="417" data-end="536"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>{article}
</span><span>\usepackage</span><span>{subfiles}
</span><span>\begin</span><span>{document}

</span><span>\subfile</span><span>{sections/intro.tex}

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

**sections/intro.tex**

<pre class="overflow-visible! px-0!" data-start="561" data-end="803"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}
</span><span>\begin</span><span>{document}

</span><span>\section</span><span>{Introduction}

</span><span>% include “child” files</span><span>
</span><span>\input</span><span>{intro/subsection1}   </span><span>% relative to sections/intro.tex when compiled as subfile</span><span>
</span><span>\input</span><span>{intro/subsection2}

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

**sections/intro/subsection1.tex**

<pre class="overflow-visible! px-0!" data-start="840" data-end="884"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\subsection</span><span>{Subsection 1}
Text...
</span></span></code></div></div></pre>

Why this is nice:

* You can compile `main.tex` (full doc) ✅
* You can compile `sections/intro.tex` alone ✅
* You don’t need `subfiles` for the leaf files; they’re just content chunks.

### One important gotcha

` \input{intro/subsection1}` inside `sections/intro.tex` is resolved **relative to the directory of the file being read** in most modern TeX setups (because `subfiles`/engines typically set the “current directory” appropriately), but some editors/build setups can behave differently.

If you ever see “file not found” depending on whether you compile `main.tex` or `intro.tex`, use Pattern B below.

---

## Pattern B (robust): Use `\subfile` at every level + `\subfix` for paths

This makes each level compilable as its own unit.

**Structure**

<pre class="overflow-visible! px-0!" data-start="1641" data-end="1708"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>main</span><span>.tex</span><span>
sections/
  intro</span><span>.tex</span><span>
  intro/
    subsection1</span><span>.tex</span><span>
</span></span></code></div></div></pre>

**main.tex**

<pre class="overflow-visible! px-0!" data-start="1723" data-end="1840"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>{article}
</span><span>\usepackage</span><span>{subfiles}
</span><span>\begin</span><span>{document}
</span><span>\subfile</span><span>{sections/intro.tex}
</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

**sections/intro.tex**

<pre class="overflow-visible! px-0!" data-start="1865" data-end="2003"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}
</span><span>\begin</span><span>{document}

</span><span>\section</span><span>{Introduction}

</span><span>\subfile</span><span>{intro/subsection1.tex}

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

**sections/intro/subsection1.tex**

<pre class="overflow-visible! px-0!" data-start="2040" data-end="2166"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[</span><span>\subfix</span><span>{../intro.tex}]{subfiles}
</span><span>\begin</span><span>{document}

</span><span>\subsection</span><span>{Subsection 1}
Text...

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

Key trick: `\subfix{...}` adjusts paths depending on what you’re compiling, so `subsection1.tex` can find its parent `intro.tex` whether you compile the main doc or the chapter.

---

## Quick rule of thumb

* If you only need **chapters** to be independently compilable → **Pattern A** (`subfile` for chapters, `input` for children).
* If you want **every nested piece** to compile standalone → **Pattern B** (subfiles all the way, using `\subfix`).

If you share your actual folders (where `main.tex` sits relative to intro + subsections + figures), I can write the exact include lines that will be “compile-proof” in both main and standalone builds.

how do I compile subsection1.tex  using pdlatex, can I do this fromroot or do i need to cd into the folder where the file is?

You can do it **from the root** — you don’t need to `cd` — as long as you pass the correct path to `pdflatex`.

### Compile a nested file from the root

<pre class="overflow-visible! px-0!" data-start="152" data-end="203"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pdflatex sections/intro/subsection1.tex
</span></span></code></div></div></pre>

That works if `subsection1.tex` is a *standalone* file (i.e., it has its own `\documentclass...` and `\begin{document}`), which is typically the case if you’re using the `subfiles` pattern where every level is compilable.

### Where the PDF/output ends up

By default, the output goes next to where you ran the command (the root), not next to the `.tex` file. If you want to force outputs into a build folder:

<pre class="overflow-visible! px-0!" data-start="615" data-end="690"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pdflatex -output-directory=build sections/intro/subsection1.tex
</span></span></code></div></div></pre>

### You do **not** need to `cd`, but you *can*

Equivalent if you prefer:

<pre class="overflow-visible! px-0!" data-start="765" data-end="819"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>cd</span><span> sections/intro
pdflatex subsection1.tex
</span></span></code></div></div></pre>

### Important gotcha: relative paths inside the file

When you compile from root, LaTeX’s “current working directory” is the root. That can break any paths in `subsection1.tex` that assume it’s being compiled from its own folder (especially `\includegraphics{...}` without a global `\graphicspath`).

Two reliable fixes:

1. Put all path configuration in `main.tex` (recommended) so subfiles inherit it.
2. Use `\subfix{...}` for paths inside subfiles, e.g.
   <pre class="overflow-visible! px-0!" data-start="1280" data-end="1338"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\includegraphics</span><span>{</span><span>\subfix</span><span>{figures/myplot}}
   </span></span></code></div></div></pre>

### If subsection1.tex is *not* standalone

If `subsection1.tex` is just a fragment (only `\subsection{...}` etc.), you  **can’t compile it directly** . You must compile its parent (`intro.tex`) or the root (`main.tex`).

If you paste the first ~5 lines of `subsection1.tex`, I can tell you instantly which case you’re in and what exact command will work.

Is everything in main.tex inherited to a subfile when compiled standalone?  even other subfiles?

Everything in **the preamble of `main.tex`** is inherited by a subfile when you compile that subfile standalone (because the subfile does `\documentclass[../main.tex]{subfiles}`, which loads `main.tex` as its “master”). That includes:

* `\documentclass` options (via the master)
* `\usepackage{...}`
* your custom macros (`\newcommand`, `\DeclareMathOperator`, etc.)
* settings like `\graphicspath`, `\hypersetup`, counters, theorem styles, etc.

What is **not** “automatically inherited”:

* The **document body** of `main.tex` (everything between `\begin{document}` and `\end{document}`), except the part that is in the subfile itself.
* **Other subfiles’ content** . Compiling `sections/intro.tex` standalone does *not* pull in the text of `sections/method.tex` unless `intro.tex` (or `main.tex`) explicitly includes it.

### Subfiles vs “other subfiles”

Think of it like this when compiling `intro.tex` standalone:

1. LaTeX loads `main.tex` **preamble** (so you get all packages/macros/settings).
2. Then it starts the document and typesets **only** what `intro.tex` includes in its own `\begin{document}...\end{document}` (plus any `\input`/`\subfile` calls inside `intro.tex`).

So:

* **Yes:** main preamble is inherited.
* **No:** other chapters/subfiles are not included unless you include them.

### Cross-references are the one “sort of” exception

Even though other subfiles’ *text* isn’t included, references to their labels can still resolve **if their `.aux` info exists** from a previous full build. Otherwise you’ll see `??` until you compile `main.tex` (or those parts) to generate aux data.

If you want, tell me whether you use `biblatex` or `natbib` and how you split the bibliography, because that’s another place where “inherited” depends on whether the bibliography commands live in the preamble vs the document body.

i use the printbibliographic in the doc body

If you’re using **biblatex** and you put `\printbibliography` in the  **document body** , here’s what that means with `subfiles`:

### What’s inherited when you compile a subfile standalone

A subfile compiled standalone **inherits the preamble of `main.tex`** (packages, `\addbibresource{...}`, options, macros, etc.).

So if your `main.tex` has something like:

<pre class="overflow-visible! px-0!" data-start="361" data-end="440"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\usepackage</span><span>[backend=biber]{biblatex}
</span><span>\addbibresource</span><span>{references.bib}
</span></span></code></div></div></pre>

…then a standalone-compiled subfile will still “know about” the bibliography database and biblatex settings.

### What is *not* inherited automatically

The *body content* from `main.tex` is not pulled in — including your `\printbibliography` command if it lives only in `main.tex`.

So:

* Compile `main.tex` → bibliography prints (because `\printbibliography` is in the body of `main.tex`).
* Compile `sections/intro.tex` standalone →  **no bibliography prints** , unless `intro.tex` itself contains `\printbibliography` (or includes something that does).

### Two common ways to handle this

#### A) You want a bibliography when compiling a subfile standalone

Add `\printbibliography` at the end of that subfile (or conditionally):

<pre class="overflow-visible! px-0!" data-start="1175" data-end="1301"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}
</span><span>\begin</span><span>{document}

... your intro text ...

</span><span>\printbibliography</span><span>

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

If you **don’t** want it to appear twice in the full build, you can gate it so it only prints in standalone compilation:

<pre class="overflow-visible! px-0!" data-start="1425" data-end="1572"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-tex"><span><span>\documentclass</span><span>[../main.tex]{subfiles}
</span><span>\begin</span><span>{document}

... content ...

</span><span>\ifSubfilesClassLoaded</span><span>
  </span><span>\printbibliography</span><span>
</span><span>\fi</span><span>

</span><span>\end</span><span>{document}
</span></span></code></div></div></pre>

#### B) You only want the bibliography in the full document

Then keep `\printbibliography` only in `main.tex` and accept that standalone subfile builds won’t show a bibliography (but citations still work).

### One more gotcha: biber run order

When compiling standalone with biblatex you typically need (same as usual):

<pre class="overflow-visible! px-0!" data-start="1895" data-end="2002"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pdflatex sections/intro.tex
biber intro
pdflatex sections/intro.tex
pdflatex sections/intro.tex
</span></span></code></div></div></pre>

The `biber` target name comes from the jobname (often the file basename). Some editors handle this automatically.

---

If you tell me whether you want **one global bibliography** (whole thesis/report) or  **a bibliography per chapter** , I can show the cleanest biblatex setup (that choice changes whether you should use `refsection`/`refsegment`).
