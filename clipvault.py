#!/usr/bin/env python3
"""ClipVault v1.2 — 极简剪贴板管理器 + 常用库 / Clipboard Manager + Snippet Library"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os, sys, sqlite3, threading, time, datetime
import pyperclip

APP_DIR = os.path.dirname(sys.executable) if getattr(sys,'frozen',False) else os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "clipvault.db")

# ======================= Language / Translations =======================
TR = {
    "zh": {
        "tab_clips": "📋 剪贴历史",
        "tab_snippets": "📁 常用库",
        "pin": "📌 置顶", "copy": "📋 复制", "delete": "🗑 删除",
        "clean": "🧹 清空", "add": "＋ 添加", "edit": "✎ 编辑",
        "search_hint": "搜索...",
        "preview_hint": "点击列表或常用库中的内容即可预览",
        "monitoring": "监听中...",
        "text_only": "仅文字 · 不存图片/文件",
        "captured": "📋 已捕获",
        "copied": "✅ 已复制到剪贴板",
        "pinned": "📌 已置顶", "unpinned": "   已取消置顶",
        "deleted": "🗑 已删除",
        "cleaned": "🧹 已清理",
        "added": "✅ 已添加",
        "updated": "✅ 已更新",
        "preview_cleared": "预览已清空",
        "clips_count": "📋 剪贴板 · {count}条",
        "snippets_count": "常用库 · {count}项",
        "confirm_clean": "删除所有非置顶的剪贴板历史？\n\n📌 已置顶的条目会保留。",
        "clean_done": "（已清空，仅保留置顶内容）",
        "help_menu": "帮助",
        "help_title": "使用说明",
        "disclaimer_title": "免责声明",
        "about_title": "关于 ClipVault",
        "help_text": (
            "📖 ClipVault 使用说明\n\n"
            "📋 剪贴板：复制任意文字自动记录，Ctrl+Shift+V 呼出窗口。\n\n"
            "📁 常用库：保存高频输入的符号、地址、公司名等。\n"
            "    点「＋ 添加」输入内容和分类即可。\n\n"
            "蓝色 📋 复制按钮：选中条目后点复制，再贴到任何地方。\n"
            "橙色 📌 置顶：重要内容固定在列表顶部。\n"
            "红色 🗑 删除：移除选中条目。\n"
            "绿色 🧹 清空：一次删除所有非置顶历史。\n\n"
            "⚠️ 仅记录文本，不保存图片/文件。"
        ),
        "title_bar": "永远的兰兰 · 极简剪贴板",
        "add_prompt": "输入要保存的文字：",
        "add_category": "分类名称（如：地址、符号、工作）：",
        "cat_default": "自定义",
        "edit_prompt": "修改文字：",
        "about_text": (
            "ClipVault v1.2\n\n极简剪贴板管理器 + 常用库\n"
            "Python 3 + tkinter + SQLite\n"
            "纯本地存储 · 零隐私风险\n\n"
            "GitHub: https://github.com/podcatcher962/ClipVault\n"
            "© 永远的兰兰"
        ),
    },
    "en": {
        "tab_clips": "📋 History",
        "tab_snippets": "📁 Library",
        "pin": "📌 Pin", "copy": "📋 Copy", "delete": "🗑 Del",
        "clean": "🧹 Clear", "add": "＋ Add", "edit": "✎ Edit",
        "search_hint": "Search...",
        "preview_hint": "Click an item to preview",
        "monitoring": "Monitoring...",
        "text_only": "Text only · No images/files",
        "captured": "📋 Captured",
        "copied": "✅ Copied to clipboard",
        "pinned": "📌 Pinned", "unpinned": "   Unpinned",
        "deleted": "🗑 Deleted",
        "cleaned": "🧹 Cleared",
        "added": "✅ Added",
        "updated": "✅ Updated",
        "preview_cleared": "Preview cleared",
        "clips_count": "📋 Clipboard · {count} items",
        "snippets_count": "Library · {count} items",
        "confirm_clean": "Delete all unpinned clipboard history?\n\n📌 Pinned items will be kept.",
        "clean_done": "(Cleared — pinned items kept)",
        "help_menu": "Help",
        "help_title": "Help",
        "disclaimer_title": "Disclaimer",
        "about_title": "About ClipVault",
        "help_text": (
            "📖 ClipVault Help\n\n"
            "📋 Clipboard: auto-records text on copy (Ctrl+C).\n\n"
            "📁 Library: save frequently used text like symbols, addresses.\n"
            "    Click ＋ Add to save an item with a category.\n\n"
            "📋 Copy: select an item, click Copy, paste anywhere.\n"
            "📌 Pin: keep important items at the top.\n"
            "🗑 Delete: remove selected item.\n"
            "🧹 Clear: delete all unpinned history at once.\n\n"
            "⚠️ Text records only. No images/files."
        ),
        "title_bar": "forever-chitanda · Clipboard Manager",
        "add_prompt": "Enter text to save:",
        "add_category": "Category name (e.g. Address, Symbols, Work):",
        "cat_default": "Custom",
        "edit_prompt": "Edit text:",
        "about_text": (
            "ClipVault v1.2\n\nClipboard Manager + Snippet Library\n"
            "Python 3 + tkinter + SQLite\n"
            "Local storage · Zero privacy risk\n\n"
            "GitHub: https://github.com/podcatcher962/ClipVault\n"
            "© 永远的兰兰 / forever-chitanda"
        ),
    },
}

DISCLAIMER = """⚠️ 免责声明 / Disclaimer

1. 本工具仅供个人学习与工作效率提升使用。所有剪贴板数据完全存储于本地 SQLite 数据库，不会上传至任何服务器，不连接互联网。

2. 剪贴板监听功能仅记录用户主动复制（Ctrl+C）的文字内容，不记录图片、文件路径、二进制数据。软件不记录键盘输入（非键盘记录器），仅被动读取系统剪贴板中的文本变化。

3. 隐私风险：任何具有管理员权限的程序均可读取系统剪贴板。本软件与 Windows 系统剪贴板机制一致，不引入额外安全风险。用户应自行避免将密码、银行卡号等敏感信息存入剪贴板。

4. 本软件按"原样"（AS-IS）提供，不提供任何明示或暗示的担保，包括但不限于适销性、特定用途适用性及不侵权担保。开发者不对因使用或无法使用本软件导致的任何直接、间接、偶然、特殊或后果性数据丢失承担责任。

5. 预设常用库中的数学符号、特殊字符等为 Unicode 标准字符，不涉及第三方版权。工作常用模板为示例文本，用户可自行修改或删除。

6. 使用者须遵守所在地法律法规。不得利用本软件从事任何非法活动。未成年人应在监护人指导下使用。

7. 开发者保留随时更新本免责声明的权利，恕不另行通知。继续使用即视为接受更新后的条款。"""

PRESET_SNIPPETS = {
    "📐 数学符号": [
        "×", "÷", "±", "∓", "√", "∛", "∜", "∞", "∝", "∂", "∇", "∆",
        "≠", "≈", "≅", "≃", "≤", "≥", "≪", "≫", "≮", "≯",
        "π", "θ", "α", "β", "γ", "δ", "ε", "λ", "μ", "σ", "φ", "ω",
        "∑", "∫", "∬", "∭", "∮", "∏", "∐",
    ],
    "🔤 特殊符号": [
        "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩",
        "★", "☆", "♥", "♦", "♣", "♠", "◆", "◇", "●", "○", "◎", "◉",
        "→", "←", "↑", "↓", "↔", "↕", "↖", "↗", "↘", "↙",
        "™", "©", "®", "℗", "№", "§", "¶",
        "█", "▓", "▒", "░", "▣", "▤", "▥", "▦",
    ],
    "⌨ 常用符号": [
        "@", "#", "$", "%", "&", "*", "(", ")", "-", "_",
        "+", "=", "{", "}", "[", "]", "|", "\\", "/",
        ":", ";", "\"", "'", "<", ">", ",", ".", "?", "!", "~", "`",
    ],
    "🈳 中文标点": [
        "「", "」", "『", "』", "【", "】", "〖", "〗", "《", "》", "〈", "〉",
        "——", "……", "～", "·", "　", "、", "：", "；", "“", "”", "‘", "’",
    ],
    "⌨️ 英文标点": [
        "—", "–", "…", "•", "·",
        "«", "»", "‹", "›", "„",
        "†", "‡", "‰", "′", "″",
        "$", "€", "£", "¥", "₩",
    ],
    "💼 工作常用": [
        "收到，谢谢！我会尽快处理。",
        "请查收附件。如有问题随时联系。",
        "好的，我确认一下再回复你。",
        "抱歉，这个需要稍等一下。",
        "✅ 已完成，请查看。",
        "📅 会议时间：",
    ],
}

# ======================= Database =======================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS clips(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT, preview TEXT,
        pinned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT(datetime('now','localtime')))""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_clips_created ON clips(created_at DESC)")
    conn.execute("""CREATE TABLE IF NOT EXISTS snippets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, content TEXT, category TEXT DEFAULT '自定义',
        sort_order INTEGER DEFAULT 0)""")
    # Auto-cap clips
    conn.execute("""DELETE FROM clips WHERE id NOT IN (
        SELECT id FROM clips ORDER BY created_at DESC LIMIT 1000) AND pinned=0""")
    # Seed presets if empty
    if conn.execute("SELECT COUNT(*) FROM snippets").fetchone()[0] == 0:
        for cat, items in PRESET_SNIPPETS.items():
            for i, text in enumerate(items):
                conn.execute("INSERT INTO snippets(title,content,category,sort_order) VALUES(?,?,?,?)",
                             (text[:30], text, cat, i))
        conn.commit()
    return conn

# ======================= App =======================
class ClipVault:
    def __init__(self):
        self.conn = init_db()
        self.root = tk.Tk()
        self.root.title("ClipVault")
        self.root.geometry("500x560+1200+200")
        self.root.minsize(400, 440)
        self.root.configure(bg='#FAFAFA')
        self.root.attributes('-topmost', True)
        self.lang = 'zh'
        self._apply_theme()
        self._build_menu()
        self._build_ui()
        self._load_clips()
        self.last_clip = ""
        self.running = True
        self._schedule_monitor()

    def _t(self, key, **fmt):
        s = TR[self.lang].get(key, key)
        if fmt: s = s.format(**fmt)
        return s

    def _apply_theme(self):
        self.BG = '#FAFAFA'
        self.card_bg = '#FFFFFF'
        self.accent = '#7C4DFF'
        self.green = '#00C853'
        self.red = '#FF5252'
        self.orange = '#FF9100'
        self.blue = '#448AFF'
        self.teal = '#00BFA5'
        self.fg = '#212121'
        self.fg2 = '#757575'

    def _toggle_lang(self):
        self.lang = 'en' if self.lang == 'zh' else 'zh'
        # Update all UI labels
        self.title_label.config(text=self._t("title_bar"))
        self.tab_btn1.config(text=self._t("tab_clips"))
        self.tab_btn2.config(text=self._t("tab_snippets"))
        self.text_only_label.config(text=self._t("text_only"))
        self.status.config(text=self._t("monitoring"))
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', self._t("preview_hint"))
        self.preview_text.config(state=tk.DISABLED, fg='#BDBDBD')
        # Buttons — rebuild label texts
        for btn in self.clip_buttons:
            cur = btn.cget('text')
            for k in ['pin','copy','delete','clean']:
                if cur.startswith(self._t(k)[:2]):
                    btn.config(text=self._t(k))
                    break
        for btn in self.snippet_buttons:
            cur = btn.cget('text')
            for k in ['copy','add','edit','delete']:
                if cur.startswith(self._t(k)[:2]):
                    btn.config(text=self._t(k))
                    break
        # Clear preview button
        for child in self.root.winfo_children():
            self._update_clear_btn(child)
        # Rebuild menu
        self._build_menu()

    def _update_clear_btn(self, widget):
        if isinstance(widget, tk.Button) and widget.cget('text') in ('清空','Clear'):
            widget.config(text=("清空" if self.lang=='zh' else "Clear"))
        for child in widget.winfo_children():
            self._update_clear_btn(child)

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=self._t("help_title"), command=self._show_help)
        help_menu.add_command(label=self._t("disclaimer_title"), command=self._show_disclaimer)
        help_menu.add_separator()
        help_menu.add_command(label=self._t("about_title"), command=self._show_about)
        menubar.add_cascade(label=self._t("help_menu"), menu=help_menu)
        self.root.config(menu=menubar)

    def _show_help(self):
        messagebox.showinfo(self._t("help_title"), self._t("help_text"))

    def _show_disclaimer(self):
        messagebox.showinfo(self._t("disclaimer_title"), DISCLAIMER)

    def _show_about(self):
        messagebox.showinfo(self._t("about_title"), self._t("about_text"))

    @staticmethod
    def _cbtn(parent, text, color, cmd, side=None, padx=1, small=False):
        btn = tk.Button(parent, text=text, bg=color, fg='white',
            font=('Microsoft YaHei UI', 9),
            relief='flat', bd=0, padx=10, pady=4,
            cursor='hand2', command=cmd, activebackground=color)
        if side: btn.pack(side=side, padx=padx)
        else: btn.pack(pady=2, padx=6)
        return btn

    def _build_ui(self):
        # Title bar
        title_bar = tk.Frame(self.root, bg=self.accent, height=36)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="📋 ClipVault", font=('Microsoft YaHei UI',11,'bold'),
                 bg=self.accent, fg='white').pack(side=tk.LEFT, padx=12, pady=5)
        self.lang_btn = tk.Button(title_bar, text="中/EN", font=('Microsoft YaHei UI',8),
            bg='#5E35B1', fg='white', relief='flat', bd=0, padx=8, pady=2,
            cursor='hand2', command=self._toggle_lang)
        self.lang_btn.pack(side=tk.RIGHT, padx=12, pady=5)
        self.title_label = tk.Label(title_bar, text=self._t("title_bar"), font=('Microsoft YaHei UI',8),
                 bg=self.accent, fg='#E0D4FF')
        self.title_label.pack(side=tk.RIGHT, padx=8, pady=5)

        # Tab switcher
        tab_bar = tk.Frame(self.root, bg=self.BG)
        tab_bar.pack(fill=tk.X, padx=10, pady=(8,0))
        self.tab_var = tk.StringVar(value='clips')
        style = {'font':('Microsoft YaHei UI',9), 'relief':'flat', 'bd':0, 'cursor':'hand2', 'padx':16, 'pady':4}
        self.tab_btn1 = tk.Button(tab_bar, text=self._t("tab_clips"), **style, fg='white', bg=self.accent,
            command=lambda: self._switch_tab('clips'))
        self.tab_btn1.pack(side=tk.LEFT, padx=(0,2))
        self.tab_btn2 = tk.Button(tab_bar, text=self._t("tab_snippets"), **style, fg=self.fg2, bg='#EEEEEE',
            command=lambda: self._switch_tab('snippets'))
        self.tab_btn2.pack(side=tk.LEFT)

        # Search
        search_frame = tk.Frame(self.root, bg=self.BG)
        search_frame.pack(fill=tk.X, padx=8, pady=(6,2))
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *a: self._on_search())
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
            font=('Microsoft YaHei UI',10), bg=self.card_bg, fg='#BDBDBD',
            relief='flat', insertbackground=self.accent)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0,4))
        self.search_entry.bind('<FocusIn>', self._on_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_focus_out)

        # Buttons - SINGLE frame, no nesting
        self.btn_frame = tk.Frame(self.root, bg=self.BG, height=32)
        self.btn_frame.pack(fill=tk.X, padx=6, pady=(0,6))
        self.btn_frame.pack_propagate(False)
        # All 8 buttons (clips + snippets) in same frame, shown/hidden per tab
        self.clip_buttons = []
        self.snippet_buttons = []
        for (text_key, color, cmd), store in [
            (("pin", self.orange, self._toggle_pin), self.clip_buttons),
            (("copy", self.blue, self._copy_selected), self.clip_buttons),
            (("delete", self.red, self._delete_selected), self.clip_buttons),
            (("clean", self.teal, self._clean_clips), self.clip_buttons),
        ]:
            btn = self._cbtn(self.btn_frame, self._t(text_key), color, cmd, side=tk.LEFT, padx=1)
            store.append(btn)
        for (text_key, color, cmd), store in [
            (("copy", self.blue, self._copy_selected), self.snippet_buttons),
            (("add", self.green, self._add_snippet), self.snippet_buttons),
            (("edit", self.orange, self._edit_snippet), self.snippet_buttons),
            (("delete", self.red, self._delete_selected), self.snippet_buttons),
        ]:
            btn = self._cbtn(self.btn_frame, self._t(text_key), color, cmd, side=tk.LEFT, padx=1)
            store.append(btn)
        # Initially show clips buttons
        for b in self.snippet_buttons: b.pack_forget()

        # List / Grid area - swap between Listbox (clips) and Grid (snippets)
        self.list_area = tk.Frame(self.root, bg=self.BG)
        self.list_area.pack(fill=tk.BOTH, expand=True, padx=6)

        # Listbox for clips tab
        self.clip_list = tk.Listbox(self.list_area, font=('Microsoft YaHei UI',9),
            bg=self.card_bg, fg=self.fg, selectbackground=self.accent, selectforeground='white',
            relief='flat', borderwidth=0, highlightthickness=0, activestyle='none')
        self.list_sb = tk.Scrollbar(self.list_area, orient=tk.VERTICAL, command=self.clip_list.yview)
        self.clip_list.configure(yscrollcommand=self.list_sb.set)
        self.clip_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.clip_list.bind('<<ListboxSelect>>', self._on_select)
        self.clip_list.bind('<Double-1>', lambda e: self._copy_selected())
        self.clip_list.bind('<Return>', lambda e: self._copy_selected())

        # Canvas+scroll for snippets tab (grid of buttons)
        self.snip_canvas = tk.Canvas(self.list_area, bg=self.card_bg, highlightthickness=0)
        self.snip_scroll_v = tk.Scrollbar(self.list_area, orient=tk.VERTICAL, command=self.snip_canvas.yview)
        self.snip_canvas.configure(yscrollcommand=self.snip_scroll_v.set)
        self.snip_grid = tk.Frame(self.snip_canvas, bg=self.card_bg)
        self.snip_window = self.snip_canvas.create_window((0,0), window=self.snip_grid, anchor='nw', tags='snip_grid')
        self.snip_grid.bind('<Configure>', lambda e: self.snip_canvas.configure(scrollregion=self.snip_canvas.bbox('all')))
        self.snip_canvas.bind('<Configure>', lambda e: self.snip_canvas.itemconfig(self.snip_window, width=e.width))
        # Mouse wheel scrolling
        def _on_mousewheel(e):
            self.snip_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        self.snip_canvas.bind('<Enter>', lambda e: self.snip_canvas.bind_all('<MouseWheel>', _on_mousewheel))
        self.snip_canvas.bind('<Leave>', lambda e: self.snip_canvas.unbind_all('<MouseWheel>'))
        self.snip_canvas.pack_forget(); self.snip_scroll_v.pack_forget()

        # Preview
        preview_frame = tk.LabelFrame(self.root, text="预览", font=('Microsoft YaHei UI',9),
            bg=self.BG, fg=self.fg2, padx=4, pady=2)
        preview_frame.pack(fill=tk.X, padx=6, pady=(0,8))
        self.preview_text = tk.Text(preview_frame, font=('Microsoft YaHei UI',9),
            wrap=tk.WORD, bg=self.card_bg, fg='#BDBDBD', state=tk.DISABLED,
            relief='flat', height=5)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        self.preview_text.insert('1.0', self._t("preview_hint"))
        self.preview_text.config(state=tk.DISABLED)
        # Clear preview button
        clear_btn = tk.Button(preview_frame, text=("清空" if self.lang=='zh' else "Clear"), font=('Microsoft YaHei UI',7),
            bg='#EEEEEE', fg=self.fg2, relief='flat', padx=8, pady=1,
            cursor='hand2', command=self._clear_preview)
        clear_btn.place(relx=1.0, anchor='ne', x=-6, y=4)

        # Status
        status_row = tk.Frame(self.root, bg=self.BG)
        status_row.pack(fill=tk.X, padx=12, pady=(0,2))
        self.status = tk.Label(status_row, text=self._t("monitoring"), font=('Microsoft YaHei UI',7),
            bg=self.BG, fg=self.teal, anchor='w')
        self.status.pack(side=tk.LEFT)
        self.text_only_label = tk.Label(status_row, text=self._t("text_only"), font=('Microsoft YaHei UI',7),
            bg=self.BG, fg='#BDBDBD')
        self.text_only_label.pack(side=tk.RIGHT)

    def _on_focus_in(self, e):
        if self.search_var.get() == '':
            self.search_entry.config(fg=self.fg)

    def _on_focus_out(self, e):
        if self.search_var.get().strip() == '':
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='#BDBDBD')

    # ======================= Tab Switching =======================
    def _switch_tab(self, tab):
        self.tab_var.set(tab)
        if tab == 'clips':
            self.tab_btn1.config(fg='white', bg=self.accent)
            self.tab_btn2.config(fg=self.fg2, bg='#EEEEEE')
            for b in self.clip_buttons: b.pack(side=tk.LEFT, padx=1)
            for b in self.snippet_buttons: b.pack_forget()
            self.snip_canvas.pack_forget(); self.snip_scroll_v.pack_forget()
            self.clip_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.list_sb.pack(side=tk.RIGHT, fill=tk.Y)
            self._load_clips()
        else:
            self.tab_btn2.config(fg='white', bg=self.accent)
            self.tab_btn1.config(fg=self.fg2, bg='#EEEEEE')
            for b in self.snippet_buttons: b.pack(side=tk.LEFT, padx=1)
            for b in self.clip_buttons: b.pack_forget()
            self.clip_list.pack_forget()
            self.snip_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.snip_scroll_v.pack(side=tk.RIGHT, fill=tk.Y)
            self._load_snippets()

    def _on_search(self):
        if self.tab_var.get() == 'clips': self._load_clips()
        else: self._load_snippets()

    def _toggle(self):
        """Always raise and focus the window"""
        try:
            if self.root.state() == 'iconic': self.root.deiconify()
        except: pass
        self.root.lift()
        self.root.focus_force()
        if self.tab_var.get() == 'clips': self._load_clips()
        else: self._load_snippets()

    def _quit(self):
        self.running = False
        self.root.destroy()

    # ======================= Clipboard Monitor =======================
    def _schedule_monitor(self):
        if not self.running: return
        try:
            try: current = pyperclip.paste()
            except: current = self.root.clipboard_get()
            if current and current != self.last_clip and len(current.strip()) > 0:
                self.last_clip = current
                preview = current.strip()[:60].replace('\n',' ')
                self.conn.execute("INSERT INTO clips(content,preview) VALUES(?,?)", (current, preview))
                self.conn.commit()
                if self.tab_var.get() == 'clips': self._load_clips()
                self.status.config(text=self._t("captured"))
        except Exception as e:
            self.status.config(text=f"监听中...")
        self.root.after(500, self._schedule_monitor)

    # ======================= Clips =======================
    def _load_clips(self):
        self.clip_list.delete(0, tk.END)
        kw = self.search_var.get().strip()
        if kw:
            rows = self.conn.execute(
                "SELECT id,preview,pinned FROM clips WHERE content LIKE ? OR preview LIKE ? ORDER BY pinned DESC, created_at DESC LIMIT 200",
                (f'%{kw}%', f'%{kw}%')).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id,preview,pinned FROM clips ORDER BY pinned DESC, created_at DESC LIMIT 200").fetchall()
        self._list_ids = []
        for cid, preview, pinned in rows:
            prefix = "📌 " if pinned else "   "
            self.clip_list.insert(tk.END, prefix + (preview or '(空)'))
            self._list_ids.append(('clip', cid))
        self.status.config(text=self._t("clips_count", count=len(rows)))

    def _load_snippets(self):
        # Clear old grid
        for w in self.snip_grid.winfo_children(): w.destroy()
        kw = self.search_var.get().strip()
        if kw:
            rows = self.conn.execute(
                "SELECT id,content,category FROM snippets WHERE content LIKE ? ORDER BY category, sort_order",
                (f'%{kw}%',)).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id,content,category FROM snippets ORDER BY category, sort_order").fetchall()
        self._snippet_ids = []
        last_cat = ""
        row_idx = 0; col_idx = 0
        max_cols = 4  # buttons per row - fits window cleanly
        # Determine button width: short symbols get smaller buttons, long text gets wider
        def btn_width(text):
            w = len(text) + 3
            return min(w, 28)
        for sid, content, cat in rows:
            if cat != last_cat:
                # Category header
                if col_idx > 0:
                    row_idx += 1; col_idx = 0
                header = tk.Label(self.snip_grid, text=cat, font=('Microsoft YaHei UI',9,'bold'),
                                  bg=self.card_bg, fg=self.accent, anchor='w')
                header.grid(row=row_idx, column=0, columnspan=max_cols, sticky='w', padx=4, pady=(10,2))
                row_idx += 1; col_idx = 0
                last_cat = cat
            display = content if len(content) <= 8 else content[:6] + '..'
            btn = tk.Button(self.snip_grid, text=display, font=('Microsoft YaHei UI',9),
                bg=self.card_bg, fg=self.fg, relief='flat', bd=1,
                padx=6, pady=3, cursor='hand2',
                command=lambda s=content, i=sid, b=None: self._snippet_click(s, i, b))
            # Fix lambda closure
            btn.configure(command=lambda s=content, i=sid, b=btn: self._snippet_click(s, i, b))
            btn.grid(row=row_idx, column=col_idx, sticky='ew', padx=1, pady=1)
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.accent, fg='white'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.card_bg, fg=self.fg))
            self._snippet_ids.append((btn, sid))
            col_idx += 1
            if col_idx >= max_cols:
                col_idx = 0; row_idx += 1
        self.status.config(text=self._t("clips_count", count=len(rows)))

    def _snippet_click(self, content, sid, btn):
        # Deselect previous (check widget still exists)
        if hasattr(self, '_last_snip_btn') and self._last_snip_btn:
            try: self._last_snip_btn.config(bg=self.card_bg, fg=self.fg)
            except: pass
        btn.config(bg=self.accent, fg='white')
        self._last_snip_btn = btn
        self._last_snip_id = sid
        self._last_snip_content = content
        self._show_preview(content)

    def _show_preview(self, text):
        self.preview_text.config(state=tk.NORMAL, fg=self.fg)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', text)
        self.preview_text.config(state=tk.DISABLED)

    def _clear_preview(self):
        self.preview_text.config(state=tk.NORMAL, fg='#BDBDBD')
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', self._t("preview_hint"))
        self.preview_text.config(state=tk.DISABLED)
        self._last_snip_id = None; self._last_snip_content = None
        self.status.config(text=self._t("preview_cleared"))

    def _on_select(self, e):
        sel = self.clip_list.curselection()
        if not sel: return
        idx = sel[0]
        if idx >= len(self._list_ids): return
        typ, rid = self._list_ids[idx]
        if typ != 'clip': return
        row = self.conn.execute("SELECT content FROM clips WHERE id=?", (rid,)).fetchone()
        if row: self._show_preview(row[0])

    def _copy_selected(self):
        if self.tab_var.get() == 'snippets':
            if hasattr(self, '_last_snip_content'):
                pyperclip.copy(self._last_snip_content)
                self.status.config(text=self._t("copied"))
            return
        sel = self.clip_list.curselection()
        if not sel: return
        idx = sel[0]
        if idx >= len(self._list_ids): return
        typ, rid = self._list_ids[idx]
        if typ != 'clip': return
        row = self.conn.execute("SELECT content FROM clips WHERE id=?", (rid,)).fetchone()
        if row:
            pyperclip.copy(row[0])
            self.status.config(text="✅ 已复制到剪贴板")
            self.conn.execute("UPDATE clips SET created_at=datetime('now','localtime') WHERE id=?", (rid,))
            self.conn.commit()
            self._load_clips()

    def _toggle_pin(self):
        sel = self.clip_list.curselection()
        if not sel: return
        idx = sel[0]
        if idx >= len(self._list_ids): return
        typ, rid = self._list_ids[idx]
        if typ != 'clip': return
        row = self.conn.execute("SELECT pinned FROM clips WHERE id=?", (rid,)).fetchone()
        if row:
            new_val = 0 if row[0] else 1
            self.conn.execute("UPDATE clips SET pinned=? WHERE id=?", (new_val, rid))
            self.conn.commit()
            self._load_clips()
            self.status.config(text=self._t("pinned") if new_val else self._t("unpinned"))

    def _delete_selected(self):
        if self.tab_var.get() == 'snippets':
            if hasattr(self, '_last_snip_id'):
                self.conn.execute("DELETE FROM snippets WHERE id=?", (self._last_snip_id,))
                self.conn.commit()
                self._load_snippets()
                self._last_snip_id = None
                self.status.config(text=self._t("deleted"))
            return
        sel = self.clip_list.curselection()
        if not sel: return
        idx = sel[0]
        if idx >= len(self._list_ids): return
        typ, rid = self._list_ids[idx]
        if typ != 'clip': return
        self.conn.execute("DELETE FROM clips WHERE id=?", (rid,))
        self.conn.commit()
        self._load_clips()
        self.status.config(text="🗑 已删除")

    def _clean_clips(self):
        if messagebox.askyesno(self._t("clean"), self._t("confirm_clean")):
            self.conn.execute("DELETE FROM clips WHERE pinned=0")
            self.conn.commit()
            self._load_clips()
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', self._t("clean_done"))
            self.preview_text.config(state=tk.DISABLED)
            self.status.config(text=self._t("cleaned"))

    # ======================= Snippets =======================
    def _add_snippet(self):
        text = simpledialog.askstring(self._t("add"), self._t("add_prompt"), parent=self.root)
        if not text or not text.strip(): return
        cat = simpledialog.askstring(self._t("add"), self._t("add_category"), initialvalue=self._t("cat_default"), parent=self.root)
        self.conn.execute("INSERT INTO snippets(title,content,category,sort_order) VALUES(?,?,?,0)",
                          (text[:30], text, cat or self._t("cat_default")))
        self.conn.commit()
        self._load_snippets()
        self.status.config(text=self._t("added"))

    def _edit_snippet(self):
        if not hasattr(self, '_last_snip_id') or not self._last_snip_id: return
        row = self.conn.execute("SELECT content FROM snippets WHERE id=?", (self._last_snip_id,)).fetchone()
        if not row: return
        if not row: return
        new_text = simpledialog.askstring(self._t("edit"), self._t("edit_prompt"), initialvalue=row[0], parent=self.root)
        if new_text and new_text.strip():
            self.conn.execute("UPDATE snippets SET content=?,title=? WHERE id=?", (new_text, new_text[:30], rid))
            self.conn.commit()
            self._load_snippets()
            self.status.config(text=self._t("updated"))


if __name__ == '__main__':
    try: import pyperclip
    except ImportError:
        os.system(f'"{sys.executable}" -m pip install pyperclip -q')
        import pyperclip
    app = ClipVault()
    app.root.mainloop()
