---
name: file-ops
description: Replaces the procedures for executing basic file operations such as rewriting, adding, and inserting content accurately and safely. Typical use cases: (1) Safe partial replacement of existing code and verifying consistency after reflection, (2) Reliable appending of metadata or new items to the end of a file, (3) Accurate insertion of code between specific lines to prevent syntax breakage.
---

# ファイル操作 (File Operations)

ファイルを安全かつ確実に操作するための手順を規定する。

## 1. ファイルの部分置換 (Safe Replace)
既存のコードを安全に書き換える際に使用する。

1. **読み込み:** 書き換え対象のファイルを読み込む。
   `read_file <file_path>`
2. **置換:** 取得した内容を基準に、`old_string` と `new_string` を指定して置換する。
   `replace --file_path <file_path> --old_string "..." --new_string "..."`
3. **確認:** 最後に `read_file <file_path>` で変更が正しく反映されたか確認する。

## 2. ファイル末尾への追加 (Append)
ファイルの末尾に新しい行やコードを追加する際に使用する。

1. **読み込み:** `read_file <file_path>` でファイルの内容を全て読み込む。
2. **結合:** 読み込んだ内容の末尾に、追加したい文字列を結合する。
3. **上書き:** `write_file --file_path <file_path> --content "<結合した内容>"` でファイルを上書きする。
4. **確認:** 最後に `read_file <file_path>` で内容を確認する。

## 3. 特定の行間への挿入 (Insert)
ファイルの途中にコードを挿入する際に使用する。

1. **読み込み:** `read_file <file_path>` でファイルの内容を全て読み込む。
2. **挿入:** 読み込んだ内容（文字列）に対して、追加したい箇所に新しいコードを挿入する。
3. **上書き:** `write_file --file_path <file_path> --content "<挿入後の内容>"` でファイルを上書きする。
4. **確認:** 最後に `read_file <file_path>` で内容を確認する。
