import time
import sys
import os

# 定义时间模式 (分钟)
MODES = {
    "1": ("❄️  深度学习 (Deep Work)", 50, 10),
    "2": ("🔨 练习巩固 (Practice)", 25, 5),
    "3": ("🔄 复习回顾 (Review)", 15, 3)
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(label, minutes):
    seconds = minutes * 60
    total_seconds = seconds
    
    try:
        while seconds > 0:
            # 计算倒计时格式
            mins, secs = divmod(seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            
            # 进度条
            progress = int((total_seconds - seconds) / total_seconds * 20)
            bar = '█' * progress + '░' * (20 - progress)
            
            clear_screen()
            print(f"\n   {label}")
            print(f"   -----------------------")
            print(f"   ⏱️  {timer}")
            print(f"   [{bar}]")
            print(f"   -----------------------")
            print("\n   [按 Ctrl+C 停止]")
            
            time.sleep(1)
            seconds -= 1
            
        # 结束提醒
        clear_screen()
        print(f"\n   ✅ {label} 结束！")
        # 简单的响铃 (Windows/Mac通用)
        print('\a')
        
    except KeyboardInterrupt:
        print(f"\n\n   🛑 计时已停止")
        return False
    
    return True

def run_timer():
    while True:
        clear_screen()
        print("=== ⏳ 第一性原理深度工作计时器 ===\n")
        print("请选择专注模式:")
        for key, (name, focus, rest) in MODES.items():
            print(f"{key}. {name} -> {focus}min 专注 + {rest}min 休息")
        print("Q. 退出")
        
        choice = input("\n请选择 (1-3): ").strip().upper()
        
        if choice == 'Q':
            print("再见！保持专注。")
            break
            
        if choice in MODES:
            name, focus_min, rest_min = MODES[choice]
            
            # 开始专注
            print(f"\n准备开始: {name}")
            input("按回车键开始专注...")
            if not countdown(f"{name} - 专注阶段", focus_min):
                continue
                
            # 开始休息
            print(f"\n专注完成！准备休息 {rest_min} 分钟。")
            input("按回车键开始休息...")
            if not countdown(f"{name} - 休息阶段", rest_min):
                continue
                
            input("\n一个周期完成！按回车键继续...")
        else:
            input("无效输入，按回车重试...")

if __name__ == "__main__":
    run_timer()
