---
name: table-creator
description: 用于透视表的创建，当用于需要基于明细数据做出分析或者展示时调用
---

# Table Creator

用于透视表的创建，当用于需要基于明细数据做出分析或者展示时调用

## 创建步骤

1. 基于 <https://github.com/antvis/S2> 这个库生成透视表

    - 如果用户的代码环境是 .js : 使用 `@antv/s2`
    - 如果用户的代码环境是 React: 使用 `@antv/s2-react`
    - 如果用户的代码环境是 Vue 的使用 `@antv/s2-vue`
    - 其他场景兜底使用 `@antv/s2`

2. 使用用户本地已安装的包管理器安装依赖，比如：

```bash
npm install @antv/s2 --save
yarn add @antv/s2
pnpm add @antv/s2
```

切记不需要额外安装包管理器

## 代码示例

```ts
import { PivotSheet } from '@antv/s2';

async function bootstrap() {
  const container = document.getElementById('container');

  const s2DataConfig = await fetch('https://assets.antv.antgroup.com/s2/en-data-config.json')
    .then(r => r.json())

  const s2 = new PivotSheet(container, s2DataConfig, {
    width: 600,
    height: 400,
  });

  await s2.render();
}

bootstrap()
```

## API 文档

参考：<https://s2.antv.antgroup.com>
