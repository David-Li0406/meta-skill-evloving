#!/usr/bin/env node
/**
 * HTML to PowerPoint ビルドスクリプト
 *
 * 使い方:
 * 1. npm install (初回のみ)
 * 2. node to_pptx.js
 * 3. node to_pptx.js part1 (フィルター指定)
 *
 * 環境変数:
 * - HTML2PPTX_PATH: html2pptxライブラリのパス (省略時はスキルのassetsを参照)
 */

const path = require("path");

async function main() {
  const filterArgs = process.argv.slice(2);

  const slidesDir = path.join(process.cwd(), "2_htmls");
  const outputDir = path.join(process.cwd(), "3_pptxs");

  const { convertHtmlToPptx } = await import("./to_pptx_core.mjs");

  console.log("🎨 プレゼンテーションを作成中...");

  const filters = filterArgs.length === 0 ? [null] : filterArgs;
  const results = [];

  for (const filter of filters) {
    const outputFile = filter
      ? path.join(outputDir, `${filter}.pptx`)
      : path.join(outputDir, "presentation.pptx");

    const result = await convertHtmlToPptx({
      slidesDir,
      outputPath: outputFile,
      filter: filter || undefined,
    });

    console.log(`  ✅ ${result.file} 作成完了 (${result.count}枚)`);
    results.push(result);
  }

  console.log("\n✨ 完成しました!");
  console.log("📊 生成ファイル:");
  for (const r of results) {
    console.log(`   - ${r.file} (${r.count}枚)`);
  }
}

main()
  .then(() => {
    console.log("\n🎉 プレゼンテーションの作成が完了しました！");
  })
  .catch((error) => {
    console.error("\n❌ エラーが発生しました:", error.message);
    console.error("\nトラブルシューティング:");
    console.error("1. npm install を実行してください");
    console.error("2. npx playwright install chromium を実行してください");
    console.error("3. 2_htmls/ フォルダにHTMLファイルがあることを確認してください");
    process.exit(1);
  });
