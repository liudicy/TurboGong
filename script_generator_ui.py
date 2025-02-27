import tkinter as tk
from tkinter import filedialog, messagebox
from template_validator import TemplateValidator

class ScriptGeneratorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("脚本生成器")
        self.root.geometry("600x400")
        
        self.validator = TemplateValidator()
        self.template_path = None
        self.excel_path = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # 模板选择部分
        template_frame = tk.LabelFrame(self.root, text="第一步：选择模板", padx=10, pady=5)
        template_frame.pack(fill="x", padx=10, pady=5)
        
        self.template_label = tk.Label(template_frame, text="未选择模板文件")
        self.template_label.pack(side="left", padx=5)
        
        template_btn = tk.Button(template_frame, text="选择模板", command=self.select_template)
        template_btn.pack(side="right", padx=5)
        
        # Excel选择部分
        excel_frame = tk.LabelFrame(self.root, text="第二步：选择数据表格", padx=10, pady=5)
        excel_frame.pack(fill="x", padx=10, pady=5)
        
        self.excel_label = tk.Label(excel_frame, text="未选择Excel文件")
        self.excel_label.pack(side="left", padx=5)
        
        self.excel_btn = tk.Button(excel_frame, text="选择Excel", 
                                 command=self.select_excel,
                                 state="disabled")
        self.excel_btn.pack(side="right", padx=5)
        
        # 生成按钮
        self.generate_btn = tk.Button(self.root, text="生成脚本", 
                                    command=self.generate_scripts,
                                    state="disabled")
        self.generate_btn.pack(pady=20)
        
    def select_template(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            if self.validator.load_template(file_path):
                self.template_path = file_path
                self.template_label.config(text=f"已选择: {file_path}")
                self.excel_btn.config(state="normal")
            else:
                messagebox.showerror("错误", "模板文件加载失败")
    
    def select_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xls")]
        )
        if file_path:
            is_valid, missing_fields = self.validator.validate_excel(file_path)
            if is_valid:
                self.excel_path = file_path
                self.excel_label.config(text=f"已选择: {file_path}")
                self.generate_btn.config(state="normal")
            else:
                messagebox.showerror("错误", 
                    f"Excel文件缺少以下字段：\n{', '.join(missing_fields)}")
    
    def generate_scripts(self):
        """生成脚本文件"""
        if not self.template_path or not self.excel_path:
            messagebox.showerror("错误", "请先选择模板和Excel文件")
            return
        
        # 选择输出目录
        output_dir = filedialog.askdirectory(title="选择脚本输出目录")
        if not output_dir:
            return
        
        # 创建配置生成器
        from src.config_generator import ConfigGenerator
        generator = ConfigGenerator(self.validator.template_content)
        
        # 生成脚本
        generated_files = generator.generate_scripts(self.excel_path, output_dir)
        
        if generated_files:
            messagebox.showinfo("成功", 
                f"已成功生成 {len(generated_files)} 个脚本文件\n保存位置：{output_dir}")
        else:
            messagebox.showerror("错误", "生成脚本过程中发生错误")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScriptGeneratorUI()
    app.run() 