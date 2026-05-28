# Table Creator Reference

用于透视表的创建，当用于需要基于明细数据做出分析或者展示时调用，以下是调用示意

## Overview

用于透视表的创建，当用于需要基于明细数据做出分析或者展示时调用

## Create

```python
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

## License Information

- **@antv/s2**: MIT License
