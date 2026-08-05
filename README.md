# 📋 ClipVault

> Minimalist Chinese clipboard manager. Copy. Search. Pin. Done.

A clean, native Windows desktop app that silently watches your clipboard and keeps everything searchable. No cloud, no account, no nonsense.

<p align="center">
  <img src="docs/screenshot.png" alt="screenshot" width="500">
</p>

---

## ✨ Features

| Feature | Detail |
|---------|--------|
| 📋 **Auto-capture** | Any text you Ctrl+C is logged instantly |
| 🔍 **Instant search** | Type to filter — works across all clips |
| 📌 **Pin** | Keep important clips (email, address) at the top |
| 🧹 **Cleanup** | One click to clear all unpinned clips |
| 📁 **Snippet Library** | Built-in math symbols, special chars, punctuation — 6 categories, 100+ items |
| ⚡ **4-column palette** | Click any symbol to copy — no scrolling in a list |
| ✏️ **Custom snippets** | Add your own (company names, addresses, templates) |
| 🌐 **Open source** | Python 3 + tkinter + SQLite, zero extra dependencies |

---

## 📁 Snippet Library (Built-in)

| Category | Content |
|----------|---------|
| 📐 数学符号 | × ÷ ± √ ∞ ≤ ≥ π α β ∑ ∫ ... |
| 🔤 特殊符号 | ① ② ③ ★ ♥ ◆ → ← ↑ ↓ ™ © ® ... |
| ⌨ 常用符号 | @ # $ % & * ( ) { } [ ] \\ ... |
| 🈳 中文标点 | 「」『』【】—— ... |
| ⌨️ 英文标点 | — – … • · $ € £ ¥ ... |
| 💼 工作常用 | 收到谢谢 / 请查收附件 / 完成确认 ... |

---

## 🚀 Quick Start

1. Download `ClipVault.exe` from [Releases](https://github.com/podcatcher962/ClipVault/releases)
2. Double-click to run
3. Start copying text — it auto-captures
4. Click any snippet to preview, double-click to copy
5. Use **📁 常用库** tab for built-in symbols + your own custom snippets

**No installation required. No Python needed.**

---

## 🛠 Tech Stack

- Python 3 + tkinter + SQLite
- Single `.exe` file (~9 MB)
- Windows 10 / 11

---

## ⚠️ Disclaimer / 免责声明

**English**

1. This tool is for personal productivity use only. All clipboard data is stored **locally** in a SQLite database. No data is ever uploaded to any server.
2. The clipboard monitor only records **text** content actively copied by the user (Ctrl+C). It does **NOT** record images, files, or keyboard input (not a keylogger). It passively reads text changes from the system clipboard only.
3. **Privacy**: any program with appropriate permissions can read the Windows clipboard. This software introduces no additional risk beyond the normal clipboard mechanism. Users should avoid storing passwords, bank details, or other sensitive data in the clipboard.
4. This software is provided **AS-IS** without warranty of any kind, express or implied. The developer shall not be liable for any direct, indirect, incidental, or consequential damages arising from the use or inability to use this software.
5. Built-in snippet library content (symbols, characters) is standard Unicode — no third-party copyright is involved.
6. Users must comply with applicable laws. Minors should use under parental guidance.

**中文**

1. 本工具仅供个人学习与工作效率提升使用。所有剪贴板数据完全存储于本地 SQLite 数据库，不会上传至任何服务器。
2. 剪贴板监听仅记录用户主动复制的文字内容，不记录图片、文件或键盘输入（非键盘记录器）。
3. 任何具有管理员权限的程序均可读取系统剪贴板，本软件不引入额外安全风险。用户应避免将敏感信息存入剪贴板。
4. 本软件按"原样"提供，开发者不对因使用导致的任何数据丢失承担责任。
5. 预设内容为标准 Unicode 字符，不涉及第三方版权。
6. 使用者须遵守所在地法律法规。

---

## 👤 Author

- **GitHub**: [podcatcher962](https://github.com/podcatcher962)
- **License**: MIT
