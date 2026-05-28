# API 接口开发 SOP

面向 AI 代理的最小指引，保证能够在现有架构中新增或改写 API。

## 基础约定
- 后端运行在 EdgeOne Functions（Node 22.13.0）与 Hono 之上；每个路由文件位于 `apps/server/functions/routers/*`，需默认导出 `new Hono<{ Bindings: ... }>()`。
- 新增路由后，记得在 `functions/routers/index.ts` 导出并在 `functions/index.tsx` 中使用 `app.route('/xxx', router)` 注册。
- 所有共享类型或工具优先复用 `apps/server/utils/*`。

## 快速模板
```ts
import { Hono } from 'hono'
import { createErrorResponse, createSuccessResponse } from '@/utils/response'
import type { DataBaseEnvBindings } from '@/utils/db'

const demo = new Hono<{ Bindings: DataBaseEnvBindings }>()

demo.post('/', async (c) => {
  try {
    const payload = await c.req.json<{ foo?: string }>().catch(() => null)
    if (!payload?.foo)
      return c.json(createErrorResponse('缺少 foo 参数', 400), 400)

    return c.json(createSuccessResponse({ foo: payload.foo }))
  }
  catch (err) {
    const message = err instanceof Error ? err.message : '服务器内部错误'
    return c.json(createErrorResponse(message, 500), 500)
  }
})

export default demo
```

## 请求校验
- 所有输入都要做最小化校验，可使用 `zod` 或正则，失败时以 `400` 配合 `createErrorResponse` 返回；文案要明确。

## 环境变量
- 公共绑定类型 `DataBaseEnvBindings` 位于 `apps/server/utils/db.ts`；如需额外变量，定义本地接口继承并在 `Context` 泛型中声明。
- 获取必需变量应封装 `getEnvOrThrow(c, 'KEY')`，缺失时抛出错误以进入统一 catch；可选变量允许 `undefined` 并设置默认值。

## 响应规范
- 统一使用 `createSuccessResponse` / `createErrorResponse`，保证返回 `{ code, message, data, timestamp }`。
- HTTP 状态码与业务 code 对齐：成功 200，校验失败 4xx，未知错误 500。
- 不在响应中泄露敏感凭证；调试信息可放进 `data` 的安全字段内。

## 外部服务
- Supabase：使用 `createSupabaseClient(c.env)`，按需调用 `.maybeSingle()`、`auth.signInWithOtp` 等方法；在业务逻辑层处理资源存在性并返回合理状态码。
- 其他三方服务请先抽象工具函数（如短信签名），将请求头、签名流程与错误处理集中在工具内，再被路由调用。

## 调试与测试
- 开发时使用 `pnpm dev:start` 启动本地 Edge 环境；临时调试路由需在合并前移除或加保护。

遵循以上约定即可与现有代码风格保持一致，确保 AI 生成的 API 路由可直接运行与维护。
