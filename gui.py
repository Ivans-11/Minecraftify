import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from tran import model_to_minecraft
import threading
from io import StringIO
import sys

# Language settings
LANGUAGES = {
    'en': {
        'title': '3DModel to Minecraft Converter',
        'obj_file': 'Model File',
        'world_path': 'Minecraft World Path',
        'browse': 'Browse',
        'materials': 'Materials',
        'wool': 'Wool',
        'concrete': 'Concrete',
        'terracotta': 'Terracotta',
        'glass': 'Glass',
        'advanced': 'Advanced Options',
        'start_pos': 'Start Position (x, y, z)',
        'rotate_angle': 'Rotate Angle (rx, ry, rz)',
        'pitch': 'Pitch',
        'game_version': 'Game Version (e.g., 1.20.1)',
        'convert': 'Convert',
        'language': 'Language',
        'save': 'Save Settings',
        'fold': 'Unfold/Fold',
        'error_no_file': 'Please select model file and world path',
        'convert_success': 'The conversion was successful! Enjoy your Minecraft model!',
        'convert_failed': 'Conversion failed',
        'output_msg': 'Output Message'
    },
    'zh': {
        'title': '三维模型转Minecraft工具',
        'obj_file': '模型文件',
        'world_path': 'Minecraft世界路径',
        'browse': '浏览',
        'materials': '材料',
        'wool': '羊毛',
        'concrete': '混凝土',
        'terracotta': '陶瓦',
        'glass': '玻璃',
        'advanced': '高级选项',
        'start_pos': '起始位置 (x, y, z)',
        'rotate_angle': '旋转角度 (rx, ry, rz)',
        'pitch': '体素大小',
        'game_version': '游戏版本 (如：1.20.1)',
        'convert': '转换',
        'language': '语言',
        'save': '保存设置',
        'fold': '展开/收起',
        'error_no_file': '未选择模型文件或世界路径',
        'convert_success': '转换成功！享受你的Minecraft模型！',
        'convert_failed': '转换失败',
        'output_msg': '输出信息'
    }
}

class StdoutRedirector(StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks() 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.language = self.load_language()
        self.model_dir = self.load_model_dir()
        self.world_dir = self.load_world_dir()
        self.title(LANGUAGES[self.language]['title'])
        self.geometry('800x700')
        self.minsize(800, 700)
        self.create_widgets()

    def load_language(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                try:
                    return json.load(f).get('language', 'zh')
                except json.JSONDecodeError:
                    return 'zh'
        else:
            return 'zh'
    
    def load_model_dir(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                try:
                    return json.load(f).get('model_dir', '')
                except json.JSONDecodeError:
                    return ''
        else:
            return ''
    
    def load_world_dir(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                try:
                    return json.load(f).get('world_dir', '')
                except json.JSONDecodeError:
                    return ''
        else:
            return ''

    def save_language(self):
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w') as f:
                json.dump({'language': self.language}, f)
        else:
            with open('settings.json', 'r') as f:
                try:
                    settings = json.load(f)
                except json.JSONDecodeError:
                    settings = {}
            settings['language'] = self.language
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
    
    def save_model_dir(self):
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w') as f:
                json.dump({'model_dir': self.model_dir}, f)
        else:
            with open('settings.json', 'r') as f:
                try:
                    settings = json.load(f)
                except json.JSONDecodeError:
                    settings = {}
            settings['model_dir'] = self.model_dir
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
    
    def save_world_dir(self):
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w') as f:
                json.dump({'world_dir': self.world_dir}, f)
        else:
            with open('settings.json', 'r') as f:
                try:
                    settings = json.load(f)
                except json.JSONDecodeError:
                    settings = {}
            settings['world_dir'] = self.world_dir
            with open('settings.json', 'w') as f:
                json.dump(settings, f)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Minecraftify", font=('Microsoft YaHei UI', 24, 'bold'))
        title_label.pack(pady=(0, 20))

        # File path
        file_frame = ttk.LabelFrame(main_frame, text=LANGUAGES[self.language]['obj_file'], padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.obj_file_entry = ttk.Entry(file_frame, width=50)
        self.obj_file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text=LANGUAGES[self.language]['browse'], command=self.browse_obj_file).pack(side=tk.RIGHT, padx=5)

        # World path
        world_frame = ttk.LabelFrame(main_frame, text=LANGUAGES[self.language]['world_path'], padding="10")
        world_frame.pack(fill=tk.X, pady=5)
        
        self.world_path_entry = ttk.Entry(world_frame, width=50)
        self.world_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(world_frame, text=LANGUAGES[self.language]['browse'], command=self.browse_world_path).pack(side=tk.RIGHT, padx=5)

        # Materials
        materials_frame = ttk.LabelFrame(main_frame, text=LANGUAGES[self.language]['materials'], padding="10")
        materials_frame.pack(fill=tk.X, pady=5)
        
        self.wool_var = tk.IntVar(value=1)
        self.concrete_var = tk.IntVar(value=1)
        self.terracotta_var = tk.IntVar(value=1)
        self.glass_var = tk.IntVar(value=1)
        
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['wool'], variable=self.wool_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['concrete'], variable=self.concrete_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['terracotta'], variable=self.terracotta_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['glass'], variable=self.glass_var).pack(side=tk.LEFT, padx=10)

        # Advanced options
        self.advanced_expanded = tk.BooleanVar(value=False)
        advanced_frame = ttk.LabelFrame(main_frame, text=LANGUAGES[self.language]['advanced'], padding="10")
        advanced_frame.pack(fill=tk.X, pady=5)
        
        advanced_content = ttk.Frame(advanced_frame)
        options = [
            (LANGUAGES[self.language]['start_pos'], '(0, -60, 0)'),
            (LANGUAGES[self.language]['rotate_angle'], '(0, 0, 0)'),
            (LANGUAGES[self.language]['pitch'], '1.0'),
            (LANGUAGES[self.language]['game_version'], '1.20.1')
        ]
        
        for i, (label_text, default_value) in enumerate(options):
            frame = ttk.Frame(advanced_content)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, width=20)
            entry.insert(0, default_value)
            entry.pack(side=tk.RIGHT, padx=5)
            setattr(self, f'option_entry_{i}', entry)
        
        ttk.Button(advanced_frame, text=LANGUAGES[self.language]['fold'], command=lambda: self.toggle_advanced(advanced_content)).pack(anchor='w', pady=5)
        
        if not self.advanced_expanded.get():
            advanced_content.pack_forget()

        # Language selection
        language_frame = ttk.Frame(main_frame)
        language_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(language_frame, text=LANGUAGES[self.language]['language']).pack(side=tk.LEFT, padx=5)
        self.language_combo = ttk.Combobox(language_frame, values=['zh', 'en'], state='readonly', width=5)
        self.language_combo.set(self.language)
        self.language_combo.bind('<<ComboboxSelected>>', self.change_language)
        self.language_combo.pack(side=tk.LEFT, padx=5)

        # Convert button
        convert_button = ttk.Button(main_frame, text=LANGUAGES[self.language]['convert'], command=self.convert)
        convert_button.pack(pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)

        # Output message
        output_frame = ttk.LabelFrame(main_frame, text=LANGUAGES[self.language]['output_msg'], padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.output_text = tk.Text(output_frame, height=4, width=60, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.bind("<Key>", lambda e: "break")

    def browse_obj_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Supported Files', '*.obj;*.stl;*.ply;*.off;*.glb;*.gltf'), ('OBJ Files', '*.obj'), ('STL Files', '*.stl'), ('PLY Files', '*.ply'), ('OFF Files', '*.off'), ('GLB Files', '*.glb;*.gltf')], initialdir=self.model_dir)
        if file_path:
            self.obj_file_entry.delete(0, tk.END)
            self.obj_file_entry.insert(0, file_path)
            self.model_dir = os.path.dirname(file_path)
            self.save_model_dir()

    def browse_world_path(self):
        folder_path = filedialog.askdirectory(initialdir=self.world_dir)
        if folder_path:
            self.world_path_entry.delete(0, tk.END)
            self.world_path_entry.insert(0, folder_path)
            self.world_dir = os.path.dirname(folder_path)
            self.save_world_dir()

    def change_language(self, event):
        self.language = self.language_combo.get()
        self.save_language()
        self.destroy()
        App().mainloop()

    def convert(self):
        obj_file = self.obj_file_entry.get()
        world_path = self.world_path_entry.get()
        if not obj_file or not world_path:
            messagebox.showerror(LANGUAGES[self.language]['title'], LANGUAGES[self.language]['error_no_file'])
            return

        def convert_thread():
            old_stdout = sys.stdout
            sys.stdout = StdoutRedirector(self.output_text)
            try:
                start_pos = eval(self.option_entry_0.get())
                rotate_angle = eval(self.option_entry_1.get())
                pitch = float(self.option_entry_2.get())
                game_version = ('java', tuple(map(int, self.option_entry_3.get().split('.'))))
                wool = bool(self.wool_var.get())
                concrete = bool(self.concrete_var.get())
                terracotta = bool(self.terracotta_var.get())
                glass = bool(self.glass_var.get())

                def call_back(stage_index, stage_num, current_step, stage_steps):
                    progress_percent = (stage_index + current_step / stage_steps) / stage_num * 100
                    self.progress['value'] = progress_percent
                    self.update_idletasks()

                model_to_minecraft(
                    obj_file=obj_file,
                    world_path=world_path,
                    start_pos=start_pos,
                    rotate_angle=rotate_angle,
                    pitch=pitch,
                    game_version=game_version,
                    wool=wool,
                    concrete=concrete,
                    terracotta=terracotta,
                    glass=glass,
                    call_back=call_back
                )
                messagebox.showinfo(LANGUAGES[self.language]['title'], LANGUAGES[self.language]['convert_success'])
            except Exception as e:
                messagebox.showerror(LANGUAGES[self.language]['title'], LANGUAGES[self.language]['convert_failed']+f': {str(e)}')
            finally:
                sys.stdout = old_stdout
                self.progress['value'] = 0

        threading.Thread(target=convert_thread).start()

    def toggle_advanced(self, content):
        if self.advanced_expanded.get():
            content.pack_forget()
        else:
            content.pack()
        self.advanced_expanded.set(not self.advanced_expanded.get())

if __name__ == '__main__':
    app = App()
    app.mainloop()