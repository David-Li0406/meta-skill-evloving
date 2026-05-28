---
name: plasmo
description: Use when working with Plasmo framework for building browser extensions. This skill covers React/TypeScript-based extension development including content scripts, CSUI, background workers, messaging, storage, and manifest configuration.
---

# Plasmo - 浏览器扩展开发框架

Plasmo 是一个功能强大的浏览器扩展开发框架，专为使用 React 和 TypeScript 构建现代浏览器扩展而设计。它被称为"浏览器扩展的 Next.js"。

核心特性

- React + TypeScript 一等支持
- 声明式开发（抽象 manifest.json）
- Content Scripts UI（CSUI）- Shadow DOM 隔离
- Tab Pages - 独立标签页
- 实时重载 + React HMR
- .env\* 文件支持
- 内置 Storage API
- 内置 Messaging API
- 远程代码打包（如 Google Analytics）
- 多浏览器和 Manifest 版本支持
- 通过 BPP 自动部署
- 支持 Svelte 和 Vue

系统要求

- Node.js 16.14.x 或更高版本
- macOS, Windows 或 Linux
- 强烈推荐使用 pnpm

项目初始化

创建新项目：

# 交互式初始化

pnpm create plasmo

# 直接指定名称

pnpm create plasmo "My Extension"

# 使用特定入口文件

pnpm create plasmo --entry=options,newtab,contents/inline

# 使用示例模板

pnpm create plasmo --with-env

# 全局安装 CLI

pnpm i -g plasmo

默认项目结构：

.
├── popup.tsx # 扩展弹窗组件
├── assets/
│ └── icon.png # 扩展图标
├── package.json # 项目配置（包含 manifest 覆盖）
├── tsconfig.json # TypeScript 配置
└── .prettierrc.cjs # 代码格式化配置

使用 src 目录：

默认情况下，Plasmo 将所有源代码放在根目录。要使用 src 目录，遵循以下步骤：

1. 在 src 目录下创建项目
2. 在 package.json 中配置：

{
"manifest": {
"name": "my-extension"
}
}

3. Plasmo 会自动识别 src 目录

开发工作流

启动开发服务器：

pnpm dev

# 或

npm run dev

# 或

plasmo dev

开发服务器特性：

- 文件变更时自动重新构建
- React HMR 支持
- 扩展名称前缀为 "DEV |"
- 图标变为灰度以区分开发/生产构建

加载扩展：

1. 打开 chrome://extensions
2. 启用开发者模式
3. 点击"加载已解压的扩展程序"
4. 导航到 build/chrome-mv3-dev 目录

生产构建：

# 标准构建

pnpm build

# 构建并打包为 zip

pnpm build --zip

# 或

pnpm package

# 指定目标浏览器

plasmo build --target=firefox-mv2
plasmo build --target=safari-mv3

# 使用自定义标签

plasmo build --tag=staging

# 生成 source maps

plasmo build --source-maps

# 禁用压缩

plasmo build --no-minify

# 使用 hoist 优化

plasmo build --hoist

扩展页面

扩展页面是浏览器识别的内置页面。

Popup 页面（弹窗）：

创建 popup.tsx 或 popup/index.tsx：

function IndexPopup() {
return (

<div style={{ padding: 16 }}>
<h1>欢迎来到扩展</h1>
</div>
)
}

export default IndexPopup

Options 页面（选项页）：

创建 options.tsx 或 options/index.tsx

New Tab 页面（新标签页）：

创建 newtab.tsx 或 newtab/index.tsx

Side Panel（侧边栏）：

创建 sidepanel.tsx 或 sidepanel/index.tsx

Dev Tools 页面（开发者工具）：

创建 devtools.tsx 或 devtools/index.tsx

Tab Pages

Tab Pages 是 Plasmo 特有的功能，是随扩展包一起提供的常规网页。

创建 tab：

1. 在源目录创建 tabs 文件夹
2. 添加 .tsx 文件，如 delta-flyer.tsx
3. 导出默认 React 组件：

tabs/delta-flyer.tsx：

function DeltaFlyerPage() {
return (

<div style={{ display: "flex", flexDirection: "column", padding: 16 }}>
<h2>Delta Flyer Tab</h2>
<p>This tab is only available on the Delta Flyer page.</p>
</div>
)
}

export default DeltaFlyerPage

访问 URL：

chrome-extension://<extension-id>/tabs/delta-flyer.html

Content Scripts（内容脚本）

内容脚本在网页的隔离世界中运行，避免与网页的 JavaScript 冲突。

添加单个内容脚本：

创建 content.ts，导出一个空对象：

export {}

console.log("Content script loaded")

重要：如果代码没有导入或导出，必须添加 export {}，因为 Plasmo 的 TypeScript 配置将所有源文件视为模块。

添加多个内容脚本：

创建 contents 目录并添加多个内容脚本文件。

配置内容脚本：

import type { PlasmoCSConfig } from "plasmo"

export const config: PlasmoCSConfig = {
matches: ["<all_urls>"],
all_frames: true,
run_at: "document_idle"
}

注入到主世界：

export const config: PlasmoCSConfig = {
matches: ["<all_urls>"],
world: "MAIN"
}

从 background 服务工作者手动注入：

chrome.scripting.executeScript({
target: { tabId },
world: "MAIN",
func: windowChanger
})

Content Scripts UI（CSUI）

Plasmo 支持 React、Svelte3 或 Vue3 组件挂载到当前网页。CSUI 使用 Shadow DOM 实现样式隔离。

基本使用：

创建 content.tsx，导出默认 React 组件：

const CustomButton = () => {
return <button>Custom button</button>
}

export default CustomButton

配置 CSUI：

export const config: PlasmoCSConfig = {
matches: ["<all_urls>"]
}

CSUI 锚点（Anchor）：

Plasmo CSUI 锚点定义了组件的挂载方式和位置。

Overlay 锚点（覆盖）：

export const getOverlayAnchor: PlasmoGetOverlayAnchor = async () =>
document.querySelector("#pricing")

// 多个 overlay 锚点
export const getOverlayAnchorList: PlasmoGetOverlayAnchorList = async () =>
document.querySelectorAll("a")

自定义位置更新：

export const watchOverlayAnchor: PlasmoWatchOverlayAnchor = (
updatePosition
) => {
const interval = setInterval(() => {
updatePosition()
}, 8472)

return () => {
clearInterval(interval)
}
}

Inline 锚点（内联）：

export const getInlineAnchor: PlasmoGetInlineAnchor = async () =>
document.querySelector("#pricing")

// 带插入位置
export const getInlineAnchor: PlasmoGetInlineAnchor = async () => ({
element: document.querySelector("#pricing"),
insertPosition: "afterend"
})

CSUI 样式化：

导出样式元素：

import styleText from "data-text:./style.css"
import type { PlasmoGetStyle } from "plasmo"

export const getStyle: PlasmoGetStyle = () => {
const style = document.createElement("style")
style.textContent = styleText
return style
}

使用 Tailwind CSS：

import cssText from "data-text:~style.css"

export const getStyle = () => {
const style = document.createElement("style")
style.textContent = cssText
return style
}

const PlasmoOverlay = () => {
return (

<div className="p-4 bg-blue-500 text-white">
Hello from Tailwind
</div>
)
}

export default PlasmoOverlay

CSS-in-JS（Emotion）：

import createCache from "@emotion/cache"
import type { PlasmoGetStyle } from "plasmo"

const styleElement = document.createElement("style")

const styleCache = createCache({
key: "plasmo-emotion-cache",
prepend: true,
container: styleElement
})

export const getStyle: PlasmoGetStyle = () => styleElement

自定义 Shadow Root：

export const createShadowRoot: PlasmoCreateShadowRoot = (shadowHost) =>
shadowHost.attachShadow({ mode: "closed" })

自定义根容器：

export const getRootContainer = () =>
document.getElementById("custom-container")

Background Service Worker

Background Service Worker 在服务工作者上下文中运行，不受 CORS 限制，适合处理繁重计算。

创建 background.ts 或 background/index.ts：

export {}

console.log("Background service worker loaded")

状态持久化：

服务工作者在几秒不活动后变为空闲，5 分钟后浏览器完全终止其进程。使用 Storage API 持久化状态：

import { Storage } from "@plasmohq/storage"

const storage = new Storage()

await storage.set("key", "value")
const data = await storage.get("key")

Messaging API

Plasmo 的 Messaging API 使扩展不同部分之间的通信变得简单。

安装依赖：

pnpm install @plasmohq/messaging

安装步骤：

1. 确保背景服务工作者位于 background/index.ts
2. 所有消息处理程序位于 background/\* 目录下

创建消息处理程序：

background/messages/ping.ts：

import type { PlasmoMessaging } from "@plasmohq/messaging"

const handler: PlasmoMessaging.MessageHandler = async (req, res) => {
const message = await querySomeApi(req.body.id)

res.send({
message
})
}

export default handler

发送消息：

import { sendToBackground } from "@plasmohq/messaging"

const resp = await sendToBackground({
name: "ping",
body: {
id: 123
}
})

Relay Flow（中继流）：

在中继之前的内容脚本中注册中继：

contents/plasmo.ts：

import { relayMessage } from "@plasmohq/messaging"

export const config: PlasmoCSConfig = {
matches: ["http://www.plasmo.com/*"]
}

relayMessage({
name: "ping"
})

从网页发送消息：

import { sendToBackgroundViaRelay } from "@plasmohq/messaging"

const resp = await sendToBackgroundViaRelay({
name: "ping"
})

Port（长连接）：

创建端口处理程序：

background/ports/mail.ts：

import type { PlasmoMessaging } from "@plasmohq/messaging"

const handler: PlasmoMessaging.PortHandler = async (req, res) => {
console.log(req)

res.send({
message: "Hello from port handler"
})
}

export default handler

在 React 中使用端口：

import { usePort } from "@plasmohq/messaging/hook"

function Component() {
const mailPort = usePort("mail")

return (

<div>
{mailPort.data?.message}
<button
onClick={async () => {
mailPort.send({ hello: "world" })
}}>
Send Data
</button>
</div>
)
}

Storage API

@plasmohq/storage 是一个浏览器扩展持久化存储的实用程序库。

安装：

pnpm install @plasmohq/storage

基础使用：

import { Storage } from "@plasmohq/storage"

const storage = new Storage()

await storage.set("key", "value")
const data = await storage.get("key") // "value"

await storage.set("capt", { color: "red" })
const data2 = await storage.get("capt") // { color: "red" }

自定义存储区域：

const storage = new Storage({
area: "local"
})

监控变化：

storage.watch({
"serial-number": (c) => {
console.log(c.newValue)
}
})

Secure Storage（加密存储）：

import { SecureStorage } from "@plasmohq/storage/secure"

const storage = new SecureStorage()

await storage.setPassword("password")
await storage.set("key", "value")
const data = await storage.get("key") // "value"

React Hook：

import { useStorage } from "@plasmohq/storage/hook"

function Component() {
const [value, setValue] = useStorage("key", "default")

return <input value={value} onChange={(e) => setValue(e.target.value)} />
}

高级用法：

const [value, setValue, {
setRenderValue,
setStoreValue,
remove
}] = useStorage("key")

环境变量

Plasmo 对环境变量提供一等支持。

内置环境变量：

- NODE_ENV：development 或 production
- PLASMO_TARGET：目标，如 chrome-mv3
- PLASMO_BROWSER：目标浏览器名称
- PLASMO_MANIFEST_VERSION：Manifest 版本（mv2 或 mv3）
- PLASMO_TAG：构建标签（dev、prod 或自定义）

自定义环境变量：

创建 .env 文件：

PLASMO_PUBLIC_SHIP_NAME=ncc-1701
PLASMO_PUBLIC_SHIELD_FREQUENCY=42
PRIVATE_KEY=xxx # 在扩展中未定义

注意：只有以 PLASMO*PUBLIC* 前缀的变量才会被注入。

环境文件优先级：

特定环境：

- .env.development
- .env.production

Bundle 特定：

- .env.safari（浏览器特定）
- .env.alpha（标签特定）

本地文件（优先级更高）：

- .env.local
- .env.<browser>.local
- .env.<tag>.local

使用环境变量：

在源代码中：

const FrontHull = () => <h1>{process.env.PLASMO_PUBLIC_SHIP_NAME}</h1>

在远程代码导入中：

import "https://www.plasmo.com/js?id=$PLASMO_PUBLIC_ITERO"

在内容脚本配置中：

export const config: PlasmoCSConfig = {
matches: ["$PLASMO_PUBLIC_SITE_URL/"]
}

在 manifest 覆盖中：

{
"manifest": {
"key": "$CRX_PUBLIC_KEY"
}
}

导入解析

Plasmo 框架自带为扩展开发定制的代码/资产打包器。

支持的文件类型：

- .{css,pcss,sass,scss,less}：样式文件
- .svg：矢量图形
- .{png,jpg,jpeg,webp,gif,tiff,avif,heic,heif}：图像
- .{json,json5}：数据文件
- .{graphql,gql}：GraphQL 查询

导入方案：

Tilde (~/) - 项目相对路径：

- 默认设置：~ 指向项目根目录
- src 目录设置：~ 指向 src 目录
- 资产方案（data-base64, data-text, url）：总是解析到项目根

使用示例：

import styleText from "data-text:~style.css"
import icon from "data-base64:~assets/icon.png"

Absolute (/) - 绝对路径：

始终解析到项目根（package.json 所在位置）

Relative (./, ../) - 相对路径：

import "./file-name"
import "../parent-dir/file"

导入方案：

raw - 复制文件到扩展包根：

import imageUrl from "raw:~/assets/image.png"
// chrome-extension://<extension-id>/image.<hash>.png

raw-env - 带环境变量的 raw：

{
"url": "$PLASMO_PUBLIC_URL"
}

url - 转换/打包/优化文件：

import styleUrl from "url:~/style.scss"
// chrome-extension://<extension-id>/style.<hash>.css

data-text - 内联为字符串：

import styleText from "data-text:~/style.scss"

data-text-env - 带环境变量的 data-text

data-base64 - 转换为 base64 字符串：

import iconBase64 from "data-base64:~/icon.png"

data-env - 自动处理环境变量：

import data from "data-env:~/data.json"
// 返回 JSON 对象，无需 JSON.parse()

react:_/_.svg - 转换为 React 组件：

import Logo from "react:~/assets/logo.svg"

const Hello = () => <Logo />

资源

内联图像：

import someCoolImage from "data-base64:~assets/image.png"

<img src={someCoolImage} alt="Pretty cool image" />

Web Accessible Resources：

在 package.json 中配置：

{
"manifest": {
"web_accessible_resources": [
{
"resources": [
"~raw.js",
"assets/pic*.png",
"resources/test.json"
],
"matches": ["https://www.plasmo.com/*"]
}
]
}
}

图标

Plasmo 自动生成较小分辨率的图标版本。只需提供高保真版本。

默认图标位置：assets/icon.png

替代图标名称：

- icon512, icon-512, icon-512x512
- icon1024, icon-1024, icon-1024x1024

开发图标：

- 开发模式下，图标自动转换为灰度
- 使用 icon.development.png 自定义开发图标

标签特定图标：

- icon.<tag>.png
- icon.<tag>.<NODE_ENV>.png

图标尺寸：
Plasmo 生成以下尺寸：16x16、32x32、48x48、64x64、128x128

覆盖特定尺寸：

- icon<size>.png
- icon-<size>.png
- icon-<size>x<size>.png

本地化和国际化

Plasmo 内置对本地化的支持。

本地化文件位置：

- /locales/{lang}/messages.json
- /assets/\_locales/{lang}/messages.json
- /assets/locales/{lang}/messages.json

英语示例：

locales/en/messages.json：

{
"extensionName": {
"message": "with-locales-i18n-en",
"description": "Name of extension."
},
"popup": {
"message": "Logic is beginning of wisdom, not the end.",
"description": "Popup message."
}
}

在源代码模块中使用：

function IndexPopup() {
return (

<div>
<h2>{chrome.i18n.getMessage("popup")}</h2>
</div>
)
}

export default IndexPopup

在 manifest 中使用：

{
"displayName": "**MSG_extensionName**",
"description": "**MSG_extensionDescription**"
}

在本地化文件中使用环境变量：

locales/en/messages.json：

{
"popup": {
"message": "Logic is beginning of wisdom, not the end. - $PLASMO_PUBLIC_QUOTE_AUTHOR",
"description": "Popup message."
}
}

远程代码导入

Plasmo 自动打包所有指向远程资源的导入语句，这是 Manifest V3 远程代码限制所必需的。

基本用法：

import "https://www.googletagmanager.com/gtag/js?id=XXXXXX"

使用环境变量：

.env.local：

PLASMO_PUBLIC_GTAG_ID=XXXXXX

在导入中使用：

import "https://www.googletagmanager.com/gtag/js?id=$PLASMO_PUBLIC_GTAG_ID"

Tailwind CSS 集成

创建带 Tailwind CSS 的 Plasmo 项目：

pnpm create plasmo --with-tailwindcss

手动安装：

# 添加依赖

pnpm i -D tailwindcss@3 postcss autoprefixer

# 生成配置

npx tailwindcss init -p

# 配置 PostCSS

postcss.config.js：

module.exports = {
plugins: {
tailwindcss: {},
autoprefixer: {}
}
}

# 配置 Tailwind

tailwind.config.js：

module.exports = {
mode: "jit",
darkMode: "class",
content: ["./**/*.tsx"],
plugins: []
}

# 添加根样式

style.css：

@tailwind base;
@tailwind components;
@tailwind utilities;

在扩展页面中使用：

popup.tsx：

import "./style.css"

function IndexPopup() {
return (
<button className="bg-blue-500 text-white px-4 py-2 rounded">
Click me
</button>
)
}

export default IndexPopup

在 CSUI 中使用：

content.tsx：

import cssText from "data-text:~style.css"

export const getStyle = () => {
const style = document.createElement("style")
style.textContent = cssText
return style
}

const PlasmoOverlay = () => {
return (

<div className="bg-blue-500 text-white p-4">
Hello
</div>
)
}

export default PlasmoOverlay

处理 CSS 变量问题：

import cssText from "data-text:~style.css"

export const getStyle = () => {
const style = document.createElement("style")
// 将 :root 替换为 :host(plasmo-csui)
style.textContent = cssText.replaceAll(':root', ':host(plasmo-csui)')
return style
}

Manifest 覆盖

Plasmo 框架通过 package.json 的 manifest 字段扩展覆盖生成的扩展 manifest。

基本用法：

{
"manifest": {
"permissions": [
"activeTab",
"scripting"
],
"host_permissions": [
"https://*/*"
]
}
}

自动传递的字段：

- packageJson.version -> manifest.version
- packageJson.displayName -> manifest.name
- packageJson.description -> manifest.description
- packageJson.author -> manifest.author
- packageJson.homepage -> manifest.homepage_url

在 manifest 中使用环境变量：

{
"manifest": {
"browser_specific_settings": {
"gecko": {
"id": "$FIREFOX_EXT_ID"
}
}
}
}

在 manifest 中使用本地化字符串：

{
"name": "**MSG_extensionName**"
}

高级自定义

使用 src 目录：

将所有源代码移至 src 目录，Plasmo 会自动识别。

别名导入：

在 package.json 中配置：

{
"manifest": {
"alias": {
"@": "~"
}
}
}

替换 HTML：

在组件目录创建 index.html 文件，Plasmo 会使用它而不是默认模板。

内部路径：

使用 ~ 符号引用项目中的文件。

常见使用场景

1. 创建简单的 popup 扩展

popup.tsx：

function IndexPopup() {
return (

<div style={{ width: 300, padding: 20 }}>
<h1>我的扩展</h1>
<p>这是一个简单的扩展示例</p>
</div>
)
}

export default IndexPopup

2. 创建内容脚本

content.ts：

export {}

const targetElement = document.querySelector("#content")
if (targetElement) {
const div = document.createElement("div")
div.textContent = "注入的内容"
targetElement.appendChild(div)
}

3. 创建 CSUI Overlay

content.tsx：

export const getOverlayAnchor: PlasmoGetOverlayAnchor = async () =>
document.querySelector("h1")

const Overlay = () => (

  <div style={{
    position: "fixed",
    top: 10,
    right: 10,
    background: "#fff",
    padding: 10,
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
  }}>
    Hello from extension
  </div>
)

export default Overlay

4. 使用 Messaging API 进行通信

background/messages/fetchData.ts：

import type { PlasmoMessaging } from "@plasmohq/messaging"

const handler: PlasmoMessaging.MessageHandler = async (req, res) => {
const data = await fetch("https://api.example.com/data")
.then(r => r.json())

res.send({ data })
}

export default handler

content.tsx：

import { sendToBackground } from "@plasmohq/messaging"

const Content = () => {
const handleClick = async () => {
const resp = await sendToBackground({
name: "fetchData"
})

    console.log(resp.data)

}

return <button onClick={handleClick}>Fetch Data</button>
}

export default Content

5. 使用 Storage API 同步状态

popup.tsx：

import { useStorage } from "@plasmohq/storage/hook"

function IndexPopup() {
const [count, setCount] = useStorage("count", 0)

return (

<div>
<h1>计数: {count}</h1>
<button onClick={() => setCount(count + 1)}>增加</button>
<button onClick={() => setCount(count - 1)}>减少</button>
</div>
)
}

export default IndexPopup

options.tsx：

import { useStorage } from "@plasmohq/storage/hook"

function OptionsPage() {
const [count, setCount] = useStorage("count", 0)

return (

<div>
<h1>选项页</h1>
<p>当前计数: {count}</p>
<input
type="number"
value={count}
onChange={(e) => setCount(Number(e.target.value))}
/>
</div>
)
}

export default OptionsPage

6. 在 CSUI 中使用自定义字体

font.css：

@font-face {
font-family: "CustomFont";
src: url(data-base64:~assets/CustomFont.woff2) format("woff2");
}

content.tsx：

import styleText from "data-text:~/font.css"
import type { PlasmoCSConfig } from "plasmo"

export const config: PlasmoCSConfig = {
css: ["font.css"]
}

export const getStyle = () => {
const style = document.createElement("style")
style.textContent = styleText
return style
}

const StyledComponent = () => (

  <div style={{ fontFamily: "CustomFont" }}>
    使用自定义字体
  </div>
)

export default StyledComponent

调试和故障排除

开发模式问题：

- 确保在 chrome://extensions 中刷新扩展
- 检查 Service Worker 的控制台日志
- 使用 chrome.runtime.getManifest() 查看生成的 manifest
- 检查 Content Scripts UI 是否正确挂载

类型错误：

- 运行 dev 服务器生成静态类型
- 重启 TypeScript 服务器
- 确保 @plasmohq/messaging 正确安装

样式问题：

- CSUI 使用 Shadow DOM，确保样式正确注入
- 检查 CSS 变量冲突
- 使用 :host 代替 :root

存储问题：

- 在 Firefox 开发时添加 Add-on ID
- 检查 storage 权限是否自动启用

最佳实践

1. 使用 TypeScript 获得类型安全
2. 利用 Plasmo 的声明式开发模式
3. 使用 Shadow DOM 隔离 CSUI 样式
4. 通过 Storage API 实现跨组件状态同步
5. 使用 Messaging API 实现松耦合通信
6. 利用环境变量管理不同环境配置
7. 为不同浏览器和 manifest 版本构建
8. 使用远程代码导入处理第三方分析工具
9. 定期清理未使用的代码和依赖
10. 遵循浏览器扩展的权限最小化原则

资源

- 官方文档：https://docs.plasmo.com
- GitHub 仓库：https://github.com/PlasmoHQ/plasmo
- Discord 社区：https://www.plasmo.com/s/d
- 示例项目：https://github.com/PlasmoHQ/examples

相关技能

- React：用于构建用户界面
- TypeScript：提供类型安全
- Tailwind CSS：快速样式化
- 浏览器扩展开发：Chrome Extension API
