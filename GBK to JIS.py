import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import chardet

class EncodingConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Shift_JIS ⇄ GBK")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        self.setup_style()
        self.setup_ui()

    def setup_style(self):
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_light': '#f5f6fa',
            'bg_card': '#ffffff',
            'accent': '#0f3460',
            'accent_hover': '#e55039',
            'success': '#4834d4',
            'text_primary': '#2f3542',
            'text_secondary': '#57606f',
            'border': '#dfe4ea',
            'input_bg': '#f8f9fa',
            'output_bg': '#e8f4fd'
        }
        self.root.configure(bg=self.colors['bg_light'])
        
    def setup_ui(self):
        canvas = tk.Canvas(self.root, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        main_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_light'], padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        self.create_title(main_frame)
        self.create_input_card(main_frame)
        self.create_convert_buttons(main_frame)
        self.create_output_card(main_frame)
        self.create_function_buttons(main_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def create_title(self, parent):
        title_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        title_frame.pack(fill='x', pady=(0, 30))

        tk.Label(title_frame, text="🔄 字符编码转换器",
                font=('Microsoft YaHei UI', 24, 'bold'),
                fg=self.colors['bg_primary'], bg=self.colors['bg_light']).pack()

        tk.Label(title_frame, text="Shift_JIS ⇄ GBK 双向转换工具",
                font=('Microsoft YaHei UI', 12),
                fg=self.colors['text_secondary'], bg=self.colors['bg_light']).pack(pady=(5, 0))
    
    def create_card_frame(self, parent, title):
        card_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief='solid', bd=1)
        card_frame.pack(fill='both', expand=True, pady=(0, 20))

        content_frame = tk.Frame(card_frame, bg=self.colors['bg_card'], padx=25, pady=20)
        content_frame.pack(fill='both', expand=True)

        tk.Label(content_frame, text=title, font=('Microsoft YaHei UI', 14, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 15))

        return content_frame
    
    def create_input_card(self, parent):
        input_card = self.create_card_frame(parent, "📝 输入区域")

        encoding_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        encoding_frame.pack(fill='x', pady=(0, 15))

        tk.Label(encoding_frame, text="输入编码:", font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(side='left')

        self.input_encoding = ttk.Combobox(encoding_frame,
                                          values=['自动检测', 'UTF-8', 'GBK', 'Shift_JIS', 'GB2312'],
                                          state='readonly', width=12, font=('Microsoft YaHei UI', 10))
        self.input_encoding.set('自动检测')
        self.input_encoding.pack(side='left', padx=(10, 0))

        text_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, pady=(0, 15))

        tk.Label(text_frame, text="输入文本:", font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))

        self.input_text = scrolledtext.ScrolledText(text_frame, height=6, wrap=tk.WORD,
                                                   font=('Consolas', 11), bg=self.colors['input_bg'],
                                                   relief='solid', bd=1)
        self.input_text.pack(fill='both', expand=True)

        encoding_display_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        encoding_display_frame.pack(fill='both', expand=True)

        tk.Label(encoding_display_frame, text="字符编码信息:", font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))

        self.input_encoding_display = tk.Text(encoding_display_frame, height=4, wrap=tk.WORD,
                                            font=('Consolas', 9), bg=self.colors['input_bg'],
                                            fg=self.colors['text_secondary'], relief='solid', bd=1, state='disabled')
        self.input_encoding_display.pack(fill='both', expand=True)

        for event in ['<KeyRelease>', '<Button-1>']:
            self.input_text.bind(event, self.on_input_change)
        self.input_encoding.bind('<<ComboboxSelected>>', self.on_input_change)
    
    def create_convert_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        button_frame.pack(pady=20)

        btn_config = {
            'font': ('Microsoft YaHei UI', 12, 'bold'),
            'fg': 'white', 'relief': 'flat', 'padx': 25, 'pady': 12, 'cursor': 'hand2'
        }

        self.convert_to_gbk_btn = tk.Button(button_frame, text="🔄 转换为 GBK",
                                           command=self.convert_to_gbk, bg=self.colors['accent'], **btn_config)
        self.convert_to_gbk_btn.pack(side='left', padx=(0, 15))

        self.convert_to_sjis_btn = tk.Button(button_frame, text="🔄 转换为 Shift_JIS",
                                            command=self.convert_to_sjis, bg=self.colors['success'], **btn_config)
        self.convert_to_sjis_btn.pack(side='left', padx=(15, 0))

        self.add_hover_effects()

    def add_hover_effects(self):
        def bind_hover(btn, normal_color, hover_color):
            btn.bind("<Enter>", lambda _: btn.config(bg=hover_color))
            btn.bind("<Leave>", lambda _: btn.config(bg=normal_color))

        bind_hover(self.convert_to_gbk_btn, self.colors['accent'], self.colors['accent_hover'])
        bind_hover(self.convert_to_sjis_btn, self.colors['success'], '#6c5ce7')

    def create_output_card(self, parent):
        output_card = self.create_card_frame(parent, "📤 输出区域")

        encoding_info_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        encoding_info_frame.pack(fill='x', pady=(0, 15))

        tk.Label(encoding_info_frame, text="输出编码:", font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(side='left')

        self.output_encoding_label = tk.Label(encoding_info_frame, text="未转换",
                                             font=('Microsoft YaHei UI', 11, 'bold'),
                                             fg='#e74c3c', bg=self.colors['bg_card'])
        self.output_encoding_label.pack(side='left', padx=(10, 0))

        text_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, pady=(0, 15))

        tk.Label(text_frame, text="输出文本:", font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))

        self.output_text = scrolledtext.ScrolledText(text_frame, height=6, wrap=tk.WORD,
                                                    font=('Consolas', 11), bg=self.colors['output_bg'],
                                                    relief='solid', bd=1, state='disabled')
        self.output_text.pack(fill='both', expand=True)

        encoding_display_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        encoding_display_frame.pack(fill='both', expand=True)

        tk.Label(encoding_display_frame, text="输出字符编码信息:", font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))

        self.output_encoding_display = tk.Text(encoding_display_frame, height=4, wrap=tk.WORD,
                                             font=('Consolas', 9), bg=self.colors['output_bg'],
                                             fg=self.colors['text_secondary'], relief='solid', bd=1, state='disabled')
        self.output_encoding_display.pack(fill='both', expand=True)
    
    def create_function_buttons(self, parent):
        func_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        func_frame.pack(pady=20)

        btn_config = {'font': ('Microsoft YaHei UI', 10), 'fg': 'white', 'relief': 'flat',
                     'padx': 20, 'pady': 8, 'cursor': 'hand2'}

        tk.Button(func_frame, text="🗑️ 清空所有", command=self.clear_all,
                 bg='#e74c3c', **btn_config).pack(side='left', padx=(0, 10))

        tk.Button(func_frame, text="📋 复制输出", command=self.copy_output,
                 bg='#f39c12', **btn_config).pack(side='left', padx=(10, 0))
    
    def detect_encoding(self, text):
        if not text.strip():
            return 'utf-8'

        try:
            result = chardet.detect(text.encode('utf-8'))
            if result and result['encoding']:
                detected = result['encoding'].lower()
                if 'shift' in detected or 'sjis' in detected:
                    return 'shift_jis'
                elif 'gb' in detected:
                    return 'gbk'
                return detected
        except:
            pass

        for char in text:
            if ord(char) > 0xFF00 or '\u4e00' <= char <= '\u9fff':
                return 'utf-8'

        return 'utf-8'
    
    def get_char_encoding_info(self, text, encoding):
        if not text.strip():
            return ""

        info_lines = []
        char_count = 0

        for char in text[:50]:
            if char_count >= 15:
                info_lines.append("... (更多字符)")
                break

            if char.strip() or char == '　':
                try:
                    target_bytes = char.encode(encoding)
                    target_hex = ' '.join(f'{b:02X}' for b in target_bytes)
                    info_lines.append(f"'{char}' -> [{target_hex}]")
                except UnicodeEncodeError:
                    info_lines.append(f"'{char}' -> [无法编码为 {encoding.upper()}]")
                except Exception as e:
                    info_lines.append(f"'{char}' -> 错误: {str(e)}")

                char_count += 1

        return '\n'.join(info_lines)
    
    def update_text_widget(self, widget, content):
        """更新文本控件内容"""
        widget.config(state='normal')
        widget.delete(1.0, tk.END)
        widget.insert(1.0, content)
        widget.config(state='disabled')
    
    def on_input_change(self, _=None):
        text = self.input_text.get(1.0, tk.END).strip()

        if text:
            if self.input_encoding.get() == '自动检测':
                detected_encoding = self.detect_encoding(text)
                encoding_info = f"🔍 检测编码: {detected_encoding.upper()}\n" + "="*50 + "\n"
            else:
                detected_encoding = self.input_encoding.get().lower()
                encoding_info = f"📌 指定编码: {detected_encoding.upper()}\n" + "="*50 + "\n"

            char_info = self.get_char_encoding_info(text, detected_encoding)
            self.update_text_widget(self.input_encoding_display, encoding_info + char_info)
        else:
            self.update_text_widget(self.input_encoding_display, "")

    def convert_to_gbk(self):
        self.convert_encoding('gbk')

    def convert_to_sjis(self):
        self.convert_encoding('shift_jis')
    
    def convert_encoding(self, target_encoding):
        input_text = self.input_text.get(1.0, tk.END).strip()

        if not input_text:
            messagebox.showwarning("⚠️ 警告", "请输入要转换的文本！")
            return

        try:
            source_encoding = (self.detect_encoding(input_text) if self.input_encoding.get() == '自动检测'
                             else self.input_encoding.get().lower())

            converted_text = input_text

            if source_encoding.lower() == target_encoding.lower():
                conversion_info = f"源编码与目标编码相同（{target_encoding.upper()}）"
                messagebox.showinfo("ℹ️ 提示", f"源编码与目标编码相同（{target_encoding.upper()}），显示原文。")
            else:
                conversion_info = f"从 {source_encoding.upper()} 转换为 {target_encoding.upper()}"

                test_chars = [char for char in input_text
                            if not self.can_encode(char, target_encoding)]

                if test_chars:
                    conversion_info += f"\n⚠️ 警告：{len(test_chars)}个字符无法在{target_encoding.upper()}中编码"

            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, converted_text)
            self.output_text.config(state='disabled')

            self.output_encoding_label.config(text=target_encoding.upper(), fg='#27ae60')

            encoding_info = f"🎯 目标编码: {target_encoding.upper()}\n{conversion_info}\n" + "="*50 + "\n"
            char_info = self.get_char_encoding_info(converted_text, target_encoding)
            self.update_text_widget(self.output_encoding_display, encoding_info + char_info)

            if source_encoding.lower() != target_encoding.lower():
                messagebox.showinfo("✅ 转换完成", f"文本已成功转换为 {target_encoding.upper()} 编码格式！")

        except Exception as e:
            messagebox.showerror("❌ 错误", f"转换过程中发生错误: {str(e)}")

    def can_encode(self, char, encoding):
        try:
            char.encode(encoding)
            return True
        except UnicodeEncodeError:
            return False
    
    def clear_all(self):
        self.input_text.delete(1.0, tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.update_text_widget(self.input_encoding_display, "")
        self.update_text_widget(self.output_encoding_display, "")
        self.output_encoding_label.config(text="未转换", fg='#e74c3c')
        messagebox.showinfo("🗑️ 清空完成", "所有内容已清空！")

    def copy_output(self):
        output_text = self.output_text.get(1.0, tk.END).strip()
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            messagebox.showinfo("📋 复制成功", "输出文本已复制到剪贴板！")
        else:
            messagebox.showwarning("⚠️ 警告", "没有可复制的输出文本！")

def main():
    root = tk.Tk()
    root.minsize(800, 600)

    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    EncodingConverter(root)

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()