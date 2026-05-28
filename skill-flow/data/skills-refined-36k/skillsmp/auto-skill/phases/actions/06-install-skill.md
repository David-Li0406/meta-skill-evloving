# Action: install-skill

从 skills.sh 安装选定的 skill。

## 输入

- `state.selected_skill`: 用户选择的skill信息
- `state.search_results`: 搜索结果（包含安装信息）

## 处理逻辑

```javascript
const skillToInstall = state.search_results.find(
  r => r.name === state.selected_skill
);

if (!skillToInstall) {
  throw new Error("无法找到安装信息");
}

// 1. 获取安装方式
const installMethod = await AskUserQuestion({
  question: `如何安装 ${skillToInstall.name}？`,
  header: "安装方式",
  options: [
    {
      label: "自动安装 (推荐)",
      description: `执行: npx @claudecode/skills install ${skillToInstall.name}`
    },
    {
      label: "手动安装",
      description: "提供安装命令，由你手动执行"
    },
    {
      label: "取消",
      description: "放弃安装"
    }
  ]
});

// 2. 执行安装
state.execution_status = "installing";

if (installMethod === "自动安装") {
  await Bash({
    command: `npx @claudecode/skills install ${skillToInstall.name}`,
    description: `安装 skill: ${skillToInstall.name}`
  });
  state.installation_status = "completed";
} else if (installMethod === "手动安装") {
  console.log(`请手动执行: npx @claudecode/skills install ${skillToInstall.name}`);
  await AskUserQuestion({
    question: "安装完成后点击继续",
    header: "等待安装",
    options: [{ label: "已完成", description: "继续执行" }]
  });
  state.installation_status = "completed";
}
```

## 安装验证

```javascript
// 验证安装成功
function verifySkillInstalled(skillName) {
  const skillPath = `~/.claude/skills/${skillName}`;
  return fs.existsSync(skillPath);
}
```

## 输出

- `state.installation_status = "completed"`
- `state.execution_status = "installing"`

## 下一步

→ [execute-skill](05-execute-skill.md)
