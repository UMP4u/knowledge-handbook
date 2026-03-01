"""
Pydantic 核心功能复习手册 (V2版本)
核心价值：数据校验、类型转换、自动文档化
"""

from typing import List, Optional
from datetime import datetime
from pydantic import (
    BaseModel, 
    Field, 
    EmailStr, 
    HttpUrl, 
    field_validator,
    model_validator,
    ValidationError
)
from typing_extensions import Self # 导入 Self 让代码更规范

# ==========================================
# 1. 基础模型定义 (Basic Model)
# ==========================================
class User(BaseModel): #继承BaseModel
    # 基础类型：如果不匹配，Pydantic 会尝试强制转换 (例如 "123" -> 123)
    id: int                          
    username: str
    
    # 默认值：如果不传此字段，则使用默认值
    is_active: bool = True           
    
    # 可选字段：允许为 None (需导入 Optional)
    signup_ts: Optional[datetime] = None #值要么是 datetime 对象，要么是 None
    

# ==========================================
# 2. 使用 Field 进行高级约束 (Constraints)
# ==========================================
class Product(BaseModel):
    # gt: 大于, lt: 小于, ge: 大于等于, le: 小于等于
    price: float = Field(..., gt=0, description="价格必须大于0") 
    # Field() 函数的第一个参数是 默认值（default）,"..."代表这个字段是“必填”的
    
    #  字符串或列表长度限制
    title: str = Field(..., min_length=2, max_length=50)
    
    # 别名 (Alias)：当输入数据的键名和 Python 变量名不一致时使用（如后端接前端传来的 "product_id"）
    tags: List[str] = Field(default=[], alias="product_tags")


# ==========================================
# 3. 嵌套模型 (Nested Models)
# ==========================================
class Address(BaseModel):
    city: str
    street: str

class Order(BaseModel):
    order_id: int
    items: List[Product]      # 列表里嵌套模型
    address: Address          # 直接嵌套模型


# ==========================================
# 4. 自定义校验器 (Custom Validators)
# ==========================================
class RegisterRequest(BaseModel):
    password: str
    confirm_password: str

    #单字段检验
    @field_validator('password')    #@装饰器
    @classmethod    #普通方法 (需要 self，对象已被创建);类方法 (需要 @classmethod 和 cls，对象可能未被创建)
    def password_strength(cls, v: str) -> str: #cls class的缩写，类方法的第一个参数必须写 cls
        if len(v) < 8:
            raise ValueError('密码长度必须至少8位')
        return v

    #多字段检验，校验两个字段是否一致  
    @model_validator(mode='after') #单字段校验之后运行. mode='before'
    def check_passwords_match(self) -> Self:
        # 此时 self 已经包含了 password 和 confirm_password
        if self.password != self.confirm_password:
            raise ValueError('两次密码输入不一致')
        
        # 必须返回 self
        return self    


# ==========================================
# 5. 常用功能操作 (Methods)
# ==========================================
def demo_operations():
    # A. 实例化与自动转换 (Data Coercion)
    # 注意：id传了字符串"1"，price传了字符串"19.9"，都会被自动转为正确类型
    raw_data = {
        "id": "1", 
        "username": "jack", 
        "price": "19.9", 
        "title": "学习手册"
    }
    
    try:
        user = User(id="123", username="pydantic_user")
        
        # B. 导出数据 (Serialization)   # dump丢掉、转储。
        print(user.model_dump())       #导出为 字典 (dict)
        print(user.model_dump_json())  # 导出为 JSON 字符串
        
        # C. 异常处理
        Product(price=-10, title="a")  # 触发验证错误
        
    except ValidationError as e:
        print(f"数据校验失败：\n{e.json()}")


# ==========================================
# 6. 进阶数据类型 (Special Types)
# ==========================================
# 需要安装: pip install "pydantic[email]"
class AdvancedType(BaseModel):
    email: EmailStr            # 自动校验邮箱格式
    website: HttpUrl           # 自动校验 URL 格式
    scores: List[int]          # 强类型列表


# ==========================================
# 复习总结清单：
# 1. 继承 BaseModel。
# 2. 类型注解是强制的（str, int, bool...）。
# 3. 强制转换：Pydantic 会尽力把数据转成你定义的类型。
# 4. 报错精准：ValidationError 会指出具体哪一个字段不符合规则。
# 5. model_dump() 是最常用的导出方法。
# ==========================================

if __name__ == "__main__":
    demo_operations()