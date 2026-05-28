#!/usr/bin/env node

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Parse command line arguments
const args = process.argv.slice(2);
const flags = {};
const positional = [];

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith("--")) {
    const [key] = arg.slice(2).split("=");
    // Check if next argument is a value (not starting with --)
    const nextArg = args[i + 1];
    if (nextArg && !nextArg.startsWith("--")) {
      flags[key] = nextArg;
      i++; // Skip next argument as it's a value
    } else {
      flags[key] = true;
    }
  } else {
    positional.push(arg);
  }
}

const name = flags.name || positional[0];
const type = flags.type || "astro";
const targetDir = flags.dir || "src/components";

if (!name) {
  console.error("Error: Component name is required");
  console.log(
    "Usage: node create-component.js --name MyComponent [--type astro|react|vue|svelte] [--dir src/components]",
  );
  process.exit(1);
}

const templates = {
  astro: (name) => `---
// ${name}.astro component
export interface Props {
  title?: string;
  className?: string;
}

const { title, className } = Astro.props;
---

<div class="{className}">
  {title && <h2>{title}</h2>}
  <slot />
</div>

<style>
  div {
    padding: 1rem;
    border-radius: 0.5rem;
    background: var(--bg-color, #f3f4f6);
  }

  h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
  }
</style>
`,

  react: (name) => `import React from 'react';
import { cn } from '@/utils/cn';

interface ${name}Props {
  title?: string;
  className?: string;
  children?: React.ReactNode;
}

export const ${name}: React.FC<${name}Props> = ({
  title,
  className,
  children
}) => {
  return (
    <div className={cn('p-4 rounded-lg bg-gray-100', className)}>
      {title && <h2 className="text-xl font-semibold mb-2">{title}</h2>}
      {children}
    </div>
  );
};

export default ${name};
`,

  vue: (name) => `<template>
  <div :class="className">
    <h2 v-if="title">{{ title }}</h2>
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string;
  className?: string;
}

withDefaults(defineProps<Props>(), {
  className: 'p-4 rounded-lg bg-gray-100'
});
</script>

<style scoped>
h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}
</style>
`,

  svelte: (name) => `<script lang="ts">
  export let title: string | undefined = undefined;
  export let className: string = 'p-4 rounded-lg bg-gray-100';
</script>

<div class={className}>
  {#if title}
    <h2>{title}</h2>
  {/if}
  <slot />
</div>

<style>
  h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    font-weight: 600;
  }
</style>
`,
};

const extensions = {
  astro: "astro",
  react: "tsx",
  vue: "vue",
  svelte: "svelte",
};

const template = templates[type];
const extension = extensions[type];

if (!template) {
  console.error(`Error: Unknown component type "${type}"`);
  console.log("Supported types: astro, react, vue, svelte");
  process.exit(1);
}

const componentDir = path.join(process.cwd(), targetDir);
const componentPath = path.join(componentDir, `${name}.${extension}`);

// Create directory if it doesn't exist
if (!fs.existsSync(componentDir)) {
  fs.mkdirSync(componentDir, { recursive: true });
}

// Write component file
fs.writeFileSync(componentPath, template(name));

// Create index file for exports if it doesn't exist
const indexPath = path.join(componentDir, "index.ts");
let indexContent = "";

if (fs.existsSync(indexPath)) {
  indexContent = fs.readFileSync(indexPath, "utf-8");
}

const exportLine = `export { ${name} } from './${name}.${extension}';\n`;

if (!indexContent.includes(exportLine)) {
  if (indexContent && !indexContent.endsWith("\n")) {
    indexContent += "\n";
  }
  indexContent += exportLine;
  fs.writeFileSync(indexPath, indexContent);
}

console.log(`✅ Created ${type} component: ${componentPath}`);
if (!indexContent.includes(exportLine)) {
  console.log(`✅ Updated exports: ${indexPath}`);
}
