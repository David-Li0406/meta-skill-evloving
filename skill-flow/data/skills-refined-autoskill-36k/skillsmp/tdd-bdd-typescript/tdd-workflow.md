# TDDワークフロー詳細ガイド

## Red-Green-Refactorサイクル詳細

### 0. TODOリストを作成

```
実装前に以下を明確にする:
1. 何を作るのか（機能の目的）
2. どのような振る舞いが期待されるか
3. 正常系・異常系・境界値のケース
```

```typescript
// TODOリストの例
/**
 * クイズ回答機能
 * - [x] 正解の場合、スコアが1増える
 * - [x] 正解の場合、次の問題に進む
 * - [ ] 不正解1回目、同じ問題を繰り返す
 * - [ ] 不正解2回目、ヒントを表示
 * - [ ] 不正解3回目、正解を表示して次へ
 * - [ ] 全問終了時、最終スコアを表示
 */
```

### 1. Red: 失敗するテストを書く

**目的**: 実装前に「何が期待されるか」を明確にする

```typescript
describe('AnswerHandler', () => {
  describe('Given: 1回目の回答で不正解の場合', () => {
    // 事前条件を明示的に設定
    const createFixture = () => ({
      sessionState: {
        questionIndex: 2,
        score: 1,
        incorrectCount: 0,  // まだ間違えていない
      },
      currentQuestion: {
        question: '青森県の県庁所在地は？',
        answer: '青森',
      },
      userAnswer: '弘前',  // 不正解
    });

    it('When: 回答を処理する Then: 不正解カウントが増える', () => {
      // Given
      const { sessionState, currentQuestion, userAnswer } = createFixture();
      const handler = createAnswerHandler();

      // When
      const result = handler.process({
        sessionState,
        currentQuestion,
        userAnswer,
      });

      // Then
      expect(result.sessionState.incorrectCount).toBe(1);
    });

    it('When: 回答を処理する Then: 同じ問題が継続される', () => {
      // Given
      const { sessionState, currentQuestion, userAnswer } = createFixture();
      const handler = createAnswerHandler();

      // When
      const result = handler.process({
        sessionState,
        currentQuestion,
        userAnswer,
      });

      // Then
      expect(result.sessionState.questionIndex).toBe(2); // 変わらない
      expect(result.shouldRepeatQuestion).toBe(true);
    });

    it('When: 回答を処理する Then: 再挑戦を促すメッセージが返る', () => {
      // Given
      const { sessionState, currentQuestion, userAnswer } = createFixture();
      const handler = createAnswerHandler();

      // When
      const result = handler.process({
        sessionState,
        currentQuestion,
        userAnswer,
      });

      // Then
      expect(result.message).toContain('もう一度');
    });
  });
});
```

**Redフェーズのルール**:
- テストは1つずつ書く
- 実行して失敗することを確認する
- 失敗メッセージが「意図通り」か確認する

### 2. Green: 最小限のコードで成功させる

**目的**: テストを通す最も単純な実装

```typescript
// 最小限の実装（完璧でなくてよい）
function createAnswerHandler() {
  return {
    process(input: AnswerInput): AnswerResult {
      const { sessionState, currentQuestion, userAnswer } = input;
      
      const isCorrect = currentQuestion.answer === userAnswer;
      
      if (isCorrect) {
        return {
          sessionState: {
            ...sessionState,
            score: sessionState.score + 1,
            questionIndex: sessionState.questionIndex + 1,
            incorrectCount: 0,
          },
          shouldRepeatQuestion: false,
          message: 'そうです！',
        };
      }
      
      // 不正解の場合
      const newIncorrectCount = sessionState.incorrectCount + 1;
      
      return {
        sessionState: {
          ...sessionState,
          incorrectCount: newIncorrectCount,
        },
        shouldRepeatQuestion: true,
        message: `${userAnswer}？ もう一度考えてみてください。`,
      };
    },
  };
}
```

**Greenフェーズのルール**:
- テストが通る最小限のコードを書く
- 「仮実装」でもよい（ハードコード可）
- 設計の美しさは後で考える

### 3. Refactor: テストが緑のまま改善

**目的**: コードの品質向上（動作は変えない）

```typescript
// リファクタリング後
interface AnswerInput {
  sessionState: SessionState;
  currentQuestion: Question;
  userAnswer: string;
}

interface AnswerResult {
  sessionState: SessionState;
  shouldRepeatQuestion: boolean;
  message: string;
}

function createAnswerHandler() {
  const handleCorrectAnswer = (state: SessionState): AnswerResult => ({
    sessionState: {
      ...state,
      score: state.score + 1,
      questionIndex: state.questionIndex + 1,
      incorrectCount: 0,
    },
    shouldRepeatQuestion: false,
    message: 'そうです！',
  });

  const handleIncorrectAnswer = (
    state: SessionState,
    userAnswer: string
  ): AnswerResult => ({
    sessionState: {
      ...state,
      incorrectCount: state.incorrectCount + 1,
    },
    shouldRepeatQuestion: true,
    message: `${userAnswer}？ もう一度考えてみてください。`,
  });

  return {
    process({ sessionState, currentQuestion, userAnswer }: AnswerInput): AnswerResult {
      const isCorrect = currentQuestion.answer === userAnswer;
      return isCorrect
        ? handleCorrectAnswer(sessionState)
        : handleIncorrectAnswer(sessionState, userAnswer);
    },
  };
}
```

**Refactorフェーズのルール**:
- テストを実行しながら小さく変更
- 変数名・関数名の改善
- 重複の排除（DRY）
- 関数の分割（SRP）

## サイクルの繰り返し

```
[TODOリスト]
- [x] 正解の場合、スコアが増える
- [x] 不正解1回目、同じ問題を繰り返す
- [ ] 不正解2回目、ヒントを表示        ← 次はこれ
- [ ] 不正解3回目、正解を表示して次へ

↓ 次のテストを書く

describe('Given: 2回目の回答で不正解の場合', () => {
  it('When: 回答を処理する Then: ヒントが表示される', () => {
    // Given
    const fixture = createFixture({
      incorrectCount: 1,  // すでに1回間違えている
    });
    
    // When
    const result = handler.process(fixture);
    
    // Then
    expect(result.message).toContain('ヒント');
  });
});
```

## アサーションのベストプラクティス

### 1テスト1アサーション（理想）

```typescript
// 良い例: 検証項目が明確
it('スコアが1増える', () => {
  const result = handler.processCorrectAnswer(state);
  expect(result.score).toBe(state.score + 1);
});

it('次の問題に進む', () => {
  const result = handler.processCorrectAnswer(state);
  expect(result.questionIndex).toBe(state.questionIndex + 1);
});
```

### 関連するアサーションのグループ化

```typescript
// 許容例: 論理的に関連するアサーション
it('正解時の状態が正しく更新される', () => {
  const result = handler.processCorrectAnswer(state);
  
  expect(result).toEqual({
    score: state.score + 1,
    questionIndex: state.questionIndex + 1,
    incorrectCount: 0,
  });
});
```

## テストの命名規則

```typescript
// パターン1: Given-When-Then形式
describe('Given: [事前条件]', () => {
  describe('When: [操作]', () => {
    it('Then: [期待結果]', () => {});
  });
});

// パターン2: シンプル形式
describe('[テスト対象]', () => {
  it('[条件]の場合、[期待結果]', () => {});
});

// パターン3: 日本語
describe('回答処理', () => {
  describe('正解の場合', () => {
    it('スコアが1増えること', () => {});
    it('次の問題に進むこと', () => {});
  });
});
```
