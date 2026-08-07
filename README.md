# ClipVault v1.2

> 剪贴板管理器 + 常用库 — 桌面版 + Web版 / Clipboard Manager + Snippet Library — Desktop + Web

[中文](#中文) | [English](#english)

---

## 中文

### 简介

ClipVault 是一款剪贴板管理工具。**两个版本**：Windows 桌面版自动监听剪贴板，**Web 版点黏贴即可读取**。内置常用符号库（数学符号、特殊字符、中文标点、工作模板），一键复制粘贴。

### 🚀 两个版本

| 版本 | 适用平台 | 剪贴板方式 | 文件 |
|------|------|------|------|
| 💻 **桌面版** | Windows (.exe) | 自动后台监听 | ClipVault.exe (12MB) |
| 🌐 **Web 版** | 浏览器通用 | 点黏贴读取 | clipvault.html (单文件) |

Web 版点黏贴按钮直接读取剪贴板（需浏览器授权），数据存储在 localStorage 中。

### 功能

- 📋 **剪贴历史** — 保存复制过的文字，最多 1000 条
- 📌 **置顶** — 重要内容固定在顶部
- 🧹 **清空** — 一键清理非置顶历史
- 📁 **常用库 (4 列网格)** — 数学符号、特殊符号、中文标点、工作模板
- ＋ **添加 / ✎ 编辑** — 自定义常用内容
- 🔍 **搜索** — 过滤历史和库
- 🌐 **中英双语** — 点 中/EN 一键切换
- 📋 **复制按钮** — 选中条目一键复制到剪贴板
- 🔒 **纯本地** — localStorage，不联网不上传

### 免责声明

1. ClipVault 是纯本地工具。桌面版数据存储在本地 SQLite 数据库，Web 版存储在浏览器 localStorage 中。均不上传至任何服务器。
2. 桌面版仅记录 Ctrl+C 复制的文本内容，不记录图片、文件、键盘输入。Web 版需用户主动点击黏贴按钮并授权。
3. 本软件按"原样"（AS-IS）提供，不提供任何明示或暗示的担保。
4. 预设库中的符号为 Unicode 标准字符，不涉及第三方版权。
5. 使用者须遵守所在地法律法规。

### 技术

- 桌面版：Python 3 + tkinter + SQLite，单文件 12MB
- Web 版：纯 HTML + CSS + JS，单文件无依赖

### 关于

GitHub: https://github.com/podcatcher962/ClipVault
© 永远的兰兰

---

## English

### Overview

ClipVault is a clipboard management tool. **Two editions**: Windows desktop with auto-monitoring, **Web version with one-click paste**. Built-in snippet library.

### 🚀 Two Editions

| Edition | Platforms | Clipboard | File |
|------|------|------|------|
| 💻 **Desktop** | Windows (.exe) | Auto-monitor | ClipVault.exe (12MB) |
| 🌐 **Web** | Any browser | Click-paste | clipvault.html (single file) |

Web version reads clipboard on paste button click (requires browser permission). Data in localStorage.

### Features

- 📋 **Clip History** — Auto-save copied text, up to 1000 items
- 📌 **Pin** — Keep important items at top
- 🧹 **Clear** — Remove all unpinned history
- 📁 **Library (4-column grid)** — Math symbols, special chars, punctuation, templates
- ＋ **Add / ✎ Edit** — Custom snippets
- 🔍 **Search** — Filter history and library
- 🌐 **Bilingual** — Click 中/EN to toggle
- 📋 **Copy button** — One-click copy
- 🔒 **Pure local** — localStorage

### Disclaimer

1. Pure local tool. Desktop: SQLite; Web: localStorage. No server uploads.
2. Desktop only records Ctrl+C text; no images, files, or keystrokes. Web requires user click + permission.
3. Provided AS-IS without warranty.
4. Preset symbols are Unicode standard.
5. Users must comply with local laws.

### Tech

- Desktop: Python 3 + tkinter + SQLite, single-file 12MB
- Web: Pure HTML + CSS + JS, single-file

### About

GitHub: https://github.com/podcatcher962/ClipVault
© 永远的兰兰 / forever-chitanda
