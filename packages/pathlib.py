from pathlib import Path
import os #传统 

# ==========================================
# 1. 基础创建与拼接 (The Modern Way)
# ==========================================
# 获取当前工作目录
cwd = Path.cwd()
os.getcwd()

# 获取用户家目录 (~ 目录)
home = Path.home()

# 路径拼接：使用 / 运算符，自动处理不同系统的斜杠
# 即使后面是字符串，只要前面是 Path 对象就能直接拼
data_file = Path("data") / "logs" / "test.log"
os.path.join('a','b')

# ==========================================
# 2. 路径属性提取 (不再需要 os.path.split)
# ==========================================
p = Path("projects/ai/model.tar.gz")

print(p.name)      # 'model.tar.gz' (文件名) os.path.basename(p)
print(p.stem)      # 'model.tar'    (不带后缀的文件名)
print(p.suffix)    # '.gz'          (最后一个后缀) os.path.splitext(p)[1]
print(p.suffixes)  # ['.tar', '.gz'] (所有后缀列表)
print(p.parent)    # 'projects/ai'  (父级目录)
print(p.parts)     # ('projects', 'ai', 'model.tar.gz') (路径拆分)



# ==========================================
# 3. 目录操作 (安全且强大)
# ==========================================
new_dir = Path("output/results")

# 创建目录：
# parents=True  -> 自动创建中间不存在的文件夹 (mkdir -p)
# exist_ok=True -> 如果文件夹已存在，不报错
new_dir.mkdir(parents=True, exist_ok=True) 
# os.makedirs(p, exist_ok=True)

# 检查路径状态
print(new_dir.exists())  # 是否存在 os.path.exists(p)
print(new_dir.is_dir())  # 是否是目录
print(new_dir.is_file()) # 是否是文件

# ==========================================
# 4. 文件查找与遍历 (Glob 模式)
# ==========================================
base = Path(".")

# 搜索当前目录下所有的 .py 文件 (不含子目录)
py_files = base.glob("*.py")

# 递归搜索当前目录及所有子目录下所有的 .ipynb 文件
notebooks = base.rglob("*.ipynb") 

# ==========================================
# 5. 文件快捷读写 (无需 open())
# ==========================================
note = Path("memo.txt")

# 直接写文本 (默认 UTF-8)
note.write_text("Hello Pathlib!")

# 直接读文本
content = note.read_text()

# 删除文件
# note.unlink(missing_ok=True)