# ClipVault v1.2

> 极简剪贴板管理器 + 常用库 / Clipboard Manager + Snippet Library

[中文](#中文) | [English](#english)

---

## 中文

### 简介

ClipVault 是一款极简的 Windows 剪贴板管理工具。复制任意文字自动记录，内置常用符号库，一键粘贴。

### 功能

- 📋 **自动监听** — 复制文本自动记录，不存图片/文件
- 📁 **常用库** — 内置数学符号、特殊符号、中文标点、工作模板
- 🔍 **搜索过滤** — 快速搜索历史记录和常用库
- 📌 **置顶** — 重要内容固定列表顶部
- 🗑 **清空** — 一键清理非置顶历史
- 🔒 **纯本地** — SQLite 存储，不联网不上传
- 🌐 **中英双语** — 点 中/EN 一键切换

### 使用

1. 下载 `ClipVault.exe`，双击运行
2. 复制任意文字（Ctrl+C）即可自动记录
3. 点「常用库」查看预设符号，点「＋ 添加」添加自定义内容
4. 选中条目点「📋 复制」即可粘贴到任何地方

### 技术

- Python 3 + tkinter + SQLite
- 单文件 12MB，无需安装
- 仅记录文本，不保存图片/文件

### 关于

GitHub: https://github.com/podcatcher962/ClipVault
© 永远的兰兰

---

## English

### Overview

ClipVault is a minimalist Windows clipboard manager. Auto-records text on copy, built-in snippet library, one-click paste.

### Features

- 📋 **Auto-monitor** — Records text on copy (Ctrl+C), no images/files
- 📁 **Snippet Library** — Built-in math symbols, special chars, work templates
- 🔍 **Search** — Filter history and library instantly
- 📌 **Pin** — Keep important items at the top
- 🗑 **Clear** — Remove all unpinned history at once
- 🔒 **Local Only** — SQLite storage, no internet, no upload
- 🌐 **Bilingual** — Click 中/EN to toggle Chinese/English

### Usage

1. Download `ClipVault.exe`, double-click to run
2. Copy any text (Ctrl+C) — it's automatically recorded
3. Click "Library" tab for preset symbols, or "＋ Add" to save your own
4. Select an item, click "📋 Copy", paste anywhere

### Tech

- Python 3 + tkinter + SQLite
- Single-file 12MB, no installation
- Text only — no images/files stored

### About

GitHub: https://github.com/podcatcher962/ClipVault
© 永远的兰兰 / forever-chitanda

---

## 免责声明 / Disclaimer

### 中文

1. ClipVault 的剪贴板监听功能仅记录用户主动复制（Ctrl+C）的文字内容，不记录图片、文件路径、二进制数据。本软件不记录键盘输入（非键盘记录器），仅被动读取系统剪贴板中的文本变化。
2. 任何具有管理员权限的程序均可读取系统剪贴板。本软件与 Windows 系统剪贴板机制一致，不引入额外安全风险。用户应自行避免将密码、银行卡号等敏感信息存入剪贴板。
3. 本软件按"原样"（AS-IS）提供，不提供任何明示或暗示的担保。开发者不对因使用或无法使用本软件导致的任何数据丢失承担责任。
4. 所有剪贴板数据完全存储于本地 SQLite 数据库，不会上传至任何服务器，不连接互联网。
5. 预设常用库中的数学符号、特殊字符等为 Unicode 标准字符，不涉及第三方版权。
6. 使用者须遵守所在地法律法规。本软件仅供个人学习与工作效率提升使用。

### English

1. ClipVault only records text copied via Ctrl+C. No images, files, or binary data. It is NOT a keylogger — it passively reads text changes from the system clipboard only.
2. Any program with admin privileges can read the system clipboard. ClipVault operates within standard Windows clipboard mechanisms and introduces no additional security risk. Do not copy sensitive information like passwords or bank card numbers.
3. This software is provided AS-IS without warranty of any kind. The developer assumes no responsibility for data loss resulting from use or inability to use this software.
4. All clipboard data is stored entirely in a local SQLite database. No data is uploaded to any server.
5. Preset library symbols are standard Unicode characters and do not involve third-party copyright.
6. Users must comply with local laws. For personal study and productivity use only.
