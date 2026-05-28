#!/usr/bin/env python3
"""补偿: R=80 → R=8 (-1 byte)
截断函数签名: func(A, R=80, T=3)
R 是宽度限制，被 mod1 短路后不再生效
"""
import sys
import re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

data = load_droid()

# X=80,Y=3) 变量名会混淆，用正则匹配
pattern = rb'(' + V + rb')=80,(' + V + rb')=3\)'
match = re.search(pattern, data)

if not match:
    print("补偿失败: 未找到目标模式")
    sys.exit(1)

old = match.group(0)
new = match.group(1) + b'=8,' + match.group(2) + b'=3)'
diff = len(new) - len(old)

data = data.replace(old, new, 1)

save_droid(data)
print(f"compensation R=80→R=8: {old} → {new} ({diff:+d} bytes)")
print(f"补偿完成 ({diff:+d} bytes)")
