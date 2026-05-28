# Action: match-local-skills

扫描本地已安装的 skills，匹配用户需求。

## 输入

- `state.request_analysis`: 请求分析结果

## 处理逻辑

```javascript
// 1. 扫描本地skills目录
const localSkills = scanLocalSkills();
// ~/.claude/skills/ 和 .claude/skills/

// 2. 读取每个skill的元数据
for (const skill of localSkills) {
  const metadata = readSkillMetadata(skill);
  // 读取 SKILL.md 的 frontmatter
}

// 3. 计算匹配度
const matches = localSkills.map(skill => {
  return {
    name: skill.name,
    description: skill.description,
    score: calculateMatchScore(state.request_analysis, skill),
    source: "local"
  };
}).filter(m => m.score > 0.3);

// 4. 排序
state.matched_skills = matches.sort((a, b) => b.score - a.score);
state.execution_status = "matching";
```

## 匹配算法

```javascript
function calculateMatchScore(analysis, skill) {
  let score = 0;

  // 关键词匹配 (权重 0.6)
  const keywordMatches = analysis.keywords.filter(kw =>
    skill.description.toLowerCase().includes(kw.toLowerCase()) ||
    skill.name.toLowerCase().includes(kw.toLowerCase())
  );
  score += (keywordMatches.length / analysis.keywords.length) * 0.6;

  // 意图匹配 (权重 0.4)
  if (skill.category === analysis.intent) {
    score += 0.4;
  }

  return score;
}
```

## 输出

- `state.matched_skills`: 匹配的本地skills列表
- `state.execution_status = "matching"`

## 下一步

- 有匹配 → [present-options](04-present-options.md)
- 无匹配 → [search-skills-sh](03-search-skills-sh.md)
