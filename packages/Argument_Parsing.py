#e.g. python train.py --batch_size 32 --lr 0.001 --data ./data/train.csv

# 1.导入并创建解析器对象
import argparse

parser = argparse.ArgumentParser()

# 2.添加参数 
parser.add_argument("name", help="输入你的名字") #位置参数，必须输入的参数
parser.add_argument('--gpu', type=int, default=0, help='指定显卡ID (0-7)') #可选参数 以--开头

parser.add_argument("--verbose", action="store_true", help="是否打印详细日志")
# 使用action，只需输入python script.py --verbose 即可，而不用python script.py --verbose True

# 3.解析参数
args = parser.parse_args()

# 4.在代码中使用
device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")

# 进阶属性
# type=float 自动转换输入的数据类型
# choices=['gpu', 'cpu'] 限制输入只能在特定的范围内
