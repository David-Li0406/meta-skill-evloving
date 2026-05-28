---
name: "sync-words-from-blob"
description: "Vercel Blobから単語ファイルをダウンロードし、ローカルの/__doc__フォルダを更新し、変更ログを記録します。ユーザーが単語ファイルの同期や更新を求めた時に呼び出します。"
---

# Sync Words from Vercel Blob

このスキルは、Vercel Blob ストレージから最新の単語ファイルを取得し、ローカル環境を更新するためのものです。

## 実行手順

1.  **環境変数の確認**:
    *   `.env.local` ファイルから `BLOB_READ_WRITE_TOKEN` を読み込みます。
    *   `BLOB_READ_WRITE_TOKEN` が設定されていない場合は、ユーザーに設定を促し、処理を中断します。

2.  **スクリプトの作成と実行**:
    *   プロジェクトルートに一時的な Node.js スクリプト（例: `sync-blob.mjs`）を作成します。
    *   スクリプト内で以下の処理を実装します:
        1.  `.env.local` から環境変数を読み込みます（正規表現での簡易パースを推奨）。
        2.  `@vercel/blob` の `list` メソッドを使用して、`words-file/word.txt` と `words-file/word_mid.txt` の情報を取得します。
        3.  `fetch` を使用してファイルの内容をダウンロードします。
        4.  ローカルの `__doc__/word.txt` と `__doc__/word_mid.txt` を読み込み、ダウンロードした内容と比較します。
        5.  差異がある場合:
            *   ファイルを上書き保存します。
            *   `__doc__` フォルダ内に `change_log_yyyymmddhhmiss.log` を作成し、変更内容（ファイル名、更新日時など）を書き込みます。
        6.  差異がない場合:
            *   「変更なし」とログに出力します。

3.  **クリーンアップ**:
    *   作成した一時スクリプトを削除します。

## スクリプトの例 (sync-blob.mjs)

```javascript
import { list } from '@vercel/blob';
import fs from 'fs';
import path from 'path';

// .env.local からトークンを読み込む簡易実装
const envPath = path.resolve(process.cwd(), '.env.local');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  // 引用符や空白に対応する正規表現
  const match = envContent.match(/BLOB_READ_WRITE_TOKEN=["']?([^"'\n]+)["']?/);
  if (match) {
    process.env.BLOB_READ_WRITE_TOKEN = match[1].trim();
  }
}

if (!process.env.BLOB_READ_WRITE_TOKEN) {
  console.error('Error: BLOB_READ_WRITE_TOKEN not found in .env.local');
  process.exit(1);
}

const DOC_DIR = path.resolve(process.cwd(), '__doc__');
const TARGET_FILES = ['word.txt', 'word_mid.txt'];
const PREFIX = 'words-file/';

async function main() {
  try {
    // ディレクトリが存在しない場合は作成
    if (!fs.existsSync(DOC_DIR)) {
      fs.mkdirSync(DOC_DIR, { recursive: true });
    }

    console.log('Fetching blob list...');
    // prefixでフィルタリングしてリスト取得
    const { blobs } = await list({ prefix: PREFIX, limit: 100 });

    let hasChanges = false;
    let logContent = `Update Log: ${new Date().toISOString()}\n\n`;

    for (const fileName of TARGET_FILES) {
      const blobKey = PREFIX + fileName;
      // パスが一致するものを探す
      const blob = blobs.find(b => b.pathname === blobKey);

      if (!blob) {
        console.warn(`Warning: Blob not found for ${blobKey}`);
        continue;
      }

      console.log(`Downloading ${blobKey} from ${blob.url}...`);
      const response = await fetch(blob.url);
      if (!response.ok) {
        console.error(`Failed to download ${blobKey}: ${response.statusText}`);
        continue;
      }
      const newContent = await response.text();
      
      const localFilePath = path.join(DOC_DIR, fileName);
      let oldContent = '';
      if (fs.existsSync(localFilePath)) {
        oldContent = fs.readFileSync(localFilePath, 'utf-8');
      }

      // 改行コードの違いを無視して比較するために normalize する場合もありますが、
      // ここでは完全一致で比較します。
      if (newContent !== oldContent) {
        console.log(`Updating ${fileName}...`);
        fs.writeFileSync(localFilePath, newContent, 'utf-8');
        hasChanges = true;
        logContent += `Updated: ${fileName}\n`;
        logContent += `Blob URL: ${blob.url}\n`;
        logContent += `Size: ${newContent.length} bytes\n\n`;
      } else {
        console.log(`No changes for ${fileName}`);
      }
    }

    if (hasChanges) {
      // yyyymmddhhmiss 形式のタイムスタンプ
      const now = new Date();
      const timestamp = now.getFullYear().toString() +
        (now.getMonth() + 1).toString().padStart(2, '0') +
        now.getDate().toString().padStart(2, '0') +
        now.getHours().toString().padStart(2, '0') +
        now.getMinutes().toString().padStart(2, '0') +
        now.getSeconds().toString().padStart(2, '0');
        
      const logFileName = `change_log_${timestamp}.log`;
      fs.writeFileSync(path.join(DOC_DIR, logFileName), logContent, 'utf-8');
      console.log(`Changes logged to ${logFileName}`);
    } else {
      console.log('All files are up to date.');
    }

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
```
