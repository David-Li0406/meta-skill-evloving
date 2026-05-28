# React メモ化パターン リファレンス

## メモ化が必要な場合の判断基準

### 1. React.memo が有効な場合

**パターン**: 親コンポーネントが頻繁に再レンダリングされるが、子コンポーネントへの props が変わらない

```javascript
// 子コンポーネント
const UserCard = ({ user, onSelect }) => {
  return <div onClick={() => onSelect(user.id)}>{user.name}</div>;
};

export default React.memo(UserCard);
```

**検出ポイント**:
- 子コンポーネントが大きい、または複雑な計算を含む
- 親コンポーネントが複数回再レンダリングされる可能性
- props がほぼ変わらない

---

## 2. useCallback が必要な場合

**パターン**: コールバック関数が子コンポーネント（特に memo でラップされたコンポーネント）へ props として渡される

```javascript
// ❌ メモ化なし - 毎回新しい関数が作成される
function ParentComponent() {
  const handleClick = (id) => {
    console.log(id);
  };
  return <MemoChild onSelect={handleClick} />;
}

// ✅ useCallback でメモ化
function ParentComponent() {
  const handleClick = useCallback((id) => {
    console.log(id);
  }, []); // 依存配列
  return <MemoChild onSelect={handleClick} />;
}
```

**検出ポイント**:
- 関数が依存配列を持たずにインラインで定義されている
- その関数が memo コンポーネントへ props として渡されている
- 関数内で外部状態（state, props）を参照している場合は、それを依存配列に含める

---

## 3. useMemo が必要な場合

**パターン**: 計算コストが高い値が何度も計算される、またはその値をコールバックの依存配列に含める場合

```javascript
// ❌ メモ化なし - レンダリング毎に計算
function DataDisplay({ items }) {
  const filteredItems = items.filter(item => item.active);
  const sortedItems = filteredItems.sort((a, b) => a.name.localeCompare(b.name));
  return <List items={sortedItems} />;
}

// ✅ useMemo でメモ化
function DataDisplay({ items }) {
  const sortedItems = useMemo(() => {
    const filtered = items.filter(item => item.active);
    return filtered.sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);
  return <List items={sortedItems} />;
}
```

**検出ポイント**:
- 複数のループやソート処理
- 文字列操作などの計算処理
- オブジェクト/配列の生成
- その値が依存配列に含まれる

---

## 4. 依存配列の正確さ

```javascript
// ❌ 依存配列が不正確
useCallback(() => {
  handleDelete(selectedItems); // selectedItems を使用
}, []); // selectedItems が依存配列にない！

// ✅ 正確な依存配列
useCallback(() => {
  handleDelete(selectedItems);
}, [selectedItems]);
```

---

## メモ化を避けるべき場合

1. **シンプルなコンポーネント** - 再レンダリングコストが低い
2. **常に props が変わる** - memo の効果がない
3. **参照比較が複雑** - カスタムコンパレータが必要で、パフォーマンス向上が不明確
4. **複数の箇所でメモ化** - 複雑性が増加し、保守が困難

---

## 検出スクリプト

`scripts/detect-memoization.js` を使用して、ファイルを自動スキャンできます。
