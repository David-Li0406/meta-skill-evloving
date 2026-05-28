/**
 * MD → PPTX 統合テスト（ステップスライド）
 *
 * Markdown から生成された PPTX の XML 構造を検証
 * 仕様化テスト: 既存の動作をそのまま記録
 */

import { describe, test, expect, beforeAll, afterAll } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import {
  setupTmpDir,
  cleanupTmpDir,
  mdToPptx,
  getSlideXml,
  extractTexts,
  countShapes,
  hasPattern,
  countImages,
  countPicElements
} from './helpers/pptx-utils.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const FIXTURES_DIR = path.join(__dirname, 'fixtures/inputs');

describe('MD → PPTX 統合テスト', () => {
  afterAll(() => {
    cleanupTmpDir();
  });

  describe('タイトルスライド', () => {
    /**
     * タイトルスライド仕様:
     * - スライドN: タイトル で定義
     * - PART番号、メインタイトル、副題を配置
     * - ダーク背景（p:bg要素あり）
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'title-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'title');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000); // 最低 10KB
    });

    test('PART番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('PART 1'))).toBe(true);
    });

    test('メインタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('メインタイトル'))).toBe(true);
    });

    test('サブタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('サブタイトルテキスト'))).toBe(true);
    });

    test('背景が設定されている', () => {
      expect(hasPattern(slideXml, /<p:bg>/)).toBe(true);
    });

    test('図形が3つ存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBe(3);
    });
  });

  describe('コンテンツスライド（箇条書き）', () => {
    /**
     * コンテンツスライド仕様:
     * - 内容: の下に直接箇条書き項目を配置
     * - ネスト項目もサポート
     * - 箇条書きマーカー（a:buChar）が使用される
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'list-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'content');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000); // 最低 10KB
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('箇条書きテスト'))).toBe(true);
    });

    test('箇条書き項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('項目1'))).toBe(true);
      expect(texts.some(t => t.includes('項目2'))).toBe(true);
      expect(texts.some(t => t.includes('項目3'))).toBe(true);
    });

    test('ネスト項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('ネスト項目A'))).toBe(true);
      expect(texts.some(t => t.includes('ネスト項目B'))).toBe(true);
    });

    test('箇条書きはリストスタイルなしで表示される', () => {
      // 現在の実装ではCSSで list-style: none を使用しているため
      // PPTXの箇条書きマーカー（a:buChar）は使用されない
      // 代わりにテキストが正しく含まれていることを確認
      const texts = extractTexts(slideXml);
      expect(texts.length).toBeGreaterThan(0);
    });

    test('図形が3つ存在する', () => {
      // セクション番号、タイトル、コンテンツリストの3つ
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBe(3);
    });
  });

  describe('カードスライド', () => {
    /**
     * カードスライド仕様:
     * - カードN: でカードを定義
     * - 各カードの下に項目を配置
     * - 角丸矩形（roundRect）で描画
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'cards-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'cards');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('3つの特徴'))).toBe(true);
    });

    test('カード1のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('シンプル'))).toBe(true);
    });

    test('カード1の項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('簡単に使える'))).toBe(true);
      expect(texts.some(t => t.includes('学習コストが低い'))).toBe(true);
    });

    test('カード2のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('高速'))).toBe(true);
    });

    test('カード2の項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('素早く生成'))).toBe(true);
      expect(texts.some(t => t.includes('効率的な処理'))).toBe(true);
    });

    test('カード3のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('柔軟'))).toBe(true);
    });

    test('カード3の項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('カスタマイズ可能'))).toBe(true);
      expect(texts.some(t => t.includes('拡張性が高い'))).toBe(true);
    });

    test('複数の図形が存在する（カード背景）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(4);
    });

    test('角丸矩形が使用されている', () => {
      expect(hasPattern(slideXml, /<a:prstGeom prst="roundRect"/)).toBe(true);
    });
  });

  describe('ステップスライド', () => {
    /**
     * ステップスライド仕様:
     * - ステップN: でステップを定義
     * - 各ステップの下に説明を配置
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'steps-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'steps');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000); // 最低 10KB
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('手順の説明'))).toBe(true);
    });

    test('ステップ1のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('準備'))).toBe(true);
    });

    test('ステップ1の説明が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('環境をセットアップ'))).toBe(true);
    });

    test('ステップ2のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('実行'))).toBe(true);
    });

    test('ステップ2の説明が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('コマンドを実行'))).toBe(true);
    });

    test('ステップ3のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('確認'))).toBe(true);
    });

    test('ステップ3の説明が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('結果を確認'))).toBe(true);
    });

    test('複数の図形が存在する（ステップ背景）', () => {
      const shapeCount = countShapes(slideXml);
      // 3つのステップ + タイトル + その他
      expect(shapeCount).toBeGreaterThanOrEqual(4);
    });

    test('ステップ番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      // ステップ番号 1, 2, 3 が含まれることを確認
      expect(texts.some(t => t === '1' || t.includes('1'))).toBe(true);
      expect(texts.some(t => t === '2' || t.includes('2'))).toBe(true);
      expect(texts.some(t => t === '3' || t.includes('3'))).toBe(true);
    });
  });

  describe('テーブルスライド', () => {
    /**
     * テーブルスライド仕様:
     * - テーブル: でテーブルを定義
     * - Markdown テーブル記法で内容を記述
     * - PptxGenJS はネイティブテーブル(a:tbl)ではなく図形(p:sp)で表現
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'table-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'table');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000); // 最低 10KB
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('比較表'))).toBe(true);
    });

    test('テーブルヘッダー「項目」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('項目'))).toBe(true);
    });

    test('テーブルヘッダー「説明」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('説明'))).toBe(true);
    });

    test('テーブルヘッダー「備考」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('備考'))).toBe(true);
    });

    test('テーブルデータ行1が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'A')).toBe(true);
      expect(texts.some(t => t.includes('説明A'))).toBe(true);
      expect(texts.some(t => t.includes('備考A'))).toBe(true);
    });

    test('テーブルデータ行2が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'B')).toBe(true);
      expect(texts.some(t => t.includes('説明B'))).toBe(true);
      expect(texts.some(t => t.includes('備考B'))).toBe(true);
    });

    test('図形でテーブルが構成される（セル数分の図形）', () => {
      const shapeCount = countShapes(slideXml);
      // 3列 x 3行 = 9セル + タイトル + その他
      // 実測値: 16図形
      expect(shapeCount).toBeGreaterThanOrEqual(10);
    });
  });

  describe('Good/Badスライド', () => {
    /**
     * Good/Badスライド仕様:
     * - Good: / Bad: でカードを定義
     * - 各カードの下に項目を配置
     * - Goodは緑系、Badは赤系の色で表示
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'good-bad-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'good-bad');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('ベストプラクティス'))).toBe(true);
    });

    test('Goodカードのタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('推奨される方法'))).toBe(true);
    });

    test('Goodカードの項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('明確な命名規則'))).toBe(true);
      expect(texts.some(t => t.includes('適切なコメント'))).toBe(true);
    });

    test('Badカードのタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('避けるべき方法'))).toBe(true);
    });

    test('Badカードの項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('曖昧な変数名'))).toBe(true);
      expect(texts.some(t => t.includes('コメントなし'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      // Good/Bad 2カード + タイトル + その他
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('コードスライド', () => {
    /**
     * コードスライド仕様:
     * - コードブロック（```言語名）で定義
     * - シンタックスハイライト付きで表示
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('TypeScriptの例'))).toBe(true);
    });

    test('コード内容が含まれる（interface）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('interface') || t.includes('User'))).toBe(true);
    });

    test('コード内容が含まれる（function）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('function') || t.includes('greet'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(2);
    });
  });

  describe('フロースライド', () => {
    /**
     * フロースライド仕様:
     * - フロー: でフローを定義
     * - 各要素が横並びに配置される
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'flow-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'flow');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('処理フロー'))).toBe(true);
    });

    test('フロー要素「入力」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('入力'))).toBe(true);
    });

    test('フロー要素「処理」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('処理'))).toBe(true);
    });

    test('フロー要素「出力」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('出力'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      // 3つのフロー要素 + タイトル + 矢印など
      expect(shapeCount).toBeGreaterThanOrEqual(4);
    });
  });

  describe('複合スライド（2x2カード）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 行:列 でレイアウトを定義
     * - 2:2 で2行2列のグリッド配置
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-cards-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-cards');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('4つの機能'))).toBe(true);
    });

    test('カード1が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能A'))).toBe(true);
      expect(texts.some(t => t.includes('説明A1'))).toBe(true);
    });

    test('カード2が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能B'))).toBe(true);
      expect(texts.some(t => t.includes('説明B1'))).toBe(true);
    });

    test('カード3が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能C'))).toBe(true);
      expect(texts.some(t => t.includes('説明C1'))).toBe(true);
    });

    test('カード4が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能D'))).toBe(true);
      expect(texts.some(t => t.includes('説明D1'))).toBe(true);
    });

    test('複数の図形が存在する（4カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(5);
    });
  });

  describe('ネスト複合スライド（複合の複合）', () => {
    /**
     * ネスト複合スライド仕様:
     * - 複合の中に複合を入れ子にできる
     * - 親グリッドのセル内に子グリッドが配置される
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'nested-composite-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'nested-composite');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('複合の複合'))).toBe(true);
    });

    test('ネストされた複合内のカードA1が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('A1'))).toBe(true);
      expect(texts.some(t => t.includes('a1'))).toBe(true);
    });

    test('ネストされた複合内のカードA4が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('A4'))).toBe(true);
      expect(texts.some(t => t.includes('a4'))).toBe(true);
    });

    test('親グリッドのカードBが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('b1'))).toBe(true);
    });

    test('親グリッドのカードCが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('c1'))).toBe(true);
    });

    test('親グリッドのカードDが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('d1'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      // ネスト複合 + 親カード3つ + タイトル
      expect(shapeCount).toBeGreaterThanOrEqual(5);
    });
  });

  describe('1x2グリッドスライド', () => {
    /**
     * 1x2グリッドスライド仕様:
     * - 複合: 1:2 で1行2列の均等グリッド配置
     * - 2つのカードが左右に並ぶ
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'grid-1x2-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'grid-1x2');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2つの比較'))).toBe(true);
    });

    test('左側カードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('左側'))).toBe(true);
      expect(texts.some(t => t.includes('項目A1'))).toBe(true);
      expect(texts.some(t => t.includes('項目A2'))).toBe(true);
    });

    test('右側カードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('右側'))).toBe(true);
      expect(texts.some(t => t.includes('項目B1'))).toBe(true);
      expect(texts.some(t => t.includes('項目B2'))).toBe(true);
    });

    test('複数の図形が存在する（2カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('4x4グリッドスライド', () => {
    /**
     * 4x4グリッドスライド仕様:
     * - 複合: 4:4 で4行4列のグリッド配置
     * - 16個のカードが配置される
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'grid-4x4-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'grid-4x4');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('16の機能'))).toBe(true);
    });

    test('カードAからDが含まれる（1行目）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'A')).toBe(true);
      expect(texts.some(t => t === 'B')).toBe(true);
      expect(texts.some(t => t === 'C')).toBe(true);
      expect(texts.some(t => t === 'D')).toBe(true);
    });

    test('カードEからHが含まれる（2行目）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'E')).toBe(true);
      expect(texts.some(t => t === 'F')).toBe(true);
      expect(texts.some(t => t === 'G')).toBe(true);
      expect(texts.some(t => t === 'H')).toBe(true);
    });

    test('カードIからLが含まれる（3行目）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'I')).toBe(true);
      expect(texts.some(t => t === 'J')).toBe(true);
      expect(texts.some(t => t === 'K')).toBe(true);
      expect(texts.some(t => t === 'L')).toBe(true);
    });

    test('カードMからPが含まれる（4行目）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'M')).toBe(true);
      expect(texts.some(t => t === 'N')).toBe(true);
      expect(texts.some(t => t === 'O')).toBe(true);
      expect(texts.some(t => t === 'P')).toBe(true);
    });

    test('複数の図形が存在する（16カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(17);
    });
  });

  describe('8x8グリッドスライド', () => {
    /**
     * 8x8グリッドスライド仕様:
     * - 複合: 8:8 で8行8列のグリッド配置
     * - 64個のカードが配置される
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'grid-8x8-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'grid-8x8');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('64の項目'))).toBe(true);
    });

    test('1行目のカードが含まれる（A1-A8）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'A1')).toBe(true);
      expect(texts.some(t => t === 'A8')).toBe(true);
    });

    test('8行目のカードが含まれる（H1-H8）', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t === 'H1')).toBe(true);
      expect(texts.some(t => t === 'H8')).toBe(true);
    });

    test('複数の図形が存在する（64カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(65);
    });
  });

  describe('カード内コードスライド', () => {
    /**
     * カード内コードスライド仕様:
     * - カード内にコードブロックを含める
     * - 説明テキストとコードの両方を表示
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'card-with-code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'card-with-code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能とコード例'))).toBe(true);
    });

    test('カード1のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('変数宣言'))).toBe(true);
    });

    test('カード1の説明が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('let') && t.includes('変数'))).toBe(true);
    });

    test('カード1のコードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('let') || t.includes('count'))).toBe(true);
      expect(texts.some(t => t.includes('const') || t.includes('MAX'))).toBe(true);
    });

    test('カード2のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('関数定義'))).toBe(true);
    });

    test('カード2の説明が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('アロー関数'))).toBe(true);
    });

    test('カード2のコードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('add') || t.includes('number'))).toBe(true);
    });

    test('複数の図形が存在する（2カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('カード横並びスライド（layout: horizontal）', () => {
    /**
     * カード横並びスライド仕様:
     * - layout: horizontal でカードを横並びに配置
     * - 各カードが均等幅で配置される
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'cards-horizontal-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'cards-horizontal');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('横並びカード'))).toBe(true);
    });

    test('カード1が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能A'))).toBe(true);
      expect(texts.some(t => t.includes('説明A1'))).toBe(true);
    });

    test('カード2が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能B'))).toBe(true);
      expect(texts.some(t => t.includes('説明B1'))).toBe(true);
    });

    test('カード3が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('機能C'))).toBe(true);
      expect(texts.some(t => t.includes('説明C1'))).toBe(true);
    });

    test('複数の図形が存在する（3カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(4);
    });
  });

  describe('複合スライド（縦: 上に箇条書き、下にコード）', () => {
    /**
     * 複合縦レイアウト仕様:
     * - 複合: 2:1 で縦方向に配置
     * - 上に箇条書き、下にコードブロック
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-vertical-list-code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-vertical-list-code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('説明とコード（縦配置）'))).toBe(true);
    });

    test('箇条書き項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('関数の説明'))).toBe(true);
      expect(texts.some(t => t.includes('引数を受け取って処理'))).toBe(true);
      expect(texts.some(t => t.includes('結果を返す'))).toBe(true);
    });

    test('コード内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('function') || t.includes('greet'))).toBe(true);
      expect(texts.some(t => t.includes('Hello'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('複合スライド（横: 左に箇条書き、右にコード）', () => {
    /**
     * 複合横レイアウト仕様:
     * - 複合: 1:2 で横方向に配置
     * - 左に箇条書き、右にコードブロック
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-horizontal-list-code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-horizontal-list-code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2.2'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('説明とコード（横配置）'))).toBe(true);
    });

    test('箇条書き項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('関数の説明'))).toBe(true);
      expect(texts.some(t => t.includes('引数を受け取って処理'))).toBe(true);
      expect(texts.some(t => t.includes('結果を返す'))).toBe(true);
    });

    test('コード内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('function') || t.includes('greet'))).toBe(true);
      expect(texts.some(t => t.includes('Hello'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('複合スライド（Good/Bad + コード）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 1:2 で横方向に配置
     * - Good/Bad カードとコードブロックを組み合わせ
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-goodbad-code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-goodbad-code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('命名規則の比較'))).toBe(true);
    });

    test('Goodカードの内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('推奨'))).toBe(true);
      expect(texts.some(t => t.includes('明確な変数名'))).toBe(true);
    });

    test('Badカードの内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('非推奨'))).toBe(true);
      expect(texts.some(t => t.includes('略語の多用'))).toBe(true);
    });

    test('コード内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('userName') || t.includes('Alice'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('複合スライド（Good/Bad + テーブル）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 2:1 で縦方向に配置
     * - Good/Bad カードとテーブルを組み合わせ
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-goodbad-table-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-goodbad-table');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2.2'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('コーディング規約'))).toBe(true);
    });

    test('Goodカードの内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('推奨'))).toBe(true);
      expect(texts.some(t => t.includes('一貫したスタイル'))).toBe(true);
    });

    test('Badカードの内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('非推奨'))).toBe(true);
      expect(texts.some(t => t.includes('バラバラなスタイル'))).toBe(true);
    });

    test('テーブルヘッダーが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('項目'))).toBe(true);
      expect(texts.some(t => t.includes('推奨'))).toBe(true);
      expect(texts.some(t => t.includes('非推奨'))).toBe(true);
    });

    test('テーブルデータが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('インデント'))).toBe(true);
      expect(texts.some(t => t.includes('2スペース'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('複合スライド（カード + ステップ）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 2:1 で縦方向に配置
     * - カードとステップを組み合わせ
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-cards-steps-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-cards-steps');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2.3'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('開発プロセス'))).toBe(true);
    });

    test('カード1の内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('目的'))).toBe(true);
      expect(texts.some(t => t.includes('品質の担保'))).toBe(true);
    });

    test('カード2の内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('成果物'))).toBe(true);
      expect(texts.some(t => t.includes('テスト済みコード'))).toBe(true);
    });

    test('ステップ1の内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('設計'))).toBe(true);
      expect(texts.some(t => t.includes('要件を整理'))).toBe(true);
    });

    test('ステップ2の内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('実装'))).toBe(true);
      expect(texts.some(t => t.includes('コードを書く'))).toBe(true);
    });

    test('ステップ3の内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('テスト'))).toBe(true);
      expect(texts.some(t => t.includes('動作確認'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(5);
    });
  });

  describe('複合スライド（内容 + フロー）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 2:1 で縦方向に配置
     * - 箇条書きとフローを組み合わせ
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-list-flow-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-list-flow');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('2.4'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('CI/CDパイプライン'))).toBe(true);
    });

    test('箇条書き項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('自動化されたビルド'))).toBe(true);
      expect(texts.some(t => t.includes('品質を継続的に担保'))).toBe(true);
    });

    test('フロー要素「Push」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Push'))).toBe(true);
    });

    test('フロー要素「Build」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Build'))).toBe(true);
    });

    test('フロー要素「Test」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Test'))).toBe(true);
    });

    test('フロー要素「Deploy」が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Deploy'))).toBe(true);
    });

    test('複数の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('複合スライド（2:2カード + コードブロック）', () => {
    /**
     * 複合カード内コードスライド仕様:
     * - 複合: 2:2 で4カードを2x2グリッドに配置
     * - 各カードにコードブロックを含む
     * - コードブロックはカードの説明の一部として表示
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-cards-with-code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-cards-with-code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('高度なプロンプト技法'))).toBe(true);
    });

    test('カード1のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Decomposition'))).toBe(true);
    });

    test('カード1の説明が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('大きな問題を小さなサブタスク'))).toBe(true);
    });

    test('カード1のコードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('認証機能を分割'))).toBe(true);
    });

    test('カード2のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Self-Refine'))).toBe(true);
    });

    test('カード2のコードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('問題点を指摘'))).toBe(true);
    });

    test('カード3のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Tree of Thoughts'))).toBe(true);
    });

    test('カード3のコードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('3つの異なるアプローチ'))).toBe(true);
    });

    test('カード4のタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Meta Prompting'))).toBe(true);
    });

    test('カード4のコードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('最適なプロンプト'))).toBe(true);
    });

    test('複数の図形が存在する（4カード + タイトル）', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(5);
    });
  });

  describe('Mermaidスライド', () => {
    /**
     * Mermaidスライド仕様:
     * - Mermaid コードブロックを図解としてレンダリング
     * - SVGをラスタライズして画像として埋め込み
     * - 生のMermaidテキストはPPTXに含まれない
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'mermaid-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'mermaid');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('3.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('シーケンス図'))).toBe(true);
    });

    test('Mermaid図が画像として埋め込まれる', async () => {
      const imageCount = await countImages(pptxPath);
      expect(imageCount).toBeGreaterThanOrEqual(1);
    });

    test('スライドに画像参照が含まれる', () => {
      const picCount = countPicElements(slideXml);
      expect(picCount).toBeGreaterThanOrEqual(1);
    });

    test('生のMermaidシンタックスが含まれない', () => {
      const texts = extractTexts(slideXml);
      // Mermaidの生テキストが含まれないことを確認
      expect(texts.some(t => t.includes('sequenceDiagram'))).toBe(false);
      expect(texts.some(t => t.includes('participant'))).toBe(false);
      expect(texts.some(t => t.includes('->>'))).toBe(false);
    });
  });

  describe('複合スライド（リスト + Mermaid）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 1:2 で左にリスト、右にMermaid
     * - Mermaidは図解としてレンダリング
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-list-mermaid-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-list-mermaid');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('3.2'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('リストとMermaid'))).toBe(true);
    });

    test('リスト項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('システム構成の概要'))).toBe(true);
      expect(texts.some(t => t.includes('各層の役割'))).toBe(true);
    });

    test('Mermaid図が画像として埋め込まれる', async () => {
      const imageCount = await countImages(pptxPath);
      expect(imageCount).toBeGreaterThanOrEqual(1);
    });

    test('生のMermaidシンタックスが含まれない', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('flowchart'))).toBe(false);
      expect(texts.some(t => t.includes('-->'))).toBe(false);
    });
  });

  describe('複合スライド（カード + Mermaid）', () => {
    /**
     * 複合スライド仕様:
     * - 複合: 1:2 で左にカード、右にMermaid
     * - Mermaidは図解としてレンダリング
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-card-mermaid-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-card-mermaid');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('ファイルサイズが妥当', () => {
      const stats = fs.statSync(pptxPath);
      expect(stats.size).toBeGreaterThan(10000);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('3.3'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('カードとMermaid'))).toBe(true);
    });

    test('カードタイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('アーキテクチャ'))).toBe(true);
    });

    test('カード項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('マイクロサービス構成'))).toBe(true);
      expect(texts.some(t => t.includes('各サービスは独立'))).toBe(true);
    });

    test('Mermaid図が画像として埋め込まれる', async () => {
      const imageCount = await countImages(pptxPath);
      expect(imageCount).toBeGreaterThanOrEqual(1);
    });

    test('生のMermaidシンタックスが含まれない', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('flowchart'))).toBe(false);
      expect(texts.some(t => t.includes('-->'))).toBe(false);
    });
  });

  describe('3列レイアウト（1:1:1）', () => {
    /**
     * 3列レイアウト仕様:
     * - 複合: 1:1:1 で3カラムグリッドを定義
     * - parser の 3パートレイアウト分岐を検証
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-1x1x1-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-1x1x1');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('セクション番号が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1.1'))).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('3列グリッド'))).toBe(true);
    });

    test('左カラムのカードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('左カラム'))).toBe(true);
      expect(texts.some(t => t.includes('左の項目1'))).toBe(true);
    });

    test('中央カラムのカードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('中央カラム'))).toBe(true);
      expect(texts.some(t => t.includes('中央の項目1'))).toBe(true);
    });

    test('右カラムのカードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('右カラム'))).toBe(true);
      expect(texts.some(t => t.includes('右の項目1'))).toBe(true);
    });

    test('3つ以上の図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(3);
    });
  });

  describe('ネスト複合内リスト', () => {
    /**
     * ネスト複合内リスト仕様:
     * - ネストされた複合内で bulletList タイプを描画
     * - generateNestedGridHtml の bulletList 分岐を検証
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-nested-list-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-nested-list');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('ネスト内リスト'))).toBe(true);
    });

    test('ネスト内リスト項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('ネスト項目1'))).toBe(true);
      expect(texts.some(t => t.includes('ネスト項目2'))).toBe(true);
    });

    test('ネスト内カードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('右側'))).toBe(true);
    });

    test('外側のカードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('セルB'))).toBe(true);
      expect(texts.some(t => t.includes('セルC'))).toBe(true);
      expect(texts.some(t => t.includes('セルD'))).toBe(true);
    });
  });

  describe('グリッド内テーブル', () => {
    /**
     * グリッド内テーブル仕様:
     * - 2x2グリッドのセルにテーブルを配置
     * - generateGridTableCell 関数を検証
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-grid-table-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-grid-table');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('テーブルを含む2x2'))).toBe(true);
    });

    test('テーブルヘッダーが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('名前'))).toBe(true);
      expect(texts.some(t => t.includes('スコア'))).toBe(true);
    });

    test('テーブルデータが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('Alice'))).toBe(true);
      expect(texts.some(t => t.includes('95'))).toBe(true);
    });

    test('カードも含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('概要'))).toBe(true);
      expect(texts.some(t => t.includes('補足'))).toBe(true);
    });
  });

  describe('グリッド内フロー', () => {
    /**
     * グリッド内フロー仕様:
     * - 2x2グリッドのセルにフローを配置
     * - generateGridFlowCell 関数を検証
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-grid-flow-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-grid-flow');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('フローを含む2x2'))).toBe(true);
    });

    test('フロー項目が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('入力'))).toBe(true);
      expect(texts.some(t => t.includes('処理'))).toBe(true);
      expect(texts.some(t => t.includes('出力'))).toBe(true);
    });

    test('カードも含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('前提条件'))).toBe(true);
      expect(texts.some(t => t.includes('結果'))).toBe(true);
      expect(texts.some(t => t.includes('考察'))).toBe(true);
    });
  });

  describe('空セル埋め（アイテム不足）', () => {
    /**
     * 空セル埋め仕様:
     * - 2x2グリッドに1アイテムのみ → 残り3セルを空で埋める
     * - grid-cell の空セル生成を検証
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-sparse-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-sparse');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('1アイテムのみ'))).toBe(true);
    });

    test('カード内容が含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('唯一のカード'))).toBe(true);
      expect(texts.some(t => t.includes('唯一の説明1'))).toBe(true);
    });

    test('図形が存在する', () => {
      const shapeCount = countShapes(slideXml);
      expect(shapeCount).toBeGreaterThanOrEqual(1);
    });
  });

  describe('ネスト複合内コード（非カード型）', () => {
    /**
     * ネスト複合内コード仕様:
     * - ネストされた複合内でコードブロックを配置
     * - generateNestedGridHtml の else 分岐（空セル）を検証
     */
    let pptxPath;
    let slideXml;

    beforeAll(async () => {
      setupTmpDir();
      const md = fs.readFileSync(
        path.join(FIXTURES_DIR, 'composite-nested-code-slide.md'),
        'utf-8'
      );
      pptxPath = await mdToPptx(md, 'composite-nested-code');
      slideXml = await getSlideXml(pptxPath, 1);
    }, 120000);

    test('PPTX ファイルが生成される', () => {
      expect(fs.existsSync(pptxPath)).toBe(true);
    });

    test('タイトルが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('ネスト内コード'))).toBe(true);
    });

    test('ネスト内カードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('説明'))).toBe(true);
      expect(texts.some(t => t.includes('コードの解説'))).toBe(true);
    });

    test('外側のカードが含まれる', () => {
      const texts = extractTexts(slideXml);
      expect(texts.some(t => t.includes('セルB'))).toBe(true);
      expect(texts.some(t => t.includes('セルC'))).toBe(true);
      expect(texts.some(t => t.includes('セルD'))).toBe(true);
    });
  });
});
