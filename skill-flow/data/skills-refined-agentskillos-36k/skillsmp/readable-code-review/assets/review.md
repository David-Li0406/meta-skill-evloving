<instructions>
1. プランに従って1レビュー単位でチェックを行ってください。
2. チェックが完了したら、`<reviewed>true</reviewed>`に変更してください。
3. レビュー結果を`.claude/skills/readable-code-review/assets/result.md`をもとに生成します。
    - レビュー結果のファイルはこのファイルと同じフォルダに保存されます。
    - {ruleId}はreveiwごとに番号が振られます。番号はitemの番号が`1.x`なら`1`、`2.x`なら`2`と判断します。
    - 結果ファイル名は`readable-review-{連番}-result-{ruleId}.md`となります。
4. これを繰り返し、すべてのレビューが完了したら終了してください。

**注意**：関数とは、クラスメソッドを含みます
**注意**：check-listのルールは厳守です。勝手に必要ないと判断することを禁じます。
<instructions>

<plan>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>1.1 抽象的(Get, Foo)や複数の解釈ができる単語を使ってはいけないこと</item>
      <item>1.2 関数は具体的に何をするのかを誤解せずに名前から読み取れること
        <important>
        - 型情報（戻り値の型、`async` キーワードなど）やコンテキスト（関数の使用箇所、引数の型など）から動作が明確に推測できる場合は、**1.7のルールを優先**して冗長な動詞（`get`, `fetch`, `create`, `build` など）を削除することを推奨
        - 例：`async channelNames(...): Promise<string[]>` のように、戻り値の型から「取得する」動作が明確な場合、`getChannelNames` ではなく `channelNames` で十分
        - 例：`convertXToY` のように `To` や `From` などの接頭辞/接尾辞で変換の方向性が明確な場合、`convert` は冗長な可能性がある
        </important>
      </item>
      <item>1.3 関数名と使用目的が一致していること</item>
      <item>1.4 booleanの変数、関数は具体的な用途・目的を誤解せずに名前から読み取れること</item>
      <item>1.5 接尾辞や接頭辞を使って単位や属性情報を追加していること</item>
      <item>1.6 10行以上のスコープ内でvやiなどの名前を使っていないこと</item>
      <item>1.7 なくても理解できる単語は削ること（ConvertToStringはToStringにできる）</item>
      <item>1.8 名前のフォーマットに一貫性があること
        <important>コード全体で一貫した命名規則（例：すべての取得関数に `get` プレフィックスを使用）が確立されている場合でも、**1.7のルールを優先**する</important>
      </item>
      <item>1.9 境界値を示す単語は(min,max)(first,last)(begin,end)などを使い、「以下」と「未満」の違いがわかるようにすること</item>
    </check-list>
  </review>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>2.1 定義の並び順は一貫性を持たせること</item>
      <item>2.2 定義と処理は意味のあるグループごとに段落を分けること</item>
    </check-list>
  </review>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>3.1 コードからすぐに分かる（ジュニアエンジニアが1秒以下で理解できること）コメントは削除すること
        <important>ただし、**3.3のルールを優先**。クラス名、関数名、プロパティ名、定数名などのコメントは日本語で維持または追加する。</important>
      </item>
      <item>3.2 複雑な内容（ジュニアエンジニアが理解に10秒以上かかる）はコメントを書くこと</item>
      <item>3.3 クラス名、関数名(コンストラクタは対象外)、プロパティ名、定数名の日本語コメントを書くこと</item>
      <item>3.4 実装意図が分かりづらい、または特殊なものにはコメントを書くこと</item>
      <item>3.5 改善が必要な箇所には`TODO:`コメントを書くこと</item>
      <item>3.6 未完成の箇所には`TODO:`コメントを書くこと</item>
      <item>3.7 定数は、なぜその値にしたのか不明な場合にはコメントを書くこと</item>
      <item>3.8 「それ」や「これ」などの曖昧な代名詞は名詞に書き換えること</item>
      <item>3.9 誤解や複数の解釈ができるコメントは書き換えること</item>
      <item>3.10 説明が複雑な関数コメントは実例も書くこと</item>
    </check-list>
  </review>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>4.1 条件式は左が調査対象、右が比較対象になっていること</item>
      <item>4.2 条件は下記で最も効果的な書き方になっていること
        <important>
        - 関心ごとの高い条件を先に書くこと(優先度:高) or 単純な条件を先に書くこと(優先度:低)
        - 条件は否定形より肯定形を使うこと
        </important>
      </item>
      <item>4.3 2つの値から1つを選ぶような単純な条件は三項演算子,null合体演算子,エルビス演算子を使うこと</item>
      <item>4.4 do/whileループや疑似do/whileはwhileループに書き直すこと</item>
      <item>4.5 適切にガード節を使うこと</item>
      <item>4.6 ネストは浅くすること
        <sub-item>失敗ケースは早い段階で`return`する</sub-item>
        <sub-item>ループ内部のifはできる限り`continue`をつかう</sub-item>
      </item>
    </check-list>
  </review>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>5.1 複雑な式は説明クラスメソッドを作ること</item>
      <item>5.2 複雑な論理式は要約クラスメソッドを作ること</item>
      <item>5.3 固定値は説明変数または定数を作ること</item>
      <item>5.4 簡潔で、明確で、一度しか使われていない式の一時変数は作らないこと
        <important>
        - 例：`const result = a + b;` のような単純な式は一時変数不要
        - 例：`const isValid = user.age >= 18 && user.hasLicense && !user.isSuspended;` のような複雑な論理式は**5.1〜5.3のルールを検討**
        </important>
      </item>
    </check-list>
  </review>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>6.1 中間結果を保持する変数は、使わずに実装できないか考えること</item>
      <item>6.2 制御フロー変数は、使わずに実装できないか考えること</item>
      <item>6.3 クラスのプロパティは、クラスメソッドのローカル引数にできないか考えること</item>
      <item>6.4 クラスメソッドはstaticにできないか考えること</item>
      <item>6.5 変数への代入は1度だけとすること</item>
    </check-list>
  </review>
  <review>
    <filepath>{対象ファイルパス}</filepath>
    <reviewed>false</reviewed>
    <check-list>
      <item>7.1 下位目的を解決するためのコードは別の関数にすること
        <important>
        - 関数コメントの内容が上位目的となる
        - 取得、セット、更新、削除、変換、除外、事前処理、事後処理などが下位目的になりやすい
        - 判断基準：関数が「**7.3のルールを満たす内容**」（1行1行が簡単な言葉で説明できる）であり、かつ「**7.2のルールを守っている**」（一つの目的のみを達成）場合、さらに分割する必要はない
        - 例：上位目的が「2点の距離を求める」ならば、下位目的は2点の距離を求めるために、「点をラジアンに変換する」
        - 例：3行程度の単純な関数をさらに分割する必要はない
        </important>
      </item>
      <item>7.2 一つの関数で一つの目的のみを達成すること（コントローラのメソッドは含めない）</item>
      <item>7.3 コードの１行１行が簡単な言葉で説明できる内容であること</item>
    </check-list>
  </review>
</plan>
