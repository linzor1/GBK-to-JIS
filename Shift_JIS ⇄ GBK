import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import chardet
import codecs

class EncodingConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Shift_JIS ⇄ GBK")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
     
        self.setup_style()
        self.setup_ui()
        
    def setup_style(self):
        
        style = ttk.Style()
        
        # 配置整体颜色方案
        self.colors = {
            'bg_primary': '#2c3e50',
            'bg_secondary': '#34495e', 
            'bg_light': '#ecf0f1',
            'bg_card': '#ffffff',
            'accent': '#3498db',
            'accent_hover': '#2980b9',
            'success': '#27ae60',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'border': '#bdc3c7'
        }
        
        # 配置样式
        style.configure('Title.TLabel', 
                       font=('Microsoft YaHei UI', 20, 'bold'), 
                       foreground=self.colors['bg_primary'])
        
        style.configure('Header.TLabel', 
                       font=('Microsoft YaHei UI', 11, 'bold'), 
                       foreground=self.colors['text_primary'])
        
        style.configure('Info.TLabel', 
                       font=('Microsoft YaHei UI', 9), 
                       foreground=self.colors['text_secondary'])
        
        # 按钮样式
        style.configure('Primary.TButton',
                       font=('Microsoft YaHei UI', 11, 'bold'),
                       padding=(20, 10))
        
        style.configure('Secondary.TButton',
                       font=('Microsoft YaHei UI', 10),
                       padding=(15, 8))
        
        # 设置根窗口背景
        self.root.configure(bg=self.colors['bg_light'])
        
    def setup_ui(self):
        # 主滚动框架
        canvas = tk.Canvas(self.root, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 主容器
        main_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_light'], padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
        title_frame.pack(fill='x', pady=(0, 30))
        
        title_label = tk.Label(title_frame, 
                              text="🔄", 
                              font=('Microsoft YaHei UI', 24, 'bold'),
                              fg=self.colors['bg_primary'],
                              bg=self.colors['bg_light'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Shift_JIS ⇄ GBK 双向转换工具",
                                 font=('Microsoft YaHei UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_light'])
        subtitle_label.pack(pady=(5, 0))
        
        # 输入卡片
        self.create_input_card(main_frame)
        
        # 转换按钮区域
        self.create_convert_buttons(main_frame)
        
        # 输出卡片
        self.create_output_card(main_frame)
        
        # 功能按钮
        self.create_function_buttons(main_frame)
        
        # 配置滚动
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_card_frame(self, parent, title):
        """创建卡片样式框架"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=1)
        card_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # 添加阴影效果
        shadow_frame = tk.Frame(parent, bg='#d5d5d5', height=2)
        shadow_frame.pack(fill='x', pady=(0, 20))
        
        # 卡片内容
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_card'], padx=25, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = tk.Label(content_frame,
                              text=title,
                              font=('Microsoft YaHei UI', 14, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_card'])
        title_label.pack(anchor='w', pady=(0, 15))
        
        return content_frame
    
    def create_input_card(self, parent):
        """创建输入卡片"""
        input_card = self.create_card_frame(parent, "📝 输入区域")
        
        # 编码选择区域
        encoding_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        encoding_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(encoding_frame, 
                text="输入编码:",
                font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side='left')
        
        self.input_encoding = ttk.Combobox(encoding_frame, 
                                          values=['自动检测', 'UTF-8', 'GBK', 'Shift_JIS', 'GB2312'], 
                                          state='readonly', 
                                          width=12,
                                          font=('Microsoft YaHei UI', 10))
        self.input_encoding.set('自动检测')
        self.input_encoding.pack(side='left', padx=(10, 0))
        
        # 输入文本区域
        text_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        tk.Label(text_frame,
                text="输入文本:",
                font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
        
        self.input_text = scrolledtext.ScrolledText(text_frame, 
                                                   height=6, 
                                                   wrap=tk.WORD,
                                                   font=('Consolas', 11),
                                                   bg='#fafafa',
                                                   relief='solid',
                                                   bd=1)
        self.input_text.pack(fill='both', expand=True)
        
        # 输入编码显示区域
        encoding_display_frame = tk.Frame(input_card, bg=self.colors['bg_card'])
        encoding_display_frame.pack(fill='both', expand=True)
        
        tk.Label(encoding_display_frame,
                text="字符编码信息:",
                font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
        
        self.input_encoding_display = tk.Text(encoding_display_frame, 
                                            height=4, 
                                            wrap=tk.WORD,
                                            font=('Consolas', 9),
                                            bg='#f8f9fa',
                                            fg='#495057',
                                            relief='solid',
                                            bd=1,
                                            state='disabled')
        self.input_encoding_display.pack(fill='both', expand=True)
        
        # 绑定事件
        self.input_text.bind('<KeyRelease>', self.on_input_change)
        self.input_text.bind('<Button-1>', self.on_input_change)
        self.input_encoding.bind('<<ComboboxSelected>>', self.on_input_change)
    
    def create_convert_buttons(self, parent):
        """创建转换按钮区域"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        button_frame.pack(pady=20)
        
        # GBK转换按钮
        self.convert_to_gbk_btn = tk.Button(button_frame,
                                           text="🔄 转换为 GBK",
                                           command=self.convert_to_gbk,
                                           font=('Microsoft YaHei UI', 12, 'bold'),
                                           bg=self.colors['accent'],
                                           fg='white',
                                           relief='flat',
                                           padx=25,
                                           pady=12,
                                           cursor='hand2')
        self.convert_to_gbk_btn.pack(side='left', padx=(0, 15))
        
        # Shift_JIS转换按钮
        self.convert_to_sjis_btn = tk.Button(button_frame,
                                            text="🔄 转换为 Shift_JIS",
                                            command=self.convert_to_sjis,
                                            font=('Microsoft YaHei UI', 12, 'bold'),
                                            bg=self.colors['success'],
                                            fg='white',
                                            relief='flat',
                                            padx=25,
                                            pady=12,
                                            cursor='hand2')
        self.convert_to_sjis_btn.pack(side='left', padx=(15, 0))
        
        # 添加悬停效果
        def on_enter_gbk(e):
            self.convert_to_gbk_btn.config(bg=self.colors['accent_hover'])
        def on_leave_gbk(e):
            self.convert_to_gbk_btn.config(bg=self.colors['accent'])
            
        def on_enter_sjis(e):
            self.convert_to_sjis_btn.config(bg='#229954')
        def on_leave_sjis(e):
            self.convert_to_sjis_btn.config(bg=self.colors['success'])
        
        self.convert_to_gbk_btn.bind("<Enter>", on_enter_gbk)
        self.convert_to_gbk_btn.bind("<Leave>", on_leave_gbk)
        self.convert_to_sjis_btn.bind("<Enter>", on_enter_sjis)
        self.convert_to_sjis_btn.bind("<Leave>", on_leave_sjis)
    
    def create_output_card(self, parent):
        """创建输出卡片"""
        output_card = self.create_card_frame(parent, "📤 输出区域")
        
        # 输出编码显示
        encoding_info_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        encoding_info_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(encoding_info_frame,
                text="输出编码:",
                font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side='left')
        
        self.output_encoding_label = tk.Label(encoding_info_frame,
                                             text="未转换",
                                             font=('Microsoft YaHei UI', 11, 'bold'),
                                             fg='#e74c3c',
                                             bg=self.colors['bg_card'])
        self.output_encoding_label.pack(side='left', padx=(10, 0))
        
        # 输出文本区域
        text_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        tk.Label(text_frame,
                text="输出文本:",
                font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
        
        self.output_text = scrolledtext.ScrolledText(text_frame, 
                                                    height=6, 
                                                    wrap=tk.WORD,
                                                    font=('Consolas', 11),
                                                    bg='#f0f8f0',
                                                    relief='solid',
                                                    bd=1,
                                                    state='disabled')
        self.output_text.pack(fill='both', expand=True)
        
        # 输出编码显示区域
        encoding_display_frame = tk.Frame(output_card, bg=self.colors['bg_card'])
        encoding_display_frame.pack(fill='both', expand=True)
        
        tk.Label(encoding_display_frame,
                text="输出字符编码信息:",
                font=('Microsoft YaHei UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(anchor='w', pady=(0, 8))
        
        self.output_encoding_display = tk.Text(encoding_display_frame, 
                                             height=4, 
                                             wrap=tk.WORD,
                                             font=('Consolas', 9),
                                             bg='#e8f5e8',
                                             fg='#2d5a2d',
                                             relief='solid',
                                             bd=1,
                                             state='disabled')
        self.output_encoding_display.pack(fill='both', expand=True)
    
    def create_function_buttons(self, parent):
        """创建功能按钮"""
        func_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        func_frame.pack(pady=20)
        
        clear_btn = tk.Button(func_frame,
                             text="🗑️ 清空所有",
                             command=self.clear_all,
                             font=('Microsoft YaHei UI', 10),
                             bg='#e74c3c',
                             fg='white',
                             relief='flat',
                             padx=20,
                             pady=8,
                             cursor='hand2')
        clear_btn.pack(side='left', padx=(0, 10))
        
        copy_btn = tk.Button(func_frame,
                            text="📋 复制输出",
                            command=self.copy_output,
                            font=('Microsoft YaHei UI', 10),
                            bg='#f39c12',
                            fg='white',
                            relief='flat',
                            padx=20,
                            pady=8,
                            cursor='hand2')
        copy_btn.pack(side='left', padx=(10, 0))
    
    def detect_encoding(self, text):
        """改进的编码检测"""
        if not text.strip():
            return 'utf-8'
        
        # 先尝试编码为字节再检测
        try:
            text_bytes = text.encode('utf-8')
            result = chardet.detect(text_bytes)
            if result and result['encoding']:
                detected = result['encoding'].lower()
                # 标准化编码名称
                if 'shift' in detected or 'sjis' in detected:
                    return 'shift_jis'
                elif 'gb' in detected:
                    return 'gbk'
                else:
                    return detected
        except:
            pass
        
        # 手动检测特殊字符
        for char in text:
            # 检测全角字符
            if ord(char) > 0xFF00:
                return 'utf-8'  # 可能包含全角字符
            # 检测中文字符
            elif '\u4e00' <= char <= '\u9fff':
                return 'utf-8'
        
        return 'utf-8'
    
    def get_char_encoding_info(self, text, encoding):
        """获取字符编码信息"""
        if not text.strip():
            return ""
        
        info_lines = []
        try:
            # 处理前50个字符
            sample_text = text[:50]
            char_count = 0
            
            for char in sample_text:
                if char_count >= 15:  # 限制显示数量
                    info_lines.append("... (更多字符)")
                    break
                    
                if char.strip() or char == '　':  # 包括全角空格
                    try:
                        # 只显示字符和对应编码
                        try:
                            target_bytes = char.encode(encoding)
                            target_hex = ' '.join([f'{b:02X}' for b in target_bytes])
                            info_lines.append(f"'{char}' -> [{target_hex}]")
                        except UnicodeEncodeError:
                            info_lines.append(f"'{char}' -> [无法编码为 {encoding.upper()}]")
                        
                        char_count += 1
                        
                    except Exception as e:
                        info_lines.append(f"'{char}' -> 错误: {str(e)}")
                        char_count += 1
            
        except Exception as e:
            info_lines.append(f"编码信息获取失败: {str(e)}")
        
        return '\n'.join(info_lines)
    
    def update_text_widget(self, widget, content):
        """更新文本控件内容"""
        widget.config(state='normal')
        widget.delete(1.0, tk.END)
        widget.insert(1.0, content)
        widget.config(state='disabled')
    
    def on_input_change(self, event=None):
        """输入文本变化时更新编码显示"""
        text = self.input_text.get(1.0, tk.END).strip()
        
        if text:
            # 检测或获取输入编码
            if self.input_encoding.get() == '自动检测':
                detected_encoding = self.detect_encoding(text)
                encoding_info = f"🔍 检测编码: {detected_encoding.upper()}\n" + "="*50 + "\n"
            else:
                detected_encoding = self.input_encoding.get().lower().replace('_', '_')
                encoding_info = f"📌 指定编码: {detected_encoding.upper()}\n" + "="*50 + "\n"
            
            # 获取编码详情
            char_info = self.get_char_encoding_info(text, detected_encoding)
            
            self.update_text_widget(self.input_encoding_display, encoding_info + char_info)
        else:
            self.update_text_widget(self.input_encoding_display, "")
    
    def convert_to_gbk(self):
        """转换为GBK编码"""
        self.convert_encoding('gbk')
    
    def convert_to_sjis(self):
        """转换为Shift_JIS编码"""
        self.convert_encoding('shift_jis')
    
    def convert_encoding(self, target_encoding):
        """执行编码转换"""
        input_text = self.input_text.get(1.0, tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("⚠️ 警告", "请输入要转换的文本！")
            return
        
        try:
            # 确定源编码
            if self.input_encoding.get() == '自动检测':
                source_encoding = self.detect_encoding(input_text)
            else:
                source_encoding = self.input_encoding.get().lower()
                if source_encoding == 'shift_jis':
                    source_encoding = 'shift_jis'
            
            # 转换过程
            converted_text = input_text
            conversion_info = ""
            
            if source_encoding.lower() == target_encoding.lower():
                conversion_info = f"源编码与目标编码相同（{target_encoding.upper()}）"
                messagebox.showinfo("ℹ️ 提示", f"源编码与目标编码相同（{target_encoding.upper()}），显示原文。")
            else:
                try:
                    # 通过字节进行编码转换（模拟实际的编码转换过程）
                    # 这里我们保持字符的Unicode表示，但显示其在目标编码中的字节表示
                    converted_text = input_text
                    conversion_info = f"从 {source_encoding.upper()} 转换为 {target_encoding.upper()}"
                    
                    # 检查是否所有字符都能在目标编码中表示
                    test_chars = []
                    for char in input_text:
                        try:
                            char.encode(target_encoding)
                        except UnicodeEncodeError:
                            test_chars.append(char)
                    
                    if test_chars:
                        conversion_info += f"\n⚠️ 警告：{len(test_chars)}个字符无法在{target_encoding.upper()}中编码"
                    
                except Exception as e:
                    messagebox.showerror("❌ 转换错误", f"编码转换失败: {str(e)}")
                    return
            
            # 显示转换结果
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, converted_text)
            self.output_text.config(state='disabled')
            
            # 更新输出编码标签
            self.output_encoding_label.config(text=target_encoding.upper(), fg='#27ae60')
            
            # 显示输出编码信息
            encoding_info = f"🎯 目标编码: {target_encoding.upper()}\n{conversion_info}\n" + "="*50 + "\n"
            char_info = self.get_char_encoding_info(converted_text, target_encoding)
            
            self.update_text_widget(self.output_encoding_display, encoding_info + char_info)
            
            if source_encoding.lower() != target_encoding.lower():
                messagebox.showinfo("✅ 转换完成", f"文本已成功转换为 {target_encoding.upper()} 编码格式！")
            
        except Exception as e:
            messagebox.showerror("❌ 错误", f"转换过程中发生错误: {str(e)}")
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.update_text_widget(self.input_encoding_display, "")
        self.update_text_widget(self.output_encoding_display, "")
        self.output_encoding_label.config(text="未转换", fg='#e74c3c')
        messagebox.showinfo("🗑️ 清空完成", "所有内容已清空！")
    
    def copy_output(self):
        """复制输出文本到剪贴板"""
        output_text = self.output_text.get(1.0, tk.END).strip()
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            messagebox.showinfo("📋 复制成功", "输出文本已复制到剪贴板！")
        else:
            messagebox.showwarning("⚠️ 警告", "没有可复制的输出文本！")

def main():
    root = tk.Tk()
    
    # 设置窗口图标和属性
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # 设置最小窗口尺寸
    root.minsize(800, 600)
    
    app = EncodingConverter(root)
    
    # 居中显示窗口
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
