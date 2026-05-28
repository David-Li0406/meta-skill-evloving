# API配置说明 - Weibo Trends Analyzer

## 当前配置

### 内置天行数据API

**接口地址**：https://apis.tianapi.com/weibohot/index?key=4dfdf794141101d7bb8ece0294dbbc02

**提供商**：天行数据 (TianAPI)
**官网**：https://www.tianapi.com/
**文档**：https://www.tianapi.com/apiview/223

### API特性

- ✅ **实时更新**：数据与微博官方热搜同步
- ✅ **免费使用**：基础配额免费
- ✅ **稳定可靠**：正规第三方数据服务商
- ✅ **丰富数据**：包含热搜关键词、热度值、标签

### 返回数据格式

```json
{
  "code": 200,
  "msg": "success",
  "result": {
    "list": [
      {
        "hotword": "初中生网购疑似侵华日军信件",
        "hotwordnum": " 1061066",
        "hottag": ""
      },
      {
        "hotword": "社保工作人员骗养老金多少蛀虫待清理",
        "hotwordnum": " 751575",
        "hottag": "新"
      },
      {
        "hotword": "痞幼上恋综进医院",
        "hotwordnum": "综艺 587870",
        "hottag": ""
      }
      // ... 更多数据
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| code | Number | 状态码，200表示成功 | 200 |
| msg | String | 返回消息 | "success" |
| result.list | Array | 热搜列表 | [...] |
| hotword | String | 热搜关键词 | "人工智能大模型" |
| hotwordnum | String | 热度值（可能含分类前缀） | "1234567" 或 "综艺 587870" |
| hottag | String | 标签：新/热/荐 | "新" |

### 数据解析规则

1. **排名**：由数组位置推断（index + 1）
2. **热度值**：从`hotwordnum`提取数字，去除分类前缀
3. **分类**：从`hotwordnum`提取前缀（如"综艺"、"剧集"、"盛典"）
4. **标签含义**：
   - "新"：新上榜
   - "热"：热度上升
   - "荐"：官方推荐
   - ""：普通热搜

---

## 更换API密钥

如果内置密钥达到请求限制，可以自行注册获取新密钥：

### 步骤1：注册账号

访问 https://www.tianapi.com/ 注册免费账号

### 步骤2：获取密钥

1. 登录后进入控制台
2. 找到"微博热搜"接口
3. 复制API Key

### 步骤3：更新Skill

编辑 `.claude/skills/weibo-trends-analyzer/SKILL.md`：

找到第16行：
```markdown
**Default API**: https://apis.tianapi.com/weibohot/index?key=4dfdf794141101d7bb8ece0294dbbc02
```

替换为你的密钥：
```markdown
**Default API**: https://apis.tianapi.com/weibohot/index?key=YOUR_NEW_KEY
```

---

## API使用限制

### 免费版限制

- 每日请求次数：100次（具体以天行数据官网为准）
- 并发限制：可能有限制
- 数据时效：实时

### 建议

- ✅ 合理使用，避免频繁请求
- ✅ 分析时限定热搜数量（推荐10-15个）
- ✅ 不要在短时间内重复分析
- ✅ 如需高频使用，考虑升级付费版

---

## 使用其他API

如果你有其他微博热搜API，可以修改Skill适配：

### 修改步骤

1. 编辑 `SKILL.md` 第16-60行，更新API地址和数据格式
2. 根据新API的返回结构，调整字段映射规则
3. 测试确保数据解析正常

### 示例：适配自建API

如果你的API返回格式为：
```json
{
  "data": {
    "trends": [
      {"title": "热搜", "value": 123456}
    ]
  }
}
```

需要修改SKILL.md中的字段映射：
```markdown
**Field Mapping**:
- `title` → Trending keyword
- `value` → Heat value
- Ranking position → Inferred from array index
```

---

## 测试API

### 命令行测试

```bash
curl -s "https://apis.tianapi.com/weibohot/index?key=4dfdf794141101d7bb8ece0294dbbc02"
```

### 浏览器测试

直接访问：
```
https://apis.tianapi.com/weibohot/index?key=4dfdf794141101d7bb8ece0294dbbc02
```

### 预期结果

- 返回code=200
- result.list包含多条热搜数据
- 每条数据包含hotword、hotwordnum、hottag字段

---

## 故障排除

### 问题1：API返回错误码

**可能原因**：
- 密钥无效或过期
- 达到请求次数限制
- 网络连接问题

**解决方案**：
1. 检查密钥是否正确
2. 等待限额重置（通常每日00:00重置）
3. 注册新账号获取新密钥

### 问题2：返回数据为空

**可能原因**：
- API暂时无数据
- 接口维护

**解决方案**：
1. 稍后重试
2. 使用测试数据验证Skill功能
3. 联系天行数据客服

### 问题3：数据格式解析失败

**可能原因**：
- API返回格式变更
- 字段名称变化

**解决方案**：
1. 手动测试API查看最新格式
2. 更新SKILL.md中的字段映射
3. 提交Issue反馈

---

## 备用方案

### 使用测试数据

如果API不可用，可以使用项目中的测试数据：

`.claude/skills/weibo-trends-analyzer/weibo-mock-data.json`

这个文件包含15个模拟热搜话题，格式与真实API完全一致。

---

## 联系支持

**天行数据客服**：
- 官网：https://www.tianapi.com/
- QQ群：见官网
- 在线客服：工作日9:00-18:00

**Skill问题反馈**：
- 在Claude Code对话中直接询问
- 查看官方文档

---

**Last Updated**: 2026-01-11
**API Version**: TianAPI Weibo Hot v1.0
**Skill Version**: 1.0
