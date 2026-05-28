#!/usr/bin/env node
/**
 * Markdown to HTML スライド変換スクリプト
 *
 * 使い方:
 * 1. node to_html.js 1_mds/sample.md
 * 2. node to_html.js 1_mds/sample.md --output 2_htmls
 * 3. node to_html.js 1_mds/sample.md --prefix slide
 *
 * オプション:
 * --output, -o  出力ディレクトリ (デフォルト: 2_htmls)
 * --prefix, -p  ファイル名プレフィックス (デフォルト: slide)
 * --dry-run     ファイルを書き込まずに確認
 */

const path = require("path");

/**
 * コマンドライン引数をパース
 */
function parseArgs(args) {
  const result = {
    input: null,
    output: "2_htmls",
    prefix: null,
    dryRun: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === "--output" || arg === "-o") {
      result.output = args[++i];
    } else if (arg === "--prefix" || arg === "-p") {
      result.prefix = args[++i];
    } else if (arg === "--dry-run") {
      result.dryRun = true;
    } else if (!arg.startsWith("-")) {
      result.input = arg;
    }
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.input) {
    console.error("使い方: node to_html.js <markdown-file> [options]");
    console.error("");
    console.error("オプション:");
    console.error("  --output, -o  出力ディレクトリ (デフォルト: 2_htmls)");
    console.error("  --prefix, -p  ファイル名プレフィックス (デフォルト: slide)");
    console.error("  --dry-run     ファイルを書き込まずに確認");
    process.exit(1);
  }

  const inputPath = path.isAbsolute(args.input)
    ? args.input
    : path.join(process.cwd(), args.input);

  const outputDir = path.isAbsolute(args.output)
    ? args.output
    : path.join(process.cwd(), args.output);

  const { convertMdToHtml } = await import("./to_html_core.mjs");

  console.log(`📄 読み込み: ${args.input}`);

  const { slides, generated } = await convertMdToHtml({
    inputPath,
    outputDir,
    prefix: args.prefix,
    dryRun: args.dryRun,
  });

  console.log(`📊 ${slides.length}枚のスライドを検出`);

  if (args.dryRun) {
    for (const { filename, slide } of generated) {
      console.log(`  📝 生成予定: ${filename} (${slide.type}: ${slide.name})`);
    }
    console.log(`\n🔍 ドライラン完了。${generated.length}枚のスライドが生成されます。`);
  } else {
    for (const { filename, slide } of generated) {
      console.log(`  ✅ 生成: ${filename} (${slide.type}: ${slide.name})`);
    }
    console.log(`\n✨ ${generated.length}枚のHTMLスライドを ${args.output}/ に生成しました！`);
  }
}

main()
  .then(() => {
    console.log("\n🎉 HTML生成が完了しました！");
  })
  .catch((error) => {
    console.error("\n❌ エラーが発生しました:", error.message);
    console.error("\nトラブルシューティング:");
    console.error("1. Markdownファイルのパスを確認してください");
    console.error("2. Markdown記法が正しいか確認してください");
    console.error("   例: ## タイトル  または  ## スライド1: タイトル");
    process.exit(1);
  });
