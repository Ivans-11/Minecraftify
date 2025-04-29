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
        # Title
        ttk.Label(self, text="Minecraftify", font=('Helvetica', 24, 'bold')).grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        # File selection
        ttk.Label(self, text=LANGUAGES[self.language]['obj_file']).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.obj_file_entry = ttk.Entry(self, width=50)
        self.obj_file_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self, text=LANGUAGES[self.language]['browse'], command=self.browse_obj_file).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self, text=LANGUAGES[self.language]['world_path']).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.world_path_entry = ttk.Entry(self, width=50)
        self.world_path_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self, text=LANGUAGES[self.language]['browse'], command=self.browse_world_path).grid(row=2, column=2, padx=5, pady=5)

        # Materials selection
        ttk.Label(self, text=LANGUAGES[self.language]['materials']).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        materials_frame = ttk.Frame(self)
        materials_frame.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky='w')
        #ttk.Label(materials_frame, text=LANGUAGES[self.language]['materials']).pack(side=tk.LEFT, padx=10)
        self.wool_var = tk.IntVar(value=1)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['wool'], variable=self.wool_var).pack(side=tk.LEFT, padx=5)
        self.concrete_var = tk.IntVar(value=1)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['concrete'], variable=self.concrete_var).pack(side=tk.LEFT, padx=5)
        self.terracotta_var = tk.IntVar(value=1)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['terracotta'], variable=self.terracotta_var).pack(side=tk.LEFT, padx=5)
        self.glass_var = tk.IntVar(value=1)
        ttk.Checkbutton(materials_frame, text=LANGUAGES[self.language]['glass'], variable=self.glass_var).pack(side=tk.LEFT, padx=5)

        # Advanced options
        self.advanced_expanded = tk.BooleanVar(value=False)
        advanced_frame = ttk.LabelFrame(self, text=LANGUAGES[self.language]['advanced'], padding=10)
        advanced_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        advanced_content = ttk.Frame(advanced_frame)

        ttk.Label(advanced_content, text=LANGUAGES[self.language]['start_pos']).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.start_pos_entry = ttk.Entry(advanced_content, width=20)
        self.start_pos_entry.insert(0, '(0, -60, 0)')
        self.start_pos_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(advanced_content, text=LANGUAGES[self.language]['rotate_angle']).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.rotate_angle_entry = ttk.Entry(advanced_content, width=20)
        self.rotate_angle_entry.insert(0, '(0, 0, 0)')
        self.rotate_angle_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(advanced_content, text=LANGUAGES[self.language]['pitch']).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.pitch_entry = ttk.Entry(advanced_content, width=20)
        self.pitch_entry.insert(0, '1.0')
        self.pitch_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(advanced_content, text=LANGUAGES[self.language]['game_version']).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.game_version_entry = ttk.Entry(advanced_content, width=20)
        self.game_version_entry.insert(0, '1.20.1')
        self.game_version_entry.grid(row=3, column=1, padx=5, pady=5)

        def fold_advanced():
            if self.advanced_expanded.get():
                advanced_content.pack_forget()
            else:
                advanced_content.pack()
            self.advanced_expanded.set(not self.advanced_expanded.get())

        ttk.Button(advanced_frame, text=LANGUAGES[self.language]['fold'], command=fold_advanced).pack(anchor='w')

        if not self.advanced_expanded.get():
            advanced_content.pack_forget()

        # Language selection
        ttk.Label(self, text=LANGUAGES[self.language]['language']).grid(row=9, column=0, padx=5, pady=5, sticky='e')
        self.language_combo = ttk.Combobox(self, values=['zh', 'en'], state='readonly')
        self.language_combo.set(self.language)
        self.language_combo.bind('<<ComboboxSelected>>', self.change_language)
        self.language_combo.grid(row=9, column=1, padx=5, pady=5)

        # Convert button
        ttk.Button(self, text=LANGUAGES[self.language]['convert'], command=self.convert).grid(row=10, column=1, padx=5, pady=20)

        # Output text
        self.output_text = tk.Text(self, height=10, width=60)
        self.output_text.grid(row=11, column=0, columnspan=3, padx=5, pady=5)
        def disable_edit(event):
            return "break"
        self.output_text.bind("<Key>", disable_edit)

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
                start_pos = eval(self.start_pos_entry.get())
                rotate_angle = eval(self.rotate_angle_entry.get())
                pitch = float(self.pitch_entry.get())
                game_version = ('java', tuple(map(int, self.game_version_entry.get().split('.'))))
                wool = bool(self.wool_var.get())
                concrete = bool(self.concrete_var.get())
                terracotta = bool(self.terracotta_var.get())
                glass = bool(self.glass_var.get())

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
                    glass=glass
                )
                messagebox.showinfo(LANGUAGES[self.language]['title'], LANGUAGES[self.language]['convert_success'])
            except Exception as e:
                messagebox.showerror(LANGUAGES[self.language]['title'], LANGUAGES[self.language]['convert_failed']+f': {str(e)}')
            finally:
                sys.stdout = old_stdout

        threading.Thread(target=convert_thread).start()

if __name__ == '__main__':
    app = App()
    app.mainloop()