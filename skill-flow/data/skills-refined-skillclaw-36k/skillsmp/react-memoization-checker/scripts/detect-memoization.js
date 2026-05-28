#!/usr/bin/env node

/**
 * React メモ化チェッカー
 * 
 * 使用方法:
 *   node detect-memoization.js <filePath>
 * 
 * 例:
 *   node detect-memoization.js src/components/UserCard.jsx
 */

const fs = require('fs');
const path = require('path');

const filePath = process.argv[2];

if (!filePath) {
  console.error('エラー: ファイルパスを指定してください');
  process.exit(1);
}

if (!fs.existsSync(filePath)) {
  console.error(`エラー: ファイルが見つかりません: ${filePath}`);
  process.exit(1);
}

const code = fs.readFileSync(filePath, 'utf8');
const issues = [];

// 1. React.memo が使われていない関数コンポーネントを検出
const functionComponentRegex = /^(export\s+)?(const|function)\s+(\w+)\s*=?\s*\(\s*({[^}]*}|[^)]*)\s*\)\s*(?:=>|{)/gm;
const matches = [...code.matchAll(functionComponentRegex)];

matches.forEach(match => {
  const fullMatch = match[0];
  const isExported = match[1];
  const componentName = match[3];
  
  // React.memo でラップされているか確認
  if (!code.includes(`React.memo(${componentName}`) && !code.includes(`memo(${componentName}`)) {
    issues.push({
      type: 'MISSING_MEMO',
      line: code.substring(0, match.index).split('\n').length,
      component: componentName,
      message: `${componentName} が React.memo でラップされていません`,
      severity: 'warning'
    });
  }
});

// 2. useCallback なしで関数が props に渡されている
const callbackPropsRegex = /(\w+)=\{(\w+)\s*=>\s*|(\w+)=\{function\s*(\w+)/g;
const callbackMatches = [...code.matchAll(callbackPropsRegex)];

callbackMatches.forEach(match => {
  if (!code.includes('useCallback')) {
    const lineNum = code.substring(0, match.index).split('\n').length;
    issues.push({
      type: 'MISSING_CALLBACK',
      line: lineNum,
      message: 'useCallback なしでコールバック関数が渡されています',
      severity: 'info'
    });
  }
});

// 3. useMemo なしで複雑な計算が行われている
const complexCalculationRegex = /\.filter\s*\(|\.map\s*\(|\.reduce\s*\(|\.sort\s*\(/g;
const calcMatches = [...code.matchAll(complexCalculationRegex)];

if (calcMatches.length > 0 && !code.includes('useMemo')) {
  issues.push({
    type: 'MISSING_MEMO_VALUE',
    message: '複雑な計算（filter, map, reduce, sort）が useMemo なしで実行されています',
    severity: 'info'
  });
}

// 4. 依存配列の欠落チェック
const emptyDependencyRegex = /use(Callback|Effect|Memo)\s*\([^,]*,\s*\[\s*\]/g;
const emptyDepMatches = [...code.matchAll(emptyDependencyRegex)];

emptyDepMatches.forEach(match => {
  const hook = match[1];
  const lineNum = code.substring(0, match.index).split('\n').length;
  issues.push({
    type: 'EMPTY_DEPENDENCY',
    line: lineNum,
    hook: hook,
    message: `${hook} の依存配列が空です。意図的な場合は問題ありませんが、確認してください`,
    severity: 'warning'
  });
});

// 結果を出力
console.log(`\n📋 メモ化チェック結果: ${filePath}\n`);

if (issues.length === 0) {
  console.log('✅ メモ化に関する問題は検出されませんでした');
  process.exit(0);
}

console.log(`⚠️  ${issues.length} 件の項目が見つかりました:\n`);

issues.forEach((issue, idx) => {
  const icon = issue.severity === 'error' ? '❌' : issue.severity === 'warning' ? '⚠️' : 'ℹ️';
  console.log(`${idx + 1}. ${icon} [${issue.type}] ${issue.message}`);
  if (issue.line) console.log(`   行: ${issue.line}`);
  if (issue.component) console.log(`   コンポーネント: ${issue.component}`);
  console.log('');
});

process.exit(issues.some(i => i.severity === 'error') ? 1 : 0);
